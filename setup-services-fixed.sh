#!/bin/bash
# Setup script for Surgi Print services - FIXED VERSION

echo "Setting up Surgi Print systemd services..."

# Get current directory
CURRENT_DIR=$(pwd)
echo "Current directory: $CURRENT_DIR"

# Check if files exist
if [ ! -f "cups_webhook_bridge.py" ]; then
    echo "Error: cups_webhook_bridge.py not found in current directory"
    exit 1
fi

if [ ! -d "webhook_env" ]; then
    echo "Error: webhook_env virtual environment not found"
    echo "Please create it first with: python3 -m venv webhook_env"
    exit 1
fi

# Create webhook service file
cat > /tmp/surgi-print-webhook.service << EOF
[Unit]
Description=Surgi Print Webhook Bridge
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/webhook_env/bin/python $CURRENT_DIR/cups_webhook_bridge.py
Restart=always
RestartSec=10
Environment=PATH=$CURRENT_DIR/webhook_env/bin

[Install]
WantedBy=multi-user.target
EOF

# Create ngrok service file
cat > /tmp/surgi-print-ngrok.service << EOF
[Unit]
Description=Surgi Print ngrok Tunnel
After=network.target surgi-print-webhook.service
Requires=surgi-print-webhook.service

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$CURRENT_DIR
ExecStart=/usr/local/bin/ngrok http 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Copy service files to systemd directory
sudo cp /tmp/surgi-print-webhook.service /etc/systemd/system/
sudo cp /tmp/surgi-print-ngrok.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable surgi-print-webhook
sudo systemctl enable surgi-print-ngrok

echo "Services installed and enabled!"
echo ""
echo "To start services:"
echo "  sudo systemctl start surgi-print-webhook"
echo "  sudo systemctl start surgi-print-ngrok"
echo ""
echo "To check status:"
echo "  sudo systemctl status surgi-print-webhook"
echo "  sudo systemctl status surgi-print-ngrok"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u surgi-print-webhook -f"
echo "  sudo journalctl -u surgi-print-ngrok -f"
