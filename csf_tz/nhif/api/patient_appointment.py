# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from csf_tz import console
from erpnext.erpnext.Healthcare.doctype.patient_appointment.patient_appointment import get_appointment_item, check_is_new_patient
from erpnext.healthcare.doctype.healthcare_settings.healthcare_settings import get_receivable_account
from erpnext.healthcare.utils import check_fee_validity
from frappe.utils import getdate


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


def invoice_appointment(appointment_doc, method):
    automate_invoicing = frappe.db.get_single_value(
        'Healthcare Settings', 'automate_appointment_invoicing')
    appointment_invoiced = frappe.db.get_value(
        'Patient Appointment', appointment_doc.name, 'invoiced')
    enable_free_follow_ups = frappe.db.get_single_value(
        'Healthcare Settings', 'enable_free_follow_ups')
    if enable_free_follow_ups:
        fee_validity = check_fee_validity(appointment_doc)
        if fee_validity and fee_validity.status == 'Completed':
            fee_validity = None
        elif not fee_validity:
            if frappe.db.exists('Fee Validity Reference', {'appointment': appointment_doc.name}):
                return
            if check_is_new_patient(appointment_doc.patient, appointment_doc.name):
                return
    else:
        fee_validity = None

    if not automate_invoicing and not appointment_doc.insurance_subscription and appointment_doc.mode_of_payment and not appointment_invoiced and not fee_validity:
        sales_invoice = frappe.new_doc('Sales Invoice')
        sales_invoice.patient = appointment_doc.patient
        sales_invoice.customer = frappe.get_value(
            'Patient', appointment_doc.patient, 'customer')
        sales_invoice.appointment = appointment_doc.name
        sales_invoice.due_date = getdate()
        sales_invoice.company = appointment_doc.company
        sales_invoice.debit_to = get_receivable_account(
            appointment_doc.company)

        item = sales_invoice.append('items', {})
        item = get_appointment_item(appointment_doc, item)

        # Add payments if payment details are supplied else proceed to create invoice as Unpaid
        if appointment_doc.mode_of_payment and appointment_doc.paid_amount:
            sales_invoice.is_pos = 1
            payment = sales_invoice.append('payments', {})
            payment.mode_of_payment = appointment_doc.mode_of_payment
            payment.amount = appointment_doc.paid_amount

        sales_invoice.set_missing_values(for_validate=True)
        sales_invoice.flags.ignore_mandatory = True
        sales_invoice.save(ignore_permissions=True)
        sales_invoice.submit()
        frappe.msgprint(_('Sales Invoice {0} created'.format(
            sales_invoice.name)), alert=True)
        frappe.db.set_value('Patient Appointment',
                            appointment_doc.name, 'invoiced', 1)
        frappe.db.set_value('Patient Appointment', appointment_doc.name,
                            'ref_sales_invoice', sales_invoice.name)
