import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    
    # Email Configuration (Mailgun)
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN', '')
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY', '')
    NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL', 'alerts@yourdomain.com')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'your-email@example.com')
    
    # API Keys
    SHODAN_API_KEY = os.getenv('SHODAN_API_KEY', '')
    VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')
    CENSYS_UID = os.getenv('CENSYS_UID', '')
    CENSYS_SECRET = os.getenv('CENSYS_SECRET', '')
    SECURITYTRAILS_API_KEY = os.getenv('SECURITYTRAILS_API_KEY', '')
    ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY', '')
    
    # Tor Configuration
    TOR_PROXY = os.getenv('TOR_PROXY', 'socks5://127.0.0.1:9050')
    USE_TOR = os.getenv('USE_TOR', 'False').lower() == 'true'
    
    # Application
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', 4))
    TIMEOUT = int(os.getenv('TIMEOUT', 30))
    
    # Redis (optional caching)
    REDIS_URL = os.getenv('REDIS_URL', None)
