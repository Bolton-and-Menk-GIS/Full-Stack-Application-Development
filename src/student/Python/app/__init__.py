from base import FlaskExtension
from flask import Flask, jsonify
from utils import *
from security import security_api, userStore, unauthorized_callback
from brewery_api import brewery_api
from flask_login import LoginManager
from .exceptions import *

# load config
config = load_config()

# downloads folder for exports
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# uploads folder (used if config.photo_storage_type is 'filesystem')
photo_storage = config.get('photo_storage_type', 'database')
if not os.path.exists(upload_folder) and photo_storage == 'filesystem':
    os.makedirs(upload_folder)

# init app inherited from our base.FlaskExtension object
app_name = os.path.basename(__file__).split('.')[0]
app = Flask(app_name, static_folder=download_folder)

# pass it through our app extension to register error handlers
FlaskExtension(app)

# register flask-login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.unauthorized_handler(unauthorized_callback)

# set secret key and cookie name for flask-login
app.config['SECRET_KEY'] = 'beer-app'
app.config['REMEMBER_COOKIE_NAME'] = 'beer_app_token'

# uploads folder for beer images
app.config['UPLOAD_FOLDER'] = upload_folder

# register blueprints to get functionality from brewery and security api's
app.register_blueprint(security_api)
app.register_blueprint(brewery_api)

# callback to reload the user object for flask-login
@login_manager.user_loader
def load_user(userid):
    return userStore.get_user(id=userid)

@login_manager.request_loader
def load_user_from_request(request):
    """ allow users to be loaded via request params or authorization header """
    # check for token in request params or in Authorization header
    args = collect_args()
    token = args.get('token') or request.headers.get('Authorization')
    if token:
        try:
            user = userStore.get_user(token=token)
            if user.activated == 'False':
                # return None
                raise UserNotActivated
            if datetime.datetime.utcnow() > user.expires:
                # return None
                raise SessionExpired
            return user
        except UserNotFound:
            # return None
            raise UserNotFound

    # return None
    raise TokenRequired


# API METHODS BELOW
@app.route('/')
def hello():
    return jsonify({'message': 'welcome to the brewery api!'})

@app.route('/test', methods=['GET', 'POST'])
def test():
    return jsonify(collect_args())
