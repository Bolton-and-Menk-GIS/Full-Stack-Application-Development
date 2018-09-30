from flask import request, jsonify
import six
import json
import os
import re
import flask_sqlalchemy
import csv
import time
import shutil
import datetime
import operator
import fnmatch
from werkzeug.exceptions import HTTPException

# https://github.com/GeospatialPython/pyshp
import shapefile

# custom modules
from exceptions import InvalidResource
from models import session

Column = flask_sqlalchemy.sqlalchemy.sql.schema.Column
InstrumentedAttribute = flask_sqlalchemy.sqlalchemy.orm.attributes.InstrumentedAttribute

# download folder
download_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

# prj file contents for shapefile exports
WGS_1984 = """GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]"""


def load_config():
    """load our configuratioo file for the app"""
    config_file = os.path.join(os.path.dirname(__file__), 'config', 'config.json')
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except:
        return {}

def get_timestamp(s=''):
    """create a timestamp in this format: '%Y%m%d%H%M%S'

    :param s: string to prefix the timestamp with
    :return: a string with timestamp inserted
    """
    return '_'.join(filter(None, [s, time.strftime('%Y%m%d%H%M%S')]))

def clean_filename(path):
    """replaces all special characters with underscores

    Required:
        path -- full path to file or folder
    """
    basename, ext = os.path.splitext(os.path.basename(path))
    fn = re.sub('[^A-Za-z0-9]+', '_', basename).replace('__', '_')
    return os.path.join(os.path.dirname(path), fn + ext)

def success(msg='success', **kwargs):
    """ returns a Response() object as JSON

    :param msg: message to send
    :param kwargs: additional key word arguments to add to json response
    :return: Response() object as JSON
    """
    kwargs['message'] = msg
    kwargs['status'] = 'success'
    return jsonify(kwargs)

def dynamic_error(**kwargs):
    """ creates a dynamic error defined at runtime

    :param **kwargs: keyword arguments for custom error name, code, description, and message
    """
    defaults = {
        'code': 501,
        'description': 'Runtime Error',
        'message': 'A runtime error has occured'
    }
    atts = {}
    for k,v in six.iteritems(defaults):
        atts[k] = kwargs.get(k) or defaults[k]

    # create HTTPException Subclass Error dynamically with type()
    errName = kwargs.get('name', 'FlaskRuntimeError')
    de = type(errName, (HTTPException,), atts)
    return json_exception_handler(de)


def json_exception_handler(error):
    """ Returns an HTTPException Object into JSON Response

    :param error: error to convert to JSON response
    :return: flask.Response() object
    """
    response = jsonify({
        'status': 'error',
        'details': {
            'code': error.code,
            'name': error.description,
            'message': error.message
        }
    })

    response.status_code = error.code
    return response

def collect_args():
    """ collects arguments from request including query string, form data, raw json, and files

    :return: dict of request arguments
    """
    # check query string first
    data = {}
    for arg in request.values:
        val = request.args.get(arg, None)
        if val is not None:
            data[arg] = val

    # form data
    for k,v in request.form.iteritems():
        data[k] = v

    # check data attribute as fallback
    request_json = request.get_json() or {}
    for k,v in six.iteritems(request_json):
        data[k] = v
        # no application/json mimetype header...
        try:
            req_data = json.loads(request.data) or {}
            for k,v in six.iteritems(req_data):
                data[k] = v
        except:
            pass

    # finally, check for files
    if request.files:
        for k,v in six.iteritems(request.files):
            data[k] = v
    return data

def list_fields(table):
    """ lists fields for a table """
    if not table:
        return []
    cols = table.__table__.columns if hasattr(table, '__table__') else table.columns
    return [f.name for f in cols]


def validate_fields(table, fields=None):
    """ ensures that available fields are fetched from a table

    :param table: table object
    :param fields: list of fields to validate, default is None
    :return: list of fields
    """
    if isinstance(fields, six.string_types):
        fields = map(lambda f: f.strip(), fields.split(','))
    if not fields or not isinstance(fields, (list, tuple)):
        fields = list_fields(table)
    return fields

def query_wrapper(table, **kwargs):
    """

    :param table: db.Model() for table
    :param kwargs: dict/kwargs of conditions for query
    :param wildcards: (keyword argument) list of field names that should use like query
            instead of equals (string contains)
    :return:
    """
    conditions = []
    wildcards = kwargs.get('wildcards', [])
    if isinstance(wildcards, six.string_types):
        wildcards = wildcards.split(',')
    for kwarg, val in six.iteritems(kwargs):
        if hasattr(table, kwarg):
            col = getattr(table, kwarg)
            if isinstance(col, (Column, InstrumentedAttribute)):
                if kwarg in wildcards:
                    conditions.append(col.like('%{}%'.format(val)))
                else:
                    conditions.append(col==val)
    if conditions:
        return session.query(table).filter(*conditions).all()
    else:
        return session.query(table).all()
        

def to_json(results, fields=None):
    """casts query results to json

    :param results: query results
    :param fields: list of field names to include
    :return:
    """
    fields = validate_fields(results[0] if isinstance(results, list) and len(results) else results, fields)
    if isinstance(results, list):
        if len(results):
            return [{f: getattr(r, f) for f in fields} for r in results]
        else:
            return []
    else:
        return {f: getattr(results, f) for f in fields}

def endpoint_query(table, fields=None, id=None, **kwargs):
    """ wrapper for for query endpoint that can query one feature by id
    or query all features via the query_wrapper

    :param table: Table to query
    :param fields: fields to be returned in query
    :param id: optional resource ID
    :return: Response() object for query result as json
    """
    if id != None:
        try:
            item = query_wrapper(table, id=int(id))[0]
            return jsonify(to_json(item, fields))
        except IndexError:
            raise InvalidResource

    # check for args and do query
    args = collect_args()
    for k,v in six.iteritems(kwargs):
        args[k] = v
    return jsonify(to_json(query_wrapper(table, **args), fields))

# toGeoJson() handler for breweries
def toGeoJson(d):
    """ return features as GeoJson (use this for brewery query)

    :param d: dict of features to return as GeoJson
    :return: GeoJson structure as dict
    """
    if not isinstance(d, list):
        d = [d]
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": f,
                "geometry": {
                    "type": "Point",
                    "coordinates": [f.get('x'), f.get('y')]
                }
            } for f in d
        ]
    }
