# Section 02: Serving Brewery Data

**TL;DR** - *The instructions for this section are outlined below.  If you do not want to copy and paste the code snippets, you can switch to the [solution branch]() for this section by running: `git checkout 02-serve-brewery-data`*

### Creating a REST API
Before just diving into the code, it is important to understand what capabilities the API will expose.  The most obvious thing is to serve the data from the `beer.db` SQLite database as `JSON` for the client application.  The API should also have convenient query options for fetching the brewery data.

The `app.utils` module already has some convenience methods inside that will be useful for serving the data.  Some of the functions that will be heavily used are:

* `success` - return a success message with a status code of 200
* `dynamic_error` - dynamically create runtime errors and return as a response object
* `collect_args` - gets all request arguments in a variety of formats
* `list_fields` - list fields from table
* `to_json` - converts a `Table` object into a `JSON` object
* `query_wrapper` - convenient wrapper function to handle simple and complex table queries. This will support queries based on multiple conditions, wildcards, as well as limiting the returned fields.
* `validate_fields` - function to validate fields passed into the `query_wrapper` function.  This ensures that the requested fields exist in the table.

So what makes a good REST endpoint for querying data? First, the route name should make sense.  So for querying breweries we should start with (all route urls are relative to `<host>:<port>`):

`GET`: `/breweries`

The above query implies that the request would fetch all breweries in the database.  However, it also makes sense to allow the user to narrow their search result by adding query string parameters.  For example, maybe the user is just interested in the breweries in Minneapolis.  Because the `breweries` table has a `city` field, that could be used in the query string:

`GET`: `/breweries?city=Minneapolis`

To acheive this, the `collect_args()` function can be used to parse the query parameters to obtain the condition to do the following query in SQLite:

`SELECT * from breweries WHERE city = 'Minneapolis'`

Fortunately, we are using `flask_sqlalchemy`, which is an [Object Relational Mapper](https://pythonspot.com/orm-with-sqlalchemy/) (ORM).  As a reminder the definition of an ORM from the above link:

>An object relational mapper maps a relational database system to objects. The ORM is independent of which relational database system is used. From within Python, you can talk to objects and the ORM will map it to the database.

#### using the `query_wrapper` function
Rather than writing raw queries, the `query_wrapper()` function can be used, which relies on `flask_sqlalchemy` Tables and the ORM to perform queries. The `query_wrapper` function will return one or more objects that are mapped to rows in the database.  These objects also have a `mapper` class that will fetch the actual `Table` subclass that performs the queries.  This is all abstracted by the `flask_sqlalchemy` and more specifically the `declarative_base`.  The `query_wrapper` function accepts the following parameters:

* `table` - Table/declarative base object to query
* `**kwargs` - primarily used to fetch the conditions to add to the query specific to each database.  In the brewery example above, a keyword argument could be `city='Mineapolis'` to filter based on breweries in Minneapolis. The keys are validated and the arguments are only used if the keys exist as fields in the database. The rest of the arguments are restricted keys that can be used across all tables:
    * `fields` - list or comma separated string for data fields to return in response
    * `wildcards` - comma separated list of fields that are passed in as conditions to be searched via wildcard rather than exact match.  By default, the condition `**kwargs` are an exact match like the case of `city='Minneapolis'`, but what if you want to to do a `field like '%<value>%'`?  That is where the wildcards parameter can be used.  An example would be to find all breweries that are like `'%man%'` to handle an auto complete list based on user search criteria.  That can be achieved by querying `/breweries?name=man&wildcards=name`.
    
Given that the `query_wrapper` will be able to handle some pretty robust queries, this is will be the core functionality used for `GET` requests for fetching data from the database.  This will be very convenient for querying multiple breweries, but what about when you just want one specific brewery?  Obviously, this can be achieved with the above logic, but may not be the cleanest way.  For example:

`GET`: `/breweries?name=Mankato Brewery` or `/breweries?id=57`

While both of the above requests are a perfectly valid way, we can also expose individual items as nested resources by using the brewery `id`.  The above could be fetched as: 

`GET`: `/breweries/57`

The above query would just return the requested resource `{...}`, where the prior two queries would return the one resource inside an array `[ {...} ]`.  In order to achieve this in a sane way, the easiest is to create a helper function that will first check to see if a resource `id` is passed in and if so, return a single object, otherwise perform the query with all other conditions applied.  In VS Code (or your preferred Python IDE) navigate to the `/student/Python/app/utils.py` file and add the following function at the bottom after the `to_json` function:

```py
def endpoint_query(table, fields=None, id=None, as_response=True, **kwargs):
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
    results = query_wrapper(table, **args)
    if kwargs
    return jsonify(to_json(results, fields)) if as_response else to_json(results, fields)
```

This function will be used to query all tables in the database and by default will return a `flask.Response()` object via the `flask.jsonify` function.  Note that this will also through our custom `InvalidResource` from the `app.exceptions` module if there is no resource matching requested `id`.  

So now that we have this function, we can actually see it in action by creating a REST endpoint route for it.  Rather than bloating our `app` module (`app/__init__.py`) with all of our API methods, it is cleaner to use the concept of [Blueprints] to make the application more modular.  For our API, we will create a blueprint called `brewery_api` to handle all the routes for working with the brewery data, and a `security_api` to handle the application security.  Let's start by creating a `brewery_api.py` file inside the `app` folder to represent a blueprint and add the following code:

```py
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

# API METHODS BELOW

@brewery_api.route('/breweries')
@brewery_api.route('/breweries/<id>')
def get_breweries(id=None):
    args = collect_args()
    return endpoint_query(Brewery, id=id, **args)
```

In the above code, we are creating a new `Blueprint` and defining 2 routes with one function (`/breweries` for full query or `/breweries/id` to get the nested resource).  Save this file and we will bring this blueprint into our flask service.  Now go to the `app/__init__.py` file and make the following changes:

* add import statement: `from brewery_api import brewery_api`
* under the line: `app.register_blueprint(security_api)` add:

```py
app.register_blueprint(brewery_api)
```

Now save the file.  One nice thing about making a flask app is that whenever changes are detected, it will automatically restart itself to reflect the changes.  If there are no errors, open Postman and run the `get breweries` query and you should get a `JSON` response similar to: 

```json
[
  {
    "address": "414 6th Ave N",
    "brew_type": "Brewery",
    "city": "Minneapolis",
    "comments": "2014 - 13,000 barrels produced (5th in MN)",
    "created_by": 1,
    "friday": "3pm-11pm",
    "id": 1,
    "monday": "",
    "name": "Fulton Brewing Co",
    "saturday": "12pm-11pm",
    "state": "MN",
    "sunday": "12pm-6pm",
    "thursday": "3pm-10pm",
    "tuesday": "3pm-10pm",
    "website": "http://www.fultonbeer.com/",
    "wednesday": "3pm-10pm",
    "x": -93.27920282199993,
    "y": 44.98494304000007,
    "zip": "55401"
  },
  ... more results
  ]
  ```
  
  Very Cool!  The `breweries` table is now searchable in a REST API!
 
  ![great success](https://media.giphy.com/media/a0h7sAqON67nO/giphy.gif)
  
  Next, feel free to play with this endpoint by adding some queries such as `/breweries?city=Minneapolis` and limit the fields to just name, and city:
  
  `/breweries?city=Minneapolis&fields=name,city` 
  
  And finally, run the `get specific brewery` test in Postman to see the nested resource for the Mankato Brewery.  The url is:
  
  `/breweries/57`
  
  Now that we know this works, other tables can also be exposed through the service.  Go back to the `brewery_api.py` file and add routes for the rest of the tables with this code:
  
  under the `brewery_fields = list_fields(Brewery)` line add:
  
  ```py
  beer_fields = list_fields(Beer)
beer_photo_fields = filter(lambda f: f != 'data', list_fields(BeerPhotos))
```

and under the get breweries route add:
  
  ```py
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
```
  
  


