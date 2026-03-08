from flask import Flask, render_template, redirect, url_for, flash
from datetime import date
from models import db, Invoice, Payment, ExceptionItem, AuditLog

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///automation_demo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

db.init_app(app)


@app.route("/")
def dashboard():
    invoice_count = Invoice.query.count()
    payment_count = Payment.query.count()
    exception_count = ExceptionItem.query.filter_by(status="Open").count()
    overdue_count = Invoice.query.filter_by(status="Overdue").count()

    return render_template(
        "dashboard.html",
        invoice_count=invoice_count,
        payment_count=payment_count,
        exception_count=exception_count,
        overdue_count=overdue_count,
    )


@app.route("/invoices")
def invoices():
    all_invoices = Invoice.query.order_by(Invoice.id.desc()).all()
    return render_template("invoices.html", invoices=all_invoices)


@app.route("/payments")
def payments():
    all_payments = Payment.query.order_by(Payment.id.desc()).all()
    return render_template("payments.html", payments=all_payments)


@app.route("/exceptions")
def exceptions():
    all_exceptions = ExceptionItem.query.order_by(ExceptionItem.id.desc()).all()
    return render_template("exceptions.html", exceptions=all_exceptions)


@app.route("/logs")
def logs():
    all_logs = AuditLog.query.order_by(AuditLog.id.desc()).all()
    return render_template("logs.html", logs=all_logs)


@app.route("/run-reconciliation")
def run_reconciliation():
    today = date.today()

    # 清空旧的 open exceptions，避免重复堆积太快
    open_exceptions = ExceptionItem.query.filter_by(status="Open").all()
    for item in open_exceptions:
        db.session.delete(item)

    payments = Payment.query.all()
    seen_payment_refs = set()

    for payment in payments:
        # duplicate payment reference
        if payment.payment_reference in seen_payment_refs:
            payment.status = "Duplicate"
            db.session.add(ExceptionItem(
                item_type="Payment",
                reference=payment.payment_reference,
                issue="Duplicate payment reference detected"
            ))
            db.session.add(AuditLog(
                action="Duplicate Payment Detected",
                reference=payment.payment_reference,
                details="Duplicate payment reference flagged during reconciliation"
            ))
            continue

        seen_payment_refs.add(payment.payment_reference)

        if not payment.invoice_number:
            payment.status = "Unmatched"
            db.session.add(ExceptionItem(
                item_type="Payment",
                reference=payment.payment_reference,
                issue="Missing invoice number reference"
            ))
            db.session.add(AuditLog(
                action="Unmatched Payment",
                reference=payment.payment_reference,
                details="Payment missing invoice reference"
            ))
            continue

        invoice = Invoice.query.filter_by(invoice_number=payment.invoice_number).first()

        if not invoice:
            payment.status = "Unmatched"
            db.session.add(ExceptionItem(
                item_type="Payment",
                reference=payment.payment_reference,
                issue="Invoice not found"
            ))
            db.session.add(AuditLog(
                action="Invoice Not Found",
                reference=payment.payment_reference,
                details=f"Invoice {payment.invoice_number} not found for payment"
            ))
            continue

        if payment.amount == invoice.amount:
            payment.status = "Matched"
            invoice.status = "Paid"
            db.session.add(AuditLog(
                action="Invoice Matched",
                reference=invoice.invoice_number,
                details="Invoice fully matched and marked as Paid"
            ))
        elif payment.amount < invoice.amount:
            payment.status = "Partial"
            invoice.status = "Partial"
            db.session.add(ExceptionItem(
                item_type="Invoice",
                reference=invoice.invoice_number,
                issue="Partial payment received"
            ))
            db.session.add(AuditLog(
                action="Partial Payment",
                reference=invoice.invoice_number,
                details="Invoice received partial payment"
            ))
        else:
            payment.status = "Exception"
            invoice.status = "Exception"
            db.session.add(ExceptionItem(
                item_type="Invoice",
                reference=invoice.invoice_number,
                issue="Payment exceeds invoice amount"
            ))
            db.session.add(AuditLog(
                action="Overpayment Exception",
                reference=invoice.invoice_number,
                details="Payment amount exceeds invoice amount"
            ))

    # mark overdue invoices
    invoices = Invoice.query.all()
    for invoice in invoices:
        if invoice.status == "Issued" and invoice.due_date < today:
            invoice.status = "Overdue"
            db.session.add(ExceptionItem(
                item_type="Invoice",
                reference=invoice.invoice_number,
                issue="Invoice overdue and unpaid"
            ))
            db.session.add(AuditLog(
                action="Invoice Overdue",
                reference=invoice.invoice_number,
                details="Invoice marked overdue during reconciliation"
            ))

    db.session.add(AuditLog(
        action="Reconciliation Run",
        reference="SYSTEM",
        details="Invoice reconciliation workflow executed"
    ))

    db.session.commit()
    flash("Reconciliation completed successfully.", "success")
    return redirect(url_for("dashboard"))


@app.route("/send-reminders")
def send_reminders():
    overdue_invoices = Invoice.query.filter_by(status="Overdue").all()

    for invoice in overdue_invoices:
        db.session.add(AuditLog(
            action="Reminder Sent",
            reference=invoice.invoice_number,
            details=f"Reminder simulated for customer {invoice.customer_name}"
        ))

    db.session.commit()
    flash("Reminders sent for overdue invoices.", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)