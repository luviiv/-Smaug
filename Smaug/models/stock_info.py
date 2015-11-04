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

    code = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(16))

    def __init__(self, code , name):
        self.code = code
        self.name = name

    def __repr__(self):
        return 'StockIdentity(%r,%r)' % (self.code, self.name)