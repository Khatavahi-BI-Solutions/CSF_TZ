# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '1.7.1'

def console(*data):
	frappe.publish_realtime('out_to_console', data, user=frappe.session.user)
