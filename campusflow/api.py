import frappe


@frappe.whitelist()
def get_cached_org_type():
	if not frappe.cache().get_value("org_type"):
		org_type = frappe.db.get_single_value("CampusFlow Settings", "organization_type")
		frappe.cache.set_value("org_type", org_type)
	return frappe.cache.get_value("org_type")


@frappe.whitelist()
def check_permission():
	if not frappe.has_permission("Fee Payment", "write"):
		frappe.throw("You are not allowed to this payment")

	return


def set_student_fees_balance(doc, method):
	if method == "on_submit":
		if frappe.db.get_value("Student", doc.student, "fees_balance") - doc.paid_amount < 0:
			frappe.throw("Payment exceeds the outstanding balance.")

		frappe.db.set_value(
			"Student",
			doc.student,
			"fees_balance",
			frappe.db.get_value("Student", doc.student, "fees_balance") - doc.paid_amount,
		)


def enqueue_evaluation_result_email(doc, method):
	frappe.enqueue(send_evaluation_result, doc=doc, queue="default")


def send_evaluation_result(doc):
	email = frappe.db.get_value("Student", doc.student, "email")
	if email:
		attachments = [
			frappe.attach_print(doc.doctype, doc.name, file_name=doc.name, print_format="Report Card")
		]

		subject = "Your evaluation result"
		message = f"Dear {doc.student},\n\nYour evaluation result for {doc.course} is: {doc.obtained_marks}\n\nBest regards,\nCampusFlow Team"
		frappe.sendmail(recipients=email, subject=subject, message=message, attachments=attachments, now=True)


def enqueue_fee_remider_email(doc, method):
	frappe.enqueue(send_fee_reminder_email, doc=doc, queue="long")


def send_fee_reminder_email(doc):
	student_balances = frappe.db.get_all("Student", fields=["name", "email", "fees_balance"])
	for student in student_balances:
		if student["fees_balance"] > 0:
			if student["email"]:
				subject = "Fee Payment Reminder"
				message = f"Dear {student['name']},\n\nThis is a reminder that you have an outstanding fee balance of {student['fees_balance']}.\nPlease make the payment at your earliest convenience.\n\nBest regards,\nCampusFlow Team"
				frappe.sendmail(recipients=student["email"], subject=subject, message=message, now=True)


@frappe.whitelist()
def get_student_count():
	return frappe.db.count(
		"Student", filters={"organization_type": get_cached_org_type(), "status": "Active"}
	)


def enqueue_fee_receipt_email(doc, method):
	frappe.enqueue(send_fee_receipt_email, doc=doc, queue="default")


def send_fee_receipt_email(doc):
	email = frappe.db.get_value("Student", doc.student, "email")
	if email:
		attachments = [
			frappe.attach_print(doc.doctype, doc.name, file_name=doc.name, print_format="Fee Receipt")
		]

		subject = "Your fee payment receipt"
		message = f"Dear {doc.student},\n\nThank you for your payment of {doc.paid_amount} towards your fees. Please find the attached receipt for your reference.\n\nBest regards,\nCampusFlow Team"
		frappe.sendmail(recipients=email, subject=subject, message=message, attachments=attachments, now=True)


def create_student_from_application(doc, method):
	if doc.status == "Approved":
		student = frappe.get_doc(
			{
				"doctype": "Student",
				"first_name": doc.student_name,
				"student_class": doc.class_applied,
				"gender": doc.gender,
				"date_of_birth": doc.date_of_birth,
				"parent_name": doc.parent_name,
				"parent_phone": doc.phone,
				"email": doc.email,
			}
		).insert(ignore_permissions=True)
		frappe.msgprint(f"Student {student.name} created successfully from application {doc.name}.")
