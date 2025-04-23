/**
 * IMPORTANT: This header comment is designed for GenAI code review and maintenance
 * Any GenAI tool working with this file MUST preserve and update this header
 *
 * [GenAI coding tool directive]
 * - Maintain this header with all modifications
 * - Update History section with each change
 * - Keep only the 4 most recent records in the history section. Sort from newer to older.
 * - Preserve Intent, Design, and Constraints sections
 * - Use this header as context for code reviews and modifications
 * - Ensure all changes align with the design principles
 * - Respect system prompt directives at all times
 *
 * [Source file intent]
 * Gestion de l'état des ressources dans l'application via Redux.
 * Ce fichier centralise la logique de récupération, filtrage et sélection des
 * ressources, facilitant l'accès aux données de ressources dans toute l'application.
 *
 * [Source file design principles]
 * - Séparation claire entre données, filtres et état de sélection
 * - Opérations asynchrones avec gestion d'état (loading, error)
 * - Filtrage dynamique côté client pour une UX réactive
 * - Structure normalisée des données de ressources
 * - Manipulation immutable via Redux Toolkit
 *
 * [Source file constraints]
 * - Dépend d'un service de ressources pour les appels API
 * - Ne doit pas excéder une complexité cyclomatique raisonnable pour les filtres
 * - Doit gérer les cas d'erreur réseau et serveur
 *
 * [Dependencies]
 * - @reduxjs/toolkit: Gestion d'état Redux simplifiée
 * - src/services/resourceService.ts: Service d'API pour les ressources
 *
 * [GenAI tool change history]
 * 2025-04-23T11:00:00Z : Ajout du header GenAI et des commentaires de documentation par CodeAssistant
 * * Ajout du header de fichier conforme aux directives
 * * Ajout des commentaires de fonction/classe avec les 3 sections requises
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import resourceService from '../../services/resourceService';

/**
 * [Class intent]
 * Types et interfaces pour la gestion des ressources.
 * 
 * [Design principles]
 * Typage fort pour garantir la cohérence et la manipulation des données de ressources.
 * 
 * [Implementation details]
 * Déclaration des interfaces pour les ressources, équipements et l'état global.
 */
// Types
/**
 * [Class intent]
 * Interface définissant une ressource réservable dans le système.
 * 
 * [Design principles]
 * Structure complète avec tous les attributs nécessaires pour l'affichage et la réservation.
 * 
 * [Implementation details]
 * Contient les identifiants, caractéristiques et méta-données de la ressource.
 */
export interface Resource {
  id: string;
  name: string;
  type: string;
  capacity: number;
  location: string;
  features: string[];
  email: string;
  calendar_id: string;
  status: string;
  created_at: string;
  manager: string;
}

/**
 * [Class intent]
 * Interface définissant un équipement associable à une ressource.
 * 
 * [Design principles]
 * Structure simple pour les caractéristiques d'équipements avec représentation visuelle.
 * 
 * [Implementation details]
 * Inclut identifiant, nom et icône pour l'affichage dans l'interface utilisateur.
 */
export interface Feature {
  id: string;
  name: string;
  icon: string;
}

/**
 * [Class intent]
 * Interface définissant l'état complet du slice de ressources.
 * 
 * [Design principles]
 * Organisation claire séparant données brutes, résultats filtrés et critères de filtrage.
 * 
 * [Implementation details]
 * Inclut collections de données, sélection courante, filtres et états de chargement.
 */
interface ResourcesState {
  resources: Resource[];
  features: Feature[];
  filteredResources: Resource[];
  selectedResource: Resource | null;
  filters: {
    type: string | null;
    features: string[];
    capacity: number | null;
    location: string | null;
    query: string;
  };
  loading: boolean;
  error: string | null;
}

/**
 * [Function intent]
 * État initial du slice de ressources.
 * 
 * [Design principles]
 * Structure complète avec valeurs par défaut cohérentes.
 * 
 * [Implementation details]
 * Initialise les collections vides et les filtres à leurs valeurs par défaut.
 */
// État initial
const initialState: ResourcesState = {
  resources: [],
  features: [],
  filteredResources: [],
  selectedResource: null,
  filters: {
    type: null,
    features: [],
    capacity: null,
    location: null,
    query: '',
  },
  loading: false,
  error: null,
};

/**
 * [Function intent]
 * Action asynchrone pour récupérer toutes les ressources.
 * 
 * [Design principles]
 * Gestion complète du cycle de vie d'une requête API avec gestion d'erreurs.
 * 
 * [Implementation details]
 * Utilise le service de ressources pour la récupération et transforme les erreurs API.
 */
// Thunks
export const fetchResources = createAsyncThunk(
  'resources/fetchResources',
  async (_, { rejectWithValue }) => {
    try {
      const response = await resourceService.getResources();
      return response;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Erreur lors de la récupération des ressources' });
    }
  }
);

/**
 * [Function intent]
 * Action asynchrone pour récupérer une ressource spécifique par son identifiant.
 * 
 * [Design principles]
 * Action dédiée pour les détails d'une ressource, permettant la mise à jour ciblée.
 * 
 * [Implementation details]
 * Utilise le service de ressources avec gestion d'erreurs spécifiques à cette opération.
 */
export const fetchResourceById = createAsyncThunk(
  'resources/fetchResourceById',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await resourceService.getResourceById(id);
      return response;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Erreur lors de la récupération de la ressource' });
    }
  }
);

/**
 * [Function intent]
 * Action asynchrone pour récupérer tous les équipements disponibles.
 * 
 * [Design principles]
 * Séparation des préoccupations pour les données de référence d'équipements.
 * 
 * [Implementation details]
 * Utilise le service de ressources avec gestion d'erreurs adaptée aux équipements.
 */
export const fetchFeatures = createAsyncThunk(
  'resources/fetchFeatures',
  async (_, { rejectWithValue }) => {
    try {
      const response = await resourceService.getFeatures();
      return response;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Erreur lors de la récupération des équipements' });
    }
  }
);

/**
 * [Class intent]
 * Configuration du slice Redux pour la gestion des ressources.
 * 
 * [Design principles]
 * Organisation claire des reducers et traitement des actions asynchrones.
 * 
 * [Implementation details]
 * Définit les reducers pour les filtres, la sélection et traite les résultats des actions API.
 */
// Slice
const resourcesSlice = createSlice({
  name: 'resources',
  initialState,
  reducers: {
    /**
     * [Function intent]
     * Applique un critère de filtrage spécifique aux ressources.
     * 
     * [Design principles]
     * Action générique pour tous types de filtres avec application immédiate.
     * 
     * [Implementation details]
     * Met à jour un filtre spécifique et recalcule les ressources filtrées.
     */
    setFilter: (state, action: PayloadAction<{ key: keyof ResourcesState['filters']; value: any }>) => {
      const { key, value } = action.payload;
      // @ts-ignore
      state.filters[key] = value;
      applyFilters(state);
    },
    /**
     * [Function intent]
     * Réinitialise tous les filtres à leurs valeurs par défaut.
     * 
     * [Design principles]
     * Action de nettoyage simple pour retourner à l'état initial des filtres.
     * 
     * [Implementation details]
     * Restaure les filtres par défaut et affiche toutes les ressources.
     */
    resetFilters: (state) => {
      state.filters = initialState.filters;
      state.filteredResources = state.resources;
    },
    /**
     * [Function intent]
     * Sélectionne une ressource par son ID ou annule la sélection.
     * 
     * [Design principles]
     * Action claire pour la navigation et l'affichage des détails.
     * 
     * [Implementation details]
     * Trouve la ressource correspondante ou définit null pour annuler la sélection.
     */
    selectResource: (state, action: PayloadAction<string | null>) => {
      if (action.payload === null) {
        state.selectedResource = null;
      } else {
        state.selectedResource = state.resources.find(r => r.id === action.payload) || null;
      }
    },
    /**
     * [Function intent]
     * Efface l'état d'erreur du slice.
     * 
     * [Design principles]
     * Action simple pour la récupération après erreur.
     * 
     * [Implementation details]
     * Réinitialise la propriété error à null.
     */
    clearError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchResources.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchResources.fulfilled, (state, action: PayloadAction<Resource[]>) => {
        state.loading = false;
        state.resources = action.payload;
        state.filteredResources = applyCurrentFilters(action.payload, state.filters);
      })
      .addCase(fetchResources.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Erreur lors de la récupération des ressources';
      })
      .addCase(fetchResourceById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchResourceById.fulfilled, (state, action: PayloadAction<Resource>) => {
        state.loading = false;
        state.selectedResource = action.payload;
        
        // Mise à jour de la ressource dans la liste si elle existe déjà
        const index = state.resources.findIndex(r => r.id === action.payload.id);
        if (index !== -1) {
          state.resources[index] = action.payload;
        } else {
          state.resources.push(action.payload);
        }
        
        state.filteredResources = applyCurrentFilters(state.resources, state.filters);
      })
      .addCase(fetchResourceById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Erreur lors de la récupération de la ressource';
      })
      .addCase(fetchFeatures.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchFeatures.fulfilled, (state, action: PayloadAction<Feature[]>) => {
        state.loading = false;
        state.features = action.payload;
      })
      .addCase(fetchFeatures.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Erreur lors de la récupération des équipements';
      });
  },
});

/**
 * [Function intent]
 * Applique les filtres actuels à la liste des ressources.
 * 
 * [Design principles]
 * Fonction utilitaire pour centraliser la logique de filtrage.
 * 
 * [Implementation details]
 * Met à jour filteredResources en utilisant la fonction applyCurrentFilters.
 */
// Fonction utilitaire pour appliquer les filtres
function applyFilters(state: ResourcesState) {
  state.filteredResources = applyCurrentFilters(state.resources, state.filters);
}

/**
 * [Function intent]
 * Applique un ensemble de filtres à une liste de ressources.
 * 
 * [Design principles]
 * Fonction pure pour le filtrage, applicable à n'importe quelle liste de ressources.
 * 
 * [Implementation details]
 * Implémente tous les filtres possibles avec une approche "early return".
 */
function applyCurrentFilters(resources: Resource[], filters: ResourcesState['filters']): Resource[] {
  return resources.filter(resource => {
    // Filtre par type
    if (filters.type && resource.type !== filters.type) {
      return false;
    }
    
    // Filtre par équipements
    if (filters.features.length > 0) {
      if (!filters.features.every(feature => resource.features.includes(feature))) {
        return false;
      }
    }
    
    // Filtre par capacité minimale
    if (filters.capacity && resource.capacity < filters.capacity) {
      return false;
    }
    
    // Filtre par localisation
    if (filters.location && !resource.location.toLowerCase().includes(filters.location.toLowerCase())) {
      return false;
    }
    
    // Filtre par recherche textuelle
    if (filters.query) {
      const query = filters.query.toLowerCase();
      return resource.name.toLowerCase().includes(query) || 
             resource.location.toLowerCase().includes(query) ||
             resource.type.toLowerCase().includes(query);
    }
    
    return true;
  });
}

export const { setFilter, resetFilters, selectResource, clearError } = resourcesSlice.actions;
export default resourcesSlice.reducer;
