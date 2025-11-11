"""
Modelo para la gestión de Pagaments
"""
from models.database import Database
from decimal import Decimal


class Pagament:
    """Modelo para operaciones CRUD de pagaments"""
    
    @staticmethod
    def get_all():
        """Obtener todos los pagaments con información del faller"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT 
                    p.id,
                    p.id_faller,
                    p.comentaris,
                    p.quantitat,
                    p.data_pagament,
                    p.metode_pagament,
                    p.total_pagament,
                    p.aportat_pagament,
                    p.falta_per_aportar,
                    p.data_aportacio,
                    f.nom,
                    f.cognoms,
                    f.dni,
                    f.edat,
                    f.grup
                FROM pagaments p
                INNER JOIN fallers f ON p.id_faller = f.id
                ORDER BY p.data_pagament DESC, p.id DESC
            """
            cursor.execute(sql)
            pagaments = cursor.fetchall()
            
            # Convertir fechas a formato string
            for pagament in pagaments:
                if pagament['data_pagament']:
                    pagament['data_pagament'] = pagament['data_pagament'].strftime('%Y-%m-%d')
                if pagament['data_aportacio']:
                    pagament['data_aportacio'] = pagament['data_aportacio'].strftime('%Y-%m-%d')
                
                # Convertir Decimal a float
                pagament['quantitat'] = float(pagament['quantitat'])
                pagament['total_pagament'] = float(pagament['total_pagament'])
                pagament['aportat_pagament'] = float(pagament['aportat_pagament'])
                pagament['falta_per_aportar'] = float(pagament['falta_per_aportar'])
                
                # Añadir campos calculados
                pagament['nom_complet'] = f"{pagament['nom']} {pagament['cognoms']}"
            
            return pagaments
    
    @staticmethod
    def get_by_faller(faller_id):
        """Obtener todos los pagaments de un faller específico"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT 
                    id, id_faller, comentaris, quantitat, data_pagament,
                    metode_pagament, total_pagament, aportat_pagament,
                    falta_per_aportar, data_aportacio
                FROM pagaments
                WHERE id_faller = %s
                ORDER BY data_pagament DESC
            """
            cursor.execute(sql, (faller_id,))
            return cursor.fetchall()
    
    @staticmethod
    def get_total_aportat_by_faller(faller_id):
        """Obtener el total aportado por un faller"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT SUM(quantitat) as total_aportat FROM pagaments WHERE id_faller = %s"
            cursor.execute(sql, (faller_id,))
            result = cursor.fetchone()
            return float(result['total_aportat']) if result['total_aportat'] else 0.0
    
    @staticmethod
    def create(data):
        """Crear un nuevo pagament"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            sql = """
                INSERT INTO pagaments
                (id_faller, comentaris, quantitat, data_pagament, metode_pagament,
                 total_pagament, aportat_pagament, falta_per_aportar, data_aportacio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(sql, (
                data.get('id_faller'),
                data.get('comentaris'),
                data.get('quantitat'),
                data.get('data_pagament'),
                data.get('metode_pagament'),
                data.get('total_pagament'),
                data.get('aportat_pagament'),
                data.get('falta_per_aportar'),
                data.get('data_aportacio')
            ))
            
            return cursor.lastrowid
    
    @staticmethod
    def get_info_faller_pagament(faller_id):
        """Obtener información resumida de pagaments de un faller"""
        from utils.tariffs import calcular_total
        
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT 
                    f.id,
                    f.nom,
                    f.cognoms,
                    CONCAT(f.nom, ' ', f.cognoms) as nom_complet,
                    f.dni,
                    f.grup,
                    f.edat,
                    COALESCE(p.total_pagament, 0) as total_pagament_guardado,
                    COALESCE(p.aportat_pagament, 0) as aportat_pagament
                FROM fallers f
                LEFT JOIN (
                    SELECT 
                        id_faller,
                        MAX(total_pagament) as total_pagament,
                        SUM(quantitat) as aportat_pagament
                    FROM pagaments
                    WHERE id_faller = %s
                    GROUP BY id_faller
                ) p ON f.id = p.id_faller
                WHERE f.id = %s
            """
            cursor.execute(sql, (faller_id, faller_id))
            result = cursor.fetchone()
            
            if result:
                # Si no tiene pagos previos (total_pagament_guardado es 0), calcular el total basado en grupo y edad
                if result['total_pagament_guardado'] == 0:
                    result['total_pagament'] = calcular_total(result['grup'], result['edat'])
                else:
                    result['total_pagament'] = float(result['total_pagament_guardado'])
                
                result['aportat_pagament'] = float(result['aportat_pagament'])
                result['falta_per_aportar'] = result['total_pagament'] - result['aportat_pagament']
                
                # Eliminar campos temporales
                del result['total_pagament_guardado']
                del result['grup']
                del result['edat']
            
            return result
