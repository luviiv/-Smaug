# -*- coding: utf-8 -*-
"""
    crawler_manager.py
    ~~~~~~~~~~~
    start crawlers
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""
import threading

from stock import SeasonlySummaryCrawler
from stock import StockCrawler
from stock import SummaryPerSeason

from Smaug.models import StockIdentity
from Smaug.models import SeasonlySummary
from Smaug.models import SummaryRatios

from Smaug.calculator import summary_ratios_calculate
from Smaug.extensions import db

from flask import current_app

import datetime, calendar

def initial_craw():
    """craw data when setup"""
    stock_list = []

    #craw the code list
    stock_crawler = StockCrawler()
    stock_list.extend(
        stock_crawler.fetch_sh_list())
    stock_list.extend(
        stock_crawler.fetch_sz_list())
    stock_list.extend(
        stock_crawler.fetch_gem_list())

    for code,name in stock_list:
        identity = StockIdentity(code, name)
        db.session.add(identity)

    db.session.commit()

def summary_craw():
    """craw seasonly summary"""
    #thread lock
    lock = threading.Lock()
    lock.acquire()
    try:
        stocks = StockIdentity.query.all()
        for company in stocks:
            current_app.logger.debug("begin to update finance summary ratio for[%s]") %company.code
            latest = SeasonlySummary.query.filter_by(code=company.code).\
                order_by(SeasonlySummary.dead_line.desc()).first()
            summaryCrawler = SeasonlySummaryCrawler()
            if latest==None:
                dead_line = None
            else:
                dead_line = latest.dead_line
            # if already latest dealine, ignore
            if dead_line is not None and is_latest_deadline(dead_line):
                current_app.logger.debug("seasonly_summary for: %s ignored" % company.code)
            else:
                result = summaryCrawler.fetch_seasonly_summary(company.code, dead_line)
                for elem in result:
                    summary = SeasonlySummary(company.code, elem)
                    db.session.add(summary)
                db.session.commit()
                current_app.logger.debug("DB commited seasonly_summary %s" % company.code)
            #summary ratios
            current_app.logger.debug("begin to update finance summary ratio...")
            latest_ratio = SummaryRatios.query.filter_by(code=company.code).\
                order_by(SummaryRatios.dead_line.desc()).first()

            if latest_ratio==None:
                dead_line = None
            else:
                dead_line = latest_ratio.dead_line

            if dead_line is not None and is_latest_deadline(dead_line):
                current_app.logger.debug("summary_ratio for: %s is ignored" % company.code)
            else:
                result = summary_ratios_calculate(company.code, dead_line)
                for key in result:
                    summary_ratio = SummaryRatios(company.code, int(key), result[key][MoM_main_business_revenue], 
                        result[key][YoY_main_business_revenue], result[key][MoM_net_profit], result[key][YoY_net_profit], 
                        result[key][MoM_earnings_per_share], result[key][YoY_earnings_per_share], 
                        result[key][MoM_cash_flow_per_share], result[key][YoY_cash_flow_per_share])
                    db.session.add(summary_ratio)
                db.session.commit()
                current_app.logger.debug("DB commited summary_ratio %s" % company.code)
    finally:
        lock.release()

def is_latest_deadline(dead_line):
    """
    if this dead_line is already the latest, according to the end of season
    """
    target_date = datetime.datetime.strptime(dead_line,'%Y-%m-%d').date()
    today = datetime.date.today()
    date_gap = abs((today-target_date).days)

    if date_gap<=93:
        if get_month_gap(today.month, target_date.month) <= 3:
            return True
        else:
            return False
    else:
        return False

def get_month_gap(target, old):
    gap = target - old
    if gap< 0:
        gap = gap + 12

    return gap

if __name__ == '__main__':
    initial_craw()