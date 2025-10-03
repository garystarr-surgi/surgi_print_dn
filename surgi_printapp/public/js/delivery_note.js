// Client Script attached to the DocType: Delivery Note
frappe.ui.form.on('Delivery Note', {
    refresh(frm) {
        // Only show the button on Draft (0) or Submitted (1) documents
        if (frm.doc.docstatus === 0 || frm.doc.docstatus === 1) {
            
            frm.remove_custom_button('Print to Warehouse'); // Prevents duplicates

            frm.add_custom_button(__('Print to Warehouse'), () => {
                
                const target_printer = 'Brother 3210'; // Matches the client script's printer name
                
                frappe.call({
                    // The method path is app_name.module_name.function_name
                    method: 'surgi_print_app.api.send_delivery_note_to_cups', 
                    
                    args: {
                        // The server function only accepts 'printer_name'
                        printer_name: target_printer
                    },
                    callback: (r) => {
                        if (r.message === true) {
                            // Success message is already handled in the Python script's frappe.msgprint
                        } else if (r.exc) {
                            // If the Python script failed (e.g., CUPS connection error, printer not found)
                            // The error is already raised via frappe.throw in Python
                            console.error("CUPS Print Error Traceback:", r.exc);
                        }
                    },
                    freeze: true,
                    freeze_message: "Generating PDF and connecting to CUPS server..."
                });
            }).addClass('btn-primary');
        } else {
            // Remove the button if the document is not in a printable status
            frm.remove_custom_button('Print to Warehouse');
        }
    }
});
