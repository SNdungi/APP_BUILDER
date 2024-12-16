import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'trustthelordmysoul')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app_builder.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
print(os.getenv('MAX_HISTORY_SIZE'))