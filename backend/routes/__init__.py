"""
Inicialización del paquete routes
"""
from routes.fallers import fallers_bp
from routes.pagaments import pagaments_bp
from routes.stats import stats_bp

__all__ = ['fallers_bp', 'pagaments_bp', 'stats_bp']
