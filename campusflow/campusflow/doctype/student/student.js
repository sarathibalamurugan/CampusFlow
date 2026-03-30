// Copyright (c) 2026, Parthasarathi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student", {
	refresh(frm) {
		frappe.db.get_single_value("CampusFlow Settings", "organization_type").then((value) => {
			frm.set_value("organization_type", value);
			if (value == "School") {
				frm.set_df_property("phone", "hidden", 1);
				frm.set_df_property("email", "hidden", 1);
				frm.set_df_property("program", "hidden", 1);
				frm.set_df_property("year", "hidden", 1);
			} else {
				frm.set_df_property("class", "hidden", 1);
			}
		});
	},
});
