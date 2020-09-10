frappe.pages['MyPage'].on_page_load = function(wrapper) {
	this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Items',
			single_column: true,
	});

	this.page.$export_tool = new frappe.v_page.ExportTool(this.page);
};

$("head").append("<link href='https://unpkg.com/primevue/resources/themes/saga-blue/theme.css' rel='stylesheet'>"); 
$("head").append("<link href='https://unpkg.com/primevue/resources/primevue.min.css' rel='stylesheet'>"); 
$("head").append("<link href='https://unpkg.com/primeicons/primeicons.css ' rel='stylesheet'>"); 
