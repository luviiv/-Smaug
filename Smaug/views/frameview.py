# -*- coding: utf-8 -*-
"""
    frameview.py
    ~~~~~~~~~~~
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""
from flask import Blueprint, render_template, abort

frameview = Blueprint('frameview', __name__,
                        template_folder='templates')

@frameview.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)