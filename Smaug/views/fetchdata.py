# -*- coding: utf-8 -*-
"""
    fetchdata.py
    ~~~~~~~~~~~
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask import Blueprint, jsonify, abort
from Smaug.models import StockIdentity
import re

fetchdata = Blueprint('fetchdata',__name__,template_folder='templates')

@fetchdata.route('/querystock/<parameter>', methods=['GET'])
def query_stock(parameter):
    try:
        pattern = re.compile(r'^[0-9]{6}$')
        match = pattern.match(parameter)
        if match:
            stock = StockIdentity.query.filter_by(code=parameter).first()
        else:
            stock = StockIdentity.query.filter_by(name=parameter).first()

        if stock is not None:
            mapped = {
                'code':stock.code,
                'name': stock.name,
            }
            return jsonify(stock=mapped)
        else:
            return jsonify(status="error")
    except:
        abort(404)