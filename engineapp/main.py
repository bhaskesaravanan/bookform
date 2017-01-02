from flask import Flask,url_for,redirect,render_template,request,flash


from  google.appengine.ext import ndb

app=Flask(__name__)




class UserDetails(ndb.Model):
    UserName=ndb.StringProperty(required=True)
    Email_ID=ndb.StringProperty(required=True)
    Book=ndb.StringProperty(required=True)
    requestbook=ndb.StringProperty(required=True)


class AddingBooks(ndb.Model):
    bookname=ndb.StringProperty(required=True)
    genre=ndb.StringProperty(required=True)
    Author=ndb.StringProperty(required=True)



@app.route('/')
def homepage():

    users = AddingBooks.query().fetch()
    return render_template('homepage.html', users=users)


@app.route('/loginpage')
def loginpage():
     return render_template('AdminLogin.html',)


@app.route('/login',methods=['POST'])
def login():
    if request.form['uname'] == 'admin' and request.form['psw'] == 'admin':
        return render_template('adminpage.html')


@app.route('/userdetails',methods=['GET'])
def userdetails():

    user = UserDetails(UserName=request.args.get('name'),Email_ID=request.args.get('mail'),Book=request.args.get('book'),requestbook=request.args.get('requirebook'))
    user.put()
    return 'Succesfully registered'




@app.route('/addingbook',methods=['GET'])
def addingBook():
    addbook=AddingBooks(bookname=request.args.get('bookname'),genre=request.args.get('genre'),Author=request.args.get('authorname'))
    addbook.put()
    # flash('Sucessfully added')




if __name__=='__main__':
    app.run(debug=True)







