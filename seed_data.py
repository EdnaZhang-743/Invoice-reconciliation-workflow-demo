from datetime import date, timedelta
from app import app
from models import db, Invoice, Payment, AuditLog, ExceptionItem

with app.app_context():
    db.drop_all()
    db.create_all()

    invoices = [
        Invoice(invoice_number="INV-1001", customer_name="Acme Ltd", amount=500.00, due_date=date.today() - timedelta(days=5)),
        Invoice(invoice_number="INV-1002", customer_name="Beta Co", amount=300.00, due_date=date.today() + timedelta(days=7)),
        Invoice(invoice_number="INV-1003", customer_name="Gamma Group", amount=450.00, due_date=date.today() - timedelta(days=2)),
        Invoice(invoice_number="INV-1004", customer_name="Delta NZ", amount=200.00, due_date=date.today() + timedelta(days=10)),
    ]

    payments = [
        Payment(payment_reference="PAY-001", invoice_number="INV-1001", amount=500.00, payment_date=date.today()),
        Payment(payment_reference="PAY-002", invoice_number="INV-1002", amount=100.00, payment_date=date.today()),
        Payment(payment_reference="PAY-003", invoice_number="INV-9999", amount=250.00, payment_date=date.today()),
        Payment(payment_reference="PAY-004", invoice_number="", amount=150.00, payment_date=date.today()),
        Payment(payment_reference="PAY-001", invoice_number="INV-1004", amount=200.00, payment_date=date.today()),
    ]

    db.session.add_all(invoices)
    db.session.add_all(payments)
    db.session.add(AuditLog(action="Seed Data Loaded", reference="SYSTEM", details="Initial demo data inserted"))
    db.session.commit()

    print("Seed data inserted successfully.")