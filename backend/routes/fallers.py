"""
Rutas para la gestión de fallers
"""
from flask import Blueprint, request, jsonify
from models.faller import Faller

fallers_bp = Blueprint('fallers', __name__, url_prefix='/api/fallers')


@fallers_bp.route('/', methods=['GET', 'OPTIONS'])
def get_fallers():
    """Obtener todos los fallers (llista_fallers.php)"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        fallers = Faller.get_all()
        return jsonify({
            'success': True,
            'count': len(fallers),
            'data': fallers,
            'message': 'Fallers obtenidos correctamente'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error del servidor: {str(e)}',
            'data': []
        }), 500


@fallers_bp.route('/<int:faller_id>', methods=['GET', 'OPTIONS'])
def get_faller(faller_id):
    """Obtener un faller por ID (obtenir_faller.php)"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        faller = Faller.get_by_id(faller_id)
        
        if not faller:
            return jsonify({
                'success': False,
                'message': 'Faller no trobat'
            }), 404
        
        return jsonify({
            'success': True,
            'faller': faller
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@fallers_bp.route('/', methods=['POST'])
def create_faller():
    """Crear un nuevo faller (insertar_fallers.php)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'JSON incorrecto'
            }), 400
        
        # Mapear posibles nombres de campos (catalán/español/inglés)
        mapped_data = {
            'nom': data.get('nom') or data.get('nombre') or data.get('name', ''),
            'cognoms': data.get('cognoms') or data.get('apellidos') or data.get('lastname', ''),
            'domicili': data.get('domicili') or data.get('domicilio') or data.get('address', ''),
            'telefon': data.get('telefon') or data.get('telefono') or data.get('phone', ''),
            'dni': data.get('dni') or data.get('nif') or data.get('documento', ''),
            'data_naixement': data.get('data_naixement') or data.get('fecha_nacimiento') or data.get('birth_date', ''),
            'email': data.get('email', ''),
            'edat': data.get('edat') or data.get('edad') or data.get('age'),
            'grup': data.get('grup') or data.get('grupo') or data.get('grupo_colaborador') or data.get('group', ''),
            'colaborador': data.get('colaborador') or data.get('colaborator') or data.get('is_colaborador', 0),
            'data_alta': data.get('data_alta') or data.get('fecha_alta') or data.get('signup_date', ''),
            'categoria': data.get('categoria') or data.get('category', 'Home')
        }
        
        # Validación de campos obligatorios
        required = ['nom', 'cognoms', 'domicili', 'telefon', 'dni', 
                   'data_naixement', 'email', 'edat', 'grup', 'data_alta']
        missing = [field for field in required if not mapped_data.get(field)]
        
        if missing:
            return jsonify({
                'success': False,
                'message': f'Faltan campos obligatorios: {", ".join(missing)}'
            }), 400
        
        # Crear faller
        insert_id = Faller.create(mapped_data)
        
        return jsonify({
            'success': True,
            'message': 'Registro insertado',
            'insert_id': insert_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@fallers_bp.route('/<int:faller_id>', methods=['POST', 'PUT'])
def update_faller(faller_id):
    """Actualizar un faller (modificar_faller.php)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'JSON inválido'
            }), 400
        
        # Preparar datos para actualización
        update_data = {
            'nom': data.get('nom', ''),
            'cognoms': data.get('cognoms', ''),
            'domicili': data.get('domicili', ''),
            'telefon': data.get('telefon', ''),
            'dni': data.get('dni', ''),
            'data_naixement': data.get('data_naixement', ''),
            'email': data.get('email', ''),
            'edat': data.get('edat'),
            'grup': data.get('grup', ''),
            'colaborador': data.get('colaborador', 0),
            'data_alta': data.get('data_alta', ''),
            'categoria': data.get('categoria', 'Home')
        }
        
        affected = Faller.update(faller_id, update_data)
        
        return jsonify({
            'success': True,
            'message': 'Actualizado',
            'affected': affected
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@fallers_bp.route('/<int:faller_id>', methods=['DELETE'])
def delete_faller(faller_id):
    """Eliminar un faller"""
    try:
        affected = Faller.delete(faller_id)
        
        if affected == 0:
            return jsonify({
                'success': False,
                'message': 'Faller no trobat'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Faller eliminat correctament',
            'affected': affected
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
