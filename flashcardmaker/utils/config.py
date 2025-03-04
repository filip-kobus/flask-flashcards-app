import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PWD = os.environ.get('DB_PWD')
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{DB_PWD}@{DB_HOST}/flask_app"
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class AWSCredentials:
    ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    REGION_NAME = "eu-central-1"