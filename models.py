from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class AdminUser(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),nullable=False,default='Nexicom Admin'); email=db.Column(db.String(180),unique=True,nullable=False); password_hash=db.Column(db.String(255),nullable=False); created_at=db.Column(db.DateTime,default=datetime.utcnow)
    def set_password(self,p): self.password_hash=generate_password_hash(p)
    def check_password(self,p): return check_password_hash(self.password_hash,p)

class SiteSetting(db.Model):
    id=db.Column(db.Integer,primary_key=True); key=db.Column(db.String(120),unique=True,nullable=False); value=db.Column(db.Text,default='')

class NavItem(db.Model):
    id=db.Column(db.Integer,primary_key=True); label=db.Column(db.String(80),nullable=False); url=db.Column(db.String(255),nullable=False); sort_order=db.Column(db.Integer,default=0); is_active=db.Column(db.Boolean,default=True)

class Service(db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(140),nullable=False); slug=db.Column(db.String(160),unique=True,nullable=False); short_description=db.Column(db.String(300),default=''); description=db.Column(db.Text,default=''); icon=db.Column(db.String(40),default='✦'); image=db.Column(db.String(255),default=''); sort_order=db.Column(db.Integer,default=0); is_active=db.Column(db.Boolean,default=True)

class TeamMember(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(140),nullable=False); role=db.Column(db.String(160),nullable=False); department=db.Column(db.String(120),default=''); short_bio=db.Column(db.String(260),default=''); bio=db.Column(db.Text,default=''); experience=db.Column(db.String(180),default=''); skills=db.Column(db.Text,default=''); achievements=db.Column(db.Text,default=''); photo=db.Column(db.String(255),default=''); email=db.Column(db.String(180),default=''); linkedin=db.Column(db.String(255),default=''); sort_order=db.Column(db.Integer,default=0); is_featured=db.Column(db.Boolean,default=False); is_active=db.Column(db.Boolean,default=True)

class Review(db.Model):
    id=db.Column(db.Integer,primary_key=True); client_name=db.Column(db.String(140),nullable=False); company=db.Column(db.String(160),default=''); service_used=db.Column(db.String(160),default=''); rating=db.Column(db.Integer,default=5); review_text=db.Column(db.Text,nullable=False); photo=db.Column(db.String(255),default=''); sort_order=db.Column(db.Integer,default=0); is_featured=db.Column(db.Boolean,default=False); is_active=db.Column(db.Boolean,default=True); created_at=db.Column(db.DateTime,default=datetime.utcnow)

class Job(db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(160),nullable=False); department=db.Column(db.String(120),default=''); location=db.Column(db.String(160),default='Bangalore'); employment_type=db.Column(db.String(80),default='Full-time'); experience=db.Column(db.String(100),default=''); salary=db.Column(db.String(100),default=''); description=db.Column(db.Text,default=''); requirements=db.Column(db.Text,default=''); is_active=db.Column(db.Boolean,default=True); created_at=db.Column(db.DateTime,default=datetime.utcnow)

class JobApplication(db.Model):
    id=db.Column(db.Integer,primary_key=True); job_id=db.Column(db.Integer,db.ForeignKey('job.id')); name=db.Column(db.String(140),nullable=False); email=db.Column(db.String(180),nullable=False); phone=db.Column(db.String(40),nullable=False); experience=db.Column(db.String(80),default=''); message=db.Column(db.Text,default=''); resume=db.Column(db.String(255),default=''); status=db.Column(db.String(60),default='New'); created_at=db.Column(db.DateTime,default=datetime.utcnow); job=db.relationship('Job',backref='applications')

class Page(db.Model):
    id=db.Column(db.Integer,primary_key=True); slug=db.Column(db.String(80),unique=True,nullable=False); title=db.Column(db.String(160),nullable=False); eyebrow=db.Column(db.String(120),default=''); body=db.Column(db.Text,default=''); meta_title=db.Column(db.String(180),default=''); meta_description=db.Column(db.String(320),default=''); is_active=db.Column(db.Boolean,default=True)

class ContactMessage(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(140),nullable=False); email=db.Column(db.String(180),nullable=False); phone=db.Column(db.String(40),default=''); subject=db.Column(db.String(180),default=''); message=db.Column(db.Text,nullable=False); status=db.Column(db.String(50),default='New'); notes=db.Column(db.Text,default=''); created_at=db.Column(db.DateTime,default=datetime.utcnow)
