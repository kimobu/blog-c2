from flask import Flask, render_template, request, flash
from flask import redirect, url_for, make_response, jsonify
from flask import session as login_session
from functools import wraps

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker

from models import Post, User, Comment
from lib import validate_username, validate_password
import json

app = Flask(__name__)
app.config['DEBUG'] = True

engine = create_engine('sqlite:///blog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

def login_required(f):
    """
    This function checks to see if a user is logged in
    If they are not logged in, they are redirected to the login page
    If they are logged in, they are sent to the page requested

    Other functions will use the @login_required decorator to call this
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not login_session.get('username'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def render(request, template, **kwargs):
    """
    This is a wrapper function so that every page can be checked for a login
    Additionally, a caller can specify an HTTP status code that will be
    applied to the response object
    """
    code = kwargs.get('code', '200')
    if code:
        return render_template(template, login_session=login_session, **kwargs), code
    else:
        return render_template(template, login_session=login_session, **kwargs)


def do_login(user):
    """
    This function performs a login by generating the secure value and
    setting a cookie
    """
    response = redirect(url_for('welcome'))
    login_session['username'] = user.username
    return response


def get_user(username):
    """
    This is an abstraction of getting a User entity out of the GAE NDB
    """
    user = session.query(User).filter_by(username=login_session['username'])
    return user


def get_post(post_id):
    """
    This is an abstraction of getting a Blog entity out of the GAE NDB
    """
    post = session.query(Post).get(post_id)
    return post

"""
Blog page handlers
"""


@app.route('/')
def home():
    """Display blog messages"""
    posts = session.query(Post).all()
    return render(request, 'home.html', posts=posts)


@app.route('/post/<post_id>')
def post(post_id):
    """Display a single post post"""
    post = get_post(post_id)
    return render(request, 'post.html', post=post)


@app.route('/newpost', methods=["POST", "GET"])
@login_required
def new_post():
    if request.method == "POST":
        username = login_session['username']
        user = session.query(User).filter(User.username == username).first()
        form = request.form
        subject = form['subject']
        body = form['body']
        if subject and body:
            new_post = Post(subject=subject, body=body, user_id=user.id)
            session.add(new_post)
            session.commit()
            return redirect(url_for('post', post_id=new_post.id))
        else:
            error = "Please check your subject and body"
            return render(request, 'newpost.html', subject=subject,
                          body=body, error=error)
    elif request.method == "GET":
        return render(request, 'newpost.html')


"""
Comment page handlers
"""
@app.route('/newcomment', methods=["POST"])
def new_comment():
    """
    Creates and saves a post comment
    """
    form = request.form
    post_id = form['post_id']
    body = form['body']
    username = form['username']
    comment = Comment(username=username, body=body, post_id=post_id)
    session.add(comment)
    session.commit()
    d = {'status': 'ok', 'username':username, 'comment_id': comment.id}
    return jsonify(**d)


"""
Auth related page handlers
"""


@app.route('/welcome')
def welcome():
    """
    Displays a welcome page after a user is logged in
    """
    username = login_session['username'] 
    if not username:
        return redirect(url_for('login'))
    response = render(request, 'welcome.html')
    return response


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        """ Try to create a new user """
        form = request.form
        username = form['username']
        valid_username = validate_username
        password = form['password']
        valid_password = validate_password
        verify = form['verify']
        error = ""
        if not valid_username:
            error += "Bad username<br />"
        if not valid_password:
            error += "Bad password or passwords don't match <br />"
        if not (valid_username and valid_password):
            return render(request, 'signup.html', username=username,
                          email=email, error=error)

        user_taken = session.query(exists().where(User.username==username)).scalar()
        if not user_taken:
            user = User(username=username, password=password)
            session.add(user)
            session.commit()
        else:
            error += "Username is already taken"
            return render(request, 'signup.html', username=username,
                          error=error)

        return do_login(user)
    else:
        return render(request, 'signup.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        """ Try to get the user and log them in """
        form = request.form
        username = form['username']
        password = form['password']
        user = session.query(User).filter(User.username==username).first()
        if user and user.password == password:
            return do_login(user)
        else:
            error = "Invalid login"
            return render(request, 'login.html', username=username,
                          password=password, error=error)
    else:
        """ Just display the login page """
        if next:
            """
            The user was redirected here
            Set the HTTP code so that the Javascript can redirect the user
            """
            return render(request, 'login.html', code=302)
        return render(request, 'login.html')


@app.route('/logout')
def logout():
    """
    Unset the cookie to log the user out
    """
    response = redirect(url_for('home'))
    del login_session['username']
    return response


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

if __name__ == '__main__':
    app.secret_key = 'inept-afield-quebec-oases'
    app.run(host='0.0.0.0', port=80)

