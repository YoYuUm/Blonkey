from app import db
#from config import SQLALCHEMY_DATABASE_URI
#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import PasswordType
from sqlalchemy_searchable import Searchable, SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from wtforms_alchemy import ModelForm

#engine = create_engine(SQLALCHEMY_DATABASE_URI)
#base = declarative_base(db)
#Session = sessionmaker(bind=db)
#session = Session()

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):   
    __tablename__ = "user"

    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    nickname = db.Column(db.String(32), index = True, nullable = False, unique = True)
    email = db.Column(db.String(120), index = True, nullable = False, unique = True)
    password = db.Column(PasswordType(
            schemes=['pbkdf2_sha512']), nullable = False) #Storing encrypted password
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = relationship("Post", backref = "author") 
    
    def __repr__(self):
        return '<Id %r, Nickname %r, Email %r, Admin %r, posts %r >' % (self.id, self.nickname, self.email, self.role, self.posts)
#Methods for user managment in Flask-login
 #Returns True if the user is authenticated, i.e. they have provided valid credentials.
 #(Only authenticated users will fulfill the criteria of login_required.)
 #TODO
    def is_authenticated(self):
        return True
#Returns True if this is an active user - in addition to being authenticated, they also have
#activated their account, not been suspended, or any condition your application has for rejecting an account.
#Inactive accounts may not log in (without being forced of course).
#TODO
    def is_active(self):
        return True
#Returns True if this is an anonymous user. (Actual users should return False instead.)
    def is_anonymous(self):
        return False
#Returns a unicode that uniquely identifies this user, and can be used to load the user 
#from the user_loader callback. Note that this must be a unicode - if the ID is natively 
#an int or some other type, you will need to convert it to unicode.
    def get_id(self):
        return unicode(self.id)

association_table = db.Table('association',
    db.Column('post_id',db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id',db.Integer, db.ForeignKey('tag.id'))
)

class PostQuery(BaseQuery, SearchQueryMixin):
    pass

class Post(db.Model, Searchable):   
    query_class = PostQuery
    __tablename__ = "post"
    __searchable_columns__ = ['title', 'text']

    __search_options__ = {
        'catalog': 'pg_catalog.english'
    }

    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    title = db.Column(db.String(128), nullable = False)
    text = db.Column(db.Text, nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = relationship("Tag", secondary=association_table, backref="posts")
    timestamp = db.Column(db.DateTime)
    #search_vector is the default name of the var vector in SQLalchemy
    search_vector= db.Column(TSVectorType) 
    def __repr__(self):
        return '<Id %r, Title %r, Author %r, tags %r> ' % (self.id, self.title, self.author, self.tags)


class Tag(db.Model):   
    __tablename__ = "tag"

    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    
    def __repr__(self):
        return self.name