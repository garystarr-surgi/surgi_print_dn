# Manual Setup for Systemd Services

## Step 1: Create Webhook Service

```bash
sudo nano /etc/systemd/system/surgi-print-webhook.service
```

Add this content (replace `/path/to/your/directory` with your actual path):

```ini
[Unit]
Description=Surgi Print Webhook Bridge
After=network.target

[Service]
Type=simple
User=gary
WorkingDirectory=/path/to/your/directory
ExecStart=/path/to/your/directory/webhook_env/bin/python /path/to/your/directory/cups_webhook_bridge.py
Restart=always
RestartSec=10
Environment=PATH=/path/to/your/directory/webhook_env/bin

[Install]
WantedBy=multi-user.target
```

## Step 2: Create ngrok Service

```bash
sudo nano /etc/systemd/system/surgi-print-ngrok.service
```

Add this content (replace `/path/to/your/directory` with your actual path):

```ini
[Unit]
Description=Surgi Print ngrok Tunnel
After=network.target surgi-print-webhook.service
Requires=surgi-print-webhook.service

[Service]
Type=simple
User=gary
WorkingDirectory=/path/to/your/directory
ExecStart=/usr/local/bin/ngrok http 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Step 3: Enable and Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable surgi-print-webhook
sudo systemctl enable surgi-print-ngrok

# Start services
sudo systemctl start surgi-print-webhook
sudo systemctl start surgi-print-ngrok
```

## Step 4: Check Status

```bash
# Check status
sudo systemctl status surgi-print-webhook
sudo systemctl status surgi-print-ngrok

# View logs
sudo journalctl -u surgi-print-webhook -f
sudo journalctl -u surgi-print-ngrok -f
```

## Troubleshooting

If services fail to start:
1. Check the logs: `sudo journalctl -u surgi-print-webhook -f`
2. Verify paths are correct in the service files
3. Make sure the virtual environment exists
4. Test manually: `python cups_webhook_bridge.py`
