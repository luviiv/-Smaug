# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~~~~~~
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask import Blueprint, render_template, abort, jsonify
from Smaug.crawler import initial_craw
from Smaug.crawler import summary_craw
from Smaug.permissions import admin

adminview = Blueprint('adminview', __name__,
                        template_folder='templates')

@adminview.route('/')
@admin.require(401)
def admin_page():
    try:
        return render_template('admin.html')
    except TemplateNotFound:
        abort(404)

@adminview.route('/update_stock_list')
@admin.require(401)
def update_stock_list():
    initial_craw()

    return jsonify(status="success")

@adminview.route('/update_finance_summary')
@admin.require(401)
def update_finance_summary():

    summary_craw()

    return jsonify(status="success")