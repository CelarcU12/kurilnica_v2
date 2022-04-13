#!/usr/bin/python

import smtplib, ssl
import base64
from datetime import datetime

def posljiemail(email, text):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "zrebanje2020@gmail.com"
    password = (base64.b64decode(b'S3VwZ25vakAz')).decode('utf-8')

    # Create a secure SSL context
    context = ssl.create_default_context()
     
    sender_email = "zrebanje2020@gmail.com"
    receiver_email = email
    # Try to log in to server and send email
    time = datetime.now()
    message ="""From: Kurilnica <iblabla@gmail.com>
Subject: Obvestilo ob: """+str(time.hour)+""":"""+str(time.minute)+"""

"""+text
   # To: """+email+""" <"""+email+"""> 
   # Subject: Kurilnica alarm
   # 
   # """+text
    # Try to log in to server and send email
    print("pred try")
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        print('before login')
        server.login(sender_email, password)
        print('sending mail.... ')
        server.sendmail(sender_email, receiver_email,message)
        print("Poslano osebi: "+ str(email))

        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 
#posljiemail('furbek.celarc@gmail.com','test ')

