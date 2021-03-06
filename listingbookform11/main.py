from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify,make_response
from flask_restful import Resource, Api, reqparse
from google.appengine.ext import deferred
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from urllib import urlencode
from google.appengine.datastore.datastore_query import Cursor
import logging

import config
import json


import logging
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
from datetime import *
import pytz
from functools import wraps
from models.bookformndbfiles import *
log = logging.getLogger(__name__)
app = Flask(__name__)
api = Api(app)
app.secret_key = os.urandom(24)

CLIENT_ID = '545443502559-k8nlkopm7l2vdvhgi2s9gjssv4msu9si.apps.googleusercontent.com'
CLIENT_SECRET = 'EzI-SFjOFkvfn5fuKQK2Iy85'  # Read from a file or environmental variable in a real app
SCOPE = 'https://www.googleapis.com/auth/userinfo.profile email'
REDIRECT_URI =  'http://helloworld-151108.appspot.com/googledetail'

USER_PROFILE_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

urlfetch.set_default_fetch_deadline(45)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('homepage'))

    return wrap

@app.route('/googlelogin')
def index():
    if 'credentials' not in session:
        return redirect(url_for('googledetail'))
    credentials = json.loads(session['credentials'])
    if credentials['expires_in'] <= 0:
        return redirect(url_for('googledetail'))
    else:
        headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
        # req_uri = 'https://www.googleapis.com/oauth2/v1/userinfo?`'
        r = urlfetch.fetch(USER_PROFILE_URL, headers=headers, method=urlfetch.GET)
        # return json.loads(r.content).get("name")
        user = json.loads(r.content)
        session['logged_in'] = True
        UserDetails(userName = user.get("name"), email_ID = user.get("email") ).put()
        return redirect(url_for('userpage'))


@app.route('/googledetail')
def googledetail():
    if 'code' not in request.args:
        auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                    '&client_id={}&redirect_uri={}&scope={}').format(CLIENT_ID, REDIRECT_URI, SCOPE)
        log.info(auth_uri)
        return redirect(auth_uri)

    else:
        auth_code = request.args.get('code')
        log.info(auth_code)
        data = {'code': auth_code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'}

        log.info(json.dumps(data))
        url = 'https://www.googleapis.com/oauth2/v4/token'
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = urlfetch.fetch(url, method=urlfetch.POST, payload=urlencode(data), headers=header )
        log.info(r.content)
        session['credentials'] = r.content

        # json_response = json.loads(r.content)
        # userinfo = flask.request.get(json_response)
        # user = UserDetails()
        # user.put()
        # return r.content
        return redirect(url_for('index'))




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


def readbook_request_mailing(book):
    book = book
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


@app.route('/loginpage', methods = ['POST'])
def loginpage():
    username = request.form['emailid']
    pswd = request.form['password']
    if UserDetails.query(UserDetails.email_ID == username).get():
        user = UserDetails.query(UserDetails.email_ID == username).get()
        if check_password_hash(user.password, pswd):
            session['logged_in'] = True
            session['user_email'] = username
            session['username'] = user.userName
            return jsonify(result='')
        else:
            data = 'Invalid username or password.'
            return jsonify(result = data)
    else:
        data = 'Invalid user credentials.'
        return jsonify(result = data)


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
    book=request.form['book']
    deferred.defer(readbook_request_mailing,book)
    data = 'Your book will be sent to you shortly.'
    return jsonify(result = data)


@app.route('/signup', methods=['POST'])
def signup():
    userdet = UserDetails.query().fetch()
    for user in userdet:
        if user.email_ID == request.form['emailid']:
            # flash('The email ID you entered has already been signed up.')
            # return redirect(url_for('homepage'))
            data = 'The email ID you entered has already been signed up.'
            return jsonify(result=data)
        else:
            continue
    else:
        userdetails()
        # flash('Signed up successfully. Log in to access your account in BookForm.')
        # return redirect(url_for('homepage'))
        data = 'Signed up successfully. Log in to access your account in BookForm.'
        return jsonify(result=data)

def userdetails():
    pwd = request.form['password']
    user_details = UserDetails(
        userName=request.form['uname'],
        email_ID=request.form['umail'],
        password=generate_password_hash(pwd)
    )
    user_details.put()


@app.route('/adminsignup')
def adminsignup():
    return render_template('adminsignup.html')


@app.route('/adminrequest')
def adminrequest():
    sender = str('bhaskar.saravanan@adaptavantcloud.com')
    to = str(session['user_email'])
    subject = str('Make me as a Admin')
    body = str('Click this link and fill up the admin signup form. \n https://http://helloworld-151108.appspot.com/adminsignup')
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

    confirmation= ForgotPassword(id=mailid,email=mailid,uid=uid,timestamp=timestamp)
    confirmation.put()

    link = 'https://helloworld-151108.appspot.com/resetpassword/{}&id={}'.format(uid,mailid)

    send_email(to=mailid, body=link)
    flash('Reset Password Link has been sent to your Email,Please check within 10 mins')
    return redirect(url_for('homepage'))




def send_email(to, body, sender='bhaskar.saravanan@adaptavantcloud.com'):
        subject = 'Reset Password Request - Bookforms'
        mail.send_mail(sender, to, subject, body)



@app.route('/resetpassword/<uid>&<mailid>')
def resetpassword(uid,mailid):

    logging.info(uid)
    uid=uid
    id=mailid
    logging.info(id)
    #key_parent = ndb.Key('ForgotPasswordParent', 'uid_parent').get()
    uid_key=ForgotPassword.query(ForgotPassword.uid==uid).get()
    #,parent=key_parent)

    logging.info(uid_key)
    timestamp=uid_key.timestamp
    logging.info(timestamp)
    utc = pytz.UTC
    currenttime = datetime.now().replace(tzinfo=utc)
    currenttime = currenttime.time()
    logging.info(currenttime)
    if timestamp.hour == currenttime.hour:
        minutedifference = currenttime.minute - timestamp.minute
        logging.info(minutedifference)
        if minutedifference <= 10:
            return render_template('resetpassword.html', uid=uid)
        else:
            return 'session expired'
    else:
        return 'session expired'


# @app.route('/resetpasswords/<uid>')
# def resetpasswords(uid):
#     uid=uid
#     return render_template('resetpaswword.html',uid)



@app.route('/resetpasswordstore',methods=['POST'])
def resetpasswordstore():
     mail= request.form['mail']
     uid=request.form['uid']
     entity_key=ForgotPassword.query(ForgotPassword.email == mail).get()
     logging.info(entity_key)
     originaluid=entity_key.uid

     if uid == originaluid:
         if request.form['password'] == request.form['reenterpassword']:
             user = UserDetails.query(UserDetails.email_ID == mail).get()
             logging.info(user)
             newpassword = request.form['password']
             newpassword = generate_password_hash(newpassword)
             user.password = newpassword
             logging.info(user.password)
             user.put()
             flash('Password reset Sucessfully')
             return redirect(url_for('homepage'))

         else:
             return 'Type correct password'

     else:
         return 'Don\'t try to change the uid'




@app.route('/admin', methods=['POST'])
def admin():
    adminname = request.form['emailid']
    adminpsw = request.form['password']
    if Admins.query(Admins.email == adminname).get():
        admin = Admins.query(Admins.email == adminname).get()
        if check_password_hash(admin.password, adminpsw):
            session['logged_in'] = True
            return jsonify(result = '')
        else:
            data = 'Invalid adminname or password.'
            return jsonify(result = data)
    else:
        data = 'Invalid admin credentials.'
        return jsonify(result = data)


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
@app.route('/bookvalidation',methods=['POST'])
def bookvalidation():
    bookname=request.form['bookname']
    authorname=request.form['authorname']
    if Books.query(Books.name == bookname).get():
        if Books.query(Books.author == authorname).get():
            data = 'The book you requested is already in the Book list.'
            return jsonify(result=data)
    user_email = session['user_email']
    name = session['username']
    deferred.defer(newbook_request_mailing, user_email, name, bookname, authorname)
    data = 'Book requested successfully'
    return jsonify(result=data)


@app.route('/get_books')
def get_books():
# data = json.dumps({'isDown': 'Nope'})
# return data, 200, {'Content-Type': 'application/json'}
    books=Books.query().fetch()
    logging.info(books)
    payload=[]
    for book in books:
        payload.append(book.name)
        logging.info(payload)
    payload = json.dumps({"Books": payload})
    logging.info(payload)
    headers = {'Content-Type': 'application/json'}
    return payload,200,headers


secret_key='anykey'
Books_Per_Page=2

parser = reqparse.RequestParser()
parser.add_argument('bookname')
parser.add_argument('authorname')
parser.add_argument('genre')





class Book(Resource):

    def get(self):
         if secret_key == request.headers.get('secret_key'):
            cursor = Cursor(urlsafe=request.args.get('cursor'))
            data, next_cursor, more = Books.query().fetch_page(Books_Per_Page, start_cursor=cursor)
            booklist = []
            for book in data:
                x = book.key.id()
                booklist.append({'id':x, 'name': book.name, 'genre': book.genre, 'author': book.author}})
            if more or next_cursor:
                book = {'books': booklist, "cursor": next_cursor.urlsafe(), "more": more}
            return jsonify(book)
         else:
             return jsonify({'Invalid Secret Key'})

    def post(self):
         args = parser.parse_args()

         if secret_key == request.headers.get('secret_key'):
             bookname = args[ 'bookname' ]
             authorname = args[ 'authorname' ]
             genre = args[ 'genre' ]
             if Books.query(ndb.AND(Books.name == bookname, Books.author == authorname)).get():
                 return make_response(jsonify({'result':'Book is already in the list'}),200)
             else:
                 bookadd = Books(name=bookname, genre=genre, author=authorname)
                 bookadd.put()
                 return make_response(jsonify({"success":"True"}),200)

         else:
             return make_response(jsonify({'Invalid Secret key'}))








# @app.route('/requestbook',methods = ['POST'])
# def requestbook():
#     if secret_key == request.headers.get('secret_key'):
#         bookname = request.form['bookname']
#         authorname = request.form['authorname']
#         emailid=request.form['Email']
#         if Books.query(ndb.AND(Books.name == bookname, Books.author == authorname)).get():
#             return make_response(jsonify({'result':'Book is already in the list'}),200)
#         else:
#             newbook_request_mailing()


api.add_resource(Book, '/Book')

if __name__ == '__main__':
    app.run(debug=True)