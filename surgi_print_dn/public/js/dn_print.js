// Client Script for Delivery Note
frappe.ui.form.on('Delivery Note', {
    refresh: function(frm) {
        // Show button only on Draft (0) or Submitted (1)
        if (frm.doc.docstatus === 0 || frm.doc.docstatus === 1) {
            
            // Check if the button already exists before removing it
            if (frm.custom_buttons && frm.custom_buttons['Print to Warehouse']) {
                frm.remove_custom_button('Print to Warehouse');
            }

            // Add custom button
            frm.add_custom_button(__('Print to Warehouse'), function() {
                const target_printer = 'Brother 3210';
                const doc_name = frm.doc.name;

                // Validate document name
                if (!doc_name) {
                    frappe.msgprint({
                        title: __('Invalid Document'),
                        message: 'Please save the document before printing.',
                        indicator: 'red'
                    });
                    return;
                }

                frappe.call({
                    method: 'surgi_print_dn.api.send_dn_print_to_cups',
                    args: {
                        doc_name: doc_name,
                        printer_name: target_printer
                    },
                    freeze: true,  // show loading overlay automatically
                    freeze_message: "Generating PDF and sending to CUPS printer...",
                    callback: function(r) {
                        // r.message contains the server return value
                        if (r.message) {
                            frappe.show_alert({
                                message: r.message,
                                indicator: 'green'
                            }, 5);
                        }
                    },
                    error: function(err) {
                        let error_message = 'An error occurred during printing. Check server logs.';
                        
                        // Try to extract more specific error message
                        if (err && err.exc && err.exc.length > 0) {
                            try {
                                const error_data = JSON.parse(err.exc[0]);
                                if (error_data.message) {
                                    error_message = error_data.message;
                                }
                            } catch (e) {
                                // If parsing fails, use the original error message
                                console.warn("Could not parse error message:", e);
                            }
                        }
                        
                        frappe.msgprint({
                            title: __('Print Failed'),
                            message: error_message,
                            indicator: 'red'
                        });
                        console.error("CUPS Print Error:", err);
                    }
                });
            }).addClass('btn-primary');
        }
    }
});
