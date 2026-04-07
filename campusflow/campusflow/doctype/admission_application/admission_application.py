# Copyright (c) 2026, Parthasarathi and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AdmissionApplication(Document):
	def on_submit(self):
		if self.status == "Draft":
			frappe.throw(_("Can't submit the Application with status as Draft."))
		if self.status == "Approved":
			frappe.enqueue(self.send_confirmation_email)

	def send_confirmation_email(self):
		if self.email:
			frappe.sendmail(
				recipients=self.email,
				subject=_("Application Approved"),
				message=_(
					"Your Application has been approved. We will contact you soon with further details."
				),
			)
