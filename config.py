"""Configuration management for Flask AI Workshop.

This module loads environment variables and provides configuration
for the Flask application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class.
    
    All configuration variables are loaded from environment variables
    for security. Never hardcode secrets in your code!
    """
    
    # Flask secret key for session management
    # This should be a random string - generate with: python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Google OAuth credentials
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
    # Groq API key for AI functionality
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    # Flask environment settings
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database file location
    DATABASE = 'database.db'
    
    @staticmethod
    def validate():
        """Validate that all required configuration variables are set.
        
        Raises:
            ValueError: If any required configuration is missing.
        """
        required_vars = [
            ('GOOGLE_CLIENT_ID', Config.GOOGLE_CLIENT_ID),
            ('GOOGLE_CLIENT_SECRET', Config.GOOGLE_CLIENT_SECRET),
            ('GROQ_API_KEY', Config.GROQ_API_KEY),
        ]
        
        missing = [var_name for var_name, var_value in required_vars if not var_value]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please check your .env file and ensure all variables are set."
            )

# Create config instance
config = Config()
