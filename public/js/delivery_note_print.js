// Client Script for Delivery Note
frappe.ui.form.on('Delivery Note', {
    refresh: function(frm) {
        // Show button only on Draft (0) or Submitted (1)
        if (frm.doc.docstatus === 0 || frm.doc.docstatus === 1) {
            
            // Prevent duplicate buttons
            frm.remove_custom_button('Print to Warehouse');

            // Add custom button
            frm.add_custom_button(__('Print to Warehouse'), function() {
                const target_printer = 'Brother 3210';
                const doc_name = frm.doc.name;

                frappe.call({
                    method: 'surgi_print.api.send_delivery_note_print_to_cups',
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
                        frappe.msgprint({
                            title: __('Print Failed'),
                            message: 'An error occurred during printing. Check server logs.',
                            indicator: 'red'
                        });
                        console.error("CUPS Print Error Traceback:", err);
                    }
                });
            }).addClass('btn-primary');
        }
    }
});
