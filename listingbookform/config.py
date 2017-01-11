import os



if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    app_url = 'https://myfirsthelloworldwithflask.appspot.com/'
else:
    app_url = 'http://localhost:9080'