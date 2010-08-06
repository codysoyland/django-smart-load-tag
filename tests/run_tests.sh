#!/bin/sh

export PYTHONPATH=`pwd`/..:$PYTHONPATH # add smart_load_tag app to path

django-admin.py test testapp --settings=testproject.settings
