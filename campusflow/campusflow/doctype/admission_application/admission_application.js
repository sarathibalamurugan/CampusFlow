// Copyright (c) 2026, Parthasarathi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Admission Application", {
	refresh(frm) {
		if (frm.doc.docstatus == 1 && frm.doc.status == "Approved") {
			frm.add_custom_button(__("Create Student"), function () {
				frappe.new_doc("Student", {
					first_name: frm.doc.student_name,
					parent_name: frm.doc.parent_name,
					date_of_birth: frm.doc.date_of_birth,
				});
			});
		}
	},
});
