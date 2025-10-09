app_name = "surgi_print_dn"
app_title = "Surgi Print DN"
app_publisher = "Gary Starr"
app_description = "CUPS Printing Integration for Delivery Notes"
app_version = "0.0.5"
app_license = "MIT"

# Load JS only for Delivery Note
doctype_js = {
    "Delivery Note": "public/js/dn_print.js"
}

# Optional: list Python dependencies
install_requires = [
    
]

# Optional: other Frappe apps required
# required_apps = ["erpnext"]
