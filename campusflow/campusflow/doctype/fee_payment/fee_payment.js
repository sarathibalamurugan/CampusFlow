// Copyright (c) 2026, Parthasarathi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fee Payment", {
	refresh(frm) {
		frm.toggle_reqd("student", true);
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

		frm.set_query("student", function () {
			return {
				filters: {
					organization_type: frm.doc.organization_type,
				},
			};
		});

		frm.set_query("fee_structure", function () {
			return {
				filters: {
					organization_type: frm.doc.organization_type,
					program: frm.doc.program,
					year: frm.doc.year,
					student_class: frm.doc.student_class,
				},
			};
		});
	},
	student(frm) {
		if (frm.doc.student) {
			frappe.db
				.get_value("Student", { name: frm.doc.student }, "fees_balance")
				.then((value) => {
					frm.set_value("your_balance", value.message.fees_balance);
				});
		}
	},
});
