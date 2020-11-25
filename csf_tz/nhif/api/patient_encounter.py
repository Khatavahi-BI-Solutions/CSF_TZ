# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals 
import frappe
from frappe import _
from frappe.utils import nowdate, get_year_start, getdate
import datetime


def validate(doc, method):
    insurance_subscription = doc.insurance_subscription
    if not insurance_subscription:
        return
    healthcare_insurance_coverage_plan = frappe.get_value("Healthcare Insurance Subscription", insurance_subscription, "healthcare_insurance_coverage_plan")
    if not healthcare_insurance_coverage_plan:
        frappe.throw(_("Healthcare Insurance Coverage Plan is Not defiend"))
    # hsic => Healthcare Service Insurance Coverage
    hsic_list = frappe.get_all("Healthcare Service Insurance Coverage", 
                                fields = {"healthcare_service_template","maximum_number_of_claims"},
                                filters = {
                                    "is_active": 1,
                                    "healthcare_insurance_coverage_plan": healthcare_insurance_coverage_plan,
                                    "start_date": ["<=",nowdate()],
                                    "end_date": [">=",nowdate()],
                                }
    )

    items_list = []
    if len(hsic_list) > 0:
        for i in hsic_list:
            items_list.append(i.healthcare_service_template)

    child_tables = {
		"drug_prescription": "drug_code",
		"lab_test_prescription": "lab_test_code",
		"procedure_prescription": "procedure",
		"radiology_procedure_prescription": "radiology_examination_template",
		"therapies": "therapy_type",
		# "diet_recommendation": "diet_plan" dosent have Healthcare Service Insurance Coverage
	}

    for key ,value in child_tables.items():
        table = doc.get(key)
        for row in table:
            if row.override_subscription:
                continue
            if row.get(value) not in items_list:
                frappe.throw(_("{0} not covred in Healthcare Insurance Coverage Plan").format(row.get(value)))
            else:
                maximum_number_of_claims = next(i for i in hsic_list if i["healthcare_service_template"] == row.get(value)).get("maximum_number_of_claims")
                if maximum_number_of_claims == 0:
                    continue
                year_start = get_year_start(nowdate(), True)
                year_end = get_year_end(nowdate(), True)
                claims_count = frappe.get_all("Healthcare Insurance Claim", filters={
                  "service_template": row.get(value),
                  "insurance_subscription": insurance_subscription,
                  "claim_posting_date": ["between",year_start,year_end],
                })
                if maximum_number_of_claims > len(claims_count):
                    frappe.throw(_("Maximum Number of Claims for {0} per year is exceeded").format(row.get(value)))



def get_year_end(dt, as_str=False):
    dt = getdate(dt)
    DATE_FORMAT = "%Y-%m-%d"
    date = datetime.date(dt.year, 12, 31)
    return date.strftime(DATE_FORMAT) if as_str else date