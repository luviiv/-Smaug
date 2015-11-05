# -*- coding: utf-8 -*-
"""
    users.py
    ~~~~~~~~~~~
    user manage
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

import hashlib

from datetime import datetime

from werkzeug import generate_password_hash, check_password_hash, \
    cached_property

from flask.ext.sqlalchemy import BaseQuery
from flask.ext.principal import RoleNeed, UserNeed, Permission

from Smaug.extensions import db
from Smaug.permissions import null

class UserQuery(BaseQuery):

    def from_identity(self, identity):
        """
        Loads user from flask.ext.principal.Identity instance and
        assigns permissions from user.
        A "user" instance is monkeypatched to the identity instance.
        If no user found then None is returned.
        """

        try:
            user = self.get(int(identity.id))
        except ValueError:
            user = None

        if user:
            identity.provides.update(user.provides)

        identity.user = user

        return user

    def authenticate(self, login, password):

        user = self.filter(db.or_(User.username==login,
                                User.email==login)).first()
        if user:
            authenticate = user.check_password(password)
        else:
            authenticate = False

        return user, authenticate

    def authenticate_openid(self, email, openid):

        user = self.filter(User.email==email).first()

        if user:
            authenticate = user.check_openid(openid)
        else:
            authenticate = False

        return user, authenticate

class User(db.Model):
    __tablename__ = "users"

    query_class = UserQuery

    # user roles 
    MEMBER = 100
    MODERATOR = 200
    ADMIN = 300

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Unicode(60), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.Integer, default = MEMBER)
    _password = db.Column("password", db.String(80))
    _openid = db.Column("openid", db.String(80), unique=True)

    class Permissions(object):

        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def send_message(self):
            if not self.obj.receive_email:
                return null

            needs = [UserNeed(user_id) for user_id in self.obj.friends]
            if not needs:
                return null

            return Permission(*needs)

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<%s>" % self

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym("_password", 
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def _get_openid(self):
        return self._openid

    def _set_openid(self, openid):
        self._openid = generate_password_hash(openid)

    openid = db.synonym("_openid", 
                          descriptor=property(_get_openid,
                                              _set_openid))

    def check_openid(self, openid):
        if self.openid is None:
            return False
        return check_password_hash(self.openid, openid)

    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'),
                 UserNeed(self.id)]

        if self.is_moderator:
            needs.append(RoleNeed('moderator'))

        if self.is_admin:
            needs.append(RoleNeed('admin'))

        return needs

    @property
    def is_moderator(self):
        return self.role >= self.MODERATOR

    @property
    def is_admin(self):
        return self.role >= self.ADMIN