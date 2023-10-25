#!/bin/bash

PYTHON=`which python`
PYTHON3=`which python3`

if [ $PYTHON ]; then
	python -m venv env
    env/bin/activate
    env/bin/pip install -r requirements.txt
    env/bin/pip install wxPython
elif [ $PYTHON3 ]; then
	python3 -m venv env
else
	echo "sem python"
fi