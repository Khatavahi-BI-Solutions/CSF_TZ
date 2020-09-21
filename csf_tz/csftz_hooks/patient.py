# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals 
import frappe
from frappe import _
from csf_tz.nhif.doctype.company_nhif_settings.company_nhif_settings import get_nhifservice_token
from erpnext import get_company_currency, get_default_company



def get_token(doc, method):
    get_nhifservice_token(get_default_company())

