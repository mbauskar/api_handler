frappe.ui.form.on("API Configuration", {
	refresh: function(frm){
		description = "<p class='help-box small text-muted hidden-xs'>URL for Rest-API will \
		be in following format: <b>http://domain_name/api_name/version/</b><br>"
		
		urls = []
		frm.doc.versions.map(function(version, idx){
			description += (idx +1) +": "+ frappe.urllib.get_base_url() +"/"+ frm.doc.api_name +"/"+ version.api_version +"/<br>"
		})
		description += "</p>"		

		frm.fields_dict.url_description.$wrapper.html(description)
	}
});