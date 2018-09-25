# Full-Stack-Application-Development

#### Minnesota GIS LIS Conference 2018 - Duluth, MN

Welcome to the Full Stack Application Development Workshop .  This repository contains the materials needed to create the sample application and the associated REST API.  In this workshop, we will see how to create a custom RESTful API using  [Flask](http://flask.pocoo.org/) - a microframework for Python.  A Single Page Application (SPA) will also be created using [Vue.js](https://vuejs.org/) to interface with our API.

We will be creating an application called `Brewery Finder` that will act as a crowdsourcing application where users can view, create, update, delete, and export brewery information in a mapping context as well as add featured beers for each brewery.  Under the hood, we will be using a Sqlite Database to store the brewery information and the REST API we create will be the broker for communicating to the database.

### Recommended Software
in order to have the best development experience, it is recommended that before starting you have the following things insalled:
 
 * [node.js](https://nodejs.org/en/about/) (version8.11+) - asynchronous JavaScript runtime
 * [git](https://git-scm.com/) (with bash) - version control software
 * code editors such as [VS Code](https://code.visualstudio.com/), [WebStorm](https://www.jetbrains.com/webstorm/), [Atom](https://atom.io/), etc.
    * need editor for Python as well, (VS Code can be configured to work with both Python and JavaScript) such as [PyScripter](https://sourceforge.net/projects/pyscripter/), [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows) (community edition is free), etc.
* [Google Chrome](https://www.google.com/chrome/?brand=CHBD&gclid=Cj0KCQjwuafdBRDmARIsAPpBmVWnLFUBgsRQnZuIBhsYc5G-sEekeIx9CEMd53Yrv0RTlVvD-k7ULsgaApzEEALw_wcB&gclsrc=aw.ds&dclid=COmg_c3R1t0CFQ_JwAodfIQA_Q) - best browser for debugging
* [Fiddler](https://www.telerik.com/fiddler) - web debugging proxy to monitor requests
* [Postman](https://www.telerik.com/fiddler) - API Development Environment that will be used to test our REST API
* [DB Browser for Sqlite](http://sqlitebrowser.org/) - convenieintly view/update Sqlite databases

In the interest of saving time, I have created some boiler plates to start with that have both the core Python Flask service set up as well as the skeleton of our `Brewery Finder` app.  These are located in the [student folder]().  The sections below outline the contents of this folder:

### `/student/Python/app`  (Python/Flask Code):

* `/config/config.json` - contains a configuration file for our app
    * email account settings, photo storage mode for beers
* `base.py` - `FlaskExtension` class that will allows error custom handling and `errorHandler` decorator
* `__init__.py` - this is the entry point file to the Flask Application
    * sets up basic Flask app configuration options as well as two test routes for our REST API `/` and `/test`
* `utils.py` - contains utility functions essential to the application such as `collect_args()`, etc
* `database_utils.py` - contains helper function for processing photos for beers
* `models.py` - contains the schema and table objects for SqlAlchemy
* `/venv` - python virtualenv for windows
* `/mac_venv` - python virtualenv for mac
* `/beer_sample` - contains csv's and other sample data used to create the brewery data
    *  `create_db_data.py` - script that creates Sqlite database and loads in all brewery data
* `create_databases.sh` - shell script that starts `virtualenv` and creates the datbase
* `run.py` - python script that runs the Flask app
* `run.sh` - shell script that runs the Flask app sript through the `virtualenv` (use this to start the app)

### `/student/app`  (JavaScript Code):
* `/components` - contains the `Vue` components used to comprise the app (`.vue` files)
* `/modules` - contains normal es6 JavaScript modules
* `App.vue` - the main template for the application
* `main.js` - entry point to application
* `babel.config.js` - contains the babel configuration options for webpack
* `package.json` - manifest for the application, includes dependency info
* `vue.config.js` - main configuration options for webpack and production build


## Getting Started 

### install node modules  (inside VS Code Terminal)
1. launch VS Code and open the `student` folder
2. open the terminal and type the following commands, hitting `enter` after each one:

    `cd app`
    `npm install`

##### this will take a while to run, so while this is working please move on to setting up Postman

### set up Postman to test our API
1. launch Postman
2. create a new environment 
    - hit the gear button in the upper right hand corner > Manage Environments > Add
    - Call it `Brewery API`
    - Add the following (key, value) pairs:
        | key  | value |
        | ------------- | ------------- |
        | host  | localhost  |
        | port  | 5001  | 
        | auth | <leave blank, we will fill this out later> |
3. import the API tests from the `/student/API_Tests/Brewery_API.postman_collection.json` file
    * this will load all the API tests for the REST API (note: the tests will not work until the routes are created!)

#### test the Flask app
1. double click the `run.sh`
    * the terminal message should say it started the `virtualenv` and the app is running on port `5001`
2. Go back to Postman and find the `Brewery API` Collection in the left pane and expand it
3. the first request in the list is a `GET` request called `endpoints`.  Click on this.
    * notice the request url is set to `{{host}}:{{port}}/endpoints`.  Postman will use our environment varialbes to fill in the host and port automatically.  It is good practice to use variables for things like this to test development and production environments by simply swapping out the host and port variables.
    * Hit the `Send` button to make the requst.  You should get a JSON response that looks like this:
   
```json
{
    "endpoints": [
        {
            "methods": "HEAD,OPTIONS,GET",
            "url": "/"
        },
        {
            "methods": "HEAD,OPTIONS,GET",
            "url": "/downloads/[filename]"
        },
        {
            "methods": "HEAD,POST,OPTIONS,GET",
            "url": "/endpoints"
        },
        {
            "methods": "HEAD,OPTIONS,GET",
            "url": "/test"
        },
        {
            "methods": "HEAD,OPTIONS,GET",
            "url": "/tests/exceptions/[code]"
        }
    ]
}
```

5. the `/endpoints` request automatically shows all the available routes in our API.  This will grow as we add more.  

#### understanding request parameters
when working with   `HTTP` requests, there's a variety of ways data/query params can be passed back and forth.  The `app.utils` Python module has a powerful function called `collect_args`, which will parse request arguments from the [query string](https://en.wikipedia.org/wiki/Query_string), [form data](https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Sending_and_retrieving_form_data), or raw json in the request body.

Next, run click on the `/test` route in the `Brewery API` Collection in Postman.  In this request, there is a parameter in the query string as well as the body.  This route just returns back a response of the arguments passed in (processed by `collect_args()`) and the response should be:

```
{
    "body_param": "bar",
    "query_param": "foo"
}
```

#### working with real data in our REST API
Now that we know our REST API is working, it is time to start playing with our Brewery Data; but first, we need a database to work with.  To create our database double click on the `create_db_data.sh` file in the `Python` folder.  This will create a SQLite database called `beer.db` inside the `/Python/db` directory and load in some CSV files.  You should see a success message pretty quick after the database is set up.

Before we start setting up the API methods, we need to should understand the data.  The `models.py` file contains the schema for our database tables represented as the following classes:

* `Brewery`  - model for `breweries` table
* `Beer` - model for `beers` table
* `Category` - model for `categories` table (beer categories) - we actually aren't using this table directly
* `Style` - model for `styles` table (beer style)
* `User` - model for `users` table (note this extends the [flask_login.UserMixin]() class

We can view this data easier by looking at the actual `beers.db` database in the [DB Browser for SQLite](http://sqlitebrowser.org/) application.











