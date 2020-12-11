# get_nhif_price_package

from __future__ import unicode_literals 
import frappe
from frappe import _
from csf_tz.nhif.api.token import get_claimsservice_token
from erpnext import get_company_currency, get_default_company
import json
import requests
from frappe.utils.background_jobs import enqueue
from csf_tz.nhif.doctype.nhif_product.nhif_product import add_product
from csf_tz.nhif.doctype.nhif_scheme.nhif_scheme import add_scheme
from frappe.utils import now
from csf_tz.nhif.doctype.nhif_response_log.nhif_response_log import add_log
from csf_tz import console



@frappe.whitelist()
def enqueue_get_nhif_price_package():
    enqueue(method=get_nhif_price_package, queue='long', timeout=10000000, is_async=True)
    frappe.msgprint(_("Start Getting NHIF Prices Packages"),alert=True)
    return


def get_nhif_price_package():
    company = get_default_company() ## TODO: need to be fixed to support pultiple company
    token = get_claimsservice_token(company)
    nhifservice_url, facility_code = frappe.get_value("Company NHIF Settings", company, ["nhifservice_url", "facility_code"])
    headers = {
        "Authorization" : "Bearer " + token
    }
    url = str(nhifservice_url) + "/claimsserver/api/v1/Packages/GetPricePackageWithExcludedServices?FacilityCode=" + str(facility_code)
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
            for item in data.get("PricePackage"):
                console(item.get("PriceCode"),item.get("ItemCode"), item.get("ItemName"))
                doc = frappe.new_doc("NHIF Price Package")
                doc.facilitycode = facility_code
                doc.time_stamp = time_stamp
                doc.log_name = log_name
                doc.itemcode = item.get("ItemCode")
                doc.pricecode = item.get("PriceCode")
                doc.levelpricecode = item.get("LevelPriceCode")
                doc.olditemcode = item.get("OldItemCode")
                doc.itemtypeid = item.get("ItemTypeID")
                doc.itemname = item.get("ItemName")
                doc.strength = item.get("Strength")
                doc.dosage = item.get("Dosage")
                doc.packageid = item.get("PackageID")
                doc.schemeid = item.get("SchemeID")
                doc.facilitylevelcode = item.get("FacilityLevelCode")
                doc.unitprice = item.get("UnitPrice")
                doc.isrestricted = item.get("IsRestricted")
                doc.maximumquantity = item.get("MaximumQuantity")
                doc.availableinlevels = item.get("AvailableInLevels")
                doc.practitionerqualifications = item.get("PractitionerQualifications")
                doc.isactive = item.get("IsActive")
                doc.save(ignore_permissions=True)
            frappe.db.commit()
            for item in data.get("ExcludedServices"):
                console(item.get("PriceCode"),item.get("SchemeID"), item.get("SchemeName"))
                doc = frappe.new_doc("NHIF Price Package")
                doc.facilitycode = facility_code
                doc.time_stamp = time_stamp
                doc.log_name = log_name
                doc.itemcode = item.get("ItemCode")
                doc.schemeid = item.get("SchemeID")
                doc.schemename = item.get("SchemeName")
                doc.excludedforproducts = item.get("ExcludedForProducts")
                doc.save(ignore_permissions=True)
            frappe.db.commit()
            return data

