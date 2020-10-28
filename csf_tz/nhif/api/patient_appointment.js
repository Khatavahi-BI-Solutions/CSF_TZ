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
            frm.set_value("mode_of_payment","")
        } else {
            frm.set_value("insurance_company","")
        }
    },
    mode_of_payment: function (frm) {
        frm.trigger("mandatory_fields")
        if (frm.doc.mode_of_payment) {
            frm.set_value("insurance_subscription","")
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
    }
})
