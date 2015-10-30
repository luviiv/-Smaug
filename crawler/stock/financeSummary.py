#encoding: UTF-8
import sys
import urllib.request
import urllib
from bs4 import BeautifulSoup

class SummaryPerSeason():
    """上市公司每季财务摘要"""
    def __init__(self):
        self.deadLine = '' #截止日期
        self.netAssestsValuePerShare = '' #每股资产净值
        self.earningsPerShare = '' #每股收益
        self.cashFlowPerShare = '' #每股现金含量
        self.capitalFundPerShare = '' #每股公积金
        self.totalFixedAssets = '' #固定资产合计
        self.totalCurrentAssets = '' #流动资产合计
        self.totalAssets = '' #资产总计
        self.totalLongTermLiabilities = '' #长期负债合计
        self.mainBusinessRevenue = '' #主营业务收入
        self.financialExpenses = '' #财务费用
        self.netProfit = '' #净利润

    def setProperty(self,idx,value):
        """按照sina网页顺序设置属性"""
        if idx==1:
            self.deadLine = value
        elif idx==2:
            self.netAssestsValuePerShare = value
        elif idx==3:
            self.earningsPerShare = value
        elif idx==4:
            self.cashFlowPerShare = value
        elif idx==5:
            self.capitalFundPerShare = value
        elif idx==6:
            self.totalFixedAssets = value
        elif idx==7:
            self.totalCurrentAssets = value
        elif idx==8:
            self.totalAssets = value
        elif idx==9:
            self.totalLongTermLiabilities = value
        elif idx==10:
            self.mainBusinessRevenue = value
        elif idx==11:
            self.financialExpenses = value
        elif idx==12:
            self.netProfit = value

    def __str__(self):
        return '['+self.deadLine+','+self.netAssestsValuePerShare+','+self.earningsPerShare+','+self.cashFlowPerShare+','+self.capitalFundPerShare+','+self.totalFixedAssets+','+self.totalCurrentAssets+','+self.totalAssets+','+self.totalLongTermLiabilities+','+self.mainBusinessRevenue+','+self.financialExpenses+','+self.netProfit+']'

class SeasonlySummaryCrawler():
    """爬取上市公司每一季度的财务摘要"""
    baseUrl = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%s.phtml'
    
    def fetchSeasonlySummary(self, companyCode):
        """获取上市公司的所有历史摘要数据"""
        url = self.baseUrl % (companyCode)
        response = urllib.request.urlopen(url)
        html = BeautifulSoup(response.read().decode('gb2312'))
        summaryHistoryList = self.__analyzeHtml(html)
        return summaryHistoryList

    def __analyzeHtml(self, data):
        resultList = []
        rows = data.find(id="FundHoldSharesTable")
        idx = 1
        summaryUnit = SummaryPerSeason()
        for row in rows.find_all('tr',recursive=False):
            td = row.find('td', class_='tdr')
            if td!=None:
                summaryUnit.setProperty(idx,td.text)
                idx+=1
            else:
                idx=1
                resultList.append(summaryUnit)
                summaryUnit = SummaryPerSeason()
        return resultList