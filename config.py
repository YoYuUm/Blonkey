import os

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = "postgres://poekatqwjbhijk:" + \
                              "TpcAx4OlFpzF9KwsP-B69fJjQG@" + \
                              "ec2-54-228-224-127.eu-west-1" + \
                              ".compute.amazonaws.com:5432/" + \
                              "dejvj3b1artnp7"  # backup
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

CSRF_ENABLED = True
SECRET_KEY = 'Thisisatrapalatrop'
# pagination
POSTS_PER_PAGE = 2
CHARS_PER_POST_PREVIEW = 200
