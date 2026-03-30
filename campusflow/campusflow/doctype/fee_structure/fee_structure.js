// Copyright (c) 2026, Parthasarathi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fee Structure", {
	refresh(frm) {
		let org_type = frappe.cache().get_value("org_type");
		if (!org_type) {
			frappe.db
				.get_single_value("CampusFlow Settings", "organization_type")
				.then((value) => {
					org_type = value;
					frm.organization_type = org_type;
				});
		}

		if (org_type == "School") {
			frm.set_df_property("program", "hidden", 1);
			frm.set_df_property("year", "hidden", 1);
		} else {
			frm.set_df_property("class", "hidden", 1);
		}
	},
});
