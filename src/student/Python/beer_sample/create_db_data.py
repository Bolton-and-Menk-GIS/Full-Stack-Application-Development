import os
import sys
import json
import six
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(thisDir))
import munch
from app.models import Beer, BeerPhotos, Brewery, Category, Style, session
from app.database_utils import create_beer_photo
from app.security import userStore
from datetime import datetime
import csv

# function get utc time string to datetime()
timestamp_to_date = lambda s: datetime.strptime(s,'%Y-%m-%d %H:%M:%S UTC')


def get_mankato_beers():
    """generator to popuplate beers from mankato brewery
    :return:
    """
    photo_dir = os.path.join(thisDir, 'photos')
    beers_json = os.path.join(thisDir, 'beers-mankato.json')

    with open(beers_json, 'r') as f:
        data = json.load(f)

        # return generator with beer info
        for beer in data:

            # beer obj
            photo_name = beer.get('photo')
            beerObj = munch.munchify({k: v for k,v in six.iteritems(beer) if k != 'photo'})
            beerObj.photo_name = photo_name

            # read photo as binary
            photo_path = os.path.join(photo_dir, photo_name)
            with open(photo_path, 'rb') as p:
                yield (beerObj, p.read())


def load_csv(table, csv_file, **kwargs):
    """loads a csv into a database table, must share the same schema.

    :param table: sqlalchemy.Base Table object
    :param csv_file: path to csv file
    :return: None
    """
    with open(csv_file, 'r') as csvfile:
        for row in csv.DictReader(csvfile):

            # convert date string to datetime() object
            if 'last_mod' in row:
                row['last_mod'] = timestamp_to_date(row['last_mod'])

            # add any additional key word arguments
            for k,v in six.iteritems(kwargs):
                row[k] = v

            # write row, unpack dict to key word arguments
            record = table(**row)
            session.add(record)
    print('loaded "{}" into SQLite database'.format(csv_file))

def create_data():
    """ creates the necessary base data for workshop demo """

    # create test_user
    user = userStore.create_user('John Doe', 'test_user@gmail.com', 'test_user', 'user123', activated='True')
    print('created test user: {}'.format(user))

    # load csv's into SQLite
    breweries = os.path.join(thisDir, 'breweries.csv')
    categories = os.path.join(thisDir, 'categories.csv')
    styles = os.path.join(thisDir, 'styles.csv')

    # call our function to load data to SQLite
    load_csv(Category, categories)
    load_csv(Style, styles)
    load_csv(Brewery, breweries, created_by=user.id)

    # find mankato brewrey and load beers from json file
    mankatoBrewery = session.query(Brewery).filter(Brewery.name == 'Mankato Brewery').first()
    for beer, photoBlob in get_mankato_beers():
        # create new beer first
        photo_name = beer.photo_name
        del beer.photo_name

        # add created by
        beer['created_by'] = user.id
        newBeer = Beer(**beer)

        # create new beer photo
        # newBeer.photos.append(create_beer_photo(beer_id=newBeer.id, photo_name=photo_name, data=photoBlob))
        newBeer.photos.append(BeerPhotos(**create_beer_photo(photo_name, photoBlob)))
        mankatoBrewery.beers.append(newBeer)

    # commit db changes
    session.commit()


if __name__ == '__main__':

    # run function to create the data
    create_data()

    # had some issues with sqlite db corrupting on my mac, see:
    #   http://www.froebe.net/blog/2015/05/27/error-sqlite-database-is-malformed-solved/
    # in sqlite run: "pragma integrity_check;"
