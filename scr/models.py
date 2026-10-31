from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False, unique=True)
    role=db.Column(db.String, nullable=False, default='user')
    password=db.Column(db.String, nullable=False)
    date_created=db.Column(db.DateTime(timezone=True), default=func.now())
    expense=db.relationship('Expense', backref='users', passive_deletes=True)
        
        
class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    title=db.Column(db.String, nullable=False)
    amount=db.Column(db.Integer, nullable=False)
    category=db.Column(db.String(50), nullable=False)
    payment_method=db.Column(db.String(20), nullable=False)
    date_created=db.Column(db.DateTime(timezone=True), default=func.now())
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id":self.user_id,
            "title":self.title,
            "amount":self.amount,
            "category":self.category,
            "payment_method":self.payment_method,
            "date_created":self.date_created
        }