// Client Script attached to the DocType: Delivery Note
// File: public/js/delivery_note.js

frappe.ui.form.on('Delivery Note', {
    // The 'refresh' event runs every time the form loads or is saved/submitted/cancelled.
    refresh(frm) {
        const BUTTON_LABEL = __('Print to Warehouse');
        
        // 1. Remove the button unconditionally to prevent duplicates on subsequent refreshes.
        frm.remove_custom_button(BUTTON_LABEL);

        // 2. Determine button visibility: Show only on Draft (0) or Submitted (1).
        if (frm.doc.docstatus === 0 || frm.doc.docstatus === 1) {
            
            frm.add_custom_button(BUTTON_LABEL, () => {
                
                // Define constant values for the current action
                const target_printer = 'Brother 3210';
                const doc_name = frm.doc.name;
                
                frappe.call({
                    // Ensure this path matches your app and whitelisted method
                    method: 'surgi_print.api.send_delivery_note_to_cups',
                    
                    args: {
                        // Pass the document name and printer name
                        doc_name: doc_name,
                        printer_name: target_printer
                    },
                    
                    // Options for the frappe.call
                    freeze: true,
                    freeze_message: "Generating PDF and connecting to CUPS server...",
                    
                    callback: (r) => {
                        // Unfreeze UI regardless of success/failure
                        frappe.unfreeze(); 

                        if (r.message) {
                            // r.message is often a string on success, not just true/false
                            // If server returns a success message string:
                            frappe.show_alert({
                                message: r.message,
                                indicator: 'green'
                            }, 5);
                        } else if (r.exc) {
                            // Handle explicit server-side exceptions (like connection errors)
                            frappe.msgprint({
                                title: __('Print Failed'),
                                message: 'An error occurred during printing. Check server logs.',
                                indicator: 'red'
                            });
                            console.error("CUPS Print Error Traceback:", r.exc);
                        }
                    }
                });
            }).addClass('btn-primary');
        }
    }
});
