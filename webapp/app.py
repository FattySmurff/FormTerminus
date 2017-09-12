import json
from pprint import pprint

from flask import Flask
from flask import render_template
from flask import request
from flask_mail import Message, Mail

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)
projects = json.load(open("data/projects.json"))


@app.route('/mailer/send/<string:domain>', methods=['POST'])
def send(domain):
    return contact_simple(domain)


@app.route('/mailer/contact/<string:domain>', methods=['POST'])
def contact_simple(domain):
    if not domain:
        return 'domain name required'

    request_data = request.get_json()
    form_data = request_data['data']

    if ('version' in form_data or 'version' in form_data) and 'captcha' not in form_data:
        return 'Error'

    # if form_data['captcha'] != 5:
    #     return 'Error'

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

    request_data = request.get_json()
    form_data = request_data['data']

    if ('version' in form_data or 'version' in form_data) and 'captcha' not in form_data:
        return 'Error'

    # if form_data['captcha'] != 5:
    #     return 'Error'

    pprint(form_data)

    msg = Message(domain + ' Form Submission',
                  recipients=[projects[domain]['to']],
                  sender=projects[domain]['sender']
                  )
    msg.body = render_template('/generic.txt', data=form_data)
    msg.html = render_template('/generic.html', data=form_data)
    mail.send(msg)

    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
