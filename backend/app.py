"""
Aplicación principal Flask - Backend Python para Gestió Falla Pare Castells
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# Importar blueprints
from routes.fallers import fallers_bp
from routes.pagaments import pagaments_bp
from routes.stats import stats_bp


def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Deshabilitar redirecciones automáticas de trailing slash
    app.url_map.strict_slashes = False
    
    # Configurar CORS de forma más permisiva para desarrollo
    CORS(app)
    
    # Añadir headers CORS manualmente para asegurar compatibilidad
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Registrar blueprints
    app.register_blueprint(fallers_bp)
    app.register_blueprint(pagaments_bp)
    app.register_blueprint(stats_bp)
    
    # Ruta de salud del servidor
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Endpoint para verificar que el servidor está funcionando"""
        return jsonify({
            'status': 'ok',
            'message': 'Backend Python Flask funcionando correctamente'
        }), 200
    
    # Ruta raíz
    @app.route('/', methods=['GET'])
    def index():
        """Endpoint raíz con información de la API"""
        return jsonify({
            'message': 'API Backend - Gestió Falla Pare Castells',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'fallers': '/api/fallers',
                'pagaments': '/api/pagaments',
                'stats': '/api/stats'
            }
        }), 200
    
    # Manejador de errores 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint no encontrado'
        }), 404
    
    # Manejador de errores 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
