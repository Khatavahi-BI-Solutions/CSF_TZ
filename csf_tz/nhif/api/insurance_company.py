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
            frappe.db.commit()
            process_prices_list(company)
            return data


def process_prices_list(company):
    facility_code = frappe.get_value("Company NHIF Settings", company, "facility_code")
    currency = frappe.get_value("Company", company, "default_currency")
    schemeid_list = frappe.db.sql(
        '''
            SELECT schemeid from `tabNHIF Price Package`
            WHERE facilitycode = {0}
            GROUP BY schemeid
        '''.format(facility_code), 
        as_dict=1
    )

    for scheme in schemeid_list:
        price_list_name = "NHIF-" + scheme.schemeid
        if not frappe.db.exists("Price List", price_list_name):
            price_list_doc = frappe.new_doc("Price List")
            price_list_doc.price_list_name = price_list_name
            price_list_doc.currency = currency
            price_list_doc.buying = 0
            price_list_doc.selling = 1
            price_list_doc.save(ignore_permissions=True)
 
    item_list = frappe.db.sql(
        '''
            SELECT ref_code, parent as item_code from `tabItem Customer Detail`
            WHERE customer_name = 'NHIF'
            GROUP by ref_code , parent
        ''', 
        as_dict=1
    )

    for item in item_list:
        for scheme in schemeid_list:
            schemeid = scheme.schemeid 
            price_list_name = "NHIF-" + schemeid
            package_list = frappe.db.sql(
                '''
                    SELECT schemeid, itemcode, unitprice, count(*) 
                    FROM `tabNHIF Price Package` 
                    WHERE facilitycode = {0} and schemeid = {1} and itemcode = {2}
                    GROUP by itemcode , schemeid
                    HAVING count(*) = 1
                '''.format(facility_code,schemeid,item.ref_code), 
                as_dict=1
            )
            if len(package_list) > 0:
                for package in package_list:
                    item_price_list = frappe.get_all("Item Price", 
                        filters={
                            "price_list" : price_list_name,
                            "item_code" : item.item_code,
                            "currency": currency,
                            "selling": 1
                        },
                        fields = ["name","price_list_rate"]
                    )
                    if len(item_price_list) > 0:
                        for price in item_price_list:
                            if price.price_list_rate != float(package.unitprice):
                                frappe.set_value("Item Price", price.name, "price_list_name", float(package.unitprice))
                    else:
                        item_price_doc = frappe.new_doc("Item Price")
                        item_price_doc.item_code = item.item_code
                        item_price_doc.price_list = price_list_name
                        item_price_doc.currency = currency
                        item_price_doc.price_list_rate = float(package.unitprice)
                        item_price_doc.buying = 0
                        item_price_doc.selling = 1
                        item_price_doc.save(ignore_permissions=True)



  
