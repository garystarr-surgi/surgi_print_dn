# Surgi Print Production Setup Guide

Complete step-by-step instructions for setting up the Surgi Print webhook bridge and ngrok tunnel on a production server.

## 📋 Prerequisites

- Ubuntu/Debian server (or similar Linux distribution)
- Root or sudo access
- CUPS server running locally
- Printer configured in CUPS
- Internet connection

## 🚀 Step 1: Server Preparation

### 1.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Install Required Packages
```bash
sudo apt install -y python3 python3-pip python3-venv git wget curl cups-client
```

### 1.3 Install ngrok
```bash
# Download ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz

# Extract and install
tar -xzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
sudo chmod +x /usr/local/bin/ngrok

# Verify installation
ngrok version
```

## 🔧 Step 2: Setup Webhook Bridge

### 2.1 Create Application Directory
```bash
# Create directory for the application
sudo mkdir -p /opt/surgi-print
sudo chown $USER:$USER /opt/surgi-print
cd /opt/surgi-print
```

### 2.2 Clone Repository
```bash
git clone https://github.com/garystarr-surgi/surgi_print_dn.git .
```

### 2.3 Create Virtual Environment
```bash
python3 -m venv webhook_env
source webhook_env/bin/activate
```

### 2.4 Install Dependencies
```bash
sudo apt install libcups2-dev
pip install Flask==2.3.3 pycups==2.0.1 requests==2.31.0
```

### 2.5 Download Webhook Bridge
```bash
# Download the webhook bridge
wget https://raw.githubusercontent.com/garystarr-surgi/surgi_print_dn/main/cups_webhook_bridge.py

# Make it executable
chmod +x cups_webhook_bridge.py
```

### 2.6 Test Webhook Bridge
```bash
# Test the webhook bridge
python3 cups_webhook_bridge.py
```

You should see:
```
Starting CUPS Webhook Bridge...
Default printer: Brother_HL-L3210CW_series
Endpoints:
  GET  /health - Health check
  POST /print - Print PDF
  GET  /printers - List printers

To expose via ngrok: ngrok http 5000
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

## 🌐 Step 3: Setup ngrok Tunnel

### 3.1 Create ngrok Account
1. Go to https://ngrok.com/
2. Sign up for a free account
3. Get your authtoken from the dashboard

### 3.2 Configure ngrok
```bash
# Add your authtoken
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### 3.3 Test ngrok
```bash
# In one terminal, start webhook bridge
python cups_webhook_bridge.py

# In another terminal, start ngrok
ngrok http 5000
```

You should see:
```
Session Status                online
Account                       your-account
Version                       3.x.x
Region                        United States (us)
Forwarding                    https://abc123.ngrok.io -> http://localhost:5000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

## 🔧 Step 4: Configure Frappe App

### 4.1 Update Webhook URL
```bash
# Edit the API file
nano surgi_print_dn/api.py

# Find this line and update with your ngrok URL:
webhook_url = "https://your-ngrok-url.ngrok.io/print"
```

### 4.2 Commit and Push Changes
```bash
git add surgi_print_dn/api.py
git commit -m "Update webhook URL for production"
git push origin main
```

### 4.3 Update Frappe Cloud App
1. Go to your Frappe Cloud site
2. Navigate to: **Settings → Apps**
3. Find **"surgi_print_dn"** and click **"Update from GitHub"**

## 🚀 Step 5: Setup Systemd Services

### 5.1 Download Setup Script
```bash
wget https://raw.githubusercontent.com/garystarr-surgi/surgi_print_dn/main/setup-services-fixed.sh
chmod +x setup-services-fixed.sh
```

### 5.2 Run Setup Script
```bash
./setup-services-fixed.sh
```

### 5.3 Start Services
```bash
sudo systemctl start surgi-print-webhook
sudo systemctl start surgi-print-ngrok
```

### 5.4 Check Status
```bash
sudo systemctl status surgi-print-webhook
sudo systemctl status surgi-print-ngrok
```

## 🧪 Step 6: Testing

### 6.1 Test Webhook Health
```bash
curl https://your-ngrok-url.ngrok.io/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2024-01-01T12:00:00.000000"}
```

### 6.2 Test Printer List
```bash
curl https://your-ngrok-url.ngrok.io/printers
```

Expected response:
```json
{"printers": ["Brother_HL-L3210CW_series"]}
```

### 6.3 Test Print Job
```bash
curl -X POST "https://your-ngrok-url.ngrok.io/print" \
  -H "Content-Type: application/json" \
  -d '{"printer_name": "Brother_HL-L3210CW_series", "job_name": "Test Print", "pdf_data": "dGVzdA=="}'
```

Expected response:
```json
{"success": true, "job_id": 1, "printer": "Brother_HL-L3210CW_series", "message": "Print job submitted successfully"}
```

### 6.4 Test Frappe Cloud Integration
1. Go to your Frappe Cloud site
2. Navigate to a Delivery Note
3. Click **"Print to Warehouse"** button
4. Check webhook bridge logs: `sudo journalctl -u surgi-print-webhook -f`

## 🔍 Step 7: Monitoring and Maintenance

### 7.1 View Logs
```bash
# Webhook bridge logs
sudo journalctl -u surgi-print-webhook -f

# ngrok logs
sudo journalctl -u surgi-print-ngrok -f

# System logs
sudo journalctl -f
```

### 7.2 Service Management
```bash
# Restart services
sudo systemctl restart surgi-print-webhook
sudo systemctl restart surgi-print-ngrok

# Stop services
sudo systemctl stop surgi-print-webhook
sudo systemctl stop surgi-print-ngrok

# Check status
sudo systemctl status surgi-print-webhook
sudo systemctl status surgi-print-ngrok
```

### 7.3 Update Webhook Bridge
```bash
cd /opt/surgi-print
git pull origin main
sudo systemctl restart surgi-print-webhook
```

## 🔒 Step 8: Security Considerations

### 8.1 Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 631   # CUPS (if needed)
sudo ufw enable
```

### 8.2 ngrok Security
- Use ngrok's authentication features
- Consider upgrading to paid plan for better security
- Monitor ngrok dashboard for unauthorized access

### 8.3 Webhook Security
- The webhook is currently open to anyone with the URL
- Consider adding authentication if needed
- Monitor webhook logs for suspicious activity

## 🚨 Troubleshooting

### Common Issues

#### Webhook Bridge Won't Start
```bash
# Check logs
sudo journalctl -u surgi-print-webhook -f

# Test manually
cd /opt/surgi-print
source webhook_env/bin/activate
python cups_webhook_bridge.py
```

#### ngrok Won't Start
```bash
# Check logs
sudo journalctl -u surgi-print-ngrok -f

# Test manually
ngrok http 5000
```

#### CUPS Printer Not Found
```bash
# Check CUPS status
sudo systemctl status cups

# List printers
lpstat -p

# Check CUPS web interface
# Open browser: http://localhost:631
```

#### Frappe Cloud Can't Connect
1. Check ngrok status: `sudo systemctl status surgi-print-ngrok`
2. Test webhook URL: `curl https://your-ngrok-url.ngrok.io/health`
3. Check Frappe Cloud logs
4. Verify webhook URL in app code

### Log Locations
- **Webhook logs**: `sudo journalctl -u surgi-print-webhook -f`
- **ngrok logs**: `sudo journalctl -u surgi-print-ngrok -f`
- **System logs**: `sudo journalctl -f`
- **CUPS logs**: `/var/log/cups/`

## 📞 Support

If you encounter issues:
1. Check the logs first
2. Test each component individually
3. Verify all URLs and paths are correct
4. Check that all services are running

## 🎯 Production Checklist

- [ ] Server updated and secured
- [ ] CUPS server running with printer configured
- [ ] Webhook bridge installed and tested
- [ ] ngrok tunnel configured and running
- [ ] Systemd services installed and enabled
- [ ] Frappe app updated with correct webhook URL
- [ ] All tests passing
- [ ] Monitoring and logging configured
- [ ] Backup procedures in place

## 🚀 Quick Start Commands

```bash
# Start everything
sudo systemctl start surgi-print-webhook
sudo systemctl start surgi-print-ngrok

# Check status
sudo systemctl status surgi-print-webhook surgi-print-ngrok

# View logs
sudo journalctl -u surgi-print-webhook -f

# Test webhook
curl https://your-ngrok-url.ngrok.io/health
```

---

**Congratulations! Your Surgi Print production setup is complete!** 🎉
