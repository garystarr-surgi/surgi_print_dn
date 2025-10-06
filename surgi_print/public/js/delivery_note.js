// Client Script attached to the DocType: Delivery Note
console.log("SURGI PRINT SCRIPT LOADING!");

frappe.ui.form.on('Delivery Note', {
    refresh(frm) {
        // --- 1. Define Constants for Consistency and Fix Reference Error ---
        const BUTTON_LABEL = __('Print to Warehouse');
        const PRINTER_NAME = 'Brother 3210';
        const METHOD_PATH = 'surgi_print.api.send_delivery_note_to_cups';

        // --- 2. Unconditionally remove the button to handle all statuses and duplicates ---
        // This addresses both of the previous remove calls and the undefined variable error.
        frm.remove_custom_button(BUTTON_LABEL); 

        // 3. Conditionally add the button back only for Draft (0) or Submitted (1) statuses.
        if (frm.doc.docstatus === 0 || frm.doc.docstatus === 1) {
            
            console.log("Docstatus is: " + frm.doc.docstatus + ". Adding button now.");

            // 4. Add the Custom Button
            frm.add_custom_button(BUTTON_LABEL, () => {
                
                // --- Prepare Arguments ---
                const doc_name = frm.doc.name;
                
                frappe.call({
                    method: METHOD_PATH,
                    args: {
                        doc_name: doc_name,
                        printer_name: PRINTER_NAME
                    },
                    
                    freeze: true,
                    freeze_message: "Generating PDF and connecting to CUPS server...",
                    
                    callback: (r) => {
                        // Ensure UI is unfrozen after the server call completes
                        frappe.unfreeze(); 

                        if (r.message === true) {
                            // If Python returns 'True', show a successful alert.
                            // The Python function already used frappe.msgprint for success, 
                            // so this is often redundant but safe for a final confirmation.
                            frappe.show_alert({
                                message: `Print job for ${doc_name} sent successfully!`,
                                indicator: 'green'
                            }, 5);
                        } else if (r.exc) {
                            // Handle exceptions raised by frappe.throw in Python
                            frappe.msgprint({
                                title: __('Print Failed'),
                                message: 'The print job failed. Please check the CUPS server connectivity and Frappe error logs.',
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
