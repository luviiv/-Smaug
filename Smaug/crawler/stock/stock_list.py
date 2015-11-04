# -*- coding: utf-8 -*-
"""
    stock_list.py
    ~~~~~~~~~~~
    stock list crawler
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

import urllib2
from urllib2 import Request

from bs4 import BeautifulSoup

class SHStockCrawler():
    """
        craw stock list for ShangHai market
    """
    url = "http://www.sse.com.cn/market/sseindex/indexlist/s/i000002/const_list.shtml"

    def fetch_all_list(self):
        
        response = urllib2.urlopen(Request(self.url))
        html = BeautifulSoup(response.read().decode('utf-8'),'html.parser')
        
        return self.__analyze_html(html)

    def __analyze_html(self, data):

        result_list = []
        rows = data.find(id="content_ab")
        #get update date
        update_date = rows.find("li",class_="tab_table_on").text
        update_date = filter(lambda ch:ch in "-0123456789", update_date)
        #get stock code list
        table = data.find("table",class_="tablestyle").find_all("tr")
        for tr in table:
            tds = tr.find_all("td")
            for td in tds:
                code = filter(lambda ch:ch in "0123456789", td.text)
                if len(code)>0:
                    result_list.append(code)
        return update_date, result_list

class StockCrawler():
    """
        craw stock list for ShangZhen market
    """
    base_url = "http://app.finance.ifeng.com/hq/list.php?type=stock_a&class=%s"

    def fetch_sh_list(self):
        return self.__fetch_all_list('ha')

    def fetch_sz_list(self):
        return self.__fetch_all_list('sa')

    def fetch_gem_list(self):
        return self.__fetch_all_list('gem')

    def __fetch_all_list(self, market):
        url = self.base_url % (market)
        response = urllib2.urlopen(Request(url))
        html = BeautifulSoup(response.read().decode('utf-8'),'html.parser')
        return self.__analyze_html(html)

    def __analyze_html(self, data):
        result_list = []
        table = data.find("div",class_="result")
        lis = table.find_all("li")
        for li in lis:
            code = filter(lambda ch:ch in "0123456789", li.text)
            name = filter(lambda ch:ch not in "()0123456789", li.text)
            result_list.append((code,name))
        return result_list

if __name__ == '__main__':
    crawler = StockCrawler()
    print crawler.fetch_sh_list()
