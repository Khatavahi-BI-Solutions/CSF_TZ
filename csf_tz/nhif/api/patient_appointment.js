frappe.ui.form.on('Patient Appointment', {
    setup: function (frm) {

    },

    onload: function (frm) {
        frm.trigger("mandatory_fields")
        frm.add_custom_button(__('get authorization num'), function () {
            frm.trigger('get_authorization_num')
        });
    },

    refresh: function (frm) {
        if (!frm.doc.invoiced && frm.doc.patient && frm.doc.mode_of_payment && !frm.doc.insurance_subscription) {
            frm.add_custom_button(__('Creat Sales Invoice'), function () {
                if (frm.is_dirty()) {
                    frm.save();
                }
                frappe.call({
                    method: 'csf_tz.nhif.api.patient_appointment.invoice_appointment',
                    args: {
                        'name': frm.doc.name
                    },
                    callback: function (data) {
                        if (data.message) {
                            frm.reload_doc()
                        }
                    }
                });
            });
        }
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
            frm.trigger('get_default_paid_amount')
        }
    },
    practitioner: function (frm) {
        frm.trigger("get_consulting_charge_item")
    },
    mandatory_fields: function (frm) {
        frm.trigger("get_consulting_charge_item")
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
                'billing_item': frm.doc.billing_item,
                'company': frm.doc.company,
            },
            callback: function (data) {
                if (data.message) {
                    frm.set_value("paid_amount", data.message)
                }
            }
        });
    },
    get_default_paid_amount: function (frm) {
        if (frm.doc.practitioner && !frm.doc.insurance_subscription) {
            frappe.call({
                method: 'csf_tz.nhif.api.patient_appointment.get_consulting_charge_amount',
                args: {
                    'appointment_type': frm.doc.appointment_type,
                    'practitioner': frm.doc.practitioner,
                },
                callback: function (data) {
                    if (data.message) {
                        frm.set_value("paid_amount", data.message);
                    }

                }
            });
        }
    },
    get_consulting_charge_item: function (frm) {
        if (!frm.doc.practitioner) {
            return
        }
        frappe.call({
            method: 'csf_tz.nhif.api.patient_appointment.get_consulting_charge_item',
            args: {
                'appointment_type': frm.doc.appointment_type,
                'practitioner': frm.doc.practitioner,
            },
            callback: function (data) {
                if (data.message) {
                    frm.set_value("billing_item", data.message)
                }
            }
        });
    },
    patient: function (frm) {
        if (frm.doc.patient) {
            setTimeout(() => {
                frm.toggle_display('mode_of_payment', 1);
                frm.toggle_display('paid_amount', 1);
            }, 100)
        }
    },
    get_authorization_num: function(frm) {
        frappe.call({
            method: 'csf_tz.nhif.api.patient_appointment.get_authorization_num',
            args: {
                'patient': frm.doc.patient,
                'company': frm.doc.company,
                'appointment_type': frm.doc.appointment_type,
                'referral_no': frm.doc.referral_no,
            },
            callback: function (data) {
                if (data.message) {
                    frm.set_value("authorization_number", data.message)
                }
            }
        });
    },
})
