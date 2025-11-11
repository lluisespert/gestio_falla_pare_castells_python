/**
 * Configuración de la API - Backend Python Flask
 */

// URL base de la API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

/**
 * Endpoints de la API
 */
export const API_ENDPOINTS = {
    // Health check
    health: `${API_BASE_URL}/health`,
    
    // Fallers
    fallers: `${API_BASE_URL}/fallers`,
    getFaller: (id) => `${API_BASE_URL}/fallers/${id}`,
    createFaller: `${API_BASE_URL}/fallers`,
    updateFaller: (id) => `${API_BASE_URL}/fallers/${id}`,
    deleteFaller: (id) => `${API_BASE_URL}/fallers/${id}`,
    
    // Pagaments
    pagaments: `${API_BASE_URL}/pagaments`,
    createPagament: `${API_BASE_URL}/pagaments`,
    infoFallerPagament: (id) => `${API_BASE_URL}/pagaments/info/${id}`,
    
    // Estadísticas
    percentatge: `${API_BASE_URL}/stats/percentatge`,
    totalQuotes: `${API_BASE_URL}/stats/total-quotes`,
};

export default API_ENDPOINTS;
