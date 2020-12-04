# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals 
import frappe
from frappe import _
from csf_tz.nhif.api.patient_appointment import get_item_price


def set_patient_encounter(doc, method):
    if doc.reference_dn:
        reference_doc = frappe.get_doc(doc.reference_dt , doc.reference_dn)
        if reference_doc.parenttype and reference_doc.parenttype == "Patient Encounter":
            doc.order_encounter = reference_doc.parent
        elif doc.reference_dt == "Healthcare Service Order" :
            doc.order_encounter = reference_doc.order_group


def set_price(doc, method):
    price_list = None
    price_list_rate = None
    if  doc.insurance_subscription:
        hic_plan = frappe.get_value(
            "Healthcare Insurance Subscription", doc.insurance_subscription, "healthcare_insurance_coverage_plan")
        price_list = frappe.get_value(
            "Healthcare Insurance Coverage Plan", hic_plan, "price_list")
        if price_list:
            if price_list_rate and price_list_rate != 0:
                price_list_rate = get_item_price(doc.service_item, price_list, doc.company)
                doc.price_list_rate = price_list_rate
                return

    if not price_list and doc.insurance_company:
        price_list = frappe.get_value(
        "Healthcare Insurance Company", doc.insurance_company, "default_price_list")
    if not price_list:
            frappe.throw(_("Please set Price List in Healthcare Insurance Coverage Plan"))
    price_list_rate = get_item_price(doc.service_item, price_list, doc.company)
    if price_list_rate == 0:
        frappe.throw(_("Please set Price List for item: {0}").format(doc.service_item))
    doc.price_list_rate = price_list_rate