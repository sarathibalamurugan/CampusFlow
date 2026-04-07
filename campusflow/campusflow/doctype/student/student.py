# Copyright (c) 2026, Parthasarathi and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form


class Student(Document):
	def before_insert(self):
		self.organization_type = frappe.cache.get_value("org_type") or frappe.db.get_single_value(
			"CampusFlow Settings", "organization_type"
		)
		fee_structure = frappe.db.exists(
			"Fee Structure",
			{
				"organization_type": self.organization_type,
				"program": self.program,
				"year": self.year,
				"student_class": self.student_class,
			},
		)
		if not fee_structure:
			frappe.throw(_("No fee structure found for the selected criteria. Create a fee structure first."))
		else:
			self.fees_balance = frappe.db.get_value("Fee Structure", fee_structure, "total_amount")

	def after_insert(self):
		frappe.enqueue(self.send_fill_details_email)

	def before_save(self):
		self.student_id = self.name
		self.full_name = (self.first_name or "") + " " + (self.second_name or "")

	def send_fill_details_email(self):
		if self.email:
			frappe.sendmail(
				recipients=self.email,
				subject=_("Your Student ID is created."),
				message=_("Your Student ID {0} is created. Please fill Further Details").format(
					get_link_to_form("Student", self.name)
				),
			)


@frappe.whitelist()
def mark_attendance(student, status, student_class=None, program=None, year=None):
	exist = frappe.db.exists("Attendance", {"student": student, "date": frappe.utils.today()})

	if exist:
		frappe.throw(
			_("Attendance {0} for this student has already been marked today.").format(
				get_link_to_form("Attendance", exist)
			)
		)
	else:
		frappe.get_doc(
			{
				"doctype": "Attendance",
				"student": student,
				"status": status,
				"student_class": student_class,
				"program": program,
				"year": year,
				"date": frappe.utils.today(),
			}
		).insert()
		frappe.msgprint("Attendance marked successfully!")
