# -*- coding: utf-8 -*-
"""
    crawler_manager.py
    ~~~~~~~~~~~
    start crawlers
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from stock import SeasonlySummaryCrawler
from stock import StockCrawler
from stock import SummaryPerSeason

from Smaug.models import StockIdentity
from Smaug.extensions import db

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
    stocks = StockIdentity.query.all()
    for company in stocks:
        summaryCrawler = SeasonlySummaryCrawler()
        result = summaryCrawler.fetch_seasonly_summary(company.code)
        print company.code
        for elem in result:
            print elem.earnings_per_share

if __name__ == '__main__':
    initial_craw()