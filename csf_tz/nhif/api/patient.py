# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals 
import frappe
from frappe import _
from csf_tz.nhif.api.token import get_nhifservice_token
from erpnext import get_company_currency, get_default_company
from csf_tz import console
import json
import requests
from time import sleep
from frappe.utils import  now, add_to_date, now_datetime




def get_token(doc, method):
    if not doc.allow_update_from_insurance:
        return
    company = get_default_company()
    token = get_nhifservice_token(company)
    console(token)
    nhifservice_url = frappe.get_value("Company NHIF Settings", company, "nhifservice_url")
    headers = {
        "Authorization" : "Bearer " + token
    }
    url = str(nhifservice_url) + "/nhifservice/breeze//verification/GetCardDetails?CardNo=" + str(doc.card_no)
    for i in range(3):
        try:
            r = requests.get(url, headers = headers, timeout=5)
            r.raise_for_status()
            frappe.logger().debug({"webhook_success": r.text})
            if json.loads(r.text):
                console(json.loads(r.text))
                return json.loads(r.text)
            else:
                frappe.throw(json.loads(r.text))
        except Exception as e:
            frappe.logger().debug({"webhook_error": e, "try": i + 1})
            sleep(3 * i + 1)
            if i != 2:
                continue
            else:
                raise e

