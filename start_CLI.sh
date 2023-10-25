#!/bin/bash

PYTHON=`which python`
PYTHON3=`which python3`

if [ $PYTHON ]; then
	python -m venv env
    env/bin/activate
    env/bin/pip install -r requirements.txt
    env/bin/pip install wxPython
    env/bin/python main_CLI.py
elif [ $PYTHON3 ]; then
	env/bin/python main_CLI.py
else
	echo "sem python"
fi