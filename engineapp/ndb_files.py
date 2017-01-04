from google.appengine.ext import ndb
from werkzeug.security import generate_password_hash, check_password_hash

class User(object):

    # def __init__(self):
        # self.username = username
        # self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


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
#
# class BookRequests(ndb.Model):
#     name = ndb.StringProperty()
#     by_user = ndb.KeyProperty(kind=User)

# hash_pwd = User('surya')
# print hash_pwd.pw_hash