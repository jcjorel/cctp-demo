///////////////////////////////////////////////////////////////////////////////
// IMPORTANT: This header comment is designed for GenAI code review and maintenance
// Any GenAI tool working with this file MUST preserve and update this header
///////////////////////////////////////////////////////////////////////////////
// [GenAI coding tool directive]
// - Maintain this header with all modifications
// - Update History section with each change
// - Keep only the 4 most recent records in the history section. Sort from newer to older.
// - Preserve Intent, Design, and Constraints sections
// - Use this header as context for code reviews and modifications
// - Ensure all changes align with the design principles
// - Respect system prompt directives at all times
///////////////////////////////////////////////////////////////////////////////
// [Source file intent]
// Hooks React Query pour la gestion des types de ressources.
// Ces hooks facilitent l'interaction avec les endpoints API liés aux types
// de ressources depuis les composants React.
///////////////////////////////////////////////////////////////////////////////
// [Source file design principles]
// - Séparation des préoccupations avec un hook par opération
// - Gestion d'état cohérente via React Query
// - Abstraction des appels API directs pour simplifier l'usage dans les composants
// - Réutilisation pour éviter la duplication de code
///////////////////////////////////////////////////////////////////////////////
// [Source file constraints]
// - Utiliser exclusivement React Query pour les requêtes API
// - Doit être compatible avec la structure API du backend
// - Assurer la cohérence des types TypeScript
///////////////////////////////////////////////////////////////////////////////
// [Dependencies]
// - react-query: useQuery, useMutation, useQueryClient
// - app/api/apiClient: client API Axios
// - app/types: interfaces et types liés aux ressources
///////////////////////////////////////////////////////////////////////////////
// [GenAI tool change history]
// 2025-04-23T12:20:00Z : Création initiale des hooks React Query pour les types de ressources par CodeAssistant
// * Implémentation des hooks useResourceTypes, useResourceType, useCreateResourceType, etc.
// * Configuration des options de mise en cache et d'invalidation
///////////////////////////////////////////////////////////////////////////////

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../../api/apiClient';

// Types
export interface ResourceType {
  id: number;
  name: string;
  description?: string;
  icon?: string;
  color?: string;
}

export interface ResourceTypeCreate {
  name: string;
  description?: string;
  icon?: string;
  color?: string;
}

export interface ResourceTypeUpdate {
  name?: string;
  description?: string;
  icon?: string;
  color?: string;
}

// Clés de requête pour React Query
export const resourceTypesKeys = {
  all: ['resourceTypes'] as const,
  lists: () => [...resourceTypesKeys.all, 'list'] as const,
  list: (filters: Record<string, any>) => [...resourceTypesKeys.lists(), { ...filters }] as const,
  details: () => [...resourceTypesKeys.all, 'detail'] as const,
  detail: (id: number) => [...resourceTypesKeys.details(), id] as const,
};

/**
 * [Function intent]
 * Hook pour récupérer la liste des types de ressources disponibles.
 * 
 * [Design principles]
 * Utilisation de React Query pour la mise en cache automatique et le rechargement.
 * 
 * [Implementation details]
 * Effectue une requête GET vers /api/v1/resource-types avec gestion d'état React Query.
 */
export const useResourceTypes = (filters = {}) => {
  return useQuery(
    resourceTypesKeys.list(filters),
    async () => {
      const response = await apiClient.get('/resource-types', { params: filters });
      return response.data;
    },
    {
      staleTime: 5 * 60 * 1000, // 5 minutes - les types de ressources changent rarement
      keepPreviousData: true,
    }
  );
};

/**
 * [Function intent]
 * Hook pour récupérer les détails d'un type de ressource spécifique.
 * 
 * [Design principles]
 * Optimisé pour la récupération et la mise en cache des détails d'un seul type.
 * 
 * [Implementation details]
 * Effectue une requête GET vers /api/v1/resource-types/{id} avec mise en cache par ID.
 */
export const useResourceType = (id: number) => {
  return useQuery(
    resourceTypesKeys.detail(id),
    async () => {
      const response = await apiClient.get(`/resource-types/${id}`);
      return response.data;
    },
    {
      enabled: !!id, // N'exécute pas la requête si id n'est pas défini
      staleTime: 10 * 60 * 1000, // 10 minutes
    }
  );
};

/**
 * [Function intent]
 * Hook pour créer un nouveau type de ressource.
 * 
 * [Design principles]
 * Utilise la mutation React Query avec invalidation automatique du cache.
 * 
 * [Implementation details]
 * Effectue une requête POST vers /api/v1/resource-types et invalide les requêtes de liste.
 */
export const useCreateResourceType = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    async (resourceType: ResourceTypeCreate) => {
      const response = await apiClient.post('/resource-types', resourceType);
      return response.data;
    },
    {
      onSuccess: () => {
        // Invalide la liste des types de ressources pour forcer un rechargement
        queryClient.invalidateQueries(resourceTypesKeys.lists());
      },
    }
  );
};

/**
 * [Function intent]
 * Hook pour mettre à jour un type de ressource existant.
 * 
 * [Design principles]
 * Combine mutation et invalidation ciblée du cache.
 * 
 * [Implementation details]
 * Effectue une requête PUT vers /api/v1/resource-types/{id} et invalide les requêtes associées.
 */
export const useUpdateResourceType = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    async ({ id, data }: { id: number; data: ResourceTypeUpdate }) => {
      const response = await apiClient.put(`/resource-types/${id}`, data);
      return response.data;
    },
    {
      onSuccess: (data: ResourceType) => {
        // Invalide à la fois la requête de détail spécifique et la liste
        queryClient.invalidateQueries(resourceTypesKeys.detail(data.id));
        queryClient.invalidateQueries(resourceTypesKeys.lists());
      },
    }
  );
};

/**
 * [Function intent]
 * Hook pour supprimer un type de ressource.
 * 
 * [Design principles]
 * Gestion de la suppression avec mise à jour optimiste du cache possible.
 * 
 * [Implementation details]
 * Effectue une requête DELETE vers /api/v1/resource-types/{id} et invalide les requêtes associées.
 */
export const useDeleteResourceType = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    async (id: number) => {
      await apiClient.delete(`/resource-types/${id}`);
      return id;
    },
    {
      onSuccess: (id: number) => {
        // Invalide à la fois la requête de détail spécifique et la liste
        queryClient.invalidateQueries(resourceTypesKeys.detail(id));
        queryClient.invalidateQueries(resourceTypesKeys.lists());
      },
    }
  );
};
