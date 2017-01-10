from flask import Flask,url_for,redirect,render_template,request,flash

from  google.appengine.ext import ndb

app=Flask(__name__)
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/resetpasswords')
def resetpasswords():
    return render_template('resetpassword.html')


@app.route('/adminpage')
def adminpage():
    return render_template('adminpage.html')


@app.route('/userpage')
def userpage():
    books = Book.query().fetch()
    return render_template('userpage.html', books=books)



