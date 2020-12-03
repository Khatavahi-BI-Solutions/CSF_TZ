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
from csf_tz import console


@frappe.whitelist()
def get_healthcare_services_to_invoice(patient, company, encounter=None, service_order_category=None, prescribed=None):
	patient = frappe.get_doc('Patient', patient)
	items_to_invoice = []
	if patient:
		validate_customer_created(patient)
		# Customer validated, build a list of billable services
		if encounter:
			items_to_invoice += get_healthcare_service_order_to_invoice(patient, company, encounter, service_order_category, prescribed)
		return items_to_invoice



def get_healthcare_service_order_to_invoice(patient, company, encounter, service_order_category=None, prescribed=None):
	encounter_dict = frappe.get_all("Patient Encounter",filters = {
		"reference_encounter": encounter,
		"docstatus": 1,
	})
	encounter_list = [encounter]

	for i in encounter_dict:
		encounter_list.append(i.name)

	filters = {
			'patient': patient.name, 
			'company': company,
			'order_group': ["in", encounter_list],
			'invoiced': False,
			'docstatus': 1
	}

	if service_order_category:
		filters['healthcare_service_order_category'] = service_order_category
	if prescribed:
		filters['prescribed'] = prescribed
	services_to_invoice = []
	services = frappe.get_list(
		'Healthcare Service Order',
		fields=['*'],
		filters=filters
	)

	if services:
		for service in services:		
			practitioner_charge = 0
			income_account = None
			service_item = None
			if service.ordered_by:
				service_item = service.billing_item
				practitioner_charge = get_insurance_amount(service.insurance_subscription, service.billing_item, company, patient.name, service.insurance_company)
				income_account = get_income_account(service.ordered_by, company)

			services_to_invoice.append({
				'reference_type': 'Healthcare Service Order',
				'reference_name': service.name,
				'service': service_item,
				'rate': practitioner_charge,
				'income_account': income_account
			})
			

	return services_to_invoice
