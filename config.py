import os

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = "postgres://jbqwkgvkchdwtd:8EYMko4APC4UgzdbjbaGMYgPfU@ec2-184-73-162-34.compute-1.amazonaws.com:5432/d6bp5f6dd0vmv2" #backup
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


CSRF_ENABLED = True
SECRET_KEY = 'Thisisatrapalatrop'
# pagination
POSTS_PER_PAGE = 2
CHARS_PER_POST_PREVIEW = 200
