from google.appengine.ext import ndb

class UserDetails(ndb.Model):
    userName = ndb.StringProperty(required=True)
    email_ID = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required = True)

class Admins(ndb.Model):
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()

class Books(ndb.Model):
    name = ndb.StringProperty()
    genre = ndb.StringProperty()
    author = ndb.StringProperty()
