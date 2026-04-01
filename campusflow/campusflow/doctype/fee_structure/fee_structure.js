// Copyright (c) 2026, Parthasarathi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fee Structure", {
	refresh(frm) {
		frappe.call({
			method: "campusflow.api.get_cached_org_type",
			callback: function (r) {
				if (r.message) {
					frm.doc.organization_type = r.message;
				}
				if (frm.doc.organization_type == "School") {
					frm.set_df_property("program", "hidden", 1);
					frm.set_df_property("year", "hidden", 1);
					frm.toggle_reqd("student_class", 1);
				} else if (frm.doc.organization_type == "College") {
					frm.set_df_property("student_class", "hidden", 1);
					frm.toggle_reqd("program", 1);
					frm.toggle_reqd("year", 1);
				}
			},
		});
	},
});
