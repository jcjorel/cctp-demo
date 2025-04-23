import axios, { AxiosRequestConfig } from 'axios';

/**
 * [Function intent]
 * Configure et exporte un client Axios avec les paramètres par défaut pour le SRR.
 * 
 * [Design principles]
 * Point d'accès centralisé pour toutes les requêtes API.
 * Configuration commune pour tous les appels HTTP.
 * 
 * [Implementation details]
 * Utilise Axios avec des intercepteurs pour la gestion des jetons et des erreurs.
 */

// Récupération de l'URL de base de l'API depuis les variables d'environnement
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Configuration de base du client API
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 secondes de timeout par défaut
});

// Intercepteur pour ajouter le token d'authentification aux requêtes
apiClient.interceptors.request.use(
  (config: AxiosRequestConfig): AxiosRequestConfig => {
    const token = localStorage.getItem('srr_token');
    if (token && config.headers) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs de réponse
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Si l'erreur est due à un token expiré (401)
    if (error.response && error.response.status === 401) {
      // Vérifie que nous ne sommes pas déjà en train d'essayer de rafraîchir le token
      const isRefreshingToken = error.config.url === '/api/auth/refresh-token';
      
      if (!isRefreshingToken) {
        // Si nous ne sommes pas sur la page de login
        if (window.location.pathname !== '/login') {
          // Tenter de rafraîchir le token ou rediriger vers la page de login
          localStorage.removeItem('srr_token');
          localStorage.removeItem('srr_user');
          window.location.href = '/login';
        }
      }
    }
    
    // Gestion des erreurs réseau
    if (!error.response) {
      console.error('Erreur réseau:', error);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
