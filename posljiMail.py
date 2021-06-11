import smtplib, ssl
import base64

def posljiemail(email, text):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "zrebanje2020@gmail.com"
    password = (base64.b64decode(b'S3VwZ25vakAz')).decode('utf-8')

    # Create a secure SSL context
    context = ssl.create_default_context()
     
    sender_email = "zrebanje2020@gmail.com"
    receiver_email = email
    message = text
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
       
        server.sendmail(sender_email, receiver_email, message)
        print("Poslano osebi: "+ str(email))

        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

