from flask import url_for, Blueprint, send_file
from flask_login import login_required, current_user
from models import *
from database_utils import create_beer_photo
from exceptions import *
from utils import *
from io import BytesIO

# add brewery API blueprint
brewery_api = Blueprint('brewery_api', __name__)

# get list of brewery fields to use as default
brewery_fields = list_fields(Brewery)
beer_fields = list_fields(Beer)
beer_photo_fields = filter(lambda f: f not in ('data', 'thumbnail'), list_fields(BeerPhotos))

# constants
category_fields = list_fields(Category)
style_fields = list_fields(Style)
table_dict = {
    'breweries': Brewery,
    'beers': Beer,
    'styles': Style,
    'categories': Category
}

# load app config file
config = load_config()
PHOTO_STORAGE_TYPE = config.get('photo_storage_type', 'database')

# helper function for removing filesystem photos
def remove_filesystem_photo(beer_photo):
    if PHOTO_STORAGE_TYPE == 'filesystem':
        photo = os.path.join(upload_folder, beer_photo.photo_name)
        if os.path.exists(photo):
            try:
                os.remove(photo)
            except:
                print('unable to remove photo from filesystem')

# REST API METHODS BELOW

@brewery_api.route('/beer/categories')
@brewery_api.route('/beer/categories/<id>')
def get_categories(id=None):
    return endpoint_query(Category, category_fields, id)

@brewery_api.route('/beer/categories/<id>/styles')
def get_category_styles(id):
    if id:
        category_styles = query_wrapper(Category, id=int(id))[0].styles
        return jsonify(to_json(category_styles, style_fields))

@brewery_api.route('/beer/styles')
@brewery_api.route('/beer/styles/<id>')
def get_styles(id=None):
    return endpoint_query(Style, style_fields, id)

@brewery_api.route('/breweries')
@brewery_api.route('/breweries/<id>')
def get_breweries(id=None):
    args = collect_args()
    f = args.get('f', 'json')
    handler = toGeoJson if f.lower() == 'geojson' else lambda t: t
    fields = args.get('fields') or brewery_fields

    results = endpoint_query(Brewery, fields, id, as_response=False, **args)
    return jsonify(handler(to_json(results, fields)))

    # if id:
    #     try:
    #         brewery = query_wrapper(Brewery, id=int(id))[0]
    #         return jsonify(handler(to_json(brewery, fields)))
    #     except IndexError:
    #         raise InvalidResource

    # # query as normal
    # results = query_wrapper(Brewery, **args)
    # return jsonify(handler(to_json(results, fields)))

@brewery_api.route('/breweries/<id>/beers')
@brewery_api.route('/breweries/<id>/beers/<bid>')
def get_beers_from_brewery(id=None, bid=None):
    if not id:
        raise InvalidResource

    # fetch brewery first
    brewery = query_wrapper(Brewery, id=int(id))[0]

    # fetch beers
    if bid:
        try:
            beers = brewery.beers
            # should be a way to achieve this via filter or join?
            return jsonify(to_json([b for b in beers if b.id ==int(bid)][0], beer_fields))
        except:
            raise InvalidResource
    return jsonify(to_json(brewery.beers, beer_fields))

@brewery_api.route('/beers')
@brewery_api.route('/beers/<id>')
def get_beer_by_id(id=None):
    return endpoint_query(Beer, id=id)

@brewery_api.route('/beers/<id>/photos')
def get_beer_photos(id=None):
    if not id:
        raise InvalidResource

    beer = query_wrapper(Beer, id=int(id))[0]
    return jsonify(to_json(beer.photos, beer_photo_fields))

@brewery_api.route('/beer_photos')
@brewery_api.route('/beer_photos/<id>')
def get_beer_photo(id=None):
    return endpoint_query(BeerPhotos, beer_photo_fields, id)

@brewery_api.route('/beer_photos/<id>/download')
def download_beer_photo(id):
    if not id:
        raise InvalidResource

    beer_photo = query_wrapper(BeerPhotos, id=int(id))[0]

    # handle appropriately based on config
    if PHOTO_STORAGE_TYPE == 'filesystem':
        to_send = os.path.join(upload_folder, beer_photo.photo_name)
    else:
        to_send = BytesIO(beer_photo.data)
    return send_file(to_send, attachment_filename=beer_photo.photo_name, as_attachment=True)

# struggling with route name here???
@brewery_api.route('/beer_photo/add', methods=['POST'])
@login_required
def add_beer_photo():
    args = collect_args()
    try:
        beer = query_wrapper(Beer, id=int(args.get('beer_id')))[0]
    except:
        return dynamic_error(description='Missing Beer ID', message='A Beer ID is required for submitting a photo')
    # return jsonify(to_json(beer, beer_fields)) #test
    photo_blob = args.get('photo')
    try:
        new_photo = BeerPhotos(**create_beer_photo(data=photo_blob.stream.read(), photo_name=photo_blob.filename))
    except Exception as e:
        return dynamic_error(message=str(e))
    print('NEW PHOTO: ', photo_blob.filename)
    beer.photos.append(new_photo)
    session.commit()
    return success('successfully updated photo', id=new_photo.id)

@brewery_api.route('/beer_photos/<id>/update', methods=['POST', 'PUT'])
@login_required
def update_beer_photo(id):
    if not id:
        raise InvalidResource
    args = collect_args()
    beer_photo = query_wrapper(BeerPhotos, id=int(id))[0]
    remove_filesystem_photo(beer_photo)

    photo_blob = args.get('photo')
    update_object(beer_photo, **create_beer_photo(data=photo_blob.stream.read(), photo_name=photo_blob.filename))
    session.commit()
    return success('successfully updated photo', id=beer_photo.id)


@brewery_api.route('/beer_photos/<id>/delete', methods=['DELETE'])
@login_required
def delete_beer_photo(id):
    if not id:
        raise InvalidResource
    beer_photo = query_wrapper(BeerPhotos, id=int(id))[0]
    remove_filesystem_photo(beer_photo)
    photo_id = beer_photo.id
    delete_object(beer_photo)
    session.commit()
    return success('successfully deleted photo', id=photo_id)


@brewery_api.route('/data/<tablename>/export', methods=['POST'])
@login_required
def export_table_data(tablename):
    table = table_dict.get(tablename)
    print(tablename, table)
    if table:
        args = collect_args()
        fields = args.get('fields')
        f = args.get('f')
        if f:
            del args['f']
        else:
            f = 'csv'
        if fields:
            del args['fields']

        outfile = export_data(table, fields, f, **args)
        return success('successfully exported data',
                       filename=os.path.basename(outfile),
                       url=url_for('static', filename=os.path.basename(outfile), _external=True))
    raise InvalidResource

@brewery_api.route('/data/<tablename>/create', methods=['POST'])
@login_required
def create_item(tablename):

    table = table_dict.get(tablename)
    if table:
        args = collect_args()
        if current_user:
            args['created_by'] = current_user.id

        # check if related feature (Beer, etc)
        obj = None
        if tablename == 'beers' and 'brewery_id' in args:
            # must get brewery first
            brewery = get_object(table_dict['breweries'], id=args['brewery_id'])
            if not brewery:
                return dynamic_error(description='Missing Brewery Information',
                                     message='A "brewery_id" is required in order to create a new beer')

            # now that we have a valid brewery, create the new beer and append to the brewery "beers" attribute
            del args['brewery_id']
            obj = create_object(table, **args)
            brewery.beers.append(obj)

        elif tablename == 'beer_photos' and 'beer_id' in args:
            # fetch beer parent first
            beer = get_object(table_dict['beers'], id=args['beer_id'])
            del args['beer_id']

            # add to photos attribute
            beer.photos.append(BeerPhotos(**create_beer_photo(**args)))
        else:
            obj = create_object(table, **args)
            session.add(obj)

        if obj:
            # commit database transaction if we have a valid object
            session.commit()
            return success('Successfully created new item in "{}"'.format(tablename), id=obj.id)
        return dynamic_error(message='Missing parameters for creating a new {}'.format(tablename))

    raise InvalidResource


@brewery_api.route('/data/<tablename>/<id>/update', methods=['POST', 'PUT'])
@login_required
def update_item(tablename, id):
    table = table_dict.get(tablename)
    if table:
        obj = get_object(table, id=id)
        if not obj:
            raise InvalidResource
        args = collect_args()
        update_object(obj, **args)
        session.commit()
        return success('Successfully updated item in "{}"'.format(tablename), id=obj.id)

    raise InvalidResource

@brewery_api.route('/data/<tablename>/<id>/delete', methods=['DELETE'])
@login_required
def delete_item(tablename, id):
    table = table_dict.get(tablename)
    if table:
        obj = get_object(table, id=id)
        if not obj:
            raise InvalidResource
        oid = obj.id
        delete_object(obj)
        session.commit()
        return success('Successfully deleted item in "{}"'.format(tablename), id=oid)

    raise InvalidResource