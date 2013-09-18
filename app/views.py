from app import app, db, login_manager
from flask import render_template, request , redirect, g, flash, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import UserForm, LoginForm, PostForm, TagForm
from models import User, Post, Tag
from config import POSTS_PER_PAGE

@login_manager.user_loader
def load_user(userid):
    return db.session.query(User).filter_by(id=userid).first()

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@app.route('/page/<int:page>')
def index(page = 1):
    #Fake data for testing propuse
    #posts = db.query(Post).order_by(Post.id).all().paginate(page,POSTS_PER_PAGE,False).items #You need a BaseQuery object, this way you have a Query
    posts = Post.query.order_by(Post.id).paginate(page,POSTS_PER_PAGE,False).items
    user = g.user
    return render_template("index.html",
        title = "Home",
        user = user,
        posts = posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        print db.session.query(User).all()
        return render_template('confirmation.html')
    return render_template('register.html', 
        title = 'Sign In',
        form = form)



@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = db.session.query(User).filter_by(nickname=form.nickname.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, form.remember.data)
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash("Password is not correct")
        else:
            flash("Username doesn't exist")
    return render_template('login.html', 
        title = 'Log in',
        form = form)

@app.route('/addtag', methods=['GET','POST'])
def addTag():
    form = TagForm(request.form)
    if request.method == 'POST' and form.validate():
        tag = Tag()
        form.populate_obj(tag)
        db.session.add(tag)
        db.session.commit()  
    return render_template('tag.html', 
        title = 'Add Tag',
        form = form,
        user = g.user)

@app.route('/addpost', methods=['GET','POST'])
def addPost():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post()
        form.populate_obj(post)
        post.author_id = g.user.id
#        post.timestamp = datetime.utcnow()
        db.session.add(post)
        db.session.commit()  
    print db.session.query(Post).all()
    return render_template('addpost.html', 
        title = 'Add post',
        form = form,
        user = g.user)
