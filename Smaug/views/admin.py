# -*- coding: utf-8 -*-
"""
    admin.py
    ~~~~~~~~~~~
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask import Blueprint, render_template, abort, jsonify
from Smaug.crawler import initial_craw

adminview = Blueprint('adminview', __name__,
                        template_folder='templates')

@adminview.route('/')
def admin():
    try:
        return render_template('admin.html')
    except TemplateNotFound:
        abort(404)

@adminview.route('/update_stock_list')
def update_stock_list():
    initial_craw()

    return jsonify(status="success")