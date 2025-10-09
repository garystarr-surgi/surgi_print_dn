import frappe
import cups
import os
import tempfile

@frappe.whitelist()
def send_dn_print_to_cups(doc_name, printer_name):
    """
    Generates a PDF of the specified Delivery Note and sends it to a CUPS printer.
    """
    doctype = "Delivery Note"
    server_ip = "47.206.233.1"  # CUPS server IP
    server_port = 631
    temp_file_path = None

    try:
        # Check document exists
        if not frappe.db.exists(doctype, doc_name):
            frappe.throw(f"Delivery Note '{doc_name}' not found.")
        
        # Generate PDF
        pdf_file = frappe.get_print(doctype, doc_name, as_pdf=True)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_file)
            temp_file_path = tmp.name

        # Connect to CUPS
        conn = cups.Connection(host=server_ip)  # remote server connection
        
        printers = conn.getPrinters()
        if printer_name not in printers:
            frappe.throw(f"Printer '{printer_name}' not found on CUPS server at {server_ip}.")

        # Send print job
        conn.printFile(printer_name, temp_file_path, f"{doctype}: {doc_name}", {})

        # Return a message for client-side
        return f"Delivery Note {doc_name} sent to printer {printer_name}"

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CUPS Delivery Note Print Error")
        frappe.throw(f"Printing Delivery Note failed (Check server {server_ip}): {e}")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
