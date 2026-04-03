// Copyright (c) 2026, Parthasarathi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student", {
	refresh(frm) {
		frappe.db.get_single_value("CampusFlow Settings", "organization_type").then((value) => {
			if (value == "School") {
				frm.set_df_property("phone", "hidden", 1);
				frm.set_df_property("program", "hidden", 1);
				frm.set_df_property("year", "hidden", 1);
				frm.toggle_reqd("student_class", 1);
			} else {
				frm.set_df_property("student_class", "hidden", 1);
				frm.toggle_reqd("program", 1);
				frm.toggle_reqd("year", 1);
			}
		});
		frm.add_custom_button(__("Mark Attendance"), function () {
			frappe.call({
				method: "campusflow.campusflow.doctype.student.student.mark_attendance",
				args: {
					student: frm.doc.name,
					status: "Present",
					student_class: frm.doc.student_class,
					program: frm.doc.program,
					year: frm.doc.year,
				},
			});
		});
		frm.add_custom_button(__("Mark Absent"), function () {
			frappe.call({
				method: "campusflow.campusflow.doctype.student.student.mark_attendance",
				args: {
					student: frm.doc.name,
					status: "Absent",
					student_class: frm.doc.student_class,
					program: frm.doc.program,
					year: frm.doc.year,
				},
			});
		});
		frm.add_custom_button(__("Check and Pay Fee"), function () {
			frappe.call({
				method: "campusflow.api.check_permission",
			});
			frappe.new_doc("Fee Payment", {
				student: frm.doc.name,
				student_name: frm.doc.student_name,
			});
		});
	},
});
