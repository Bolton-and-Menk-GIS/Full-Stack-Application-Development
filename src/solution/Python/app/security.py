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

@security_api.route('/users')
@security_api.route('/users/<id>')
def get_users(id=None):
    args = collect_args()
    fields = validate_fields(User, args.get('fields'))
    fields = [f for f in fields if f in user_fields]
    return endpoint_query(User, fields, id)

@security_api.route('/users/create', methods=['POST'])
def create_user():
    args = collect_args()
    args['activated'] = 'False'
    try:
        args['password'] = base64.b64decode(args.get('password'))
    except:
        # in case not passed in as base64
        args['password'] = args.get('password')
    activation_url = args.get('activation_url')
    if 'activation_url' in args:
        del args['activation_url']

    try:
        user = userStore.create_user(**args)
        send_authentication_email(user.email, activation_msg.format(activation_url.format(id=user.id)))
        return success('successfully created user: {}'.format(args.get('username')), activation_url=activation_url.format(id=user.id))
    except:
        raise CreateUserError

@security_api.route('/users/<id>/activate', methods=['POST'])
def activate_user(id):
    user = userStore.get_user(id=int(id))
    if user:
        if user.activated == 'True':
            return success('User is already activated!')
        user.activated = 'True'
        session.commit()
        return success('Successfully activated user')
    return UserNotFound

@security_api.route('/users/login', methods=['POST'])
def login():
    args = collect_args()
    username = args.get('username')
    password = base64.b64decode(args.get('password', ''))
    remember_me = args.get('remember', False) in ('true', True)
    validatedUser = userStore.check_user(username, password)
    if validatedUser:
        if validatedUser.activated == 'False':
            raise UserNotActivated
        login_user(validatedUser, remember=remember_me)

        # update last login and expires
        validatedUser.last_login = datetime.utcnow()
        validatedUser.expires = validatedUser.last_login + timedelta(hours=8)
        session.commit()
        return success('user logged in', token=validatedUser.token)
    raise InvalidCredentials

@security_api.route('/users/welcome')
@login_required
def welcome():
    return success('Welcome {}'.format(current_user.name))

@security_api.route('/users/logout', methods=['POST'])
@login_required
def logout():
    print('CURRENT USER: ', current_user)
    try:
        logout_user()
    except Exception as e:
        raise UnauthorizedUser
    return success('successfully logged out')
