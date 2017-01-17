from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from google.appengine.ext import deferred
from google.appengine.api import mail
from google.appengine.api import urlfetch
from urllib import urlencode
import logging
import json
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps
from ndb_files import *
import uuid
from datetime import *
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = '531123111669-91emkitt854rsv3hh77rciou0241sitt.apps.googleusercontent.com'
CLIENT_SECRET = '7NbJoty0Ym5kGTrNG5FbYF4M'
SCOPE = 'https://www.googleapis.com/auth/userinfo.profile email'
REDIRECT_URI = 'https://keepanyname.appspot.com/googledetail'

USER_PROFILE_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

urlfetch.set_default_fetch_deadline(45)

@app.route('/googlelogin')
def index():
    if 'credentials' not in session:
        return redirect(url_for('googledetail'))
    credentials = json.loads(session['credentials'])
    if credentials['expires_in'] <= 0:
        return redirect(url_for('googledetail'))
    else:
        headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
        r = urlfetch.fetch(USER_PROFILE_URL, headers=headers, method=urlfetch.GET)
        user = json.loads(r.content)
        session['logged_in'] = True
        session['user_email'] = user.get('email')
        session['username'] = user.get('name')
        mail = user.get('email')
        if UserDetails.query(UserDetails.email_ID == mail).get():
            return redirect(url_for('userpage'))
        UserDetails(userName = user.get("name"), email_ID = user.get("email") ).put()
        return redirect(url_for('userpage'))

@app.route('/googledetail')
def googledetail():
    if 'code' not in request.args:
        auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                    '&client_id={}&redirect_uri={}&scope={}').format(CLIENT_ID, REDIRECT_URI, SCOPE)
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        data = {'code': auth_code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'}
        url = 'https://www.googleapis.com/oauth2/v4/token'
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = urlfetch.fetch(url, method=urlfetch.POST, payload=urlencode(data), headers=header )
        session['credentials'] = r.content
        return redirect(url_for('index'))


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('homepage'))
    return wrap

def userdetails(data):
    pwd = data.get('psw')
    user_details = UserDetails(
        userName = data.get('uname'),
        email_ID = data.get('umail'),
        password = generate_password_hash(pwd)
    )
    user_details.put()


def newbook_request_mailing(to_user, name, book, author):
    sender = 'karthik.sabapathy@adaptavantcloud.com'
    subject_to_user = "Book Request acknowledgement"
    mailbody_to_user = '%s Book written by %s has been requested successfully. Thank you for requesting book on Book Forms.' % (book, author)
    mail.send_mail(sender, to_user, subject_to_user, mailbody_to_user)
    to_admin = sender
    subject_to_admin = 'You have a new Book Request'
    mailbody_to_admin = '%s from %s has requested for %s book written by %s to be added to the list. Please acknowledge and add the book to the list.' % (name, to_user, book, author)
    mail.send_mail(sender, to_admin, subject_to_admin, mailbody_to_admin)

def readbook_request_mailing(book, receiver, name):

    sender = "karthik.sabapathy@adaptavantcloud.com"

    subject = "New Read Book Requested"
    body = 'Your request to read book %s has been submitted successfully.' % (book)
    mail.send_mail(sender, receiver, subject, body)
    admin_receiver = sender
    subject_to_admin = 'New Read Book Requested'

    body_to_admin = '%s from %s has been requested to read %s.' % (name, receiver, book)
    mail.send_mail(sender, admin_receiver, subject_to_admin, body_to_admin)

def admin_request_mail(to):
    sender = 'karthik.sabapathy@adaptavantcloud.com'
    subject = 'Make me as a Admin'
    body = 'Click this link and fill up the admin signup form. \nhttps://keepanyname.appspot.com/adminsignup'
    mail.send_mail(sender, to, subject, body)

@app.route('/')
def homepage():
    return render_template('loginpopup.html')

@app.route('/loginpage', methods = ['POST'])
def loginpage():
    data = request.get_json(force=True)
    username = data.get('name')
    pswd = data.get('password')
    if UserDetails.query(UserDetails.email_ID == username).get():
        user = UserDetails.query(UserDetails.email_ID == username).get()
        if check_password_hash(user.password, pswd):
            session['logged_in'] = True
            session['user_email'] = username
            session['username'] = user.userName
            # return redirect(url_for('userpage'))
            # return render_template('userpage.html')
            data = ''
            return jsonify(result = data)
        else:
            # flash('Invalid username or password.')
            # return redirect(url_for('homepage'))
            data = 'Invalid username or password'
            return jsonify(result = data)
    else:
        # flash('Invalid user credentials.')
        # return redirect(url_for('homepage'))
        data = 'Invalid user credentials.'
        return jsonify(result = data)

@app.route('/userpage')
@login_required
def userpage():
    books = Books.query().fetch()
    return render_template('userpage.html',book=books)

@app.route('/userlogout')
def userlogout():
    session.pop('user_email', None)
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('credentials', None)
    return redirect(url_for('homepage'))

@app.route('/bookrequest', methods = ['POST'])
def bookrequest():
    data = request.get_json(force=True)
    book = data.get('name')
    author = data.get('author')
    if Books.query(ndb.AND(Books.name == book, Books.author == author)).get():
    # if Books.query(Books.name == book).get():
        # if Books.query(Books.author == author).get():
            # flash('The Book you requested is already in the Book list.')
            # return redirect(url_for('userpage'))
            data = 'The book you requested is already in the Book list.'
            return jsonify(result = data)
            # data = json.dumps({'book': {'name': book, 'author': author}})
            # return data, 200, {'Content-type': 'application/json'}
    if book == '' or author == '':
        data = 'Book name or Author is missing. Please enter.'
        return jsonify(result = data)
    user_email = session['user_email']
    name = session['username']
    deferred.defer(newbook_request_mailing, user_email, name, book, author)
    # flash('Book requested successfully')
    # return redirect(url_for('userpage'))
    data = 'Book requested successfully'
    return jsonify(result = data)

@app.route('/bookread', methods = ['POST'])
def bookread():
    data = request.get_json(force=True)
    book = data.get('name')
    receiver = session['user_email']
    name = session['username']
    deferred.defer(readbook_request_mailing, book, receiver, name)
    # flash('Your book will be sent to you shortly.')
    # return redirect(url_for('userpage'))
    data = 'Your book will be sent to you shortly'
    return jsonify(result = data)

@app.route('/signup', methods=['POST'])
def signup():
    userdet = UserDetails.query().fetch()
    data = request.get_json(force=True)
    for user in userdet:
        if user.email_ID == data.get('umail'):
            # flash('The email ID you entered has already been signed up.')
            # return redirect(url_for('homepage'))
            data = 'The email ID you entered has already been signed up.'
            return jsonify(result = data)
        else:
            continue
    else:
        userdetails(data)
        # flash('Signed up successfully. Log in to access your account in BookForm.')
        # return redirect(url_for('homepage'))
        return_data = 'Signed up successfully. Log in to access your account in BookForm.'
        return jsonify(result = return_data)

@app.route('/adminsignup')
@login_required
def adminsignup():
    if Admins.query(Admins.email == session['user_email']).get():

        data = 'You are already an Admin on BookForms.'
        return jsonify(result=data)
    else:
        data = ''
        return jsonify(result=data)
    # return render_template('adminsignup.html')


@app.route('/admin_signup_page')
@login_required
def admin_signup_page():
    return render_template('adminsignup.html')


# @app.route('/adminrequest')
# def adminrequest():
#     usermail = session['user_email']
#     if Admins.query(Admins.email == usermail).get():
#         # flash('You are already an Admin in BookForms.')
#         # return redirect(url_for('userpage'))
#         data = 'You are already an Admin  in BookForms.'
#         return jsonify(result = data)
#     deferred.defer(admin_request_mail, to)
#     # flash('Check out your email to get the link for admin form.')
#     # return redirect(url_for('userpage'))
#     data = 'Check out your mail to get the link for admin form.'
#     return jsonify(result = data)

@app.route('/signedup', methods=['POST'])
def signedup():
    # if Admins.query(Admins.email != session['user_email']).get():
    # if request.form['adminpassword'] == request.form['confirmpassword']:
        # if Admins.query(Admins.email == request.form['adminemail']).get():
        #     flash('You are already an Admin in Bookforms.')
        #     return redirect(url_for('adminsignup'))
        # elif UserDetails.query(UserDetails.email_ID == request.form['adminemail']).get():
            data = request.get_json(force=True)
            pw = data.get('password')
            user_key = ndb.Key(UserDetails, session['user_email'])
            admins = Admins(
            username = session['username'],
            email = session['user_email'],
            password = generate_password_hash(pw),
            by_user = user_key
            )
            admins.put()
            data = 'Signed up successfully.'
            return jsonify(result = data)
            # flash('Signed up successfully')
            # return redirect(url_for('userpage'))
        # else:
        #     flash('You are not a user on BookForms. Only users of BookForms can become Admin on BookForms')
        #     return redirect(url_for('adminsignup'))
    # flash('You are already an Admin on BookForms.')
    # return redirect(url_for('adminsignup'))

@app.route('/admin', methods=['POST'])
def admin():
    data = request.get_json(force=True)
    adminname = data.get('adminname')
    adminpsw = data.get('password')
    if Admins.query(Admins.email == adminname).get():
        admin = Admins.query(Admins.email == adminname).get()
        if check_password_hash(admin.password, adminpsw):
            session['logged_in'] = True
            # return redirect(url_for('adminpage'))
            data = ''
            return jsonify(result = data)
        else:
            # flash('Invalid adminname or password.')
            # return redirect(url_for('homepage'))
            data = 'Invalid admin mail or password.'
            return jsonify(result = data)
    else:
        # flash('Invalid admin credentials.')
        # return redirect(url_for('homepage'))
        data = 'Invalid admin credentials.'
        return jsonify(result = data)


@app.route('/adminpage')
@login_required
def adminpage():
    return render_template('adminpage.html')

@app.route('/addingbook',methods=['POST'])
def addingBook():
    data = request.get_json(force=True)
    bookname = data.get('bookname')
    authorname = data.get('authorname')
    genre = data.get('genre')
    if Books.query(ndb.AND(Books.name == bookname, Books.author == authorname)).get():
    # if Books.query(Books.name == bookname).get():
    #     if Books.query(Books.author == authorname).get():
            # flash('This book is already in our list.')
            # return redirect(url_for('adminpage'))
            data = 'This book is already in our list.'
            return jsonify(result = data)
    addbook=Books(name=bookname,genre=genre,author=authorname)
    addbook.put()
    # flash("Book added successfully")
    # return redirect(url_for('adminpage'))
    data = 'Book added successfully.'
    return jsonify(result = data)

@app.route('/adminlogout')
def adminlogout():
    session.pop('logged_in', None)
    return redirect(url_for('homepage'))

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
    sender = "karthik.sabapathy@adaptavantcloud.com"
    confirmation= ForgotPassword(id=mailid,email=mailid,uid=uid,timestamp=timestamp)
    confirmation.put()
    subject = 'Reset Password - link'
    link = 'https://keepanyname.appspot.com/resetpassword/{}&id={}'.format(uid,mailid)
    mail.send_mail(sender, mailid, subject, link)
    flash('Reset Password Link has been sent to your Email,Please check within 10 mins')
    return redirect(url_for('homepage'))

# @app.route("/getbooks")
# def get_books():
#     import json
#     data = json.dumps({"books":{'id': 1, 'name': 'hp'}})
#     return data, 200, {'Content-type': 'application/json'}

@app.route('/resetpassword/<uid>&<mailid>')
def resetpassword(uid,mailid):
    logging.info(uid)
    uid=uid
    id=mailid
    uid_key=ForgotPassword.query(ForgotPassword.uid==uid).get()
    timestamp=uid_key.timestamp
    utc = pytz.UTC
    currenttime = datetime.now().replace(tzinfo=utc)
    currenttime = currenttime.time()
    minutedifference = currenttime.minute - timestamp.minute
    if minutedifference <= 10:
        return render_template('resetpassword.html', uid=uid)
    else:
       return 'session expired'

@app.route('/resetpasswordstore',methods=['POST'])
def resetpasswordstore():
     mail= request.form['mail']
     uid=request.form['uid']
     entity_key=ForgotPassword.query(ForgotPassword.email == mail).get()
     originaluid=entity_key.uid
     if uid == originaluid:
         user=UserDetails.query(UserDetails.email_ID == mail).get()
         logging.info(user)
         newpassword=request.form['password']
         newpassword=generate_password_hash(newpassword)
         user.password = newpassword
         user.put()
         flash('Password reset Sucessfully')
         return redirect(url_for('homepage'))
     else:
         return 'Don\'t try to change the uid'


if __name__ == '__main__':
    app.run(debug=True)