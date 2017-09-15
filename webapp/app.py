import json
from pprint import pprint

from flask import Flask
from flask import render_template
from flask import request
from flask_mail import Message, Mail

app = Flask(__name__)
app.config.from_object('private_config')
mail = Mail(app)
projects = json.load(open("data/projects.json"))


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/', methods=['GET'])
def index():
    return """  <div style="margin: 100px auto;
                font-size: 96px; text-align: center;">
                Howdy partner</div>"""


@app.route('/mailer/send/<string:domain>', methods=['POST'])
def send(domain):
    return contact_simple(domain)


@app.route('/mailer/contact/<string:domain>', methods=['POST'])
def contact_simple(domain):
    if not domain:
        return 'domain name required'

    form_data = request.get_json()
    pprint(form_data)

    if (('version' in form_data or 'version' in form_data) and
                'captcha' not in form_data):
        return 'Error'

    if form_data['captcha'] != "5":
        return 'Error'

    data = {
        "first_name": form_data['firstName'],
        "last_name": form_data['lastName'],
        "company": form_data['company'],
        "email": form_data['email'],
        "phone": form_data['phone'],
        "message": form_data['notes'],

    }

    pprint(data)

    msg = Message(domain + ' Form Submission',
                  recipients=[projects[domain]['to']],
                  sender=projects[domain]['sender']
                  )
    msg.body = render_template('/contact.txt', **data)
    msg.html = render_template('/contact.html', **data)
    mail.send(msg)

    return 'ok'


@app.route('/mailer/generic/<string:domain>', methods=['POST'])
def generic(domain):
    if not domain:
        return 'domain name required'

    form_data = request.get_json()
    pprint(form_data)

    if (('version' in form_data or 'version' in form_data) and
                'captcha' not in form_data):
        return 'Error'

    if form_data['captcha'] != "5":
        return 'Error'

    msg = Message(domain + ' Form Submission',
                  recipients=[projects[domain]['to']],
                  sender=projects[domain]['sender']
                  )
    msg.body = render_template('/generic.txt', data=form_data)
    msg.html = render_template('/generic.html', data=form_data)
    mail.send(msg)

    return 'ok'


if __name__ == '__main__':
    # context = ('fake.cert', 'fake.key')
    app.run(host='0.0.0.0', debug=True)
