# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "csf_tz"
app_title = "CSF TZ"
app_publisher = "Aakvatech"
app_description = "Country Specific Functionality Tanzania"
app_icon = "octicon octicon-bookmark"
app_color = "green"
app_email = "info@aakvatech.com"
app_license = "GNU General Public License (v3)"

fixtures = [
	{"doctype":"Custom Field", "filters": [["name", "in", (
		"Address-tax_category",
		"Account-item",
		"Appointment Type-visit_type_id",
		"Company-auto_create_for_purchase_withholding",
		"Company-auto_create_for_sales_withholding",
		"Company-auto_submit_for_purchase_withholding",
		"Company-auto_submit_for_sales_withholding",
		"Company-block_number",
		"Company-bypass_material_request_validation",
		"Company-city",
		"Company-column_break_55",
		"Company-column_break_60",
		"Company-company_bank_details",
		"Company-default_withholding_payable_account",
		"Company-default_withholding_receivable_account",
		"Company-education_section",
		"Company-enabled_auto_create_delivery_notes",
		"Company-fee_bank_account",
		"Company-max_records_in_dialog",
		"Company-nmb_password",
		"Company-nmb_series",
		"Company-nmb_url",
		"Company-nmb_username",
		"Company-p_o_box",
		"Company-plot_number",
		"Company-section_break_12",
		"Company-send_fee_details_to_bank",
		"Company-street",
		"Company-student_applicant_fees_revenue_account",
		"Company-tin",
		"Company-vrn",
		"Company-withholding_section",
		"Contact-is_billing_contact",
		"Customer-vrn",
		"Deleted Document-github_sync_id",
		"Deleted Document-hub_sync_id",
		"Delivery Note-form_sales_invoice",
		"Employee-attachments",
		"Employee-files",
		"Fees-abbr",
		"Fees-bank_reference",
		"Fees-callback_token",
		"Healthcare Insurance Claim-reference_dn",
		"Healthcare Insurance Claim-reference_dt",
		"Healthcare Insurance Company-default_price_list",
		"Healthcare Insurance Company-facility_code",
		"Healthcare Insurance Subscription-coverage_plan_card_number",
		"Healthcare Insurance Subscription-coverage_plan_name",
		"Healthcare Practitioner-doctors_signature",
		"Healthcare Practitioner-title_and_qualification",
		"Healthcare Practitioner-tz_mct_code",
		"Item-hub_sync_id",
		"Item-withholding_tax_rate_on_sales",
		"Item-witholding_tax_rate_on_purchase",
		"Journal Entry-expense_record",
		"Journal Entry-from_date",
		"Journal Entry-to_date",
		"Material Request Item-stock_reconciliation",
		"Medication-strength_text",
		"Mode of Payment-price_list",
		"Operation-image",
		"Patient Appointment-authorization_number",
		"Patient Appointment-coverage_plan_card_number",
		"Patient Appointment-coverage_plan_name",
		"Patient Appointment-insurance_company_name",
		"Patient Appointment-ref_vital_signs",
		"Patient Appointment-reference_journal_entry",
		"Patient Appointment-referral_no",
		"Patient Encounter-examination_detail",
		"Patient-card_no",
		"Patient-column_break_3",
		"Patient-insurance_company",
		"Patient-insurance_details",
		"Patient-patient_details_with_formatting",
		"Payment Entry Reference-end_date",
		"Payment Entry Reference-posting_date",
		"Payment Entry Reference-section_break_9",
		"Payment Entry Reference-start_date",
		"POS Profile-column_break_1",
		"POS Profile-electronic_fiscal_device",
		"Print Settings-compact_item_print",
		"Print Settings-print_taxes_with_zero_amount",
		"Print Settings-print_uom_after_quantity",
		"Procedure Prescription-column_break_10",
		"Procedure Prescription-hso_payment_method",
		"Procedure Prescription-override_insurance_subscription",
		"Project-github_sync_id",
		"Purchase Invoice Item-withholding_tax_entry",
		"Purchase Invoice Item-withholding_tax_rate",
		"Purchase Invoice-expense_record",
		"Purchase Order-posting_date",
		"Radiology Examination Template-body_part",
		"Radiology Examination Template-radiology_report",
		"Radiology Examination Template-radiology_report_details",
		"Radiology Examination Template-radiology_report_type",
		"Radiology Examination-body_part",
		"Radiology Examination-radiology_report",
		"Radiology Examination-radiology_report_details",
		"Sales Invoice Item-allow_over_sell",
		"Sales Invoice Item-allow_override_net_rate",
		"Sales Invoice Item-delivery_status",
		"Sales Invoice Item-insurance_claim",
		"Sales Invoice Item-insurance_claim_amount",
		"Sales Invoice Item-insurance_claim_coverage",
		"Sales Invoice Item-reference_dn",
		"Sales Invoice Item-reference_dt",
		"Sales Invoice Item-withholding_tax_entry",
		"Sales Invoice Item-withholding_tax_rate",
		"Sales Invoice-column_break_29",
		"Sales Invoice-delivery_status",
		"Sales Invoice-efd_z_report",
		"Sales Invoice-electronic_fiscal_device",
		"Sales Invoice-enabled_auto_create_delivery_notes",
		"Sales Invoice-patient",
		"Sales Invoice-patient_name",
		"Sales Invoice-patient_payable_amount",
		"Sales Invoice-price_reduction",
		"Sales Invoice-ref_practitioner",
		"Sales Invoice-statutory_details",
		"Sales Invoice-total_insurance_claim_amount",
		"Sales Invoice-tra_control_number",
		"Sales Invoice-witholding_tax_certificate_number",
		"Sales Order-cost_center",
		"Sales Order-posting_date",
		"Stock Entry Detail-column_break_32",
		"Stock Entry Detail-item_weight_details",
		"Stock Entry Detail-total_weight",
		"Stock Entry Detail-weight_per_unit",
		"Stock Entry Detail-weight_uom",
		"Stock Entry-column_break_69",
		"Stock Entry-driver",
		"Stock Entry-driver_name",
		"Stock Entry-final_destination",
		"Stock Entry-item_uom",
		"Stock Entry-qty",
		"Stock Entry-repack_qty",
		"Stock Entry-repack_template",
		"Stock Entry-total_net_weight",
		"Stock Entry-transport_receipt_date",
		"Stock Entry-transport_receipt_no",
		"Stock Entry-transporter",
		"Stock Entry-transporter_info",
		"Stock Entry-transporter_name",
		"Stock Entry-vehicle_no",
		"Stock Reconciliation Item-material_request",
		"Stock Reconciliation-sort_items",
		"Student Applicant-bank_reference",
		"Student Applicant-fee_structure",
		"Student Applicant-program_enrollment",
		"Student Applicant-student_applicant_fee",
		"Student-bank",
		"Supplier-vrn",
		"Task-github_sync_id",
		"Vital Signs-oxygen_saturation_spo2",
		"Patient-product_code",
		"Patient-membership_no",
		"Patient Appointment-get_authorization_number",
		"Healthcare Service Order-prescribed",
		"Healthcare Service Insurance Coverage-maximum_claim_duration",
		"Healthcare Insurance Claim-section_break_40",
		"Healthcare Insurance Claim-ready_to_submit",
		"Healthcare Insurance Claim-column_break_38",
		"Healthcare Insurance Claim-insurance_company_item_name",
		"Healthcare Insurance Claim-insurance_company_item_code",
		"Healthcare Insurance Claim-section_break_35",
		"Patient Encounter-section_break_28",
		"Patient Encounter-patient_encounter_preliminary_diagnosis",
		"Patient Encounter-patient_encounter_final_diagnosis",
		"Drug Prescription-medical_code",
		"Lab Prescription-medical_code",
		"Procedure Prescription-medical_code",
		"Radiology Procedure Prescription-medical_code",
		"Therapy Plan Detail-medical_code",
		"Diet Recommendation-medical_code",
		"Patient Encounter-reference",
		"Patient Encounter-encounter_type",
		"Patient Encounter-duplicate",
		"Patient Encounter-column_break_31",
		"Patient Encounter-reference_encounter",
		"Patient Encounter-from_encounter",
		"Patient Encounter-previous_lab_prescription",
		"Patient Encounter-previous_drug_prescription",
		"Patient Encounter-previous_procedure_prescription",
		"Patient Encounter-previous_radiology_procedure_prescription",
		"Patient Encounter-previous_therapy_plan_detail",
		"Patient Encounter-previous_diet_recommendation",
		"Medication-default_comments",
		"Lab Test Template-lab_routine_normals",
		"Lab Test Template-m_text",
		"Lab Test Template-column_break_26",
		"Lab Test Template-f_text",
		"Lab Test Template-column_break_30",
		"Lab Test Template-c_min_range",
		"Lab Test Template-c_max_range",
		"Lab Test Template-c_text",
		"Lab Test Template-column_break_34",
		"Lab Test Template-i_min_range",
		"Lab Test Template-i_max_range",
		"Lab Test Template-i_text",
		"Lab Test Template-m_min_range",
		"Lab Test Template-m_max_range",
		"Lab Test Template-f_min_range",
		"Lab Test Template-f_max_range",
		"Normal Test Result-detailed_normal_range",
		"Normal Test Result-result_status",
		"Normal Test Result-min_normal",
		"Normal Test Result-max_normal",
		"Normal Test Result-text_normal"
		"Healthcare Insurance Claim-order_encounter",
		"Drug Prescription-override_subscription",
		"Lab Prescription-override_subscription",
		"Radiology Procedure Prescription-override_subscription",
		"Procedure Prescription-override_subscription",
		"Therapy Plan Detail-override_subscription",
		"Patient Encounter-section_break_52",
		"Patient Encounter-healthcare_service_unit",
		"Lab Prescription-prescribe",
		"Radiology Procedure Prescription-prescribe",
		"Procedure Prescription-prescribe",
		"Drug Prescription-prescribe",
		"Therapy Plan Detail-prescribe",
		"Delivery Note Item-reference_name",
		"Delivery Note Item-reference_doctype",
		"Delivery Note-reference_name",
		"Delivery Note-reference_doctype",
		"Healthcare Service Order-original_his",
		"Healthcare Service Order-clear_insurance_details",
		"Vital Signs-rbg",
		"Vital Signs-height_in_cm",
		"Therapy Plan Detail-comment",
		"Therapy Plan Detail-column_break_6",
		"Patient-next_to_kid_column_break",
		"Patient-next_to_kin_relationship",
		"Patient-next_to_kin_mobile_no",
		"Patient-next_to_kin_name",
		"Patient-next_to_kin_details",
		"Patient Encounter-image",
		"Vital Signs-image",
		"Patient Appointment-patient_image2",
	)]]},
	{"doctype":"Property Setter", "filters": [["name", "in", (
		"Bank Reconciliation Detail-payment_entry-columns",
		"Bank Reconciliation Detail-posting_date-columns",
		"Bank Reconciliation Detail-posting_date-in_list_view",
		"Customer-tax_id-label",
		"Document Attachment-attachment-in_list_view",
		"Healthcare Insurance Subscription-main-search_fields",
		"Medication-main-search_fields",
		"Operation-image_field",
		"Patient Appointment-radiology_examination_template-depends_on",
		"Patient-patient_details-hidden",
		"Payment Entry Reference-due_date-columns",
		"Payment Entry Reference-due_date-width",
		"Payment Entry Reference-reference_doctype-columns",
		"Payment Entry Reference-reference_doctype-in_list_view",
		"Payment Entry Reference-reference_name-columns",
		"Payment Entry-payment_accounts_section-collapsible",
		"Payment Entry-section_break_12-collapsible",
		"Payment Reconciliation Payment-posting_date-columns",
		"Payment Reconciliation Payment-posting_date-in_list_view",
		"Radiology Examination Template-main-quick_entry",
		"Radiology Examination-tc_name-fetch_from",
		"Radiology Examination-tc_name-hidden",
		"Radiology Examination-terms-hidden",
		"Sales Invoice-is_pos-in_standard_filter",
		"Sales Invoice-pos_profile-in_standard_filter",
		"Sales Invoice-posting_date-in_list_view",
		"Stock Entry-from_warehouse-fetch_from",
		"Student Applicant-application_status-options",
		"Student Applicant-application_status-read_only",
		"Patient Appointment-naming_series-hidden",
		"Patient-main-quick_entry",
		"Patient Appointment-section_break_19-hidden",
		"Patient Encounter-diagnosis_in_print-hidden",
		"Patient Encounter-diagnosis-hidden",
		"Patient Encounter-physical_examination-hidden",
		"Patient Encounter-codification-hidden",
		"Patient Encounter-codification-collapsible",
		"Drug Prescription-comment-fetch_from",
		"Healthcare Service Insurance Coverage-is_active-allow_on_submit",
		"Healthcare Service Insurance Coverage-end_date-Allow on Submit",
		"Radiology Examination-appointment-hidden",
		"Lab Test-insurance_section-hidden",
		"Radiology Examination-insurance_section-hidden",
		"Drug Prescription-dosage-fetch_if_empty",
		"Drug Prescription-period-fetch_if_empty",
		"Drug Prescription-dosage_form-fetch_if_empty",
		"Patient Encounter-section_break_3-collapsible",
		"Patient Encounter-sb_source-collapsible,",
		"Patient Encounter-insurance_section-collapsible",
		"Patient Encounter-sb_test_prescription-collapsible",
		"Patient Encounter-radiology_procedures_section-collapsible",
		"Patient Encounter-sb_procedures-collapsible",
		"Patient Encounter-rehabilitation_section-collapsible",
		"Patient Encounter-diet_recommendation_section-collapsible",
		"Patient Encounter-encounter_comment-hidden",
		"Patient Encounter-rehabilitation_section-collapsible_depends_on",
		"Patient Encounter-sb_drug_prescription-collapsible_depends_on",
		"Patient Encounter-sb_procedures-collapsible_depends_on",
		"Patient Encounter-radiology_procedures_section-collapsible_depends_on",
		"Patient Encounter-sb_test_prescription-collapsible_depends_on",
		"Patient Encounter-source-read_only_depends_on",
		"Patient Encounter-company-read_only",
		"Patient Encounter-appointment_type-read_only_depends_on",
		"Patient-more_info-collapsible_depends_on",
		"Healthcare Insurance Subscription-country-hidden",
		"Healthcare Insurance Subscription-insurance_company_customer-hidden",
		"Healthcare Insurance Subscription-insurance_company_name-read_only",
		"Healthcare Insurance Subscription-gender-read_only",
		"Healthcare Insurance Subscription-customer-hidden",
		"Healthcare Insurance Subscription-patient_name-read_only",
		"Patient-default_price_list-hidden",
		"Patient-default_currency-read_only",
		"Patient-territory-hidden",
		"Patient-invite_user-default",
		"Patient-triage-hidden",
		"Drug Prescription-comment-mandatory_depends_on",
		"Procedure Prescription-comments-mandatory_depends_on",
		"Radiology Procedure Prescription-radiology_test_comment-mandatory_depends_on",
		"Lab Prescription-lab_test_comment-mandatory_depends_on",
		"Patient Encounter-main-image_field",
		"Vital Signs-main-image_field",
		"Patient Appointment-main-image_field",
		"Item-customer_details-collapsible_depends_on",
		"Item-customer_details-collapsible",
	)]]},
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/csf_tz/css/csf_tz.css"
# app_include_js = "/assets/csf_tz/js/csf_tz.js"
app_include_js = [
	"/assets/js/select_dialog.min.js",
	"/assets/js/to_console.min.js",
	"/assets/js/jobcards.min.js",
	"/assets/csf_tz/node_modules/vuetify/dist/vuetify.js",
	]

app_include_css = "/assets/csf_tz/css/theme.css"
web_include_css = "/assets/csf_tz/css/theme.css"
# include js, css files in header of web template
# web_include_css = "/assets/csf_tz/css/csf_tz.css"
# web_include_js = "/assets/csf_tz/js/csf_tz.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Payment Entry" : "csf_tz/payment_entry.js",
	"Sales Order" : "csf_tz/sales_order.js",
	"Delivery Note" : "csf_tz/delivery_note.js",
	"Customer" : "csf_tz/customer.js",
	"Supplier" : "csf_tz/supplier.js",
	"Stock Entry" : "csf_tz/stock_entry.js",
	"Account" : "csf_tz/account.js",
	"Asset" : "csf_tz/asset.js",
	"Warehouse" : "csf_tz/warehouse.js",
	"Company": "csf_tz/company.js",
	"Stock Reconciliation": "csf_tz/stock_reconciliation.js",
	"Fees": "csf_tz/fees.js",
	"Program Enrollment Tool": "csf_tz/program_enrollment_tool.js",
	"Purchase Invoice": "csf_tz/purchase_invoice.js",
	"Quotation": "csf_tz/quotation.js",
	"Purchase Receipt": "csf_tz/purchase_receipt.js",
	"Purchase Order": "csf_tz/purchase_order.js",
	"Student Applicant": "csf_tz/student_applicant.js",
	"Bank Reconciliation": "csf_tz/bank_reconciliation.js",
	"Program Enrollment": "csf_tz/program_enrollment.js",
	"Payroll Entry": "csf_tz/payroll_entry.js",
	"Salary Slip": "csf_tz/salary_slip.js",
	"Patient Appointment": "nhif/api/patient_appointment.js",
	"Patient": "nhif/api/patient.js",
	"Sales Invoice" : [
		"csf_tz/sales_invoice.js",
		"nhif/api/sales_invoice.js"
	],
	"Patient Encounter": "nhif/api/patient_encounter.js",
	"Lab Test": "nhif/api/lab_test.js",
	"Healthcare Service Order": "nhif/api/service_order.js",
	"Healthcare Insurance Company": "nhif/api/insurance_company.js",
	"Vital Signs": "nhif/api/vital_signs.js",
}
#csf_tz.nhif.api.patient_appointment
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "csf_tz.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "csf_tz.install.before_install"
# after_install = "csf_tz.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "csf_tz.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Open Invoice Exchange Rate Revaluation": {
		"validate": "csf_tz.custom_api.getInvoiceExchangeRate"
	},
	"Sales Invoice": {
		"on_submit":[
			'csf_tz.custom_api.validate_net_rate',
			"csf_tz.custom_api.create_delivery_note",
			'csf_tz.custom_api.check_submit_delivery_note',
			'csf_tz.custom_api.make_withholding_tax_gl_entries_for_sales',
			"csf_tz.nhif.api.sales_invoice.create_healthcare_docs",
			],
		'validate': [
			'csf_tz.custom_api.check_validate_delivery_note',
			'csf_tz.custom_api.validate_items_remaining_qty',
			'csf_tz.custom_api.calculate_price_reduction',
			],
		'on_cancel': 'csf_tz.custom_api.check_cancel_delivery_note',
	},
	'Delivery Note': {
		'on_submit': 'csf_tz.custom_api.update_delivery_on_sales_invoice',
		'on_cancel': 'csf_tz.custom_api.update_delivery_on_sales_invoice',
  },
	"Account": {
		"on_update":"csf_tz.custom_api.create_indirect_expense_item",
		"after_insert":"csf_tz.custom_api.create_indirect_expense_item",
	},
	"Purchase Invoice": {
		"on_submit":"csf_tz.custom_api.make_withholding_tax_gl_entries_for_purchase",
	},
	"Fees": {
		"before_insert":"csf_tz.custom_api.set_fee_abbr",
		"after_insert":"csf_tz.bank_api.set_callback_token",
		"on_submit":"csf_tz.bank_api.invoice_submission",
		"on_cancel":"csf_tz.bank_api.cancel_invoice",
	},
	"Program Enrollment": {
		"onload":"csf_tz.csftz_hooks.program_enrollment.create_course_enrollments_override",
		"refresh":"csf_tz.csftz_hooks.program_enrollment.create_course_enrollments_override",
		"reload":"csf_tz.csftz_hooks.program_enrollment.create_course_enrollments_override",
		"before_submit":"csf_tz.csftz_hooks.program_enrollment.validate_submit_program_enrollment",
	},
	"*": {
		"validate"                      :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"onload"                        :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_insert"                 :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"after_insert"                  :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_naming"                 :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_change"                 :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_update_after_submit"    :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_validate"               :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_save"                   :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_update"                     :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_submit"                 :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"autoname"                      :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_cancel"                     :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_trash"                      :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_submit"                     :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_update_after_submit"        :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_change"                     :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
	},
	"Stock Entry": {
		"validate": "csf_tz.custom_api.calculate_total_net_weight",
	},
	"Student Applicant": {
		"on_update_after_submit":"csf_tz.csftz_hooks.student_applicant.make_student_applicant_fees",
	},
	"Patient Appointment": {
		"validate":[
			"csf_tz.nhif.api.patient_appointment.make_vital",
		]
	},
	"Vital Signs": {
		"on_submit":"csf_tz.nhif.api.patient_appointment.make_encounter",
	},
	"Patient": {
		"validate":"csf_tz.nhif.api.patient.validate",
	},
	"Healthcare Insurance Claim": {
		"before_insert":[
			"csf_tz.nhif.api.insurance_claim.set_patient_encounter",
			"csf_tz.nhif.api.insurance_claim.set_price",
		]
	},
	"Patient Encounter": {
		"validate":"csf_tz.nhif.api.patient_encounter.validate",
		"on_submit":"csf_tz.nhif.api.patient_encounter.on_submit",
	},
	"Healthcare Service Order": {
		"before_insert": "csf_tz.nhif.api.service_order.set_missing_values"
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"csf_tz.tasks.all"
	# ],
	"daily": [
		"csf_tz.custom_api.create_delivery_note_for_all_pending_sales_invoice",
		"csf_tz.csf_tz.doctype.visibility.visibility.trigger_daily_alerts",
		"csf_tz.csf_tz.doctype.vehicle_fine_record.vehicle_fine_record.check_fine_all_vehicles",
		"csf_tz.bank_api.reconciliation",
	],
	# "hourly": [
	# 	"csf_tz.tasks.hourly"
	# ],
	"weekly": [
		"csf_tz.custom_api.make_stock_reconciliation_for_all_pending_material_request"
	]
	# "monthly": [
	# 	"csf_tz.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "csf_tz.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "csf_tz.event.get_events"
# }

