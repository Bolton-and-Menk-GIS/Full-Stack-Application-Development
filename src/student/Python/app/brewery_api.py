from flask import url_for, Blueprint, send_file
from flask_login import login_required, current_user
from models import *
from database_utils import create_beer_photo
from exceptions import *
from utils import *
from io import BytesIO
from base import errorHandler

# add brewery API blueprint
brewery_api = Blueprint('brewery_api', __name__)

# default fields
beer_photo_fields = [f for f in list_fields(BeerPhotos) if f != 'data']

# load app config file
config = load_config()
PHOTO_STORAGE_TYPE = config.get('photo_storage_type', 'database')

# json object to lookup Table objects by name
table_dict = {
    'breweries': Brewery,
    'beers': Beer,
    'styles': Style,
    'categories': Category,
    'beer_photos': BeerPhotos
}

# API METHODS BELOW

@brewery_api.route('/breweries')
@brewery_api.route('/breweries/<id>')
@errorHandler
def get_breweries(id=None):
    args = collect_args()
    f = args.get('f', 'json')
    handler = toGeoJson if f.lower() == 'geojson' else lambda t: t
    fields = args.get('fields')

    if id:
        try:
            brewery = query_wrapper(Brewery, id=int(id))[0]
            return jsonify(handler(to_json(brewery, fields)))
        except IndexError:
            raise InvalidResource

    # query as normal
    results = query_wrapper(Brewery, **args)
    return jsonify(handler(to_json(results, fields)))

@brewery_api.route('/breweries/<id>/beers')
@brewery_api.route('/breweries/<id>/beers/<bid>')
def get_beers_from_brewery(id=None, bid=None):
    if not id:
        raise InvalidResource

    # fetch brewery first
    brewery = query_wrapper(Brewery, id=int(id))[0]
    args = collect_args()
    fields = args.get('fields')

    # fetch beers
    if bid:
        try:
            beers = brewery.beers
            # should be a way to achieve this via filter or join?
            return jsonify(to_json([b for b in beers if b.id ==int(bid)][0], fields))
        except:
            raise InvalidResource
    return jsonify(to_json(brewery.beers, **collect_args()))

@brewery_api.route('/beers')
@brewery_api.route('/beers/<id>')
def get_beer_by_id(id=None):
    return endpoint_query(Beer, id=id, **collect_args())

@brewery_api.route('/beers/<id>/photos')
def get_beer_photos(id=None):
    if not id:
        raise InvalidResource

    beer = query_wrapper(Beer, id=int(id))[0]
    return jsonify(to_json(beer.photos, beer_photo_fields))

@brewery_api.route('/beer/photos')
@brewery_api.route('/beer/photos/<id>')
def get_beer_photo(id=None):
    return endpoint_query(BeerPhotos, beer_photo_fields, id)

@brewery_api.route('/beer/categories')
@brewery_api.route('/beer/categories/<id>')
def get_categories(id=None):
    return endpoint_query(Category, id=id, **collect_args())

@brewery_api.route('/beer/categories/<id>/styles')
def get_category_styles(id):
    if id:
        try:
            category_styles = query_wrapper(Category, id=int(id))[0].styles
        except IndexError:
            raise InvalidResource
        return jsonify(to_json(category_styles, **collect_args()))
    raise InvalidResource

@brewery_api.route('/beer/styles')
@brewery_api.route('/beer/styles/<id>')
def get_styles(id=None):
    return endpoint_query(Style, id=id, **collect_args())


@brewery_api.route('/beer/photos/<id>/download')
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


@brewery_api.route('/data/<tablename>/export', methods=['POST'])
@login_required
def export_table_data(tablename):
    if tablename == 'beer_photos':
        return dynamic_error(message='data export is not available for beer photos')
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


# EDITING API BELOW

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

        elif tablename == 'beer_photos' and 'beer_id' in args and 'photo' in args:
            # fetch beer parent first
            try:
                beer = query_wrapper(Beer, id=args.get('beer_id'))[0]
            except:
                return dynamic_error(description='Missing Beer ID', message='A Beer ID is required for submitting a photo')
            photo_blob = args.get('photo')
            try:
                obj = table(**create_beer_photo(data=photo_blob.stream.read(), photo_name=photo_blob.filename))
            except Exception as e:
                return dynamic_error(message=str(e))
            beer.photos.append(obj)

        elif tablename == 'styles' and 'cat_id' in args:
            # fetch parent category first
            category = get_object(Category, id=args.get('cat_id'))
            return dynamic_error(description='Missing Category Information',
                                     message='A "cat_id" (category ID) is required in order to create a new beer style')
            del args['cat_id']
            obj = create_object(Style, **args)
            category.styles.append(obj)

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

        if tablename == 'beer_photos' and args.get('photo'):
            beer_photo = query_wrapper(table, id=id)[0]
            remove_filesystem_photo(beer_photo)

            photo_blob = args.get('photo')
            update_object(beer_photo, **create_beer_photo(data=photo_blob.stream.read(), photo_name=photo_blob.filename))
        else:
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
