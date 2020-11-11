frappe.ui.form.on('Patient', {
    setup: function (frm) {
    },
    onload: function (frm) {
        frm.trigger('get_patinet_info')
    },
    refresh: function (frm) {
        frm.trigger('get_patinet_info')
    },
    get_patinet_info: function (frm) {
        frm.add_custom_button(__('Get Patinet Info'), function () {
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
                        // frm.set_value("", card.ProductCode)
                        // frm.set_value("", card.MembershipNo)
                    }
                }
            });
        });
    },
    
})
