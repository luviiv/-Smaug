# -*- coding: utf-8 -*-
"""
    stock_info.py
    ~~~~~~~~~~~
    stock info models
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from Smaug.extensions import db

class StockIdentity(db.Model):
    __tablename__ = "stock_identity"

    code = db.Column(db.String(6), primary_key = True)
    name = db.Column(db.String(16))

    def serialize(self):
        return {
            'code':self.code,
            'name':self.name,
        }

    def __init__(self, code , name):
        self.code = code
        self.name = name

    def __repr__(self):
        return 'StockIdentity(%r,%r)' % (self.code, self.name)

class SeasonlySummary(db.Model):
    __tablename__ = "seasonly_summary"

    code = db.Column(db.String(6), db.ForeignKey('stock_identity.code'), 
        primary_key=True)
    dead_line = db.Column(db.String(10), primary_key=True) #截止日期
    net_assets_value_per_share = db.Column(db.String(20), nullable=True) #每股资产净值
    earnings_per_share = db.Column(db.String(20), nullable=True) #每股收益
    cash_flow_per_share = db.Column(db.String(20), nullable=True) #每股现金含量
    capital_fund_per_share = db.Column(db.String(20), nullable=True) #每股公积金
    total_fixed_assets = db.Column(db.String(20), nullable=True) #固定资产合计
    total_current_assets = db.Column(db.String(20), nullable=True) #流动资产合计
    total_assets = db.Column(db.String(20), nullable=True) #资产总计
    total_long_term_liabilities = db.Column(db.String(20), nullable=True) #长期负债合计
    main_business_revenue = db.Column(db.String(20), nullable=True) #主营业务收入
    financial_expenses = db.Column(db.String(20), nullable=True) #财务费用
    net_profit = db.Column(db.String(20), nullable=True) #净利润

    def serialize(self):
        return {
            'code': self.code,
            'dead_line': self.dead_line,
            'net_assets_value_per_share':self.net_assets_value_per_share,
            'earnings_per_share':self.earnings_per_share,
            'cash_flow_per_share':self.cash_flow_per_share,
            'capital_fund_per_share':self.capital_fund_per_share,
            'total_fixed_assets': self.total_fixed_assets,
            'total_current_assets': self.total_current_assets,
            'total_assets': self.total_assets,
            'total_long_term_liabilities': self.total_long_term_liabilities,
            'main_business_revenue': self.main_business_revenue,
            'financial_expenses': self.financial_expenses,
            'net_profit': self.net_profit,
        }

    def __init__(self,code, summary_obj):
        self.dead_line = summary_obj.dead_line
        self.net_assets_value_per_share = summary_obj.net_assets_value_per_share
        self.earnings_per_share = summary_obj.earnings_per_share
        self.cash_flow_per_share = summary_obj.cash_flow_per_share
        self.capital_fund_per_share = summary_obj.capital_fund_per_share
        self.total_fixed_assets = summary_obj.total_fixed_assets
        self.total_current_assets = summary_obj.total_current_assets
        self.total_assets = summary_obj.total_assets
        self.total_long_term_liabilities = summary_obj.total_long_term_liabilities
        self.main_business_revenue = summary_obj.main_business_revenue
        self.financial_expenses = summary_obj.financial_expenses
        self.net_profit = summary_obj.net_profit

class SummaryRatios(db.Model):
    __tablename__ = 'summary_ratios'

    code = db.Column(db.String(6), db.ForeignKey('stock_identity.code'), 
        primary_key=True)
    dead_line = db.Column(db.Integer,primary_key=True)
    MoM_main_business_revenue = db.Column(db.Numeric, default=0.0)
    YoY_main_business_revenue = db.Column(db.Numeric, default=0.0)
    MoM_net_profit = db.Column(db.Numeric, default=0.0)
    YoY_net_profit = db.Column(db.Numeric, default=0.0)
    MoM_earnings_per_share = db.Column(db.Numeric, default=0.0)
    YoY_earnings_per_share = db.Column(db.Numeric, default=0.0)
    MoM_cash_flow_per_share = db.Column(db.Numeric, default=0.0)
    YoY_cash_flow_per_share = db.Column(db.Numeric, default=0.0)
    def __init__(self, code, dead_line, MoM_main_business_revenue, YoY_main_business_revenue,
        MoM_net_profit, YoY_net_profit, MoM_earnings_per_share, YoY_earnings_per_share,
        MoM_cash_flow_per_share, YoY_cash_flow_per_share):
        self.code = code
        self.dead_line = dead_line
        self.MoM_main_business_revenue = MoM_main_business_revenue
        self.YoY_main_business_revenue = YoY_main_business_revenue
        self.MoM_net_profit = MoM_net_profit
        self.YoY_net_profit = YoY_net_profit
        self.MoM_earnings_per_share = MoM_earnings_per_share
        self.YoY_earnings_per_share = YoY_earnings_per_share
        self.MoM_cash_flow_per_share = MoM_cash_flow_per_share
        self.YoY_cash_flow_per_share = YoY_cash_flow_per_share

    def serialize(slef):
        return {
            'code': self.code,
            'dead_line': self.dead_line,
            'MoM_main_business_revenue': self.MoM_main_business_revenue,
            'YoY_main_business_revenue': self.YoY_main_business_revenue,
            'MoM_net_profit': self.MoM_net_profit,
            'YoY_net_profit': self.YoY_net_profit,
            'MoM_earnings_per_share': self.MoM_earnings_per_share,
            'YoY_earnings_per_share': self.YoY_earnings_per_share,
            'MoM_cash_flow_per_share': self.MoM_cash_flow_per_share,
            'YoY_cash_flow_per_share': self.YoY_cash_flow_per_share,
        }