frappe.ui.form.on('Healthcare Service Insurance Coverage', {
    onload: function (frm) {
        add_get_price_btn(frm)
    },
    refresh: function(frm) {
        add_get_price_btn(frm)
    },
});

var add_get_price_btn = function(frm) {
    frm.add_custom_button(__('Get NHIF Price Package'), function() {
        frappe.call({
            method: 'csf_tz.nhif.api.insurance_coverage.enqueue_get_nhif_price_package',
            args: {},
            callback: function (data) {
                if (data.message) {
                    console.log(data.message.ExcludedServices)
                }
            }
        });
    });
  
}