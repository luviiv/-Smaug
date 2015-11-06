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