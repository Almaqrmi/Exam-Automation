import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية من ملف .env
load_dotenv()

class Config:
    """إعدادات التطبيق الأساسية"""
    
    # المفتاح السري للتطبيق (لتشفير الجلسات)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # مسار قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'database.db')
    
    # إصلاح رابط PostgreSQL إذا كان بصيغة قديمة
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql+psycopg://", 1)
    elif SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgresql://", "postgresql+psycopg://", 1)
    
    # تعطيل تتبع التعديلات (لتحسين الأداء)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # مجلد رفع الملفات
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    
    # الحد الأقصى لحجم الملف المرفوع (16 ميجابايت)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # الامتدادات المسموحة للملفات
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # مفتاح Gemini API
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    @staticmethod
    def init_app(app):
        """تهيئة التطبيق"""
        # إنشاء المجلدات المطلوبة إذا لم تكن موجودة
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'), exist_ok=True)