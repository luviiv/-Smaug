# -*- coding: utf-8 -*-
"""
    frameview.py
    ~~~~~~~~~~~
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""
from flask import Blueprint, render_template, \
    abort, jsonify, request, url_for
from sqlalchemy.orm import joinedload
from Smaug.extensions import db
from Smaug.models import StockIdentity, SeasonlySummary

frameview = Blueprint('frameview', __name__,
                        template_folder='templates')

@frameview.route('/')
def index():
    try:
        return render_template('panels/home_panel.html')
    except:
        abort(404)

@frameview.route('/finance_summary', methods=('GET',))
@frameview.route('/finance_summary/<code>', methods=('GET',))
def finance_summary(code=None):
    try:
        if code==None:
            if request.args.get('code',None) is None:
                abort(404)
            query_code = request.args.get('code',None)
            if request.args.get('name', None) is None:
                query_name = StockIdentity.query.filter_by(code=query_code)\
                            .first().name
            company={'code': query_code,
                    'name':query_name,
                    'query_url': url_for('frameview.finance_summary',code=query_code),
                    }
            return render_template('panels/finance_summary.html', 
                company=company)
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