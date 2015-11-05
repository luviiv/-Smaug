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
from flask import Flask, request, jsonify, g, flash, redirect, url_for
#flaskext
from flask.ext.babel import Babel, gettext as _
from flask.ext.principal import Principal, identity_loaded
#Smaug
from Smaug import views
from Smaug.config import DefaultConfig
from Smaug.extensions import db, cache
from Smaug.models import User
__all__ = ["create_app"]

DEFAULT_APP_NAME = "Smaug"

DEFAULT_MODULES = (
    (views.frameview,""),
    (views.adminview,"/admin"),
    (views.account,"/account"),
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
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_modules(app, modules)

    return app

def configure_app(app, config):
    """read configuration"""
    app.config.from_object(DefaultConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('APP_CONFIG', silent=True)

def configure_modules(app, modules):
    """load modules that want to be used"""

    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)

def configure_before_handlers(app):

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)

def configure_extensions(app):
    """all extensions goes here"""

    cache.init_app(app)
    db.init_app(app)
    
    configure_identity(app)
    configure_i18n(app)

def configure_identity(app):

    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)

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

def configure_errorhandlers(app):

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/404.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed'))
        return render_template("errors/403.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return render_template("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonfiy(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("account.login", next=request.path))

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