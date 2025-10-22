#!/bin/bash
# Setup script for Surgi Print services

echo "Setting up Surgi Print systemd services..."

# Get current directory
CURRENT_DIR=$(pwd)
echo "Current directory: $CURRENT_DIR"

# Update service files with actual paths
sed -i "s|/home/gary/surgi_print_webhook|$CURRENT_DIR|g" surgi-print-webhook.service
sed -i "s|/home/gary/surgi_print_webhook|$CURRENT_DIR|g" surgi-print-ngrok.service

# Copy service files to systemd directory
sudo cp surgi-print-webhook.service /etc/systemd/system/
sudo cp surgi-print-ngrok.service /etc/systemd/system/

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
