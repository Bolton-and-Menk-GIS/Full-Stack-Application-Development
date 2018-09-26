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
* it would also be beneficial to have both `pip` and `virtualenv` installed for Python

### Demo Application
Images of the `Brewery Finder` Demo App can be found below:

![map](/sections/images/app_images/map_view.PNG)

**Map View showing Brewery Locations**

![search](/sections/images/app_images/typeahead.png)

**Auto-Complete searches for breweries by name**

![brewrey info](/sections/images/app_images/brewery_info.PNG)

**Quick overview of Brewery with featured beers**

![login](/sections/images/app_images/login.PNG)

**Login Page to authenticate users for extended app functionality**

![sign up](/sections/images/app_images/sign_up.PNG)

**As well as allowing new users to register**

#### extra functionality for authenticated users

![export brewery info](/sections/images/app_images/export.PNG)

**Export Tables from the database (with a shapefile option for Breweries)**

![edit brewery 1](/sections/images/app_images/editable_brewery1.PNG)

**Add/Edit/Update/Delete Brewery**

![edit brewery 2](/sections/images/app_images/editable_brewery2.PNG)

**Also can add/delete featured beers from this screen**

![edit beer](/sections/images/app_images/editable_beer.PNG)

**Edit a featured beer**

![create beer](/sections/images/app_images/create_beer.PNG)

**Or create a new beer and upload a photo for it**

#### we will also create a feature rich REST API

![api test](/sections/images/api_test.PNG)

**Serve up brewery database tables via REST**

### Folder Structure
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
* `/mac_venv` - python `virtualenv` for mac
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

### Workshop Instructions
The instructions for going through this workshop are broken into sections for each part.  There is also an associated branch for each part with the exception of part one as the boiler plates are already created in the `master` version of this branch.  To begin, go to [Step 1. Getting Started](https://github.com/Bolton-and-Menk-GIS/Full-Stack-Application-Development/blob/master/sections/01_Getting_Started.md).



