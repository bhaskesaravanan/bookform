from flask import Flask, render_template, request, redirect, url_for, flash, session
from google.appengine.ext import deferred
from google.appengine.api import mail
from google.appengine.ext import ndb
import logging

import config

# import logging
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
from datetime import *
import pytz
from functools import wraps
from models.bookformndbfiles import *

app = Flask(__name__)
app.secret_key = os.urandom(24)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('homepage'))

    return wrap


def userdetails():
    if request.form['psw'] == request.form['rpsw']:
        # uname = request.form['uname']
        pwd = request.form['psw']
        # hash_pwd = User(pwd)
        user_details = UserDetails(
            userName=request.form['uname'],
            email_ID=request.form['email'],
            password=generate_password_hash(pwd),

        )
        user_details.put()


def newbook_request_mailing(to_user, name, book):
    sender = str('bhaskar.saravanan@adaptavantcloud.com')
    subject_to_user = str("Book Request acknowledgement")
    mailbody_to_user = str(
        '%s Book has been requested successfully. Thank you for requesting book on Book Forms.' % (book))
    mail.send_mail(sender, to_user, subject_to_user, mailbody_to_user)
    to_admin = sender
    subject_to_admin = str('You have a new Book Request')
    mailbody_to_admin = str(
        '%s from %s has requested for %s book to be added to the list. Please acknowledge and add the book to the '
        'list' % (name, to_user, book))
    mail.send_mail(sender, to_admin, subject_to_admin, mailbody_to_admin)


def readbook_request_mailing():
    book = request.form['book']
    sender = str('bhaskar.saravanan@adaptavantcloud.com')
    receiver = str(session['user_email'])
    subject = str('New Read Book Requested')
    body = str('Your request to read book %s has been submitted successfully.' % (book))
    mail.send_mail(sender, receiver, subject, body)
    receiver = sender
    subject_to_admin = str('New Read Book Requested')
    name = str(session['username'])
    body_to_admin = str('%s from %s has been requested to read %s.' % (name, receiver, book))
    mail.send_mail(sender, receiver, subject_to_admin, body_to_admin)


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/loginpage', methods=['POST'])
def loginpage():
    username = request.form['uemail']
    pswd = request.form['psw']

    if UserDetails.query(UserDetails.email_ID == username).get():

        user = UserDetails.query(UserDetails.email_ID == username).get()

        if check_password_hash(user.password, pswd):

            session['logged_in'] = True
            session['user_email'] = username
            session['username'] = user.userName
            return redirect(url_for('userpage'))
        else:

            flash('Invalid username or password.')
            return redirect(url_for('homepage'))
    else:

        flash('Invalid user credentials.')
        return redirect(url_for('homepage'))


@app.route('/userpage')
@login_required
def userpage():
    books = Books.query().fetch()
    return render_template('userpage.html', book=books)


@app.route('/userlogout')
def userlogout():
    session.pop('user_email', None)
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('homepage'))


@app.route('/bookrequest', methods=['POST'])
def bookrequest():
    book = request.form['requirebook']
    user_email = session['user_email']
    name = session['username']
    newbook_request_mailing(user_email, name, book)
    flash('Book requested successfully')
    return redirect(url_for('userpage'))


@app.route('/bookread', methods=['POST'])
def bookread():
    deferred.defer(readbook_request_mailing)
    flash('Your book will be sent to you shortly.')
    return redirect(url_for('userpage'))


@app.route('/signup', methods=['POST'])
def signup():
    userdet = UserDetails.query().fetch()
    for user in userdet:
        if user.email_ID == request.form['email']:
            flash('The email ID you entered has already been signed up.')
            return redirect(url_for('homepage'))
        else:
            continue
    else:
        userdetails()
        flash('Signed up successfully. Log in to access your account in BookForm.')
        return redirect(url_for('homepage'))


@app.route('/adminsignup')
def adminsignup():
    return render_template('adminsignup.html')


@app.route('/adminrequest')
def adminrequest():
    sender = str('bhaskar.saravanan@adaptavantcloud.com')
    to = str(session['user_email'])
    subject = str('Make me as a Admin')
    body = str('Click this link and fill up the admin signup form. \n https://keepanyname.appspot.com/adminsignup')
    mail.send_mail(sender, to, subject, body)
    flash('Check out your email to get the link for admin form.')
    return redirect(url_for('userpage'))


@app.route('/signedup', methods=['POST'])
def signedup():
    if request.form['adminpassword'] == request.form['confirmpassword']:
        if UserDetails.query(UserDetails.email_ID == request.form['adminemail']).get():
            pw = request.form['adminpassword']
            admins = Admins(
                username=request.form['adminname'],
                email=request.form['adminemail'],
                password=generate_password_hash(pw)
            )
            admins.put()
            flash('Signed up successfully')
            return redirect(url_for('homepage'))
        else:
            flash('You are not a user on BookForms. Only users of BookForms can become Admin on BookForms')
            return redirect(url_for('adminsignup'))
    flash('Passwords do not match')
    return redirect(url_for('adminsignup'))

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
    uid_key=ForgotPassword.get_by_id((uid))#,parent=key_parent)

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




@app.route('/admin', methods=['POST'])
def admin():
    adminname = request.form['adminname']
    adminpsw = request.form['psw']
    if Admins.query(Admins.email == adminname).get():
        admin = Admins.query(Admins.email == adminname).get()
        if check_password_hash(admin.password, adminpsw):
            session['logged_in'] = True
            return redirect(url_for('adminpage'))
        else:
            flash('Invalid adminname or password.')
            return redirect(url_for('homepage'))
    else:
        flash('Invalid admin credentials.')
        return redirect(url_for('homepage'))


@app.route('/adminpage')
@login_required
def adminpage():
    return render_template('adminpage.html')


@app.route('/addingbook', methods=['POST'])
def addingBook():
    addbook = Books(name=request.form['bookname'], genre=request.form['genre'], author=request.form['authorname'])
    addbook.put()
    flash("Book added successfully")
    return render_template('adminpage.html')


@app.route('/adminlogout')
def adminlogout():
    session.pop('logged_in', None)
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run(debug=True)