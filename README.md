# Surgi Print App

A custom Frappe application designed to integrate Delivery Note printing with a remote CUPS (Common Unix Printing System) server.

## Features

-   Generates a PDF of a specific Delivery Note.
-   Sends the PDF to a designated printer on a remote CUPS server using the PyCUPS library.
-   Custom button on the Delivery Note form to trigger the print job.

## Installation

1.  Add the app to your Frappe Bench:
    ```bash
    bench get-app [https://github.com/yourusername/surgi_print_app.git](https://github.com/yourusername/surgi_print_app.git)
    ```
2.  Install the app on your site:
    ```bash
    bench --site your-site-name install-app surgi_print_app
    ```
3.  Ensure the underlying host environment has the CUPS client libraries installed, typically required by `pycups`.

## Configuration

### Server Details

The CUPS server IP and port are **hardcoded** in `surgi_print_app/api.py`. You must modify this file or update the logic to fetch these values from a custom Frappe DocType/Settings.

### Client Script

The Client Script is attached to the **Delivery Note** DocType and triggers the print job with the hardcoded printer name: `'Brother 3210'`.

## Requirements

This app requires the `pycups` Python library, which is specified in `surgi_print_app.txt` and `hooks.py`.
