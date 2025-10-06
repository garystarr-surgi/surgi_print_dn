// Client Script attached to the DocType: Delivery Note
frappe.ui.form.on('Delivery Note', {
    refresh(frm) {
        // CORRECTION 1: Always remove the button first to prevent duplicates
        frm.remove_custom_button('Print to Warehouse'); 

        // Only show the button on Draft (0) or Submitted (1) documents
        if (frm.doc.docstatus === 0 || frm.doc.docstatus === 1) {
            
            frm.add_custom_button(__('Print to Warehouse'), () => {
                
                const target_printer = 'Brother 3210'; 
                
                frappe.call({
                    method: 'surgi_print.api.send_delivery_note_to_cups',
                    
                    args: {
                        // *** CRITICAL CORRECTION: Pass the current document's name ***
                        doc_name: frm.doc.name, 
                        printer_name: target_printer
                    },
                    callback: (r) => {
                        if (r.message === true) {
                            // Success message handled by frappe.msgprint on server
                        } else if (r.exc) {
                            console.error("CUPS Print Error Traceback:", r.exc);
                        }
                    },
                    freeze: true,
                    freeze_message: "Generating PDF and connecting to CUPS server..."
                });
            }).addClass('btn-primary');
        } 
        // No 'else' needed; button is already removed at the start of refresh.
    }
});
