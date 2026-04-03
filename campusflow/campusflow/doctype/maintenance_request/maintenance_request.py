# Copyright (c) 2026, Parthasarathi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MaintenanceRequest(Document):
	def before_save(self):
		if self.asset_name:
			frappe.db.set_value("Campus Asset", self.asset_name, "status", "Repair")
		else:
			frappe.throw("Please select an asset for the maintenance request.")

	def on_submit(self):
		if self.status == "Closed":
			frappe.db.set_value("Campus Asset", self.asset_name, "status", "Working")
