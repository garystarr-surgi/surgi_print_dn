# CUPS Webhook Bridge Setup Guide

This guide shows how to set up a webhook bridge to connect Frappe Cloud to your local CUPS server.

## Architecture

```
Frappe Cloud → Webhook Bridge (ngrok) → Local CUPS Server → Printer
```

## Step 1: Install Webhook Bridge

1. **Install Python dependencies** on your local machine:
   ```bash
   pip install -r webhook_requirements.txt
   ```

2. **Run the webhook bridge**:
   ```bash
   python cups_webhook_bridge.py
   ```

3. **Test locally**:
   ```bash
   curl http://localhost:5000/health
   curl http://localhost:5000/printers
   ```

## Step 2: Expose via ngrok

1. **Install ngrok**: https://ngrok.com/download

2. **Expose the webhook**:
   ```bash
   ngrok http 5000
   ```

3. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

## Step 3: Update Frappe App

1. **Edit `surgi_print_dn/api.py`**:
   ```python
   webhook_url = "https://your-ngrok-url.ngrok.io/print"
   ```

2. **Update the app on Frappe Cloud**

## Step 4: Test

1. **Test the webhook**:
   ```bash
   curl -X POST https://your-ngrok-url.ngrok.io/print \
     -H "Content-Type: application/json" \
     -d '{
       "printer_name": "Brother 3210",
       "job_name": "Test Print",
       "pdf_data": "base64-encoded-pdf-data"
     }'
   ```

2. **Test from Frappe Cloud** - click the "Print to Warehouse" button

## Alternative: Email-to-Print

If webhook is too complex, use email-to-print:

1. **Set up email-to-print service** (like PaperCut)
2. **Configure Frappe to send PDFs via email**
3. **Email service prints to local printer**

## Security Notes

- **Use HTTPS** (ngrok provides this)
- **Add authentication** to webhook if needed
- **Consider VPN** for production use
- **Monitor webhook logs** for security

## Troubleshooting

- **Check webhook logs**: `python cups_webhook_bridge.py`
- **Test CUPS locally**: `lpstat -p`
- **Check ngrok status**: https://dashboard.ngrok.com
- **Verify printer**: `lpstat -p | grep Brother`
