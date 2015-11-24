# -*- coding: utf-8 -*-
"""
    summary_calculator.py
    ~~~~~~~~~~~
    calculate summary statistics
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""
from Smaug.models import SeasonlySummary

dummy_summary = {
            'main_business_revenue': '',
            'net_profit': '',
            'earnings_per_share': '',
            'cash_flow_per_share': '',
        }

def summary_ratios_calculate(stock_code, dead_line=None):
    if dead_line==None:
        dead_line_int = '19000101'
    else:
        dead_line_int = ''.join(dead_line.split('-'))
    summaries = SeasonlySummary.query.filter_by(code=stock_code)
    data_map = {}
    #get data needed for each deadline
    for s in summaries:
        tmp_map = {
            'main_business_revenue': s.main_business_revenue,
            'net_profit': s.net_profit,
            'earnings_per_share': s.earnings_per_share,
            'cash_flow_per_share': s.cash_flow_per_share,
        }
        date_int = ''.join(s.dead_line.split('-'))
        data_map[date_int] = tmp_map
    result_map = {}
    for d in data_map:
        if int(d)<int(dead_line_int):
            continue
        current_summary = data_map[d]
        MoM_date = _get_MoM_date(d)
        YoY_date = _get_YoY_date(d)
        if MoM_date in data_map:
            MoM_summary = data_map[MoM_date]
        else:
            MoM_summary = dummy_summary

        if YoY_date in data_map:
            YoY_summary = data_map[YoY_date]
        else:
            YoY_summary = dummy_summary

        ratio_map = {
            'MoM_main_business_revenue': _get_MoM_ratio(
                current_summary['main_business_revenue'],
                 MoM_summary['main_business_revenue']),
            'YoY_main_business_revenue': _get_YoY_ratio(
                current_summary['main_business_revenue'],
                YoY_summary['main_business_revenue']),
            'MoM_net_profit': _get_MoM_ratio(current_summary['net_profit'],
                MoM_summary['net_profit']),
            'YoY_net_profit': _get_YoY_ratio(current_summary['net_profit'], 
                YoY_summary['net_profit']),
            'MoM_earnings_per_share':_get_MoM_ratio(current_summary['earnings_per_share'],
                MoM_summary['earnings_per_share']),
            'YoY_earnings_per_share':_get_YoY_ratio(current_summary['earnings_per_share'],
                YoY_summary['earnings_per_share']),
            'MoM_cash_flow_per_share':_get_MoM_ratio(current_summary['cash_flow_per_share'], 
                MoM_summary['cash_flow_per_share']),
            'YoY_cash_flow_per_share':_get_YoY_ratio(current_summary['cash_flow_per_share'], 
                YoY_summary['cash_flow_per_share']),
        }
        result_map[d] = ratio_map
    return result_map

def _get_MoM_ratio(current, MoM):
    if current=='' or MoM=='' or float(MoM)==0.0:
        return 0.0
    return (float(current)-float(MoM))/float(MoM)

def _get_YoY_ratio(current, YoY):
    if current=='' or YoY=='' or float(YoY)==0.0:
        return 0.0
    return (float(current)-float(YoY))/float(YoY)

def _get_MoM_date(date):
    prev_m_map={
        '0331':'1231',
        '0630':'0331',
        '0930':'0630',
        '1231':'0930',
    }
    year = date[0:4]
    month_date = date[4:8]
    if month_date=='0331':
        year = str(int(year)-1)

    return year+prev_m_map[month_date]

def _get_YoY_date(date):
    return str(int(date)-10000)  

