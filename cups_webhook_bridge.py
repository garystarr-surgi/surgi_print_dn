#!/usr/bin/env python3
"""
CUPS Webhook Bridge Service
Bridges Frappe Cloud to local CUPS server
"""
from flask import Flask, request, jsonify
import cups
import tempfile
import base64
import os
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# CUPS Configuration
CUPS_SERVER = "localhost"  # Local CUPS server
CUPS_PORT = 631
DEFAULT_PRINTER = "Brother 3210"

def print_pdf(pdf_data, printer_name, job_name):
    """Print PDF to local CUPS printer"""
    try:
        # Connect to local CUPS
        conn = cups.Connection(host=CUPS_SERVER, port=CUPS_PORT)
        
        # Check if printer exists
        printers = conn.getPrinters()
        if printer_name not in printers:
            raise Exception(f"Printer '{printer_name}' not found. Available: {list(printers.keys())}")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_data)
            temp_file_path = tmp.name
        
        # Print the file
        job_id = conn.printFile(printer_name, temp_file_path, job_name, {})
        
        # Clean up
        os.unlink(temp_file_path)
        
        return job_id
        
    except Exception as e:
        logging.error(f"Print error: {e}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/print', methods=['POST'])
def print_webhook():
    """Webhook endpoint for printing"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'pdf_data' not in data:
            return jsonify({"error": "Missing pdf_data"}), 400
        
        # Extract data
        pdf_base64 = data['pdf_data']
        printer_name = data.get('printer_name', DEFAULT_PRINTER)
        job_name = data.get('job_name', f"Webhook Print {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Decode PDF
        pdf_data = base64.b64decode(pdf_base64)
        
        # Print
        job_id = print_pdf(pdf_data, printer_name, job_name)
        
        return jsonify({
            "success": True,
            "job_id": job_id,
            "printer": printer_name,
            "message": f"Print job submitted successfully"
        })
        
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/printers', methods=['GET'])
def list_printers():
    """List available printers"""
    try:
        conn = cups.Connection(host=CUPS_SERVER, port=CUPS_PORT)
        printers = conn.getPrinters()
        return jsonify({"printers": list(printers.keys())})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting CUPS Webhook Bridge...")
    print(f"Default printer: {DEFAULT_PRINTER}")
    print("Endpoints:")
    print("  GET  /health - Health check")
    print("  POST /print - Print PDF")
    print("  GET  /printers - List printers")
    print("\nTo expose via ngrok: ngrok http 5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
