app_name = "surgi_print_app"
app_title = "Surgi Print App"
app_publisher = "Your Name"
app_description = "CUPS Printing Integration for Delivery Notes"
app_version = "0.0.1"
app_license = "mit"

# Client Script Hook (Optional, but good practice for external scripts)
# This isn't needed if the script is managed via the UI, but it's part of the standard template.
# doc_events = {
# 	"Delivery Note": {
# 		"refresh": "surgi_print_app.client_scripts.delivery_note.refresh"
# 	}
# }

# Custom Whitelisted Python Modules
# The `api.py` file contains whitelisted functions and must be included here
apis = {
    "surgi_print_app.api": "surgi_print_app.api"
}

# Python Requirements
# You must list 'pycups' as a requirement since your code uses it
# Note: pycups is typically named 'cups' when imported but 'pycups' for installation.
required_apps = []
install_requires = [
    "pycups" 
]
