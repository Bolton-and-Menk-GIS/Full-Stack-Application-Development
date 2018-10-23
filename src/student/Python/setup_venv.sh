#!/usr/bin/env bash
# create virtualenv first
# find python (I'm sure there's a better way to do this...)
if [ -e c:/python27/python.exe ]; then
    c:/python27/python -m virtualenv ./app/venv
else
    echo "no regular Python found, searching for ArcGIS implementation?"

    if [ -e c:/python27/ArcGIS10.3/python.exe ]; then 
		echo "found arcgis python 10.3"
        c:/python27/arcgis10.3/scripts/virtualenv --download ./app/venv
    elif [ -e c:/python27/ArcGIS10.4/python.exe ]; then 
		echo "found arcgis python 10.4"
        c:/python27/arcgis10.4/scripts/virtualenv --download ./app/venv
    elif [ -e c:/python27/ArcGIS10.5/python.exe ]; then 
		echo "found arcgis python 10.5"
        c:/python27/arcgis10.5/scripts/virtualenv --download ./app/venv
    elif [ -e c:/python27/ArcGIS10.6/python.exe ]; then 
		echo "found arcgis python 10.6"
        c:/python27/arcgis10.6/scripts/virtualenv --download ./app/venv
    else
        read -p "cannot find python, you will need to manually install it before running this script again. press any key to exit..."
        exit
    fi
fi
echo "created virtualenv"

# check for pip
if [ ! -f ./app/venv/pip.exe ]; then
    echo "installing pip in virtualenv"
    ./app/venv/Scripts/python ./get_pip.py
    echo "installed pip"
fi

# check for virtual env
if [ ! -f ./app/venv/activate.bat ]; then
    echo "installing virtualenv in our virtualenv"
    ./app/venv/Scripts/pip install virtualenv
    echo "installed virtualenv"
fi

# activate venv
source ./app/venv/Scripts/activate
echo "Activated Virtual Environment, now installing dependencies..."

# install all dependencies
pip install six
echo "installed six"

pip install Flask
echo "installed Flask"

pip install Flask-Login
echo "installed Flask-Login"

pip install Flask-CORS
echo "installed Flask-CORS"

pip install Flask-SQLAlchemy
echo "installed Flask-SQLAlchemy"

pip install git+https://github.com/GeospatialPython/pyshp.git
echo "installed shapefile"

pip install wfastcgi
echo "installed wfastcgi"

read -p "finished installing dependencies, hit any key to exit..."