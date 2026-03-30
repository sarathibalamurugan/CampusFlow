# Copyright (c) 2026, Parthasarathi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CampusFlowSettings(Document):
	def before_save(self):
		frappe.cache().set_value("org_type", self.organization_type)
