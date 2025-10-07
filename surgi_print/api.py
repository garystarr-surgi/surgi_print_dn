import frappe
import cups
import os
# Import for better temporary file handling
import tempfile 

@frappe.whitelist()
def send_delivery_note_print_to_cups(docname):
    doc = frappe.get_doc("Delivery Note", docname)
    # Example placeholder
    frappe.msgprint(f"Sending {docname} to CUPS printer")
    """
    Generates a PDF of the specified Delivery Note and sends it to a CUPS printer.
    """
    doctype = "Delivery Note"
    
    # NOTE: These IP/Port values should ideally be fetched from a Frappe Setting DocType
    server_ip = "47.206.233.1"  
    server_port = 631
    temp_file_path = None # Will store the path of the secure temporary file

    try:
        # Check if the document exists
        if not frappe.db.exists(doctype, doc_name):
            frappe.throw(f"Delivery Note '{doc_name}' not found.")
            
        # 1. Generate PDF of the Delivery Note
        pdf_file = frappe.get_print(doctype, doc_name, as_pdf=True)
        
        # *** CORRECTION 2: Use Python's built-in secure tempfile handling ***
        # Create a named temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_file)
            temp_file_path = tmp.name # Save the path for CUPS and cleanup

        # 2. Connect to the CUPS server
        cups.setServer(server_ip)
        cups.setPort(server_port)
        conn = cups.Connection()
        
        # Check if the printer exists
        printers = conn.getPrinters()
        if printer_name not in printers:
            frappe.throw(f"Printer '{printer_name}' not found on CUPS server at {server_ip}.")
            
        # 3. Send the print job
        conn.printFile(printer_name, temp_file_path, f"{doctype}: {doc_name}", {})
        
        frappe.msgprint(f"Print job sent for {doc_name} to printer: {printer_name}")
        return True
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CUPS Delivery Note Print Error")
        # Propagate a user-friendly error message
        frappe.throw(f"Printing Delivery Note failed (Check server {server_ip}): {e}")
    finally:
        # 4. Clean up the temporary file
        if temp_file_path and os.path.exists(temp_file_path): 
            os.remove(temp_file_path)
