app_name = "surgi_print"
app_title = "Surgi Print App"
app_publisher = "Gary Starr"
app_description = "CUPS Printing Integration for Delivery Notes"
app_version = "0.0.1"
app_license = "mit"

# Register the surgi_print.js file to be loaded across the entire Frappe Desk.
# The path uses the app name: /assets/{app_name}/js/{filename}.js
app_include_js = "/assets/surgi_print/js/surgi_print.js"

# **DOCYPE-SPECIFIC JAVASCRIPT HOOK (ADDED)**
# -------------------------------------------
# Tells Frappe to load 'public/js/delivery_note.js' only when the Delivery Note form is opened.
doctype_js = {
	"Delivery Note": "public/js/delivery_note.js"

# Client Script Hook (Optional, but good practice for external scripts)
# This isn't needed if the script is managed via the UI, but it's part of the standard template.
# doc_events = {
# 	"Delivery Note": {
# 		"refresh": "surgi_print.client_scripts.delivery_note.refresh"
# 	}
# }

# Custom Whitelisted Python Modules
# The `api.py` file contains whitelisted functions and must be included here
apis = {
    "surgi_print.api": "surgi_print.api"
}

# Python Requirements
# You must list 'pycups' as a requirement since your code uses it
# Note: pycups is typically named 'cups' when imported but 'pycups' for installation.
required_apps = []
install_requires = [
    "pycups" 
]
