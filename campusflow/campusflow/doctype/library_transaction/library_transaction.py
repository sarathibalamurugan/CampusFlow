# Copyright (c) 2026, Parthasarathi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryTransaction(Document):
	def on_submit(self):
		if self.type == "Issue":
			return_transaction = frappe.new_doc("Library Transaction")
			return_transaction.student = self.student
			return_transaction.book_name = self.book_name
			return_transaction.type = "Return"
			return_transaction.returned = 1
			return_transaction.due_date = self.due_date
			return_transaction.date = frappe.utils.today()
			return_transaction.returned_against = self.name
			return_transaction.insert()
			return_transaction.submit()
			frappe.msgprint("Book returned successfully!")
			frappe.enqueue(send_return_mail, doc=return_transaction)


def send_return_mail(doc):
	student_email = frappe.db.get_value("Student", doc.student, "email")
	if student_email:
		attachments = [
			frappe.attach_print(doc.doctype, doc.name, file_name=doc.name, print_format="Library Receipt")
		]
		frappe.sendmail(
			recipients=student_email,
			subject="Book Return Reminder",
			message=f"Dear Student, this is a reminder to return the book '{doc.book_name}' by {doc.date}.",
			attachments=attachments,
			now=True,
		)
