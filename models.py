from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """نموذج المستخدم (الدكتور)"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # علاقة مع الاختبارات
    exams = db.relationship('Exam', backref='creator', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """تشفير كلمة المرور"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """التحقق من كلمة المرور"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Exam(db.Model):
    """نموذج الاختبار"""
    
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    pdf_filename = db.Column(db.String(255))
    num_questions = db.Column(db.Integer, default=10)
    question_type = db.Column(db.String(50))  # 'mixed', 'mcq', 'tf', 'fill', 'direct'
    difficulty = db.Column(db.String(20))     # 'easy', 'medium', 'hard'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # مفتاح خارجي للمستخدم
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # علاقة مع الأسئلة
    questions = db.relationship('Question', backref='exam', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Exam {self.title}>'


class Question(db.Model):
    """نموذج السؤال"""
    
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50)) 
    correct_answer = db.Column(db.Text)
    options = db.Column(db.Text)  
    points = db.Column(db.Integer, default=1)
    
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    
    def __repr__(self):
        return f'<Question {self.id}>'