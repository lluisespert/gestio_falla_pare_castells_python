"""
Modelo para la gestión de Fallers
"""
from models.database import Database
from datetime import datetime


class Faller:
    """Modelo para operaciones CRUD de fallers"""
    
    @staticmethod
    def get_all():
        """Obtener todos los fallers ordenados por ID descendente"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT 
                    id, nom, cognoms, domicili, telefon, dni,
                    data_naixement,
                    email, edat, `grup`, colaborador, categoria,
                    data_alta
                FROM fallers
                ORDER BY id DESC
            """
            cursor.execute(sql)
            fallers = cursor.fetchall()
            
            # Convertir tipos de datos
            for faller in fallers:
                faller['id'] = int(faller['id'])
                faller['edat'] = int(faller['edat']) if faller['edat'] is not None else None
                faller['colaborador'] = int(faller['colaborador'])
                
                # Convertir fechas a string YYYY-MM-DD
                if faller['data_naixement']:
                    faller['data_naixement'] = faller['data_naixement'].strftime('%Y-%m-%d')
                if faller['data_alta']:
                    faller['data_alta'] = faller['data_alta'].strftime('%Y-%m-%d')
            
            return fallers
    
    @staticmethod
    def get_by_id(faller_id):
        """Obtener un faller por su ID"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT 
                    id, nom, cognoms, domicili, telefon, dni,
                    data_naixement,
                    email, edat, `grup`, colaborador, categoria,
                    data_alta
                FROM fallers
                WHERE id = %s
            """
            cursor.execute(sql, (faller_id,))
            faller = cursor.fetchone()
            
            if faller:
                faller['id'] = int(faller['id'])
                faller['edat'] = int(faller['edat']) if faller['edat'] is not None else None
                faller['colaborador'] = int(faller['colaborador'])
                
                # Convertir fechas a string YYYY-MM-DD
                if faller['data_naixement']:
                    faller['data_naixement'] = faller['data_naixement'].strftime('%Y-%m-%d')
                if faller['data_alta']:
                    faller['data_alta'] = faller['data_alta'].strftime('%Y-%m-%d')
            
            return faller
    
    @staticmethod
    def create(data):
        """Crear un nuevo faller"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            # Normalizar campo colaborador a 0 o 1
            colaborador = data.get('colaborador', 0)
            if isinstance(colaborador, bool):
                colaborador = 1 if colaborador else 0
            elif isinstance(colaborador, str):
                lc = colaborador.lower()
                colaborador = 1 if lc in ['true', '1', 'yes'] else 0
            else:
                colaborador = 1 if int(colaborador) else 0
            
            sql = """
                INSERT INTO fallers
                (nom, cognoms, domicili, telefon, dni, data_naixement, email, edat, `grup`, colaborador, data_alta, categoria)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(sql, (
                data.get('nom'),
                data.get('cognoms'),
                data.get('domicili'),
                data.get('telefon'),
                data.get('dni'),
                data.get('data_naixement'),
                data.get('email'),
                data.get('edat'),
                data.get('grup'),
                colaborador,
                data.get('data_alta'),
                data.get('categoria', 'Home')
            ))
            
            return cursor.lastrowid
    
    @staticmethod
    def update(faller_id, data):
        """Actualizar un faller existente"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            # Normalizar campo colaborador
            colaborador = data.get('colaborador', 0)
            if isinstance(colaborador, bool):
                colaborador = 1 if colaborador else 0
            else:
                colaborador = 1 if int(colaborador) else 0
            
            sql = """
                UPDATE fallers
                SET nom=%s, cognoms=%s, domicili=%s, telefon=%s, dni=%s, data_naixement=%s,
                    email=%s, edat=%s, `grup`=%s, colaborador=%s, data_alta=%s, categoria=%s
                WHERE id=%s
            """
            
            cursor.execute(sql, (
                data.get('nom'),
                data.get('cognoms'),
                data.get('domicili'),
                data.get('telefon'),
                data.get('dni'),
                data.get('data_naixement'),
                data.get('email'),
                data.get('edat'),
                data.get('grup'),
                colaborador,
                data.get('data_alta'),
                data.get('categoria', 'Home'),
                faller_id
            ))
            
            return cursor.rowcount
    
    @staticmethod
    def delete(faller_id):
        """Eliminar un faller"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM fallers WHERE id = %s"
            cursor.execute(sql, (faller_id,))
            return cursor.rowcount
