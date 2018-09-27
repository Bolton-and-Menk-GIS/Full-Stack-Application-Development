import random
import string
import base64
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models import User
from utils import *
from exceptions import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# user fields to return (no others allowed for security purposes)
user_fields = ['id', 'name', 'username', 'email', 'activated']

# create blue print
security_api = Blueprint('security_api', __name__)

__all__ = ('User', 'security_api', 'userStore', 'unauthorized_callback')

# unauthorized user callback for flask login (must return a Response() )
unauthorized_callback = lambda: json_exception_handler(UnauthorizedUser)

# activation email template
activation_msg = """<div>
<h4 style="color: forestgreen; font-weight: bold; margin-top: 10px;">Thank you for signing up for Brewery Finder</h4>
<p sytle="color: gray; font-size: 18px;">To complete the activation process for your account, please follow <a href="{}" style="color: orange; font-weight: bold; text-decoration: underline;">this link</a>.</p>
</div>"""

def create_random_string(length=64):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in xrange(length or 64)])

class UserStore(object):
    """helper class for user store"""

    @property
    def users(self):
        return session.query(User).all()

    def get_user(self, **kwargs):
        try:
            return query_wrapper(User, **kwargs)[0]
        except IndexError:
            raise UserNotFound

    def get_users(self, **kwargs):
        return query_wrapper(User, **kwargs)

    def create_user(self, name=None, email=None, username=None, password=None, activated='False'):

        # create a token for this user, this hash is used by service to lookup user
        token = create_random_string()
        pw = generate_password_hash(password, salt_length=16)
        user = User(name=name, email=email, username=username, password=pw, token=token, activated=activated)
        session.add(user)
        session.commit()
        return user

    def check_user(self, username, password):
        user = self.get_user(username=username)
        if not user:
            return None
        return user if check_password_hash(user.password, password) else None

userStore = UserStore()

# send authentication email
def send_authentication_email(to_addr, msg):
    config = load_config()
    host = config.get('out_email_host')
    port = config.get('out_email_port')
    from_addr = config.get('out_email_address')
    pw = config.get('out_email_pw')

    # build email
    emsg = MIMEMultipart('alternative')
    emsg['Subject'] = 'Brewery Finder Registration'
    emsg['TO'] = to_addr
    emsg['FROM'] = from_addr

    if msg.startswith('<'):
        # it is html?
        emsg.attach(MIMEText(msg, 'html'))
    else:
        emsg.attach(MIMEText(msg, 'plain'))

    # connect to email server
    s = smtplib.SMTP(host)
    s.starttls()
    s.ehlo()
    s.login(from_addr, pw)
    s.sendmail(from_addr, to_addr, emsg.as_string())
    s.quit()


# API METHODS BELOW