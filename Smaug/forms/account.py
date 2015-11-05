# -*- coding: utf-8 -*-
"""
    account.py
    ~~~~~~~~~~~
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""
from flask_wtf import Form
from wtforms import HiddenField, BooleanField, TextField, \
        PasswordField, SubmitField
from wtforms.validators import Required

from flask.ext.babel import gettext, lazy_gettext as _ 

from Smaug.models import User
from Smaug.extensions import db

class LoginForm(Form):
    next = HiddenField()
    remember = BooleanField(_("Remember me"))
    login = TextField(_("Username or email address"), validators=[
                      Required(message=\
                               _("You must provide an email or username"))])
    password = PasswordField(_("Password"))

    submit = SubmitField(_("Login"))