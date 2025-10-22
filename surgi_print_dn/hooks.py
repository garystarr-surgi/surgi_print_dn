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

# App configuration
app_include_css = []
app_include_js = []

# Python dependencies
install_requires = [
    "pycups>=2.0.1",
    "requests"
]

# Required Frappe apps
required_apps = ["erpnext"]

# App configuration
app_config = {
    "cups_server_ip": "47.206.233.1",
    "cups_server_port": 631,
    "default_printer": "Brother 3210"
}
