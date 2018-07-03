from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request

from flask_assets import Environment, Bundle
from flask_compress import Compress

from datetime import datetime
from datetime import timedelta

import boto3
import http.client
import json
import os


app = Flask(__name__)
Compress(app)

assets = Environment(app)
css = Bundle('css/about_me.css', 'css/alert.css', 'css/bootstrap.css', 'css/bootstrap-grid.min.css', 'css/carousel.css',
             'css/education.css', 'css/footer.css', 'css/form-control.css', 'css/general.css', 'css/index.css',
             'css/meter.css', 'css/modal.css', 'css/navbar.css', 'css/overview.css', 'css/projects.css',
             'css/sidebar.css', 'css/technical_skills.css', 'css/work_history.css',
             filters='cssmin', output='gen/css_all.css')
assets.register('css_all', css)


@app.route('/')
def index():
    return render_template('index.html', now=datetime.utcnow() - timedelta(hours=5))


@app.before_request
def redirect_to_https():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


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
    try:
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        company = request.json['company']
        message = request.json['message']
        token = request.json['token']

        print('%s is attempting to send a message to %s' % (name, os.environ['TO_ADDRESS']))

        if recaptcha_is_valid(token):
            aws = boto3.client('ses', region_name='us-east-1')
            response = aws.send_email(
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

            print('Successfully sent email from %s to %s' % (os.environ['FROM_ADDRESS'], os.environ['TO_ADDRESS']))
            print('Response from AWS: %s' % response)
            return jsonify({'success': 'true'})
        else:
            print('An error occurred while attempting to send email: recaptcha failed')
            return jsonify({'success': 'false'})
    except Exception as e:
        print('An error occurred while attempting to send email: %s' % e)
        return jsonify({'success': 'false'})
