# get_nhif_price_package

from __future__ import unicode_literals 
import frappe
from frappe import _
from csf_tz.nhif.api.token import get_claimsservice_token
import json
import requests
from frappe.utils.background_jobs import enqueue
from csf_tz.nhif.doctype.nhif_product.nhif_product import add_product
from csf_tz.nhif.doctype.nhif_scheme.nhif_scheme import add_scheme
from frappe.utils import now
from csf_tz.nhif.doctype.nhif_response_log.nhif_response_log import add_log
from csf_tz import console



@frappe.whitelist()
def enqueue_get_nhif_price_package(company):
    enqueue(method=get_nhif_price_package, queue='long', timeout=10000000, is_async=True, kwargs = company)
    frappe.msgprint(_("Start Getting NHIF Prices Packages"),alert=True)
    return


def get_nhif_price_package(kwargs):
    company = kwargs
    frappe.db.sql("DELETE FROM `tabNHIF Price Package` WHERE name != 'ABC'")
    frappe.db.sql("DELETE FROM `tabNHIF Excluded Services` WHERE name != 'ABC'")
    frappe.db.commit()
    token = get_claimsservice_token(company)
    claimsserver_url, facility_code = frappe.get_value("Company NHIF Settings", company, ["claimsserver_url", "facility_code"])
    headers = {
        "Authorization" : "Bearer " + token
    }
    url = str(claimsserver_url) + "/claimsserver/api/v1/Packages/GetPricePackageWithExcludedServices?FacilityCode=" + str(facility_code)
    r = requests.get(url, headers = headers, timeout=5)
    if r.status_code != 200:
        console("Erorr")
        add_log(
            request_type = "GetCardDetails", 
            request_url = url, 
            request_header = headers, 
        )
        frappe.throw(json.loads(r.text))
    else:
        if json.loads(r.text):
            log_name = add_log(
                request_type = "GetPricePackageWithExcludedServices", 
                request_url = url, 
                request_header = headers, 
                response_data = json.loads(r.text) 
            )
            time_stamp = now()
            data = json.loads(r.text)
            insert_data = []
            for item in data.get("PricePackage"):
                insert_data.append((
					frappe.generate_hash("", 20),
                    facility_code,
                    time_stamp,
                    log_name,
                    item.get("ItemCode"),
                    item.get("PriceCode"),
                    item.get("LevelPriceCode"),
                    item.get("OldItemCode"),
                    item.get("ItemTypeID"),
                    item.get("ItemName"),
                    item.get("Strength"),
                    item.get("Dosage"),
                    item.get("PackageID"),
                    item.get("SchemeID"),
                    item.get("FacilityLevelCode"),
                    item.get("UnitPrice"),
                    item.get("IsRestricted"),
                    item.get("MaximumQuantity"),
                    item.get("AvailableInLevels"),
                    item.get("PractitionerQualifications"),
                    item.get("IsActive"),
				))
            frappe.db.sql('''
				INSERT INTO `tabNHIF Price Package`
				(
					`name`, `facilitycode`, `time_stamp`, `log_name`, `itemcode`, `pricecode`,
					`levelpricecode`, `olditemcode`, `itemtypeid`, `itemname`, `strength`, 
                    `dosage`, `packageid`, `schemeid`, `facilitylevelcode`, `unitprice`, 
                    `isrestricted`, `maximumquantity`, `availableinlevels`, 
                    `practitionerqualifications`, `IsActive`
				)
				VALUES {}
			'''.format(', '.join(['%s'] * len(insert_data))), tuple(insert_data))
            frappe.db.commit()
            insert_data = []
            for item in data.get("ExcludedServices"):
                insert_data.append((
					frappe.generate_hash("", 20),
                    facility_code,
                    time_stamp,
                    log_name,
                    item.get("ItemCode"),
                    item.get("SchemeID"),
                    item.get("SchemeName"),
                    item.get("ExcludedForProducts"),
				))
            frappe.db.sql('''
				INSERT INTO `tabNHIF Excluded Services`
				(
					`name`, `facilitycode`, `time_stamp`, `log_name`, `itemcode`, `schemeid`,
                    `schemename`, `excludedforproducts`
				)
				VALUES {}
			'''.format(', '.join(['%s'] * len(insert_data))), tuple(insert_data))
            return data

