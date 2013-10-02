from app import app, db, login_manager
from flask import (render_template, request, redirect, g, flash, url_for,
                   jsonify, json)
from flask.ext.login import (login_user, logout_user, current_user,
                             login_required)
from forms import UserForm, LoginForm, PostForm, TagForm
from models import User, Post, Tag, ROLE_USER, ROLE_ADMIN
from config import POSTS_PER_PAGE, CHARS_PER_POST_PREVIEW
from datetime import *


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@app.route('/page/<int:page>')
def index(page=1):
    posts = Post.query.order_by(Post.id.desc()).paginate(page,
                                                         POSTS_PER_PAGE, False)
    user = g.user
    return render_template('content_index.html',
                           title='Home',
                           user=user,
                           posts=posts,
                           charLimit=CHARS_PER_POST_PREVIEW,
                           endpoint='index')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (g.user.role == ROLE_ADMIN):
        form = UserForm(request.form)
        if request.method == 'POST':
            if form.validate():
                user = User()
                form.populate_obj(user)
                db.session.add(user)
                db.session.commit()
                flash('User %s created' % user.nickname)
                return redirect(url_for('index'))
            else:
                # This can be improved recognizing errors such Username in use,
                # repeated mail..
                flash('Error while creating user')
        return render_template('content_register.html',
                               title='Sign In',
                               user=g.user,
                               form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user is None:
            flash("Username doesn't exist")
        elif user.password != form.password.data:
            flash('Password is not correct')
        else:
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('content_login.html',
                           title='Log in',
                           user=g.user,
                           form=form)


@app.route('/tags', methods=['GET', 'POST'])
@login_required
def manage_tags():
    if (g.user.role == ROLE_ADMIN):
        form = TagForm()
        tags = Tag.query.all()
        return render_template('content_manage_tags.html',
                               title='Manage Tags',
                               tags=tags,
                               user=g.user,
                               form=form)
    return redirect(url_for("index"))

# Called using AJAX


@app.route('/tags/add', methods=['POST'])
@login_required
def add_tag():
    # TODO:Add tag to the db if user = admin
    if (g.user.role == ROLE_ADMIN):
        form = TagForm(request.form)
        if request.method == 'POST' and form.validate():
            tag = Tag()
            form.populate_obj(tag)
            db.session.add(tag)
            db.session.commit()
            return jsonify(id=tag.id, name=tag.name)
        flash("Not valid tag")
        return jsonify(error="Not valid Tag")
    return jsonify(error="Not allowed")

# Called using AJAX


@app.route('/tags/del', methods=['POST'])
@login_required
def delete_tag():
    # TODO:Add tag to the db if user = admin
    if (g.user.role == ROLE_ADMIN):
        tag_id = request.form['id']
        tag = Tag.query.filter_by(id=tag_id).first()
        if tag:
            db.session.delete(tag)
            db.session.commit()
            return jsonify(id=tag.id)
        return jsonify(error="Tag doesn't exist")
    return jsonify(error="Not allowed")


@app.route('/tags/<int:query>')
def show_tag(page=1, query=0):  # Query is the ID number of the tag
    tag = Tag.query.filter_by(id=query).first()
    if tag:
        posts = Post.query.filter(Post.tags.any(Tag.name == tag.name))
        page = posts.paginate(page, POSTS_PER_PAGE, False)
        return render_template('content_show_tag.html',
                               title=tag.name,
                               tag=tag,
                               posts=page,
                               user=g.user,
                               charLimit=CHARS_PER_POST_PREVIEW,
                               endpoint='show_tag',
                               query=query)
    return redirect(url_for("index"))


@app.route("/tags/<int:tag_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    if (g.user.role == ROLE_ADMIN):
        form = TagForm(request.form, obj=tag)
        if request.method == 'POST' and form.validate():
            form.populate_obj(tag)
            db.session.add(tag)
            db.session.commit()
            return redirect(url_for('show_tag', tag_id=tag.id))
        return render_template('content_edit_tag.html',
                               title=tag.name,
                               form=form,
                               user=g.user)
    return redirect(url_for('index'))


@app.route('/post/add', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post()
        form.populate_obj(post)
        post.author_id = g.user.id
        post.timestamp = datetime.utcnow()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))
    return render_template('content_add_post.html',
                           title='Add post',
                           form=form,
                           user=g.user)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        return render_template('content_show_post.html',
                               title=post.title,
                               post=post,
                               user=g.user)

    return redirect(url_for("index"))


@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    # To edit a post, if GET check author and populate form,
    # if POST check author and update
    post = Post.query.filter_by(id=post_id).first()
    if ((post.author.id == g.user.id) or g.user.role == ROLE_ADMIN):
        form = PostForm(request.form, obj=post)
        if request.method == 'POST' and form.validate():
            form.populate_obj(post)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('show_post', post_id=post.id))

        return render_template('content_add_post.html',
                               title=post.title,
                               form=form,
                               user=g.user,
                               edit=post_id)

    return redirect(url_for('index'))


@app.route("/post/<int:post_id>/delete")
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if ((post.author.id == g.user.id) or g.user.role == ROLE_ADMIN):
        db.session.delete(post)
        db.session.commit()
        flash("Post %s has been deleted successfully" % post.title)
    return redirect(url_for('index'))


@app.route("/post/search", methods=['GET'])
@app.route("/post/search/page/<int:page>", methods=['GET'])
def post_search(page=1, query=""):
    if (query == ""):
        query = request.args.get('query')
    posts = Post.query.search(query).paginate(page, POSTS_PER_PAGE, False)
    return render_template("content_search.html",
                           title='Searching %s' % query,
                           posts=posts,
                           user=g.user,
                           query=query,
                           endpoint="post_search",
                           charLimit=CHARS_PER_POST_PREVIEW)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html', user=g.user), 404


@app.errorhandler(500)
def internal_error(error):
    # SQLAlchemy should take care of the rollback
    return render_template('error_500.html', user=g.user), 500
