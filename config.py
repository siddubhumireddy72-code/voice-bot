"""
Configuration Management for Voice Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-this')
    
    # Server
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///voice_bot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Asterisk
    ASTERISK_HOST = os.getenv('ASTERISK_HOST', 'localhost')
    ASTERISK_PORT = int(os.getenv('ASTERISK_PORT', 5060))
    ASTERISK_USER = os.getenv('ASTERISK_USER', 'admin')
    ASTERISK_PASSWORD = os.getenv('ASTERISK_PASSWORD', 'password')
    ASTERISK_CONTEXT = os.getenv('ASTERISK_CONTEXT', 'from-internal')
    
    # Speech
    SPEECH_LANGUAGE = os.getenv('SPEECH_LANGUAGE', 'en-US')
    SPEECH_RATE = float(os.getenv('SPEECH_RATE', 1.0))
    SPEECH_VOLUME = float(os.getenv('SPEECH_VOLUME', 1.0))
    
    # Call Settings
    DEFAULT_GREETING = os.getenv('DEFAULT_GREETING', 'Hello! You have reached the voice bot.')
    DEFAULT_MAX_CALL_DURATION = int(os.getenv('DEFAULT_MAX_CALL_DURATION', 300))
    DEFAULT_SILENCE_TIMEOUT = int(os.getenv('DEFAULT_SILENCE_TIMEOUT', 10))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
