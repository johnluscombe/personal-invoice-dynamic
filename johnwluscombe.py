from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

import boto3
import http.client
import json
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
    connection.request('POST', path)
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
    try:
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        company = request.json['company']
        message = request.json['message']
        token = request.json['token']

        if recaptcha_is_valid(token):
            aws = boto3.client('ses')
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

            return jsonify({'success': 'true'})
        else:
            return jsonify({'success': 'false'})
    except Exception as e:
        return jsonify({'success': 'false'})