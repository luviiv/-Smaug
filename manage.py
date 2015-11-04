#encoding: utf-8
"""
    manager.py
    ~~~~~~~~~~~
    manage the app from command line
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask.ext.script import Manager, prompt, prompt_bool

from Smaug import create_app
from Smaug.extensions import db
manager = Manager(create_app)

@manager.command
def createall():
    """create all table"""

    db.create_all()

@manager.command
def dropall():
    """drop all table"""

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

if __name__ == "__main__":
    manager.run()