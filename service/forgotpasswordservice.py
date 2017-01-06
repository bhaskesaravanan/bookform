from flask import Flask,request,redirect,render_template,url_for
import uuid,datetime
app=Flask(__name__)
from models.bookformndbfiles import *
from google.appengine.api import mail

@app.route('/forgotpassword',methods=['POST'])
def forgotpassword():
    mailid=request.form['mail']
    uid=uuid.uuid4()
    timestamp=ForgotPassword(key_name="TIMESTAMP")
    forgotpassword=ForgotPassword(email=mail,uid=uid,timestamp=timestamp)
    forgotpassword.put()
    link = 'https://helloworld-151108.appspot.com/resetpassword/{}'.format(uid)
    send_email(to=mailid, body=link)
    return render_template('homepage.html')




def send_email(to, body, sender='bhaskar.saravanan@adaptavantcloud.com'):
        subject = 'Reset Password Request - Bookforms'
        mail.send_mail(sender, to, subject, body)



@app.route('/resetpassword/<uid>')
def resetpassword(uid):
    keys=ForgotPassword.get_by_id(uid)
    timestamp=keys.timestamp
    currenttime = datetime.time()
    if timestamp.hour == currenttime.hour:
        minutedifference = timestamp.minute - currenttime.minute
        if minutedifference <= 10:
            return redirect(url_for(resetpasswords,uid=uid))

    return 'session expired'




def resetpasswords(uid):
    return render_template('resetpaswword.html',uid)


@app.route('resetpasswordstore',methods=['POST'])
def resetpasswordstore():
     mail= request.form['mail']
     uid=request.form['uid']
     keys=ForgotPassword.get_by_id(mail)
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










