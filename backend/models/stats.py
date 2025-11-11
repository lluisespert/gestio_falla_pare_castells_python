"""
Modelo para estadísticas y consultas agregadas
"""
from models.database import Database


class Stats:
    """Modelo para operaciones de estadísticas"""
    
    @staticmethod
    def get_percentatge():
        """Obtener fallers agrupados por su porcentaje de pago"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT 
                    f.id,
                    f.nom,
                    f.cognoms,
                    CONCAT(f.nom, ' ', f.cognoms) as nom_complet,
                    datos.total_pagament,
                    datos.aportat_pagament,
                    ROUND((datos.aportat_pagament / datos.total_pagament * 100), 2) as percentatge
                FROM fallers f
                INNER JOIN (
                    SELECT 
                        id_faller,
                        MAX(total_pagament) as total_pagament,
                        SUM(quantitat) as aportat_pagament
                    FROM pagaments
                    GROUP BY id_faller
                ) as datos ON f.id = datos.id_faller
                WHERE datos.total_pagament > 0
                ORDER BY percentatge DESC, f.cognoms, f.nom
            """
            cursor.execute(sql)
            fallers = cursor.fetchall()
            
            amb_80 = []
            sense_80 = []
            
            for faller in fallers:
                faller_data = {
                    'id': int(faller['id']),
                    'nom_complet': faller['nom_complet'],
                    'total_pagament': float(faller['total_pagament']),
                    'aportat_pagament': float(faller['aportat_pagament']),
                    'percentatge': float(faller['percentatge'])
                }
                
                if faller_data['percentatge'] >= 80:
                    amb_80.append(faller_data)
                else:
                    sense_80.append(faller_data)
            
            return {
                'amb_80': amb_80,
                'sense_80': sense_80,
                'total_amb_80': len(amb_80),
                'total_sense_80': len(sense_80)
            }
    
    @staticmethod
    def get_total_quotes():
        """Obtener totales de pagaments agregados"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT 
                    COALESCE(SUM(datos.total_pagament), 0) as total_pagament,
                    COALESCE(SUM(datos.aportat_total), 0) as aportat_pagament,
                    COUNT(DISTINCT datos.id_faller) as total_fallers
                FROM (
                    SELECT 
                        id_faller,
                        MAX(total_pagament) as total_pagament,
                        SUM(quantitat) as aportat_total
                    FROM pagaments
                    GROUP BY id_faller
                ) as datos
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            
            total_pagament = float(result['total_pagament'])
            aportat_pagament = float(result['aportat_pagament'])
            falta_per_aportar = total_pagament - aportat_pagament
            
            return {
                'total_pagament': total_pagament,
                'aportat_pagament': aportat_pagament,
                'falta_per_aportar': falta_per_aportar,
                'total_fallers': int(result['total_fallers'])
            }
