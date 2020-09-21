# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals 
import frappe
from frappe.model.document import Document
from frappe.utils import get_url_to_form, get_url
from frappe import _
from frappe.utils.password import get_decrypted_password
import json
import requests
from time import sleep
from frappe.utils import today, format_datetime, now, nowdate, getdate, get_url, get_host_name, add_to_date
from csf_tz import console



class CompanyNHIFSettings(Document):
	def validate(self):
		get_nhifservice_token(self.company)


def get_nhifservice_token(company):
	setting_doc = frappe.get_doc("Company NHIF Settings", company)
	username = setting_doc.username
	password = get_decrypted_password("Company NHIF Settings", company, "password")
	payload = 'grant_type=password&username={0}&password={1}'.format(username, password)
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	url = str(setting_doc.nhifservice_url) + "/nhifservice/token" 

	for i in range(3):
		try:
			r = requests.request("GET", url, headers = headers, data = payload, timeout = 5)
			r.raise_for_status()
			frappe.logger().debug({"webhook_success": r.text})
			if json.loads(r.text)["token_type"] == "bearer":
				token = json.loads(r.text)["access_token"]
				exoired = json.loads(r.text)["expires_in"]
				setting_doc.nhifservice_token = token
				setting_doc.db_update()
				console(token)
				console(exoired)
				return token
			else:
				frappe.throw(json.loads(r.text))
		except Exception as e:
			frappe.logger().debug({"webhook_error": e, "try": i + 1})
			sleep(3 * i + 1)
			if i != 2:
				continue
			else:
				raise e