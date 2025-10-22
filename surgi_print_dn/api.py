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
    # Webhook bridge URL (you'll need to set this up)
    webhook_url = "https://your-ngrok-url.ngrok.io/print"  # Replace with your ngrok URL
    temp_file_path = None

    try:
        # Log the print request
        frappe.logger().info(f"Starting webhook print job for Delivery Note '{doc_name}' to printer '{printer_name}'")
        
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
        
        # Encode PDF to base64 for webhook
        pdf_base64 = base64.b64encode(pdf_file).decode('utf-8')
        
        # Send to webhook bridge
        frappe.logger().info(f"Sending print job via webhook to {webhook_url}")
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


# Backup method with old name for compatibility
@frappe.whitelist()
def send_delivery_note_print_to_cups(doc_name, printer_name):
    """
    Legacy method name for backward compatibility.
    Calls the main send_dn_print_to_cups function.
    """
    return send_dn_print_to_cups(doc_name, printer_name)
