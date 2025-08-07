import os

class Config:
    MAIL_SERVER = 'in-v3.mailjet.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAILJET_API_KEY', 'c31f85503f563082717e312df1220f9c')
    MAIL_PASSWORD = os.getenv('MAILJET_API_SECRET', 'b568aa0697d95055a2ec00923f0e0032')
    MAIL_DEFAULT_SENDER = os.getenv('MAILJET_SENDER', 'no-reply@example.com')
