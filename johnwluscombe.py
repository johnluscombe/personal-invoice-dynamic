from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

import boto3
import http.client
import json
import logging
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def recaptcha_is_valid(token):
    connection = http.client.HTTPSConnection('www.google.com')
    endpoint = '/recaptcha/api/siteverify'
    params = '?secret=%s&response=%s'% (os.environ['RECAPTCHA_SECRET'], token)
    path = endpoint + params
    headers = {'Content-Length': 0}
    connection.request('POST', path, None, headers)
    httpResponse = connection.getresponse()
    stringResponse = httpResponse.read().decode()
    response = json.loads(stringResponse)
    return response['success']


def get_email_body(name, email, phone, company, message):
    body = "<strong>Name:</strong> %s<br>" % name
    body += "<strong>Email:</strong> %s<br>" % email

    if phone:
        body += "<strong>Phone:</strong> %s<br>" % phone

    if company:
        body += "<strong>Company:</strong> %s<br>" % name

    body += "<br>%s" % message
    return body


@app.route('/send-email', methods=['POST'])
def send_email():
    logger = logging.getLogger('johnwluscombe.com')
    try:
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        company = request.json['company']
        message = request.json['message']
        token = request.json['token']

        logger.info('%s is attempting to send a message to %s' % (name, os.environ['TO_ADDRESS']))

        if recaptcha_is_valid(token):
            aws = boto3.client('ses', region_name='us-east-1')
            aws.send_email(
                Source='"%s" <%s>' % (name, os.environ['FROM_ADDRESS']),
                Destination={
                    'ToAddresses': [os.environ['TO_ADDRESS']]
                },
                Message={
                    'Subject': {
                        'Data': "New message from %s" % name,
                        'Charset': 'UTF-8'
                    },
                    'Body': {
                        'Html': {
                            'Data': get_email_body(name, email, phone, company, message)
                        }
                    }
                }
            )

            logger.info('Successfully sent email from %s to %s' % (os.environ['FROM_ADDRESS'], os.environ['TO_ADDRESS']))
            return jsonify({'success': 'true'})
        else:
            logger.error('An error occurred while attempting to send email: recaptcha failed')
            return jsonify({'success': 'false'})
    except Exception as e:
        logger.exception('An error occurred while attempting to send email: %s' % e)
        return jsonify({'success': 'false'})