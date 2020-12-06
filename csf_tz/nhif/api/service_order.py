# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals 
import frappe
from frappe import _


def set_missing_values(doc, method):
    if doc.order_reference_name and doc.order_reference_name:
        prescribe = frappe.get_value(doc.order_reference_name, doc.order_reference_name, "prescribe")
        if not prescribe:
            return
        doc.prescribed = prescribe
