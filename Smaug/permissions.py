# -*- coding: utf-8 -*-
"""
    permissions.py
    ~~~~~~~~~~~
    permission list
    :copyright: (c) 2015 by Lu Tianchao.
    :license: Apache, see LICENSE for more details.
"""

from flask.ext.principal import RoleNeed, Permission

admin = Permission(RoleNeed('admin'))
moderator = Permission(RoleNeed('moderator'))
auth = Permission(RoleNeed('authenticated'))

# this is assigned when you want to block a permission to all
# never assign this role to anyone !
null = Permission(RoleNeed('null'))