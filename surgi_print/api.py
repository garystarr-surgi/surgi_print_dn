import frappe
import cups
import os

@frappe.whitelist()
def send_delivery_note_to_cups(printer_name): # Removed 'name' as a function argument
    """
    Sends a print job of a Delivery Note to the specified CUPS server.
    """
    doctype = "Delivery Note"
    # *** EDIT: Hardcoded the document name as requested ***
    name = "Surgi Delivery Note"
    
    # NOTE: These IP/Port values are specific to the script's logic and must be reachable
    # from the Frappe Cloud server instance.
    server_ip = "47.206.233.1" 
    server_port = 631
    temp_file_path = None 

    try:
        if not frappe.db.exists(doctype, name):
             frappe.throw(f"Delivery Note '{name}' not found.")
             
        # 1. Generate PDF of the Delivery Note
        # frappe.get_print is used instead of frappe.get_pdf
        pdf_file = frappe.get_print(doctype, name, as_pdf=True)
        
        # Save PDF to a temporary file
        temp_dir = frappe.get_site_path("private", "tmp", "print_jobs")
        frappe.create_folder(temp_dir)
        temp_file_path = os.path.join(temp_dir, f"{doctype}_{name}.pdf")
        
        with open(temp_file_path, "wb") as f:
            f.write(pdf_file)

        # 2. Connect to the CUPS server
        # *** FIXES: Setting the remote server configuration ***
        cups.setServer(server_ip)
        cups.setPort(server_port)
        conn = cups.Connection()
        
        # Check if the printer exists
        printers = conn.getPrinters()
        if printer_name not in printers:
            frappe.throw(f"Printer '{printer_name}' not found on CUPS server at {server_ip}.")
            
        # 3. Send the print job
        # Uses the hardcoded 'name' variable
        conn.printFile(printer_name, temp_file_path, f"{doctype}: {name}", {})
        
        frappe.msgprint(f"Print job sent for {name} to printer: {printer_name}")
        return True
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CUPS Delivery Note Print Error")
        # Propagate a user-friendly error message
        frappe.throw(f"Printing Delivery Note failed (Check server {server_ip}): {e}")
    finally:
        # Clean up the temporary file
        if temp_file_path and os.path.exists(temp_file_path): 
            os.remove(temp_file_path)
