## https://stackoverflow.com/questions/73026671/how-do-i-now-since-june-2022-send-an-email-via-gmail-using-a-python-script

## https://developers.google.com/gmail/api/quickstart/python

## https://www.twilio.com/blog/receiving-emails-python-flask-twilio-sendgrid

## above two not required
# 1 enable two factor authentication for gmail account
# 2 generate 16 char app password and use as normal password in env file

# https://github.com/The-Intrigued-Engineer/python_emails/blob/main/text_email.py

import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

## while testing without https
##>> os.environ["OAUTHLIB_INSECURE_TRANSPORT"]="1"


# After 'Create app'
#app.config['MAIL_SERVER'] = 'smtp.example.com'
#app.config['MAIL_PORT'] = 465
#app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_USERNAME'] = 'username'
#app.config['MAIL_PASSWORD'] = 'password'

mail_server = environ.get('MAIL_SERVER')
mail_port = environ.get('MAIL_PORT')
mail_username = environ.get('MAIL_USERNAME')
mail_password = environ.get('MAIL_PASSWORD')
sender_email = environ.get('MAIL_SENDEREMAIL')
receiver_email = environ.get('MAIL_RECEIVEREMAIL')

subject = 'some subject message'
body = """text body of the email"""
#sender_email = 'my_gmail_account_name@gmail.com'
#receiver_email = 'some_recipient@something.com'

# Create a multipart message and set headers
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
# Add body to email
message.attach(MIMEText(body, 'plain'))
# Open file in binary mode
#with open( client_zip_filename, 'rb') as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    #part = MIMEBase('application', 'octet-stream')
    #part.set_payload(attachment.read())
# Encode file in ASCII characters to send by email    
#encoders.encode_base64(part)
# Add header as key/value pair to attachment part
#part.add_header(
#    'Content-Disposition',
#    f'attachment; filename={subject}',
#)
# Add attachment to message and convert message to string
#message.attach(part)
text = message.as_string()
# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    print( 'waiting to login...')
    server.login(sender_email, mail_password)
    print( 'waiting to send...')
    server.sendmail(sender_email, receiver_email, text)
print( 'email appears to have been sent')
