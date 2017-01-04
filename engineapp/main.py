import json
import sys
import os


from google.appengine.ext import ndb
#from oauth2client import client, crypt
from flask import Flask,render_template,request




app=Flask(__name__)
CLIENT_ID="409456169998-ltl07nbg70vlpkhfeuauphoqmvjghuci.apps.googleusercontent.com"
CLIENTSECRETS_LOCATION = 'A7nYiIso9mveuh6YIMzUAsZS'
REDIRECT_URI = '["http://workwithflask.appspot.com/addbook","http://localhost:9080/addbook"]'
SCOPES = [
                'https://www.googleapis.com/auth/gmail.readonly',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                # Add other requested scopes.
        ]


@app.route('/')
def homepage():
    return render_template('mainpage.html')

@app.route('/addbook')
def googledetails():
    return render_template(addbook.html)


# @app.route('/addbook')
# def logindetails():
#     return render_template('addbook.html')

@app.route('/add', methods=['POST'])
def addbook():
    # uemail = request.form['email']
    # p=request.form['pwd']
    # a=UserInformation.query(UserInformation.email == uemail).get()
    # b=UserInformation.query(UserInformation.password == pwd).get()
    # user = uemail.Key().get()
    # return user
    if request.form['email'] == 'admin' and request.form['psw'] == 'admin' :
        return render_template('addbook.html')
    else:
        return "your entered username and password dosent match "

@app.route('/usersinup')
def sinup():
    return render_template('usersinup.html')


@app.route('/userdetails', methods=['POST'])
def userInfo():
    users = UserInformation(firstname = request.form['fname'], lastname = request.form['lname'],  email = request.form['email'],  password = request.form['pwd'])
    users.put()
    return render_template('regsuccess.html')

# @app.route('/regsuccess')
# def regsucess():
#     return render_template('mainpage.html')




# @app.route('/login',methods=['POST'])
# def login():
#     if request.form['uname'] == 'admin' and request.form['psw'] == 'admin':
#         return render_template('addbook.html')
#     else:
#         return render_template('authentication.html')




# @app.route('/userdetails',methods=['GET'])
# def userdetail():
#     user = UserDetails(name=request.args.get('uname'),email=request.args.get('email'),book=request.args.get('book'))
#     user.put()
#     return render_template('sucess.html')
#
#
# # @app.route('/login',method='post')
# # def admindetails():
# #     admin = AdminDetails(UserName=request.args.get('uname'),password=request.args.get('pwd'))
# #     admin.put()
#
# @app.route('/bookdetails', methods=['GET'])
# def bookdetail():
#     bookdet = BookDetails(bookname = request.args.get('bookname'), author_name=request.args.get('authorname'), description=request.args.get('des'))
#     bookdet.put()
#     return render_template('addsucess.html')

if __name__=='__main__':
    app.run(debug = True)