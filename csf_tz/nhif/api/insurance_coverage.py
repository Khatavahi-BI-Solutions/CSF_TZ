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
            for item in data.get("PricePackage"):
                doc_pack = frappe.new_doc("NHIF Price Package")
                doc_pack.facilitycode = facility_code
                doc_pack.time_stamp = time_stamp
                doc_pack.log_name = log_name
                doc_pack.itemcode = item.get("ItemCode")
                doc_pack.pricecode = item.get("PriceCode")
                doc_pack.levelpricecode = item.get("LevelPriceCode")
                doc_pack.olditemcode = item.get("OldItemCode")
                doc_pack.itemtypeid = item.get("ItemTypeID")
                doc_pack.itemname = item.get("ItemName")
                doc_pack.strength = item.get("Strength")
                doc_pack.dosage = item.get("Dosage")
                doc_pack.packageid = item.get("PackageID")
                doc_pack.schemeid = item.get("SchemeID")
                doc_pack.facilitylevelcode = item.get("FacilityLevelCode")
                doc_pack.unitprice = item.get("UnitPrice")
                doc_pack.isrestricted = item.get("IsRestricted")
                doc_pack.maximumquantity = item.get("MaximumQuantity")
                doc_pack.availableinlevels = item.get("AvailableInLevels")
                doc_pack.practitionerqualifications = item.get("PractitionerQualifications")
                doc_pack.isactive = item.get("IsActive")
                doc_pack.save(ignore_permissions=True)
                console(doc_pack.name ,item.get("PriceCode"),item.get("ItemCode"), item.get("ItemName"))
            frappe.db.commit()
            for item in data.get("ExcludedServices"):
                console(item.get("PriceCode"),item.get("SchemeID"), item.get("SchemeName"))
                doc_exc = frappe.new_doc("NHIF Excluded Services")
                doc_exc.facilitycode = facility_code
                doc_exc.time_stamp = time_stamp
                doc_exc.log_name = log_name
                doc_exc.itemcode = item.get("ItemCode")
                doc_exc.schemeid = item.get("SchemeID")
                doc_exc.schemename = item.get("SchemeName")
                doc_exc.excludedforproducts = item.get("ExcludedForProducts")
                doc_exc.save(ignore_permissions=True)
                console(item.get(doc_exc.name ,"PriceCode"),item.get("SchemeID"), item.get("SchemeName"))
            frappe.db.commit()
            return data

