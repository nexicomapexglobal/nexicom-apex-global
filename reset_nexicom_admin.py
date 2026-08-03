from pathlib import Path

from app import app
from models import db, AdminUser

EMAIL = "admin@nexicomapexglobal.com"
PASSWORD = "Admin@123"
NAME = "Nexicom Admin"

with app.app_context():
    db_path = Path(app.root_path) / "instance" / "nexicom.db"
    print(f"Database: {db_path}")

    user = AdminUser.query.filter_by(email=EMAIL).first()
    if user is None:
        user = AdminUser(name=NAME, email=EMAIL)
        db.session.add(user)
        print("Admin account created.")
    else:
        user.name = NAME
        print(f"Existing admin found (ID: {user.id}).")

    user.set_password(PASSWORD)
    db.session.commit()

    verified = AdminUser.query.filter_by(email=EMAIL).first()
    if verified and verified.check_password(PASSWORD):
        print("SUCCESS: Password verified successfully.")
        print(f"Email: {EMAIL}")
        print(f"Password: {PASSWORD}")
    else:
        raise RuntimeError("Password verification failed.")
