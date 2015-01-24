#!/usr/bin/env python

#import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import Encoders

import os
import boto

def mail(email_id, subject, html):
   
    me = "support@taiyyari.com"
    you = email_id

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you   

    part = MIMEBase('application', "octet-stream")
    installation_dir = os.path.dirname(__file__)
    try:
        #part.set_payload(open(os.path.join('/static_files', 'attachment.'+attachment_ext), "rb").read())
        Encoders.encode_base64(part)

        #part.add_header('Content-Disposition', 'attachment; filename="attachment.'+attachment_ext+'"')

        msg.attach(part)
    except Exception as ex:
        print 'no attachment present'
    # Create the body of the message (a plain-text and an HTML version).
    #text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"


    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)


    connection = boto.connect_ses('access_id','access_secet_key_id')
    result = connection.send_raw_email(msg.as_string(), source=msg['From'], destinations=[msg['To']])
    print result
    # Send the message via local SMTP server.
    #s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    #s.sendmail(me, you, msg.as_string())
    #s.quit()


