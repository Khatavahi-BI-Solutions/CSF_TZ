# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals 
import frappe
from frappe import _
from frappe.model.document import Document
import uuid
from csf_tz.nhif.api.token import get_claimsservice_token
import json
import requests
from frappe.utils.background_jobs import enqueue
from frappe.utils import now, now_datetime, nowdate
from csf_tz.nhif.doctype.nhif_response_log.nhif_response_log import add_log
from csf_tz.nhif.api.healthcare_utils import get_item_rate
import os
from frappe.utils.background_jobs import enqueue
from frappe.utils.pdf import get_pdf, cleanup
from PyPDF2 import PdfFileWriter
from csf_tz import console

class NHIFPatientClaim(Document):
	def validate(self):
		self.patient_encounters = self.get_patient_encounters()
		self.set_claim_values()
		enqueue_generate_pdf(self)
		
	
	def before_submit(self):
		if not self.patient_signature:
			frappe.throw(_("Patient signature is required"))


	def set_claim_values(self):
		if not self.folio_id:
			self.folio_id = str(uuid.uuid1())
		self.facility_code = frappe.get_value("Company NHIF Settings", self.company, "facility_code")
		self.posting_date = now()
		self.claim_year = int(now_datetime().strftime("%Y"))
		self.claim_month = int(now_datetime().strftime("%m"))
		self.folio_no = int(self.name[-9:])
		self.created_by = frappe.get_value("User", frappe.session.user, "full_name")
		final_patient_encounter = self.get_final_patient_encounter()
		self.practitioner_no = frappe.get_value("Healthcare Practitioner", final_patient_encounter.practitioner, "tz_mct_code")
		if not self.practitioner_no:
			frappe.throw(_("There no TZ MCT Code for Practitioner {0}").format(final_patient_encounter.practitioner))
		self.date_discharge = final_patient_encounter.encounter_date
		self.date_admitted = frappe.get_value("Patient Appointment", self.patient_appointment, "appointment_date")
		self.attendance_date = frappe.get_value("Patient Appointment", self.patient_appointment, "appointment_date")
		appointment_type = frappe.get_value("Patient Appointment", self.patient_appointment, "appointment_type")
		self.patient_type_code = "OUTPATIENT" if appointment_type != "In Patient" else "IN PATIENT"
		self.patient_file_no = self.get_patient_file_no()
		self.set_patient_claim_disease()
		self.set_patient_claim_item()


	def get_patient_encounters(self):
		patient_encounters = frappe.get_all("Patient Encounter",
		 filters = {
			"appointment": self.patient_appointment,
			"docstatus": 1,
		 }
		)
		return patient_encounters


	def set_patient_claim_disease(self):
		self.nhif_patient_claim_disease = []
		diagnosis_list = []
		for encounter in self.patient_encounters:
			encounter_doc = frappe.get_doc("Patient Encounter", encounter.name)
			for row in encounter_doc.patient_encounter_preliminary_diagnosis:
				if row.code in diagnosis_list:
					continue
				diagnosis_list.append(row.code)
				new_row = self.append("nhif_patient_claim_disease", {})
				new_row.diagnosis_type = "Preliminary Diagnosis"
				new_row.patient_encounter = encounter.name
				new_row.codification_table = row.name
				new_row.folio_disease_id = str(uuid.uuid1())
				new_row.folio_id = self.folio_id
				new_row.medical_code = row.medical_code
				new_row.disease_code = row.code
				new_row.description = row.description
				new_row.created_by = frappe.get_value("User", row.modified_by, "full_name")
				new_row.date_created = row.modified.strftime("%Y-%m-%d")
			for row in encounter_doc.patient_encounter_final_diagnosis:
				if row.code in diagnosis_list:
					continue
				diagnosis_list.append(row.code)
				new_row = self.append("nhif_patient_claim_disease", {})
				new_row.diagnosis_type = "Final Diagnosis"
				new_row.patient_encounter = encounter.name
				new_row.codification_table = row.name
				new_row.folio_disease_id = str(uuid.uuid1())
				new_row.folio_id = self.folio_id
				new_row.medical_code = row.medical_code
				new_row.disease_code = row.code
				new_row.description = row.description
				new_row.created_by = frappe.get_value("User", row.modified_by, "full_name")
				new_row.date_created = row.modified.strftime("%Y-%m-%d")


	def set_patient_claim_item(self):
		childs_map = [
			{
				"table": "lab_test_prescription",
				"doctype": "Lab Test Template",
				"item": "lab_test_code",
				"comment": "lab_test_comment"
			},
			{
				"table": "radiology_procedure_prescription",
				"doctype": "Radiology Examination Template",
				"item": "radiology_examination_template",
				"comment": "radiology_test_comment"
			},
			{
				"table": "procedure_prescription",
				"doctype": "Clinical Procedure Template",
				"item": "procedure",
				"comment": "comments"
			},
			{
				"table": "drug_prescription",
				"doctype": "Medication",
				"item": "drug_code",
				"comment": "comment"
			},
			{
				"table": "therapies",
				"doctype": "Therapy Type",
				"item": "therapy_type",
				"comment": "comment"
			}
    	]
		self.nhif_patient_claim_item = []
		for encounter in self.patient_encounters:
			encounter_doc = frappe.get_doc("Patient Encounter", encounter.name)
			for i in childs_map:
				for row in encounter_doc.get(i.get("table")):
					if row.prescribe:
						continue
					item_code = frappe.get_value(i.get("doctype"), row.get(i.get("item")), "item")
					item_rate = get_item_rate(item_code, self.company, encounter_doc.insurance_subscription, encounter_doc.insurance_company)
					new_row = self.append("nhif_patient_claim_item", {})
					new_row.item_name = row.get(i.get("item"))
					new_row.item_code = get_item_refcode(item_code)
					new_row.item_quantity = row.get("quantity") or 1
					new_row.unit_price = item_rate
					new_row.amount_claime = item_rate * new_row.item_quantity
					new_row.approval_ref_no = row.get(i.get("comment"))
					new_row.patient_encounter = encounter.name
					new_row.ref_doctype = row.doctype
					new_row.ref_docname = row.name
					new_row.folio_item_id = str(uuid.uuid1())
					new_row.folio_id = self.folio_id
					new_row.date_created = row.modified.strftime("%Y-%m-%d")
					new_row.created_by = frappe.get_value("User", row.modified_by, "full_name")
		
		sorted_patient_claim_item = sorted(self.nhif_patient_claim_item, key=lambda k: k.get("ref_doctype"))
		idx = 2
		for row in sorted_patient_claim_item:
			row.idx = idx
			idx += 1
		self.nhif_patient_claim_item = sorted_patient_claim_item

		patient_appointment_doc = frappe.get_doc("Patient Appointment", self.patient_appointment)
		item_code = patient_appointment_doc.billing_item
		item_rate = get_item_rate(item_code, self.company, patient_appointment_doc.insurance_subscription, patient_appointment_doc.insurance_company)
		new_row = self.append("nhif_patient_claim_item", {})
		new_row.item_name = patient_appointment_doc.billing_item
		new_row.item_code = get_item_refcode(item_code)
		new_row.item_quantity = 1
		new_row.unit_price = item_rate
		new_row.amount_claime = item_rate
		# new_row.approval_ref_no = ""
		new_row.ref_doctype = patient_appointment_doc.doctype
		new_row.ref_docname = patient_appointment_doc.name
		new_row.folio_item_id = str(uuid.uuid1())
		new_row.folio_id = self.folio_id
		new_row.date_created = patient_appointment_doc.modified.strftime("%Y-%m-%d")
		new_row.created_by = frappe.get_value("User", patient_appointment_doc.modified_by, "full_name")
		new_row.idx = 1
		
				


	def get_final_patient_encounter(self):
		patient_encounter_list = frappe.get_all("Patient Encounter",
		 filters = {
			"appointment": self.patient_appointment,
			"docstatus": 1,
			"encounter_type": "Final",
		 },
		 fields = {"*"}
		)
		if len(patient_encounter_list) == 0:
			frappe.throw(_("There no Final Patient Encounter for this Appointment"))
		return patient_encounter_list[0]


	def get_patient_file_no(self):
		patient_encounters = self.get_patient_encounters()
		patient_file_no = ""
		for encounter in patient_encounters:
			patient_file_no += encounter.name + " "
		return patient_file_no


def get_item_refcode(item_code):
	code_list = frappe.get_all("Item Customer Detail", 
		filters = {
			"parent": item_code,
			"customer_name": "NHIF"
		},
		fields = ["ref_code"]
	)
	if len(code_list) == 0:
		frappe.throw(_("Item {0} has not NHIF Code Reference").format(item_code))
	ref_code = code_list[0].ref_code
	if not ref_code:
		frappe.throw(_("Item {0} has not NHIF Code Reference").format(item_code))
	return ref_code



def enqueue_generate_pdf(doc):
    enqueue(method=generate_pdf, queue='short', timeout=100000, is_async=True ,job_name="print_salary_slips", kwargs=doc )


def generate_pdf(kwargs):
	doc = kwargs
	doc_name = doc.name
	data = doc.patient_encounters
	data_list = []
	for i in data:
		data_list.append(i.name)
	doctype = dict(
		{"Patient Encounter": data_list}
	)
	print_format = ""
	default_print_format = frappe.db.get_value('Property Setter', dict(property='default_print_format', doc_type="Patient Encounter"), "value")
	if default_print_format:
		print_format = default_print_format
	else:
		print_format = "Standard"

	pdf = download_multi_pdf(doctype, doc_name,
								format=print_format, no_letterhead=0)
	if pdf:
		ret = frappe.get_doc({
			"doctype": "File",
			"attached_to_doctype": "NHIF Patient Claim",
			"attached_to_name": doc_name,
			"folder": "Home/Attachments",
			"file_name": doc_name + ".pdf",
			"file_url": "/files/" + doc_name + ".pdf",
			"content": pdf
		})
		ret.save(ignore_permissions=1)
		return ret


def download_multi_pdf(doctype, name, format=None, no_letterhead=0):
    output = PdfFileWriter()
    if isinstance(doctype, dict):
        for doctype_name in doctype:
            for doc_name in doctype[doctype_name]:
                try:
                    console(doc_name)
                    output = frappe.get_print(
                        doctype_name, doc_name, format, as_pdf=True, output=output, no_letterhead=no_letterhead)
                except Exception:
                    frappe.log_error("Permission Error on doc {} of doctype {}".format(
                        doc_name, doctype_name))
        frappe.local.response.filename = "{}.pdf".format(name)

    return read_multi_pdf(output)


def read_multi_pdf(output):
    fname = os.path.join(
        "/tmp", "frappe-pdf-{0}.pdf".format(frappe.generate_hash()))
    output.write(open(fname, "wb"))

    with open(fname, "rb") as fileobj:
        filedata = fileobj.read()

    return filedata