#!/usr/bin/env bash
source ./app/venv/Scripts/activate
./app/venv/Scripts/python ./beer_sample/create_db_data.py
read -p "SQLite Databases Created Successfully: press any key to exit..."