"""
Rutas para la gestión de pagaments
"""
from flask import Blueprint, request, jsonify
from models.faller import Faller
from models.pagament import Pagament
from utils.tariffs import calcular_total
from datetime import datetime

pagaments_bp = Blueprint('pagaments', __name__, url_prefix='/api/pagaments')


@pagaments_bp.route('/', methods=['GET', 'OPTIONS'])
def get_pagaments():
    """Obtener todos los pagaments (llista_pagaments.php)"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from utils.tariffs import calcular_total
        pagaments = Pagament.get_all()
        
        # Recalcular valores correctos para cada pago
        for pagament in pagaments:
            id_faller = pagament['id_faller']
            grup = pagament.get('grup', '')
            edat = pagament.get('edat', 0)
            
            # Recalcular total correcto
            total_correcte = calcular_total(grup, edat)
            
            # Obtener total aportado por este faller
            total_aportat_real = Pagament.get_total_aportat_by_faller(id_faller)
            
            # Calcular falta correcta
            falta_correcta = max(0, total_correcte - total_aportat_real)
            
            # Actualizar valores
            pagament['total_pagament'] = round(total_correcte, 2)
            pagament['aportat_pagament'] = round(float(pagament['quantitat']), 2)
            pagament['falta_per_aportar'] = round(falta_correcta, 2)
            pagament['total_aportat_acumulat'] = round(total_aportat_real, 2)
            pagament['porcentatge_completat'] = round((total_aportat_real / total_correcte) * 100, 1) if total_correcte > 0 else 0
            
            # Formatear fechas
            if pagament.get('data_pagament'):
                try:
                    if isinstance(pagament['data_pagament'], str):
                        dt = datetime.strptime(pagament['data_pagament'], '%Y-%m-%d')
                        pagament['data_pagament_formatted'] = dt.strftime('%d/%m/%Y')
                except:
                    pass
        
        return jsonify({
            'success': True,
            'data': pagaments,
            'total': len(pagaments),
            'message': 'Pagaments obtinguts correctament'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error del servidor: {str(e)}',
            'data': []
        }), 500


@pagaments_bp.route('/', methods=['POST'])
def create_pagament():
    """Crear un nuevo pagament (insertar_pagament.php)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'JSON inválido'
            }), 400
        
        # Extraer datos
        id_faller = int(data.get('id_faller', 0))
        comentaris = str(data.get('comentaris', '')).strip()[:500]
        quantitat = round(float(data.get('quantitat', 0)), 2)
        data_pagament = str(data.get('data_pagament', '')).strip()
        metode_pagament = str(data.get('metode_pagament', '')).strip().lower()
        
        # Validar método de pago
        allowed_methods = ['efectiu', 'targeta', 'transferencia', 'transferència', 'bizum']
        if metode_pagament not in allowed_methods:
            return jsonify({
                'success': False,
                'message': 'Mètode de pagament no vàlid'
            }), 400
        
        # Normalizar transferència a transferencia
        if metode_pagament == 'transferència':
            metode_pagament = 'transferencia'
        
        # Validar fecha
        try:
            dt = datetime.strptime(data_pagament, '%Y-%m-%d')
            valid_date = dt.strftime('%Y-%m-%d') == data_pagament
        except:
            valid_date = False
        
        # Validar campos obligatorios
        if id_faller <= 0 or not comentaris or quantitat <= 0 or not valid_date:
            return jsonify({
                'success': False,
                'message': 'Campos obligatorios incompletos o inválidos'
            }), 400
        
        # Obtener información del faller
        faller = Faller.get_by_id(id_faller)
        
        if not faller:
            return jsonify({
                'success': False,
                'message': 'Faller no trobat'
            }), 404
        
        edat = int(faller.get('edat', 0))
        grup = str(faller.get('grup', ''))
        
        # Calcular total a pagar
        total_pagament = calcular_total(grup, edat)
        
        # Obtener total aportado previamente
        total_aportat_previo = Pagament.get_total_aportat_by_faller(id_faller)
        
        # Calcular valores
        quantitat_actual = quantitat
        aportat_pagament_total = total_aportat_previo + quantitat_actual
        falta_per_aportar = max(0, round(total_pagament - aportat_pagament_total, 2))
        aportat_pagament = quantitat_actual  # Para este registro específico
        data_aportacio = data_pagament  # Por defecto, misma fecha
        
        # Preparar datos para insertar
        pagament_data = {
            'id_faller': id_faller,
            'comentaris': comentaris,
            'quantitat': quantitat,
            'data_pagament': data_pagament,
            'metode_pagament': metode_pagament,
            'total_pagament': total_pagament,
            'aportat_pagament': aportat_pagament,
            'falta_per_aportar': falta_per_aportar,
            'data_aportacio': data_aportacio
        }
        
        # Insertar pagament
        insert_id = Pagament.create(pagament_data)
        
        # Preparar respuesta
        response = {
            'success': True,
            'message': 'Pagament registrat correctament',
            'id': insert_id,
            'recibo': {
                'nom_complet': f"{faller['nom']} {faller['cognoms']}",
                'dni': faller['dni'],
                'comentaris': comentaris,
                'data_pagament': data_pagament,
                'metode_pagament': metode_pagament,
                'total_pagament': total_pagament,
                'aportat_anterior': total_aportat_previo,
                'quantitat_pagada': quantitat_actual,
                'total_aportat': aportat_pagament_total
            },
            'resum_pagament': {
                'faller': f"{faller['nom']} {faller['cognoms']}",
                'grup': grup,
                'edat': edat,
                'total_a_pagar': total_pagament,
                'aportat_previamente': total_aportat_previo,
                'aporte_actual': quantitat_actual,
                'total_aportado': aportat_pagament_total,
                'falta_por_aportar': falta_per_aportar,
                'porcentaje_completado': round((aportat_pagament_total / total_pagament) * 100, 2) if total_pagament > 0 else 0,
                'estado': 'COMPLETADO' if falta_per_aportar <= 0 else 'PENDIENTE'
            }
        }
        
        return jsonify(response), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@pagaments_bp.route('/info/<int:faller_id>', methods=['GET', 'OPTIONS'])
def get_info_faller_pagament(faller_id):
    """Obtener información de pagaments de un faller (info_faller_pagament.php)"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        info = Pagament.get_info_faller_pagament(faller_id)
        
        if not info:
            return jsonify({
                'success': False,
                'message': 'Faller no trobat'
            }), 404
        
        return jsonify({
            'success': True,
            'data': info
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
