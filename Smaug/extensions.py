# -*- coding: utf-8 -*-
"""
    extensions.py
    ~~~~~~~~~~~
    finance summary crawler
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})