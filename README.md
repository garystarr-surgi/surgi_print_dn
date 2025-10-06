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
