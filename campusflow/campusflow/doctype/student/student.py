# Copyright (c) 2026, Parthasarathi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Student(Document):
	def before_save(self):
		self.student_id = self.name
		self.full_name = (self.first_name or "") + " " + (self.second_name or "")
