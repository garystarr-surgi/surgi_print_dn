// Client Script attached to the DocType: Delivery Note
console.log("SURGI PRINT SCRIPT LOADING!");

frappe.ui.form.on('Delivery Note', {
    refresh(frm) {
                
        // 1. FIX: Unconditionally remove the button to handle cancelled (docstatus 2) and duplicates.
        frm.remove_custom_button(BUTTON_LABEL); 

        // 2. Conditionally add the button back only for valid statuses.
        if (frm.doc.docstatus === 0 || frm.doc.docstatus === 1) {
            
             // 1. Prevent Duplicates (best practice for 'refresh')
            frm.remove_custom_button('Print to Warehouse');

            // 2. Add the Custom Button
            frm.add_custom_button(__('Print to Warehouse'), () => {
            
            console.log("Docstatus is: " + frm.doc.docstatus + ". Adding button now.");
            
                      
                const target_printer = 'Brother 3210';
                const doc_name = frm.doc.name;
                
                frappe.call({
                    method: 'surgi_print.api.send_delivery_note_to_cups',
                    args: {
                        doc_name: doc_name,
                        printer_name: target_printer
                    },
                    
                    freeze: true,
                    freeze_message: "Generating PDF and connecting to CUPS server...",
                    
                    callback: (r) => {
                        // Ensure UI is unfrozen after the server call completes
                        frappe.unfreeze(); 

                        if (r.message) {
                            frappe.show_alert({
                                message: r.message,
                                indicator: 'green'
                            }, 5);
                        } else if (r.exc) {
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
