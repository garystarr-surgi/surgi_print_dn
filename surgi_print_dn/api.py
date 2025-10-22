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
        # Log the print request
        frappe.logger().info(f"Starting print job for Delivery Note '{doc_name}' to printer '{printer_name}' on server {server_ip}")
        
        # Check document exists
        if not frappe.db.exists(doctype, doc_name):
            frappe.throw(f"Delivery Note '{doc_name}' not found.")
        
        # Generate PDF
        frappe.logger().info(f"Generating PDF for Delivery Note '{doc_name}'")
        pdf_file = frappe.get_print(doctype, doc_name, as_pdf=True)

        # Ensure pdf_file is in bytes (frappe.get_print returns bytes for PDF)
        if isinstance(pdf_file, str):
            # If it's a string, it might be base64 encoded or file path
            if pdf_file.startswith('data:'):
                # Handle data URL format
                import base64
                pdf_file = base64.b64decode(pdf_file.split(',')[1])
            else:
                # Assume it's a file path
                with open(pdf_file, 'rb') as f:
                    pdf_file = f.read()
        elif not isinstance(pdf_file, bytes):
            # Convert to bytes if it's neither string nor bytes
            pdf_file = bytes(pdf_file)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
           tmp.write(pdf_file)  # Ensure pdf_file is in bytes
           temp_file_path = tmp.name

        # Connect to CUPS
        frappe.logger().info(f"Connecting to CUPS server at {server_ip}:{server_port}")
        conn = cups.Connection(host=server_ip, port=server_port)
        
        # Get available printers
        printers = conn.getPrinters()
        frappe.logger().info(f"Available printers on CUPS server: {list(printers.keys())}")
        
        if printer_name not in printers:
            frappe.throw(f"Printer '{printer_name}' not found on CUPS server at {server_ip}. Available printers: {', '.join(printers.keys())}")

        # Send print job
        frappe.logger().info(f"Sending print job to printer '{printer_name}'")
        job_id = conn.printFile(printer_name, temp_file_path, f"{doctype}: {doc_name}", {})
        
        frappe.logger().info(f"Print job submitted successfully. Job ID: {job_id}")
        return f"Delivery Note {doc_name} sent to printer {printer_name} (Job ID: {job_id})"

    except cups.IPPError as e:
        error_msg = f"CUPS server error: {e}"
        frappe.logger().error(f"CUPS IPP Error: {error_msg}")
        frappe.throw(error_msg)
    except ConnectionError as e:
        error_msg = f"Cannot connect to CUPS server at {server_ip}:{server_port}: {e}"
        frappe.logger().error(f"CUPS Connection Error: {error_msg}")
        frappe.throw(error_msg)
    except FileNotFoundError as e:
        error_msg = f"PDF file not found: {e}"
        frappe.logger().error(f"File Error: {error_msg}")
        frappe.throw(error_msg)
    except Exception as e:
        error_msg = f"Printing Delivery Note failed: {e}"
        frappe.logger().error(f"CUPS Delivery Note Print Error: {frappe.get_traceback()}")
        frappe.throw(error_msg)

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
