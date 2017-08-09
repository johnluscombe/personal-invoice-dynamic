from flask import Flask
from flask import jsonify
from flask import render_template
import boto3
import http.client
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/verify-recaptcha', methods=['POST'])
def verify_recaptcha():
    #TODO: token=[get token from request]
    connection = http.client.HTTPSConnection('www.google.com')
    headers = {'Content-type': 'application/json'}
    body = {'secret': os.environ['RECAPTCHA_SECRET'], 'response': token}
    jsonBody = json.dumps(body)
    connection.request('POST', '/recaptcha/api/siteverify', jsonBody, headers)
    httpResponse = connection.getresponse()
    return httpResponse.read().decode()


def get_email_body(name, email, phone, company, message):
    body = "<strong>Name:</strong> %s\n" % name
    body += "<strong>Email:</strong> %s\n" % email

    if phone:
        body += "<strong>Phone:</strong> %s\n" % phone

    if company:
        body += "<strong>Company:</strong> %s\n" % name

    body += "\n%s" % message
    return body


@app.route('/send-email', methods=['POST'])
def send_email(name, email, phone, company, message):
    try:
        #TODO: token=[get name, email, phone, company, and message from request]
        if os.environ['EMAIL_TOKEN'] == '80e0adba56fb2852647fe3c3fa901a20499cccfe6191feec':
            aws = boto3.client('ses')
            aws.send_email(
                Source=os.environ['FROM_ADDRESS'],
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
    except:
        return jsonify({'success': 'false'})


if __name__ == '__main__':
    app.run()
