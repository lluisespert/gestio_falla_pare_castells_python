"""
Clase base para la conexión a la base de datos
"""
import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from config import Config


class Database:
    """Gestor de conexiones a la base de datos"""
    
    @staticmethod
    @contextmanager
    def get_connection():
        """
        Context manager para manejar conexiones a la base de datos
        Uso:
            with Database.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tabla")
        """
        connection = None
        try:
            connection = pymysql.connect(
                host=Config.DB_CONFIG['host'],
                user=Config.DB_CONFIG['user'],
                password=Config.DB_CONFIG['password'],
                database=Config.DB_CONFIG['database'],
                charset=Config.DB_CONFIG['charset'],
                cursorclass=DictCursor
            )
            yield connection
            connection.commit()
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
