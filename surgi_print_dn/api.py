import frappe
import cups
import os
import tempfile
import requests
import base64

@frappe.whitelist()
def print_delivery_note_via_webhook(doc_name, printer_name):
    """
    Generates a PDF of the specified Delivery Note and sends it to a CUPS printer.
    """
    doctype = "Delivery Note"
    # Webhook bridge URL (you'll need to set this up)
    webhook_url = "https://suzanna-multiplicative-francina.ngrok-free.dev/print"  # Replace with your ngrok URL
    temp_file_path = None

    try:
        # Log the print request
        frappe.logger().info(f"Starting webhook print job for Delivery Note '{doc_name}' to printer '{printer_name}'")
        
        # Check document exists
        if not frappe.db.exists(doctype, doc_name):
            frappe.throw(f"Delivery Note '{doc_name}' not found.")
        
        # Generate PDF
        frappe.logger().info(f"Generating PDF for Delivery Note '{doc_name}'")
        try:
            pdf_file = frappe.get_print(doctype, doc_name, as_pdf=True)
            frappe.logger().info(f"PDF generated successfully, type: {type(pdf_file)}")
        except Exception as pdf_error:
            frappe.logger().error(f"PDF generation failed: {pdf_error}")
            frappe.throw(f"PDF generation failed: {pdf_error}")

        # Ensure pdf_file is in bytes (frappe.get_print returns bytes for PDF)
        if isinstance(pdf_file, str):
            # If it's a string, it might be base64 encoded or file path
            if pdf_file.startswith('data:'):
                # Handle data URL format
                pdf_file = base64.b64decode(pdf_file.split(',')[1])
            else:
                # Assume it's a file path
                with open(pdf_file, 'rb') as f:
                    pdf_file = f.read()
        elif not isinstance(pdf_file, bytes):
            # Convert to bytes if it's neither string nor bytes
            pdf_file = bytes(pdf_file)
        
        # Encode PDF to base64 for webhook
        try:
            frappe.logger().info(f"Encoding PDF to base64, PDF type: {type(pdf_file)}, size: {len(pdf_file) if hasattr(pdf_file, '__len__') else 'unknown'}")
            pdf_base64 = base64.b64encode(pdf_file).decode('utf-8')
            frappe.logger().info(f"PDF encoded successfully, base64 length: {len(pdf_base64)}")
        except Exception as encode_error:
            frappe.logger().error(f"PDF encoding failed: {encode_error}")
            frappe.throw(f"PDF encoding failed: {encode_error}")
        
        # Send to webhook bridge
        frappe.logger().info(f"Sending print job via webhook to {webhook_url}")
        frappe.logger().info(f"PDF size: {len(pdf_base64)} characters")
        frappe.logger().info(f"Printer: {printer_name}")
        job_id = send_via_webhook(webhook_url, printer_name, pdf_base64, f"{doctype}: {doc_name}")
        
        frappe.logger().info(f"Webhook print job submitted successfully. Job ID: {job_id}")
        return f"Delivery Note {doc_name} sent to printer {printer_name} via webhook (Job ID: {job_id})"

    except Exception as e:
        error_msg = f"Webhook printing failed: {e}"
        frappe.logger().error(f"Webhook Print Error: {frappe.get_traceback()}")
        frappe.throw(error_msg)


def send_via_webhook(webhook_url, printer_name, pdf_base64, job_name):
    """
    Send print job via webhook bridge to local CUPS server.
    """
    try:
        # Prepare the webhook payload
        payload = {
            'printer_name': printer_name,
            'job_name': job_name,
            'pdf_data': pdf_base64
        }
        
        # Send to webhook
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Frappe-Surgi-Print/1.0'
        }
        
        frappe.logger().info(f"Sending webhook request to {webhook_url}")
        response = requests.post(webhook_url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                frappe.logger().info(f"Webhook print successful: {result.get('message')}")
                return result.get('job_id', 'webhook-success')
            else:
                frappe.throw(f"Webhook print failed: {result.get('error', 'Unknown error')}")
        else:
            frappe.throw(f"Webhook request failed with status {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        frappe.logger().error(f"Webhook request failed: {e}")
        frappe.throw(f"Webhook request failed: {e}")
    except Exception as e:
        frappe.logger().error(f"Webhook print failed: {e}")
        frappe.throw(f"Webhook print failed: {e}")


# Test method to verify app is updated
@frappe.whitelist()
def test_webhook_connection():
    """
    Test method to verify the app is updated and webhook is accessible.
    """
    try:
        import requests
        response = requests.post("https://suzanna-multiplicative-francina.ngrok-free.dev/print", 
                                json={"printer_name": "Brother_HL-L3210CW_series", "job_name": "Test", "pdf_data": "dGVzdA=="},
                                timeout=10)
        return {
            "success": True,
            "status_code": response.status_code,
            "response": response.json()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist()
def print_delivery_note_with_watermark(doc_name, printer_name, print_format=None):
    """
    Generates a PDF of the specified Delivery Note with temperature critical watermark
    and sends it to a CUPS printer.
    """
    doctype = "Delivery Note"
    webhook_url = "https://suzanna-multiplicative-francina.ngrok-free.dev/print"
    
    try:
        frappe.logger().info(f"Starting watermarked print job for Delivery Note '{doc_name}' to printer '{printer_name}'")
        
        # Check document exists
        if not frappe.db.exists(doctype, doc_name):
            frappe.throw(f"Delivery Note '{doc_name}' not found.")
        
        # Check if any items have temperature_critical = 1
        doc = frappe.get_doc(doctype, doc_name)
        has_critical_items = any(item.get('temperature_critical') == 1 for item in doc.items)
        
        # Use custom print format if critical items found
        if has_critical_items and print_format:
            frappe.logger().info(f"Using custom print format '{print_format}' for critical items")
            pdf_file = frappe.get_print(doctype, doc_name, print_format=print_format, as_pdf=True)
        else:
            pdf_file = frappe.get_print(doctype, doc_name, as_pdf=True)
        
        # Convert to bytes if needed
        if isinstance(pdf_file, str):
            if pdf_file.startswith('data:'):
                pdf_file = base64.b64decode(pdf_file.split(',')[1])
            else:
                with open(pdf_file, 'rb') as f:
                    pdf_file = f.read()
        elif not isinstance(pdf_file, bytes):
            pdf_file = bytes(pdf_file)
        
        # Encode PDF to base64
        pdf_base64 = base64.b64encode(pdf_file).decode('utf-8')
        
        # Send to webhook bridge
        job_id = send_via_webhook(webhook_url, printer_name, pdf_base64, f"{doctype}: {doc_name}")
        
        watermark_status = "with temperature critical watermark" if has_critical_items else "standard"
        frappe.logger().info(f"Webhook print job submitted successfully. Job ID: {job_id}")
        return f"Delivery Note {doc_name} sent to printer {printer_name} {watermark_status} (Job ID: {job_id})"

    except Exception as e:
        error_msg = f"Watermarked printing failed: {e}"
        frappe.logger().error(f"Watermarked Print Error: {frappe.get_traceback()}")
        frappe.throw(error_msg)


@frappe.whitelist()
def print_document_via_webhook(doctype, doc_name, printer_name, print_format=None):
    """
    Generic function to print any document type via webhook to CUPS printer.
    Can be used for Delivery Note, Packing Slip, or any other document.
    """
    webhook_url = "https://suzanna-multiplicative-francina.ngrok-free.dev/print"
    
    try:
        frappe.logger().info(f"Starting webhook print job for {doctype} '{doc_name}' to printer '{printer_name}'")
        
        # Check document exists
        if not frappe.db.exists(doctype, doc_name):
            frappe.throw(f"{doctype} '{doc_name}' not found.")
        
        # Generate PDF
        if print_format:
            frappe.logger().info(f"Using print format '{print_format}' for {doctype}")
            pdf_file = frappe.get_print(doctype, doc_name, print_format=print_format, as_pdf=True)
        else:
            pdf_file = frappe.get_print(doctype, doc_name, as_pdf=True)
        
        # Convert to bytes if needed
        if isinstance(pdf_file, str):
            if pdf_file.startswith('data:'):
                pdf_file = base64.b64decode(pdf_file.split(',')[1])
            else:
                with open(pdf_file, 'rb') as f:
                    pdf_file = f.read()
        elif not isinstance(pdf_file, bytes):
            pdf_file = bytes(pdf_file)
        
        # Encode PDF to base64
        pdf_base64 = base64.b64encode(pdf_file).decode('utf-8')
        
        # Send to webhook bridge
        job_id = send_via_webhook(webhook_url, printer_name, pdf_base64, f"{doctype}: {doc_name}")
        
        frappe.logger().info(f"Webhook print job submitted successfully. Job ID: {job_id}")
        return f"{doctype} {doc_name} sent to printer {printer_name} via webhook (Job ID: {job_id})"

    except Exception as e:
        error_msg = f"Webhook printing failed for {doctype}: {e}"
        frappe.logger().error(f"Print Error: {frappe.get_traceback()}")
        frappe.throw(error_msg)


@frappe.whitelist()
def print_packing_slip_via_webhook(doc_name, printer_name, print_format=None):
    """
    Generates a PDF of the specified Packing Slip and sends it to a CUPS printer.
    """
    return print_document_via_webhook("Packing Slip", doc_name, printer_name, print_format)


# Backup method with old name for compatibility
@frappe.whitelist()
def send_delivery_note_print_to_cups(doc_name, printer_name):
    """
    Legacy method name for backward compatibility.
    Calls the main send_dn_print_to_cups function.
    """
    return send_dn_print_to_cups(doc_name, printer_name)
