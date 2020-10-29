frappe.ui.form.on('Patient Appointment', {
    setup: function (frm) {

    },

    onload: function (frm) {
        frm.trigger("mandatory_fields")
    },

    refresh: function (frm) {

    },
    insurance_subscription: function (frm) {
        frm.trigger("mandatory_fields")
        if (frm.doc.insurance_subscription) {
            frm.set_value("mode_of_payment", "")
            frm.trigger('get_paid_amount')
        } else {
            frm.set_value("insurance_company", "")
            frm.trigger('get_default_paid_amount')
        }
    },
    mode_of_payment: function (frm) {
        frm.trigger("mandatory_fields")
        if (frm.doc.mode_of_payment) {
            frm.set_value("insurance_subscription", "")
        }
    },
    mandatory_fields: function (frm) {
        if (frm.doc.insurance_subscription) {
            frm.toggle_reqd("mode_of_payment", false);
        }
        else {
            frm.toggle_reqd("mode_of_payment", true);
        }
        if (frm.doc.mode_of_payment) {
            frm.toggle_reqd("insurance_subscription", false);
        }
        else {
            frm.toggle_reqd("insurance_subscription", true);
        }
    },
    get_paid_amount: function (frm) {
        if (!frm.doc.insurance_subscription || !frm.doc.billing_item) {
            return
        }
        frappe.call({
            method: 'csf_tz.nhif.api.patient_appointment.get_paid_amount',
            args: {
                'insurance_subscription': frm.doc.insurance_subscription,
                'billing_item':frm.doc.billing_item,
                'company': frm.doc.company,
            },
            callback: function (data) {
                if (data.message) {
                    frm.set_value("paid_amount", data.message)
                }
            }
        });
    },
    get_default_paid_amount: function(frm) {
        if (frm.doc.practitioner) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Healthcare Practitioner',
                    name: frm.doc.practitioner
                },
                callback: function (data) {
                    frappe.model.set_value(frm.doctype, frm.docname, 'paid_amount', data.message.op_consulting_charge);
                }
            });
        }
    },
})
