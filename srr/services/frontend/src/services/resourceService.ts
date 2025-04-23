import apiClient from '../api/apiClient';
import { Resource, Feature } from '../store/slices/resourcesSlice';

/**
 * [Class intent]
 * Service de gestion des ressources (salles, équipements) pour le SRR.
 * 
 * [Design principles]
 * Interface claire et fonctionnelle pour simplifier l'intégration avec Redux.
 * Séparation des responsabilités pour une meilleure maintenabilité.
 * 
 * [Implementation details]
 * Utilise le client API centralisé pour toutes les requêtes liées aux ressources.
 */
const resourceService = {
  /**
   * [Function intent]
   * Récupère la liste de toutes les ressources disponibles.
   * 
   * [Design principles]
   * Interface simple avec filtrage optionnel côté serveur.
   * 
   * [Implementation details]
   * Effectue une requête GET vers l'API de ressources avec gestion des filtres optionnels.
   */
  getResources: async (filters?: Record<string, any>): Promise<Resource[]> => {
    const params = filters || {};
    const response = await apiClient.get<Resource[]>('/exchange/resources', { params });
    return response.data;
  },

  /**
   * [Function intent]
   * Récupère les détails d'une ressource spécifique.
   * 
   * [Design principles]
   * Interface simple basée sur l'identifiant unique de la ressource.
   * 
   * [Implementation details]
   * Effectue une requête GET vers l'API de ressources avec l'ID spécifié.
   */
  getResourceById: async (id: string): Promise<Resource> => {
    const response = await apiClient.get<Resource>(`/exchange/resources/${id}`);
    return response.data;
  },

  /**
   * [Function intent]
   * Récupère la liste de toutes les fonctionnalités/équipements disponibles.
   * 
   * [Design principles]
   * Interface simple pour récupérer les métadonnées des équipements.
   * 
   * [Implementation details]
   * Effectue une requête GET vers l'API des fonctionnalités.
   */
  getFeatures: async (): Promise<Feature[]> => {
    const response = await apiClient.get<Feature[]>('/exchange/features');
    return response.data;
  },

  /**
   * [Function intent]
   * Recherche des ressources en fonction de critères spécifiques.
   * 
   * [Design principles]
   * Interface flexible supportant de multiples critères de recherche.
   * 
   * [Implementation details]
   * Effectue une requête GET vers l'API de recherche avec les critères spécifiés.
   */
  searchResources: async (searchParams: {
    type?: string;
    features?: string[];
    capacity?: number;
    location?: string;
    query?: string;
  }): Promise<Resource[]> => {
    const response = await apiClient.get<Resource[]>('/exchange/resources', {
      params: {
        ...searchParams,
        features: searchParams.features?.join(','),
      }
    });
    return response.data;
  },

  /**
   * [Function intent]
   * Récupère les types de ressources disponibles.
   * 
   * [Design principles]
   * Interface simple pour récupérer les métadonnées des types de ressources.
   * 
   * [Implementation details]
   * Effectue une requête GET vers l'API des types de ressources.
   */
  getResourceTypes: async (): Promise<string[]> => {
    // Cette information pourrait être dérivée des données de ressources si l'API ne fournit pas d'endpoint spécifique
    const resources = await resourceService.getResources();
    // Extraire les types uniques
    const types = [...new Set(resources.map(r => r.type))];
    return types;
  },

  /**
   * [Function intent]
   * Récupère les localisations disponibles des ressources.
   * 
   * [Design principles]
   * Facilite le filtrage des ressources par localisation.
   * 
   * [Implementation details]
   * Dérive les informations depuis les données de ressources existantes.
   */
  getLocations: async (): Promise<string[]> => {
    // Cette information pourrait être dérivée des données de ressources
    const resources = await resourceService.getResources();
    // Extraire les localisations uniques
    const locations = [...new Set(resources.map(r => r.location))];
    return locations;
  }
};

export default resourceService;
