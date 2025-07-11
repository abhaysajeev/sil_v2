import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_customer_addresses(customer):
    try:
        if not customer:
            frappe.throw("Customer is required.")

        addresses = frappe.db.sql("""
            SELECT 
                a.name,
                a.city AS city_or_town, 
                CONCAT_WS(', ', a.address_line1, a.address_line2) AS full_address,
                a.is_primary_address
            FROM 
                `tabAddress` a
            JOIN 
                `tabDynamic Link` dl ON dl.parent = a.name
            WHERE 
                dl.link_doctype = 'Customer' AND dl.link_name = %s
            ORDER BY 
                a.is_primary_address DESC
        """, (customer,), as_dict=True)

        return addresses

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_customer_addresses Error")
        frappe.throw(f"An error occurred while fetching addresses: {e}")


@frappe.whitelist(allow_guest=True)
def get_item_details_from_serial_no(serial_no):
    try:
        if not serial_no:
            frappe.throw("Serial No is required.")

        item_details = frappe.db.sql("""
            SELECT
                name,              
                customer, 
                item,
                custom_item_classification,                         
                custom_item_name
            FROM 
                `tabItem Family Serial No List` 
            WHERE 
                name = %s
        """, (serial_no,), as_dict=True)

        if item_details:
            cust = item_details[0].get("customer")
            address = get_customer_addresses(cust)

            combined = {**item_details[0], **address[0]}
            return combined
        else:
            return "Item Details not found for this Serial No"

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_item_details_from_serial_no function Error")
        frappe.throw(f"An error occurred while fetching Item Details: {e}")
