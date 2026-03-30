# Copyright (c) 2026, Parthasarathi and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionApplication(Document):
	def on_submit(self):
		if self.status == "Draft":
			frappe.throw(_("Can't submit the Application with status as Draft."))
