"""
Rutas para estadísticas y consultas agregadas
"""
from flask import Blueprint, request, jsonify
from models.stats import Stats

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')


@stats_bp.route('/percentatge', methods=['GET', 'OPTIONS'])
def get_percentatge():
    """
    Obtener fallers agrupados por su porcentaje de pago (percentatge.php)
    Separa en dos grupos: con 80% o más y menos del 80%
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = Stats.get_percentatge()
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error en la consulta: {str(e)}'
        }), 500


@stats_bp.route('/total-quotes', methods=['GET', 'OPTIONS'])
def get_total_quotes():
    """
    Obtener totales agregados de pagaments (total_quotes.php)
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = Stats.get_total_quotes()
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error en la consulta: {str(e)}'
        }), 500
