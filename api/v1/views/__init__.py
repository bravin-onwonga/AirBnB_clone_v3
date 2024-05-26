#!/usr/bin/python3
"""
Setting up flask using BluePrint
"""

from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint(url_prefix='/api/vi')
