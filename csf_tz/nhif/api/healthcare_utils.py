# -*- coding: utf-8 -*-
# Copyright (c) 2018, earthians and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import math
import frappe
from frappe import _
from erpnext.healthcare.doctype.healthcare_settings.healthcare_settings import get_income_account
from erpnext.healthcare.utils import validate_customer_created
from csf_tz.nhif.api.patient_appointment import get_insurance_amount


@frappe.whitelist()
def get_healthcare_services_to_invoice(patient, company, service_order_category=None, encounter=None, prescribed=None):
	patient = frappe.get_doc('Patient', patient)
	items_to_invoice = []
	if patient:
		validate_customer_created(patient)
		# Customer validated, build a list of billable services
		if service_order_category and encounter:
			items_to_invoice += get_healthcare_service_order_to_invoice(patient, company, service_order_category, encounter, prescribed)
		return items_to_invoice



def get_healthcare_service_order_to_invoice(patient, company, service_order_category, encounter, prescribed=None):
	services_to_invoice = []
	services = frappe.get_list(
		'Healthcare Service Order',
		fields=['*'],
		filters={
			'patient': patient.name, 
			'company': company,
			'healthcare_service_order_category': service_order_category,
			'order_group': encounter,
			'invoiced': False,
			'docstatus': 1
		}
	)
	if services:
		for service in services:		
			practitioner_charge = 0
			income_account = None
			service_item = None
			if service.ordered_by:
				service_item = service.billing_item
				practitioner_charge = get_insurance_amount(service.insurance_subscription, service.billing_item, company, patient, service.insurance_company)
				income_account = get_income_account(service.ordered_by, company)

			services_to_invoice.append({
				'reference_type': 'Patient Encounter',
				'reference_name': service.name,
				'service': service_item,
				'rate': practitioner_charge,
				'income_account': income_account
			})
			

	return services_to_invoice



@frappe.whitelist()
def duplicate_encounter(encounter):
	doc = frappe.get_doc("Patient Encounter", encounter)
	appointment_doc = frappe.copy_doc(doc)
	appointment_doc.save()
	frappe.msgprint(_('Patient Encounter {0} created'.format(appointment_doc.name)), alert=True)
	return appointment_doc.name