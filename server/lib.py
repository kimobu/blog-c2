import re, hmac, random, string, hashlib

SECRET = '7_oBCRkuV(dqLnUnGz8G'

"""
Form validation functions
"""
PASSWORD_RE = re.compile(r"^.{3,20}$")
def validate_password(password1, password2):
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    if not PASSWORD_RE.match(password1):
        return False
    return True if password1 == password2 else False
    
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validate_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)
    
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def validate_email(email):
    if email == "":
        # Emails are optional
        return True
    else:
        return EMAIL_RE.match(email)
    
"""
Password related functions
"""
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))
    
def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' %(h, salt)
    
def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

def make_secure_val(s):
    return hmac.new(SECRET, s).hexdigest()
    
def check_secure_val(s):
    return True if s and make_secure_val(s) else False
