from . import utils
import os
import io
import json
from PIL import Image

def load_config():
    config_file = os.path.join(os.path.dirname(__file__), 'config', 'config.json')
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return {}

# load config
config = load_config()

# helper for creating a beer photo
def create_beer_photo(photo_name, data):
    """custom handler for inserting data"""
    name, ext = os.path.splitext(photo_name)
    photo_name = utils.clean_filename('{}.png'.format(os.path.basename(name)))

    # create thumbnail version of photo
    storage_type = config.get('photo_storage_type', 'database')
    if storage_type == 'database':
        thumbnail = io.BytesIO()
    else:
        photo_name = '{}_{}.png'.format(os.path.splitext(photo_name)[0], utils.get_timestamp())
        thumbnail = open(os.path.join(utils.upload_folder, photo_name), 'wb')
    print('storage type: ', storage_type)
    thumbData = None
    with Image.open(io.BytesIO(data)) as im:

        # create thumbnail 256x256 pixels
        im.thumbnail((256, 256), Image.ANTIALIAS)
        im.save(thumbnail, 'PNG', optimize=True, quality=50, progressive=True)
        thumbData = thumbnail.getvalue() if storage_type == 'database' else None
        thumbnail.close()
    del thumbnail

    # create actual photo
    return {
        'photo_name': photo_name,
        'data': thumbData
    }