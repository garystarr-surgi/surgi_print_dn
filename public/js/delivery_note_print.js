frappe.ui.form.on('Delivery Note', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 0 || frm.doc.docstatus === 1) {
            
            frm.remove_custom_button('Print to Warehouse');

            frm.add_custom_button(__('Print to Warehouse'), function() {
                
                const target_printer = 'Brother 3210';
                const doc_name = frm.doc.name;
                
frappe.call({
    method: 'surgi_print.api.send_delivery_note_print_to_cups',
    args: {
        doc_name: frm.doc.name,
        printer_name: target_printer
    },
    freeze: true,
    freeze_message: "Generating PDF and connecting to CUPS server...",
    callback: function(r) {
        // r.message contains server return
        if (r.message) {
            frappe.show_alert({ message: r.message, indicator: 'green' }, 5);
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
