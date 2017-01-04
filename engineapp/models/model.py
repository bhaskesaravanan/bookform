from google.appengine.ext import ndb

class UserInformation(ndb.Model):
    firstname = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    # timestamp = ndb.DateTimeUpdate(auto_new_add = True)


class GoogleLogin():
    CLIENT_ID = '409456169998-ltl07nbg70vlpkhfeuauphoqmvjghuci.apps.googleusercontent.com'
    CLIENT_SECRET = 'Gz_7FOoUyWABfm_qEYRS217_'
    REDIRECT_URI = 'workwithflask.appspot.com/addbook'


class GoogleUser(UserInformation):
    token = ndb.StringProperty(required=True)
    oauth_type = ndb.StringProperty(choices=["google", "facebook"])


# class AdminDetails(ndb.Model):
#     username = ndb.StringProperty(required = True)
#     password = ndb.StringProperty(required = True)
#     #timestamp = ndb.DateTimeUpdate(auto_new_add=True)
#


# class BookDetails(ndb.Model):
#     bookname = ndb.StringProperty(required = True)
#     author_name = ndb.StringProperty(required = True)
#     description = ndb.TextProperty(required = True)
