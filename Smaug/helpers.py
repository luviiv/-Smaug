# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~~~~
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

def str_2_float(str_val):
    if str_val.strip():
        return float(str_val)
    else:
        return 0.0

def wrapGrowthRatioDiv(value, MoM, YoY):
    """
    Wrap the growth ratio into grids
    MoM: month on month growth ratio
    YoY: year on year growth ratio
    """
    return "<div style='width:50%'>"+value+\
            "</div><div style='width:50%'><table><tr><td>"+MoM+ \
            "</td></tr><tr><td>"+YoY+"</td></tr></table></div>"