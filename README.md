[![Stories in Ready](https://badge.waffle.io/yoyuum/blonkey.png?label=ready&title=Ready)](https://waffle.io/yoyuum/blonkey)
Blonkey
=======

Blonkey is the name of a blog, developed using Flask. Flask is a web framework built over python

Requirements
============

Flask==0.9

Flask-Login==0.2.7

Flask-SQLAlchemy==0.16

Jinja2==2.7.1

MarkupSafe==0.18

SQLAlchemy==0.8.2

SQLAlchemy-Searchable==0.2.1

SQLAlchemy-Utils==0.16.9

WTForms==1.0.4

WTForms-Alchemy==0.7.15

WTForms-Components==0.7.0

Werkzeug==0.9.4

gunicorn==18.0

passlib==1.6.1

six==1.4.1


How to run
==========

Clone this repository and execute "python run.py"

NOTE: If you want to use your own postgres db you may change the addess in "config.py" and use a different secret key for the CSRF Validation

Live demo @ Heroku

http://blonkey.herokuapp.com
