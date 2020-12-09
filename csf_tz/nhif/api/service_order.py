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


@frappe.whitelist()
def clear_insurance_details(service_order):
    service_order_doc = frappe.get_doc('Healthcare Service Order', service_order)
    if service_order_doc.docstatus != 0:
        return
    insurance_claim = service_order_doc.insurance_claim
    service_order_doc.insurance_claim = ""
    service_order_doc.insurance_subscription = ""
    service_order_doc.insurance_company = ""
    service_order_doc.claim_status = ""
    service_order_doc.db_update()
    frappe.db.commit()

    insurance_claim_doc = frappe.get_doc('Healthcare Insurance Claim', insurance_claim)
    insurance_claim_doc.cancel()
    insurance_claim_doc.db_update()
    insurance_claim_doc.reload()
    insurance_claim_doc.delete()
    frappe.db.commit()
    frappe.msgprint(_('Healthcare Insurance Claim {0} deleted successfully.').format(
                frappe.bold(insurance_claim)), alert=True)
    return True