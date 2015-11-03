#encoding: utf-8
"""
    financeSummary.py
    ~~~~~~~~~~~
    Finance Summary Crawler
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""
import sys
import urllib2
from urllib2 import Request

from bs4 import BeautifulSoup

class SummaryPerSeason():
    """summary of finance status of a company"""
    def __init__(self):
        self.dead_line = '' #截止日期
        self.net_assets_value_per_share = '' #每股资产净值
        self.earnings_per_share = '' #每股收益
        self.cash_flow_per_share = '' #每股现金含量
        self.capital_fund_per_share = '' #每股公积金
        self.total_fixed_assets = '' #固定资产合计
        self.total_current_assets = '' #流动资产合计
        self.total_assets = '' #资产总计
        self.total_long_term_liabilities = '' #长期负债合计
        self.main_business_revenue = '' #主营业务收入
        self.financial_expenses = '' #财务费用
        self.net_profit = '' #净利润

    def set_property(self,idx,value):
        """setup the property by order in the crawed html"""
        if idx==1:
            self.dead_line = value
        elif idx==2:
            self.net_assets_value_per_share = value
        elif idx==3:
            self.earnings_per_share = value
        elif idx==4:
            self.cash_flow_per_share = value
        elif idx==5:
            self.capital_fund_per_share = value
        elif idx==6:
            self.total_fixed_assets = value
        elif idx==7:
            self.total_current_assets = value
        elif idx==8:
            self.total_assets = value
        elif idx==9:
            self.total_long_term_liabilities = value
        elif idx==10:
            self.main_business_revenue = value
        elif idx==11:
            self.financial_expenses = value
        elif idx==12:
            self.net_profit = value

    def __str__(self):
        return ','.join([self.dead_line, self.net_assets_value_per_share,
            self.earnings_per_share, self.cash_flow_per_share,
            self.capital_fund_per_share, self.total_fixed_assets,
            self.total_current_assets, self.total_assets,
            self.total_long_term_liabilities, self.main_business_revenue,
            self.financial_expenses,self.net_profit])

class SeasonlySummaryCrawler():
    """craw the seasonly finance summary"""
    base_url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%s.phtml'
    def fetch_seasonly_summary(self, companyCode):
        """fetch the seasonly finance summary of a given company"""
        url = self.base_url % (companyCode)
        response = urllib2.urlopen(Request(url))
        html = BeautifulSoup(response.read().decode('gb2312'),'html.parser')
        summary_history_list = self.__analyzeHtml(html)
        return summary_history_list

    def __analyzeHtml(self, data):
        """analyze the html and setup each property"""
        result_list = []
        rows = data.find(id="FundHoldSharesTable")
        idx = 1
        summary_unit = SummaryPerSeason()
        for row in rows.find_all('tr',recursive=False):
            td = row.find('td', class_='tdr')
            if td!=None:
                propertyValue = td.text.replace(u'\xa0',u'')
                summary_unit.set_property(idx,filter(lambda ch:ch in '-.0123456789', propertyValue))
                idx+=1
            else:
                idx=1
                result_list.append(summary_unit)
                summary_unit = SummaryPerSeason()
        return result_list

if __name__ == '__main__':
    """test for the crawed result"""
    crawler = SeasonlySummaryCrawler()
    result = crawler.fetch_seasonly_summary('600710')
    for x in result:
        print x    