frappe.ui.form.on('Patient Appointment', {
    setup: function (frm) {
    },
    onload: function (frm) {
        frm.trigger("mandatory_fields")
    },
    refresh: function (frm) {
        frm.trigger("update_primary_action")
        if (!frm.doc.invoiced && frm.doc.patient && frm.doc.mode_of_payment && !frm.doc.insurance_subscription) {
            frm.add_custom_button(__('Create Sales Invoice'), function () {
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
        frm.trigger("mandatory_fields")
    },
    insurance_subscription: function (frm) {
        frm.trigger("mandatory_fields")
        frm.trigger("update_primary_action")
        if (frm.doc.insurance_subscription) {
            frm.set_value("mode_of_payment", "")
            frm.trigger('get_insurance_amount')
        } else {
            frm.set_value("insurance_company", "")
            frm.trigger('get_mop_amount')
        }
    },
    mode_of_payment: function (frm) {
        frm.trigger("mandatory_fields")
        frm.trigger("update_primary_action")
        if (frm.doc.mode_of_payment) {
            frm.set_value("insurance_subscription", "")
            frm.trigger('get_mop_amount')
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
        if (frm.doc.invoiced && frm.doc.mode_of_payment) {
            frm.set_value(["insurance_subscription","insurance_company"], "")
            frm.toggle_display('insurance_section', false);
            frm.toggle_enable(['referral_no', 'source', 'mode_of_payment', 'paid_amount'], false)
        }
        if (frm.doc.insurance_claim) {
            frm.set_value(["mode_of_payment", "paid_amount"], "")
            frm.toggle_display('section_break_16', false);
            frm.toggle_enable(['referral_no', 'source', 'insurance_subscription'], false)
        }
    },
    get_insurance_amount: function (frm) {
        if (!frm.doc.insurance_subscription || !frm.doc.billing_item) {
            return
        }
        frappe.call({
            method: 'csf_tz.nhif.api.patient_appointment.get_insurance_amount',
            args: {
                'insurance_subscription': frm.doc.insurance_subscription,
                'billing_item': frm.doc.billing_item,
                'company': frm.doc.company,
                'patient': frm.doc.patient,
                'insurance_company': frm.doc.insurance_company,
            },
            callback: function (data) {
                if (data.message) {
                    frm.set_value("paid_amount", data.message)
                }
            }
        });
    },
    get_mop_amount: function (frm) {
        if (frm.doc.practitioner && !frm.doc.insurance_subscription) {
            frappe.call({
                method: 'csf_tz.nhif.api.patient_appointment.get_mop_amount',
                args: {
                    'billing_item': frm.doc.billing_item,
                    'mop': frm.doc.mode_of_payment,
                    'company': frm.doc.company,
                    'patient': frm.doc.patient,
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
                frm.toggle_display('mode_of_payment', true);
                frm.toggle_display('paid_amount', true);
            }, 100)
        }
    },
    get_authorization_number: function(frm) {
        frm.trigger("get_authorization_num")
    },
    get_authorization_num: function(frm) {
        if (!frm.doc.insurance_subscription) {
            frappe.msgprint("Select Insurance Subscription to get authorization number")
            return
        }
        frappe.call({
            method: 'csf_tz.nhif.api.patient_appointment.get_authorization_num',
            args: {
                'insurance_subscription': frm.doc.insurance_subscription,
                'company': frm.doc.company,
                'appointment_type': frm.doc.appointment_type,
                'referral_no': frm.doc.referral_no
            },
            callback: function (data) {
                if (data.message) {
                    const card = data.message;
                        if (card.Remarks == 'Verified OK') {
                            frm.set_value("authorization_number", card.AuthorizationNo)
                            frappe.show_alert({
                                message:__("Authorization Number is updated"),
                                indicator:'green'
                            }, 5);
                        } else {
                            frm.set_value("insurance_subscription", "")
                        }
                    }
            }
        });
    },
    invoiced: function(frm) {
        frm.trigger("mandatory_fields")
    },
    insurance_claim: function(frm) {
        frm.trigger("mandatory_fields")
    },
    update_primary_action: function(frm) {
        if (frm.is_new()) {
            if (!frm.doc.mode_of_payment && !frm.doc.insurance_subscription) {
                frm.page.set_primary_action(__('Panding'), () => {
                    frappe.show_alert({
                        message:__("Please select Insurance Subscription or Mode of Payment"),
                        indicator:'red'
                        }, 15);
                });
            }
            else {
                frm.page.set_primary_action(__('Check Availability'), function () {
                    if (!frm.doc.patient) {
                        frappe.msgprint({
                            title: __('Not Allowed'),
                            message: __('Please select Patient first'),
                            indicator: 'red'
                        });
                    } else {
                        frappe.call({
                            method: 'erpnext.healthcare.doctype.patient_appointment.patient_appointment.check_payment_fields_reqd',
                            args: { 'patient': frm.doc.patient },
                            callback: function (data) {
                                if (data.message == true) {
                                    if (frm.doc.mode_of_payment && frm.doc.paid_amount) {
                                        check_and_set_availability(frm);
                                    }
                                    if (!frm.doc.mode_of_payment) {
                                        frappe.msgprint({
                                            title: __('Not Allowed'),
                                            message: __('Please select a Mode of Payment first'),
                                            indicator: 'red'
                                        });
                                    }
                                    if (!frm.doc.paid_amount) {
                                        frappe.msgprint({
                                            title: __('Not Allowed'),
                                            message: __('Please set the Paid Amount first'),
                                            indicator: 'red'
                                        });
                                    }
                                } else {
                                    check_and_set_availability(frm);
                                }
                            }
                        });
                    }
                });
            }
        } else {
            frm.page.set_primary_action(__('Save'), () => frm.save());
        }
    }
})
