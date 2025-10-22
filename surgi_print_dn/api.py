import frappe
import cups
import os
import tempfile
import requests
import base64

@frappe.whitelist()
def send_dn_print_to_cups(doc_name, printer_name):
    """
    Generates a PDF of the specified Delivery Note and sends it to a CUPS printer.
    """
    doctype = "Delivery Note"
    server_ip = "47.206.233.222"  # CUPS server IP
    server_port = 443  # Try HTTPS port 443
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

        # Try multiple ports for Frappe Cloud compatibility
        ports_to_try = [443, 80, 631]  # HTTPS, HTTP, IPP
        conn = None
        job_id = None
        
        for port in ports_to_try:
            try:
                frappe.logger().info(f"Trying CUPS connection on port {port}")
                conn = cups.Connection(host=server_ip, port=port)
                
                # Get available printers
                printers = conn.getPrinters()
                frappe.logger().info(f"Available printers on CUPS server: {list(printers.keys())}")
                
                if printer_name not in printers:
                    frappe.throw(f"Printer '{printer_name}' not found on CUPS server at {server_ip}. Available printers: {', '.join(printers.keys())}")

                # Send print job
                frappe.logger().info(f"Sending print job to printer '{printer_name}' via port {port}")
                job_id = conn.printFile(printer_name, temp_file_path, f"{doctype}: {doc_name}", {})
                frappe.logger().info(f"Successfully connected via port {port}")
                break
                
            except Exception as cups_error:
                frappe.logger().warning(f"CUPS connection failed on port {port}: {cups_error}")
                if port == ports_to_try[-1]:  # Last port failed
                    # Try HTTP fallback
                    frappe.logger().info("All CUPS ports failed, attempting HTTP-based print fallback...")
                    job_id = send_via_http_print(server_ip, 80, printer_name, temp_file_path, f"{doctype}: {doc_name}")
                continue
        
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


def send_via_http_print(server_ip, server_port, printer_name, file_path, job_name):
    """
    Fallback method to send print job via HTTP when IPP fails.
    """
    try:
        # Read the PDF file
        with open(file_path, 'rb') as f:
            pdf_data = f.read()
        
        # Try both HTTP and HTTPS
        protocols = ['https', 'http'] if server_port == 443 else ['http', 'https']
        
        for protocol in protocols:
            try:
                # Encode to base64
                pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
                
                # Prepare the print job data
                print_data = {
                    'printer_name': printer_name,
                    'job_name': job_name,
                    'file_data': pdf_base64
                }
                
                # Send via HTTP/HTTPS POST to CUPS web interface
                url = f"{protocol}://{server_ip}:{server_port}/printers/{printer_name}"
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Frappe-Surgi-Print/1.0'
                }
                
                frappe.logger().info(f"Trying {protocol.upper()} print via {url}")
                response = requests.post(url, data=print_data, headers=headers, timeout=30, verify=False)
                
                if response.status_code == 200:
                    frappe.logger().info(f"{protocol.upper()} print job submitted successfully via {url}")
                    return f"{protocol.upper()}-{response.status_code}"
                else:
                    frappe.logger().warning(f"{protocol.upper()} print failed with status {response.status_code}: {response.text}")
                    
            except Exception as protocol_error:
                frappe.logger().warning(f"{protocol.upper()} print attempt failed: {protocol_error}")
                continue
        
        # If all protocols failed
        frappe.throw("All HTTP/HTTPS print attempts failed")
            
    except Exception as e:
        frappe.logger().error(f"HTTP print fallback failed: {e}")
        frappe.throw(f"HTTP print fallback failed: {e}")


# Backup method with old name for compatibility
@frappe.whitelist()
def send_delivery_note_print_to_cups(doc_name, printer_name):
    """
    Legacy method name for backward compatibility.
    Calls the main send_dn_print_to_cups function.
    """
    return send_dn_print_to_cups(doc_name, printer_name)
