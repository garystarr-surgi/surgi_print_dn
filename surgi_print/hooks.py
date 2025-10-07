app_name = "surgi_print"
app_title = "surgi_print"
app_publisher = "Gary Starr"
app_description = "CUPS Printing Integration for Delivery Notes"
app_version = "0.0.5"
app_license = "MIT"

# Load JS only for Delivery Note
doctype_js = {
    "Delivery Note": "public/js/delivery_note_print.js"
}

# Optional: list Python dependencies
install_requires = [
    "pycups"
]

# Optional: other Frappe apps required
# required_apps = ["erpnext"]
