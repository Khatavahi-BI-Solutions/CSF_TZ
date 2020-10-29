# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from csf_tz import console


def test(doc, method):
    pass
    # console(doc.name, method)


@frappe.whitelist()
def get_paid_amount(insurance_subscription, billing_item, company):
    paid_amount = 0
    healthcare_insurance_coverage_plan = frappe.get_value(
        "Healthcare Insurance Subscription", insurance_subscription, "healthcare_insurance_coverage_plan")
    pric_list = frappe.get_value(
        "Healthcare Insurance Coverage Plan", healthcare_insurance_coverage_plan, "price_list")
    company_currency = frappe.get_value("Company", company, "default_currency")

    item_prices_data = frappe.get_all("Item Price",
                                      fields=[
                                          "item_code", "price_list_rate", "currency"],
                                      filters={
                                          'price_list': pric_list, 'item_code': billing_item, 'currency': company_currency},
                                      order_by="valid_from desc")
    if len(item_prices_data):
        paid_amount = item_prices_data[0].price_list_rate

    return paid_amount
