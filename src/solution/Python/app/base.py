from flask import Flask, jsonify, url_for
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import default_exceptions, HTTPException
import urllib
from functools import wraps
from . import exceptions
from utils import *
import types

# get all exceptions from our module
exceptionFilter = lambda c: isinstance(c, (type, types.ClassType)) and issubclass(c, HTTPException)
app_exceptions = filter(exceptionFilter, [getattr(exceptions, e) for e in dir(exceptions)])
exception_lookup = {e.code: e for e in app_exceptions}
exception_names = [e.name for e in app_exceptions]

__all__ = ('FlaskExtension', 'JSONExceptionHandler', 'errorHandler')

# handlers for json exceptions
HANDLERS = [(exc, json_exception_handler) for exc in app_exceptions]

class JSONExceptionHandler(object):
    """https://coderwall.com/p/xq88zg/json-exception-handler-for-flask"""

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def std_handler(self, error):
        response = jsonify(message=error.message)
        response.status_code = error.code if isinstance(error, HTTPException) else 500
        return response

    def init_app(self, app):
        self.app = app
        self.register(HTTPException)
        for code, v in default_exceptions.iteritems():
            self.register(code)

    def register(self, exception_or_code, handler=None):
        self.app.errorhandler(exception_or_code)(handler or self.std_handler)

class FlaskExtension(object): 

    def __init__(self, app):
        
        # create attribute for flask app
        self.app = app

        # wrap in CORS for cross origin sharing
        self.app.cors = CORS(self.app)
        self.app.config['CORS_HEADERS'] = 'Content-Type'

        # register error handlers
        self.app.handler = JSONExceptionHandler(self.app)
        for ex, h in HANDLERS:
            self.app.handler.register(ex, h)

        # lookup for all endpoints
        @self.app.route('/endpoints', methods=['GET', 'POST'])
        def endpoints():
            output = []
            for rule in self.app.url_map.iter_rules():

                options = {}
                for arg in rule.arguments:
                    options[arg] = "[{0}]".format(arg)

                methods = ','.join(rule.methods)
                url = url_for(rule.endpoint, **options)
                output.append({'methods': methods, 'url': urllib.unquote(url)})
            return jsonify({'endpoints': sorted(output, key=lambda d: d.get('url'))})

        # preview exceptions by passing in error code
        @errorHandler
        @self.app.route('/tests/exceptions/<code>')
        def testException(code):
            raise exception_lookup.get(code, InvalidResource)


def errorHandler(f):
    @wraps(f)  # functools.wraps
    @cross_origin(origin='*')
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if hasattr(e, 'name') and e.name in exception_names:
                # can safely raise this as it's wrapped in a response
                raise e
            else:
                return dynamic_error(
                    name=e.name if hasattr(e, 'name') else e.__class__.__name__,
                    description=e.message,
                    message=e.args
                )
    return wrapped
