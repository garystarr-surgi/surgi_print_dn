# Surgi Print Quick Reference

## 🚀 Quick Start Commands

### Start Services
```bash
sudo systemctl start surgi-print-webhook
sudo systemctl start surgi-print-ngrok
```

### Stop Services
```bash
sudo systemctl stop surgi-print-webhook
sudo systemctl stop surgi-print-ngrok
```

### Restart Services
```bash
sudo systemctl restart surgi-print-webhook
sudo systemctl restart surgi-print-ngrok
```

### Check Status
```bash
sudo systemctl status surgi-print-webhook
sudo systemctl status surgi-print-ngrok
```

## 🔍 Monitoring Commands

### View Logs
```bash
# Webhook bridge logs
sudo journalctl -u surgi-print-webhook -f

# ngrok logs
sudo journalctl -u surgi-print-ngrok -f

# All logs
sudo journalctl -f
```

### Test Webhook
```bash
# Health check
curl https://your-ngrok-url.ngrok.io/health

# List printers
curl https://your-ngrok-url.ngrok.io/printers

# Test print
curl -X POST "https://your-ngrok-url.ngrok.io/print" \
  -H "Content-Type: application/json" \
  -d '{"printer_name": "Brother_HL-L3210CW_series", "job_name": "Test", "pdf_data": "dGVzdA=="}'
```

## 🔧 Maintenance Commands

### Update Webhook Bridge
```bash
cd /opt/surgi-print
git pull origin main
sudo systemctl restart surgi-print-webhook
```

### Check CUPS Status
```bash
sudo systemctl status cups
lpstat -p
```

### Check ngrok Status
```bash
ngrok version
ngrok config check
```

## 🚨 Troubleshooting

### Service Won't Start
```bash
# Check logs
sudo journalctl -u surgi-print-webhook -f

# Test manually
cd /opt/surgi-print
source webhook_env/bin/activate
python cups_webhook_bridge.py
```

### ngrok Issues
```bash
# Check ngrok status
sudo systemctl status surgi-print-ngrok

# Test manually
ngrok http 5000
```

### CUPS Issues
```bash
# Restart CUPS
sudo systemctl restart cups

# Check printer
lpstat -p | grep Brother
```

## 📁 File Locations

- **Webhook Bridge**: `/opt/surgi-print/cups_webhook_bridge.py`
- **Virtual Environment**: `/opt/surgi-print/webhook_env/`
- **Service Files**: `/etc/systemd/system/surgi-print-*.service`
- **Logs**: `sudo journalctl -u surgi-print-*`

## 🔗 Important URLs

- **ngrok Dashboard**: https://dashboard.ngrok.com/
- **Frappe Cloud**: https://your-site.frappe.cloud/
- **CUPS Web Interface**: http://localhost:631/

## ⚡ Emergency Commands

### Restart Everything
```bash
sudo systemctl restart surgi-print-webhook
sudo systemctl restart surgi-print-ngrok
sudo systemctl restart cups
```

### Check All Services
```bash
sudo systemctl status surgi-print-webhook surgi-print-ngrok cups
```

### View All Logs
```bash
sudo journalctl -u surgi-print-webhook -u surgi-print-ngrok -f
```
