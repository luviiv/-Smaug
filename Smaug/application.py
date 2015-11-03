#encoding: utf-8
"""
    application.py
    ~~~~~~~~~~~
    Application configuration
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""
#flask library
from flask import Flask
#Smaug
from Smaug import views

DEFAULT_APP_NAME = "Smaug"

DEFAULT_MODULES = (
    (views.frameview,""),
)

def create_app(config=None, app_name=None, modules=None):
    """create app for server"""
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(app_name)
    configure_modules(app, modules)
    return app

def configure_modules(app, modules):
    """load modules that want to be used"""
    for module, url_prefix in modules:
        return app.register_blueprint(module, url_prefix=url_prefix)