# Multi-user blog

This project is designed for Google App Engine. To run it:

cd multi-user-blog
dev_appserver.py app.yaml

Then, browser to 127.0.0.1:8080 in your web browser.

Important files:
main.py:
    This is the main python file. It implements a Flask-based website
    
lib.py:
    This contains helper functions that primarily enable authentication
    
templates:
    These are the HTML files that get displayed to a user
    
    
## Features
* User creation
    * Users can create their own accounts
    * Users are prevented from creating an account with an existing username

* Login
    * User accounts are remembered and users can log in and out
    * User login is tracked via a secure code

* Blog creation
    * Users can write blog posts that are viewable by everyone on the internet
    * Users can edit and delete their own blog posts

* Social aspects
    * Users can like and comment on blog posts
    * Users cannot like their own posts
    * Be careful, comments cannot be edited or deleted!
# blog-c2
