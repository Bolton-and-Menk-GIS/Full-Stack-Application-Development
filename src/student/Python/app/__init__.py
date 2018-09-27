from base import FlaskExtension
from flask import Flask, jsonify
from utils import *
from security import security_api, userStore, unauthorized_callback
from brewery_api import brewery_api

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

# set secret key and cookie name for flask-login
app.config['SECRET_KEY'] = 'beer-app'
app.config['REMEMBER_COOKIE_NAME'] = 'beer_app_token'

# uploads folder for beer images
app.config['UPLOAD_FOLDER'] = upload_folder

# register blueprints to get functionality from brewery and security api's
app.register_blueprint(security_api)
app.register_blueprint(brewery_api)


# API METHODS BELOW
@app.route('/')
def hello():
    return jsonify({'message': 'welcome to the brewery api!'})

@app.route('/test', methods=['GET', 'POST'])
def test():
    return jsonify(collect_args())
