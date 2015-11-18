# -*- coding: utf-8 -*-
"""
    frameview.py
    ~~~~~~~~~~~
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""
from flask import Blueprint, render_template, abort, jsonify
from sqlalchemy.orm import joinedload
from Smaug.extensions import db
from Smaug.models import StockIdentity, SeasonlySummary

frameview = Blueprint('frameview', __name__,
                        template_folder='templates')

@frameview.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@frameview.route('/finance_summary/')
@frameview.route('/finance_summary/<code>')
def finance_summary(code=None):
    try:
        if code==None:
            return render_template('panels/finance_summary.html')
        else:
            results = SeasonlySummary.query.filter_by(code=code).\
                order_by(SeasonlySummary.dead_line.desc()).all()
            summaries = [e.serialize() for e in results]
            json_map={
                'total': len(summaries),
                'page':1,
                'records': len(summaries),
                'rows':summaries,
            }
            return jsonify(json_map)
    except:
        abort(404)