import os
import hashlib
import datetime
from flask import Flask , render_template, request
app = Flask(__name__)
from mongoengine import *
from ses_mailer import mail

app.config["SECRET_KEY"] = "wirefoot"
connect('taiyyari')

class subscription(Document):
    email_id = StringField(required=True)
    activation_link = StringField(required=True)
    activated=BooleanField(required=True)
    account_created=DateTimeField(default=datetime.datetime.now, required=True)
    account_activated_stamp=DateTimeField(default=datetime.datetime.now, required=True)
    ip_address=StringField(required=True)

@app.route('/verify/<activation_link>',methods=['GET'])
def get(activation_link):
    subscriber_exists=subscription.objects(activation_link=activation_link)
    if len(subscriber_exists)==1:
        subscriber_exists[0].update(set__activated=True)
	return 'verified!'
    else:
        return 'bad link!'
    

@app.route('/',methods=['GET','POST'])
def subscribe():
    if request.method=='GET': 
        
        context = {}
        html = render_template('form.html',**context)
        return html

    if request.method=='POST':
	x = request.form['email_id']
	subscriber_exists=subscription.objects(email_id=x)
	print x, type(subscriber_exists)
	if len(subscriber_exists)==0: 
		print 'kjhjewkfhkjf'        
		linkxyz=hashlib.sha256(x+'spinach').hexdigest()
		activated=False
		ip=""
		subscribe=subscription(email_id=x,activation_link=linkxyz,activated=activated,ip_address=ip)
		subscribe.save()
		context = {'verify':linkxyz}
		mail_html = render_template('verification.html',**context)
		     #self.response.write(html)
		     # mail bhejo
		mail(x, subject="Your account has been approved", html=mail_html)
		      
		return 'new email submitted!!!'
	else:
		return 'email exists!!!'


if __name__ == '__main__':
    app.run(debug=True,port=80,host="0.0.0.0")
