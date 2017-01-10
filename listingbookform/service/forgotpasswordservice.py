from flask import Flask,request,redirect,render_template,url_for
import uuid,datetime
import pytz


app=Flask(__name__)
from models.bookformndbfiles import *
from google.appengine.api import mail

@app.route('/forgot')
def forgot():
    return render_template('forgotpassword.html')


@app.route('/forgotpassword',methods=['POST'])
def forgotpassword():
    mailid=request.form['mail']
    uid=str(uuid.uuid4())
    utc = pytz.UTC
    timestamp= datetime.now().replace(tzinfo=utc)
    timestamp=timestamp.time()

    confirmation= ForgotPassword(email=mailid,uid=uid,timestamp=timestamp)
    confirmation.put()

    link = 'https://helloworld-151108.appspot.com/resetpassword/{}'.format(uid)

    send_email(to=mailid, body=link)
    return redirect(url_for('homepage'))




def send_email(to, body, sender='bhaskar.saravanan@adaptavantcloud.com'):
        subject = 'Reset Password Request - Bookforms'
        mail.send_mail(sender, to, subject, body)



@app.route('/resetpassword/<uid>')
def resetpassword(uid):
    logging.info(uid)
    #key_parent = ndb.Key('ForgotPasswordParent', 'uid_parent').get()
    uid_key=ForgotPassword.query(forgotpassword.uid==uid).get()
    #,parent=key_parent)

    logging.info(uid_key)
    timestamp=uid_key.timestamp
    utc = pytz.UTC
    currenttime = datetime.now().replace(tzinfo=utc)
    currenttime = currenttime.time()
    if timestamp.hour == currenttime.hour:
        minutedifference = timestamp.minute - currenttime.minute
        if minutedifference <= 10:
            return redirect(url_for(resetpasswords,uid=uid))

    return 'session expired'


def resetpasswords(uid):
    return render_template('resetpaswword.html',uid)



@app.route('/resetpasswordstore',methods=['POST'])
def resetpasswordstore():
     mail= request.form['mail']
     uid=request.form['uid']
     keys=ForgotPassword.get_by_id('mail')
     originaluid=keys.uid

     if uid == originaluid:
         if request.form['password'] == request.form['reenterpassword']:
             user=UserDetails.get_by_id(mail)
             user.password = request.form['password']
             user.put()

         else:
             return 'Type correct password'

     else:
         return 'Don\'t try to change the uid'










