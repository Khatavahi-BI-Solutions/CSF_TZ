# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals 
import frappe
from frappe import _
from csf_tz import console


def set_patient_encounter(doc, method):
    if doc.reference_dn:
        reference_doc = frappe.get_doc(doc.reference_dt , doc.reference_dn)
        if reference_doc.parenttype and reference_doc.parenttype == "Patient Encounter":
            doc.order_encounter = reference_doc.parent
