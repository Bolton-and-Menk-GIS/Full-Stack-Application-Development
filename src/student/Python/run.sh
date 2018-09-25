#!/usr/bin/env bash

# activate our virtual environmnent
source ./app/venv/Scripts/activate;

# display message
echo "Activated Virtual Environment, now running Flask REST API."

# run the python file using our virtualenv
./app/venv/Scripts/python run.py

# display this message when exiting the app (either terminated via error or manually by hitting Ctrl + C)
read -p "Application Terminated: press any key to exit..."