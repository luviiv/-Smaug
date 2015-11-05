# -*- coding: utf-8 -*-
"""
    account.py
    ~~~~~~~~~~~
    login methods
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask import Blueprint, render_template, abort, jsonify, \
    session, url_for, redirect, current_app, flash, request

from flask.ext.babel import gettext as _
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity

from Smaug.models import User
from Smaug.extensions import db
from Smaug.permissions import auth
from Smaug.forms import LoginForm

account = Blueprint('account', __name__,
                    template_folder='templates')

@account.route("/login/", methods=("GET", "POST"))
def login():
    form = LoginForm(login=request.args.get("login", None),
                     next=request.args.get("next", None))

    # TBD: ensure "next" field is passed properly

    if form.validate_on_submit():
        user, authenticated = \
            User.query.authenticate(form.login.data,
                                    form.password.data)

        if user and authenticated:
            session.permanent = form.remember.data
            
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            # check if openid has been passed in
            openid = session.pop('openid', None)
            if openid:
                user.openid = openid
                db.session.commit()
                
                flash(_("Your OpenID has been attached to your account. "
                      "You can now sign in with your OpenID."), "success")


            else:
                flash(_("Welcome back, %(name)s", name=user.username), "success")

            next_url = form.next.data

            if not next_url or next_url == request.path:
                next_url = url_for('adminview.admin', username=user.username)

            return redirect(next_url)

        else:
            flash(_("Sorry, invalid login"), "error")

    return render_template("account/login.html", form=form)
 

@account.route("/logout/")
def logout():

    flash(_("You are now logged out"), "success")
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('account.login'))