#encoding: utf-8
"""
    manager.py
    ~~~~~~~~~~~
    manage the app from command line
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask.ext.script import Manager

from Smaug import create_app

manager = Manager(create_app)

@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()