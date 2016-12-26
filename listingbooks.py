from flask import Flask,redirect,url_for,render_template,request

from google.appengine.ext import ndb

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/loginpage')
def loginpage():
    return render_template('AdminLogin.html')


@app.route('/login',methods=['POST'])
def login():
    if request.form['uname'] == 'admin' and request.form['psw'] == 'admin':
        return render_template('adminpage.html')



if __name__=='__main__':
    app.run(debug=True)







