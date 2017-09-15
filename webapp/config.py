import ast
import datetime
import os

# Global
DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'False'))
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'djsdhajdhashda13366ywglsa6ksnnnsggddfaosdsdhisudislskjwuw')
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

# Flask-Mail
MAIL_USE_TLS = True
MAIL_DEFAULT_SENDER = 'ThoughtLogix <noreply@thoughtlogix.com>'
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEBUG = False
