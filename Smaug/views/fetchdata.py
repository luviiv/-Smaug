# -*- coding: utf-8 -*-
"""
    fetchdata.py
    ~~~~~~~~~~~
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask import Blueprint, jsonify, abort
from Smaug.models import StockIdentity, SummaryRatios
from Smaug.calculator import summary_ratios_calculate
from Smaug.extensions import db
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

@fetchdata.route('/summaryratio/<code>', methods=['GET'])
def query_summary_ratio(code):
    latest_ratio = SummaryRatios.query.filter_by(code=code).\
                order_by(SummaryRatios.dead_line.desc()).all()
    if latest_ratio==None:
        result = summary_ratios_calculate(code, dead_line)
        for key in result:
            summary_ratio = SummaryRatios(code, int(key), 
                result[key]['MoM_main_business_revenue'], result[key]['YoY_main_business_revenue'], 
                result[key]['MoM_net_profit'], result[key]['YoY_net_profit'], 
                result[key]['MoM_earnings_per_share'], result[key]['YoY_earnings_per_share'], 
                result[key]['MoM_cash_flow_per_share'], result[key]['YoY_cash_flow_per_share'])
            db.session.add(summary_ratio)
        db.session.commit()
        current_app.logger.debug("DB commited summary_ratio %s" % code)
    else:
        result = {}
        for elem in latest_ratio:
            result[str(elem.dead_line)] = elem.serialize()
    return jsonify(ratios = result)