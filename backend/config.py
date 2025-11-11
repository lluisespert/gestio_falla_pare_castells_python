"""
Configuración de la base de datos y la aplicación Flask
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Configuración de la aplicación"""
    
    # Configuración de Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Configuración de la base de datos MySQL
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASS', ''),
        'database': os.getenv('DB_NAME', 'pare_castells'),
        'charset': 'utf8mb4',
        'cursorclass': 'DictCursor'
    }
    
    # Configuración CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
