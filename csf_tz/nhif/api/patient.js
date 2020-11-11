frappe.ui.form.on('Patient', {
    setup: function (frm) {
    },
    onload: function (frm) {
        frm.trigger('add_get_info_btn')
    },
    refresh: function (frm) {
        frm.trigger('add_get_info_btn')
    },
    add_get_info_btn: function(frm) {
        frm.add_custom_button(__('Get Patinet Info'), function () {
            frm.trigger('get_patinet_info')
        });
    },
    card_no:function(frm) {
        frm.trigger('get_patinet_info')
    },
    get_patinet_info: function (frm) {
        // if (!frm.doc.insurance_subscription || !frm.doc.billing_item) {
        //     return
        // }
        frappe.call({
            method: 'csf_tz.nhif.api.patient.get_patinet_info',
            args: {
                'card_no': frm.doc.card_no,
            },
            callback: function (data) {
                if (data.message) {
                    const card = data.message
                    frm.set_value("first_name", card.FirstName)
                    frm.set_value("last_name", card.LastName)
                    frm.set_value("patient_name", card.FullName)
                    frm.set_value("sex", card.Gender)
                    frm.set_value("dob", card.DateOfBirth)
                    frm.set_value("product_code", card.ProductCode)
                    frm.set_value("membership_no", card.MembershipNo)
                }
            }
        });
    },
})
