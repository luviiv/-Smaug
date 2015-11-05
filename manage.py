#encoding: utf-8
"""
    manager.py
    ~~~~~~~~~~~
    manage the app from command line
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask.ext.script import Manager, prompt, prompt_pass, \
    prompt_bool, prompt_choices

from Smaug import create_app
from Smaug.extensions import db
from Smaug.models import User

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

@manager.option('-u', '--username', dest="username", required=False)
@manager.option('-p', '--password', dest="password", required=False)
@manager.option('-e', '--email', dest="email", required=False)
@manager.option('-r', '--role', dest="role", required=False)
def createuser(username=None, password=None, email=None, role=None):
    """
    Create a new user
    """
    
    if username is None:
        while True:
            username = prompt("Username")
            user = User.query.filter(User.username==username).first()
            if user is not None:
                print "Username %s is already taken" % username
            else:
                break

    if email is None:
        while True:
            email = prompt("Email address")
            user = User.query.filter(User.email==email).first()
            if user is not None:
                print "Email %s is already taken" % email
            else:
                break

    if password is None:
        password = prompt_pass("Password")

        while True:
            password_again = prompt_pass("Password again")
            if password != password_again:
                print "Passwords do not match"
            else:
                break
    
    roles = (
        (User.MEMBER, "member"),
        (User.MODERATOR, "moderator"),
        (User.ADMIN, "admin"),
    )

    if role is None:
        role = prompt_choices("Role", roles, resolve=int, default=User.MEMBER)

    user = User(username=username,
                email=email,
                password=password,
                role=role)

    db.session.add(user)
    db.session.commit()

    print "User created with ID", user.id

if __name__ == "__main__":
    manager.run()