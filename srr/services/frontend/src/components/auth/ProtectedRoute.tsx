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
 * Composant React qui protège les routes nécessitant une authentification.
 * Ce fichier empêche les utilisateurs non authentifiés d'accéder aux parties
 * protégées de l'application et les redirige vers la page de connexion.
 *
 * [Source file design principles]
 * - Protection des routes basée sur l'état d'authentification
 * - Conservation du contexte de navigation pour redirection après connexion
 * - Utilisation des hooks React Router pour la gestion des routes
 * - Séparation claire entre la logique d'authentification et le rendu
 *
 * [Source file constraints]
 * - Dépend de l'état global d'authentification (Redux)
 * - Fonctionne avec React Router v6+ uniquement
 * - Doit être utilisé comme wrapper dans la configuration des routes
 *
 * [Dependencies]
 * - react-router-dom: Gestion du routage et de la navigation
 * - src/hooks/index.ts: Hooks personnalisés pour accéder à l'état Redux
 *
 * [GenAI tool change history]
 * 2025-04-23T11:03:00Z : Ajout du header GenAI par CodeAssistant
 * * Ajout du header de fichier conforme aux directives
 */

import React, { useEffect } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAppSelector } from '../../hooks';

/**
 * [Function intent]
 * Composant de protection des routes nécessitant une authentification.
 * 
 * [Design principles]
 * Sécurisation des routes selon l'état d'authentification de l'utilisateur.
 * Redirection automatique vers la page de connexion si non authentifié.
 * 
 * [Implementation details]
 * Utilise le state Redux pour vérifier l'authentification et React Router pour la redirection.
 * Conserve l'emplacement actuel pour rediriger l'utilisateur après connexion.
 */
const ProtectedRoute: React.FC = () => {
  const { isAuthenticated } = useAppSelector(state => state.auth);
  const location = useLocation();
  
  // Si l'utilisateur n'est pas authentifié, rediriger vers la page de connexion
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Sinon, afficher les routes enfants
  return <Outlet />;
};

export default ProtectedRoute;
