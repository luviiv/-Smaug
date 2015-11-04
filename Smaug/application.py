# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~
    Application configuration
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
#flask library
from flask import Flask, request, jsonify
#flaskext
from flask.ext.babel import Babel, gettext as _
#Smaug
from Smaug import views
from Smaug.config import DefaultConfig
from Smaug.extensions import db, cache

__all__ = ["create_app"]

DEFAULT_APP_NAME = "Smaug"

DEFAULT_MODULES = (
    (views.frameview,""),
    (views.adminview,"/admin"),
)

def create_app(config=None, app_name=None, modules=None):
    """create app for server"""

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(app_name)

    configure_app(app, config)

    configure_logging(app)
    configure_extensions(app)
    configure_modules(app, modules)

    return app

def configure_app(app, config):
    """read configuration"""
    app.config.from_object(DefaultConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('APP_CONFIG', silent=True)

def configure_extensions(app):
    """all extensions goes here"""

    cache.init_app(app)
    db.init_app(app)
    
    configure_i18n(app)

def configure_modules(app, modules):
    """load modules that want to be used"""

    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)

def configure_i18n(app):
    """configure language setting"""

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        """
            change here,
            if you want to support multi locale
        """
        return app.config['BABEL_DEFAULT_LOCALE']

def configure_logging(app):
    if app.debug or app.testing:
        return

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path, 
                             app.config['DEBUG_LOG'])

    debug_file_handler = \
        RotatingFileHandler(debug_log,
                            maxBytes=100000,
                            backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path, 
                             app.config['ERROR_LOG'])

    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)