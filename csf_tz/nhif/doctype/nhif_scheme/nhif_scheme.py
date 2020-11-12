# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class NHIFScheme(Document):
	pass


def add_scheme(id, name=None):
	if frappe.db.exists('NHIF Scheme', id):
		return
	doc = frappe.new_doc('NHIF Scheme')
	doc.scheme_id = id
	if name:
		doc.scheme_name = name
	doc.save(ignore_permissions=True)
	doc.submit()
	return id