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
// Point d'entrée pour tous les hooks API du SRR.
// Ce fichier centralise les exports des différents hooks React Query
// pour faciliter leur importation et utilisation dans les composants.
///////////////////////////////////////////////////////////////////////////////
// [Source file design principles]
// - Organisation claire des exports par domaine fonctionnel
// - Point d'accès unique pour tous les hooks liés à l'API
// - Facilitation des imports dans les composants consommateurs
///////////////////////////////////////////////////////////////////////////////
// [Source file constraints]
// - Ne pas contenir d'implémentation de hooks, seulement des re-exports
// - Maintenir une organisation cohérente par domaine fonctionnel
///////////////////////////////////////////////////////////////////////////////
// [Dependencies]
// - hooks/api/useResourceTypes: hooks pour les types de ressources
///////////////////////////////////////////////////////////////////////////////
// [GenAI tool change history]
// 2025-04-23T12:25:41Z : Création initiale du point d'entrée pour les hooks API par CodeAssistant
// * Export des hooks pour les types de ressources
///////////////////////////////////////////////////////////////////////////////

// Exports des hooks pour les types de ressources
export {
  useResourceTypes,
  useResourceType,
  useCreateResourceType,
  useUpdateResourceType,
  useDeleteResourceType,
  type ResourceType,
  type ResourceTypeCreate,
  type ResourceTypeUpdate
} from './useResourceTypes';

// Exports des hooks pour les ressources
// TODO: Ajouter les exports pour les hooks de ressources une fois implémentés

// Exports des hooks pour les réservations
// TODO: Ajouter les exports pour les hooks de réservations une fois implémentés

// Exports des hooks pour les utilisateurs
// TODO: Ajouter les exports pour les hooks d'utilisateurs une fois implémentés
