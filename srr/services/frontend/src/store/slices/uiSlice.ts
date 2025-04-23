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
 * Gestion de l'état de l'interface utilisateur de l'application avec Redux.
 * Ce fichier centralise la gestion des éléments d'UI comme la barre latérale,
 * les notifications, l'état de chargement et les préférences de thème.
 *
 * [Source file design principles]
 * - Organisation séparée des états d'UI par composant fonctionnel
 * - Persistance sélective des préférences utilisateur (thème)
 * - Gestion des notifications avec états de lecture et temporisation
 * - Manipulation immutable de l'état via Redux Toolkit
 * - Indicateurs de chargement granulaires par section de l'application
 *
 * [Source file constraints]
 * - Ne doit pas contenir de logique métier ou d'appels API
 * - Utilise localStorage uniquement pour les préférences persistantes
 * - Doit rester découplé des slices métiers pour éviter les dépendances circulaires
 *
 * [Dependencies]
 * - @reduxjs/toolkit: Gestion d'état Redux simplifiée
 *
 * [GenAI tool change history]
 * 2025-04-23T10:58:00Z : Ajout du header GenAI et des commentaires de documentation par CodeAssistant
 * * Ajout du header de fichier conforme aux directives
 * * Ajout des commentaires de fonction avec les 3 sections requises
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

/**
 * [Class intent]
 * Interface définissant la structure de l'état de l'interface utilisateur.
 * 
 * [Design principles]
 * Séparation claire des différentes préoccupations UI.
 * Typage fort pour éviter les erreurs de manipulation d'état.
 * 
 * [Implementation details]
 * Regroupe les états relatifs à l'affichage, aux chargements,
 * aux notifications et aux préférences utilisateur.
 */
interface UiState {
  sidebarOpen: boolean;
  currentView: string;
  loading: {
    global: boolean;
    resources: boolean;
    bookings: boolean;
  };
  notifications: Notification[];
  theme: 'light' | 'dark';
}

/**
 * [Class intent]
 * Interface définissant la structure d'une notification système.
 * 
 * [Design principles]
 * Structure complète avec métadonnées pour le suivi et la gestion.
 * Types fortement typés pour la cohérence visuelle.
 * 
 * [Implementation details]
 * Inclut un identifiant unique, un type pour le style visuel,
 * un message, un timestamp et un état de lecture.
 */
interface Notification {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  timestamp: number;
  read: boolean;
}

/**
 * [Function intent]
 * État initial du slice d'interface utilisateur.
 * 
 * [Design principles]
 * Valeurs par défaut raisonnables pour une première visite.
 * Configuration de base qui s'applique à tous les utilisateurs.
 * 
 * [Implementation details]
 * Initialise la barre latérale ouverte, la vue sur le tableau de bord,
 * aucun chargement en cours, aucune notification et thème clair.
 */
const initialState: UiState = {
  sidebarOpen: true,
  currentView: 'dashboard',
  loading: {
    global: false,
    resources: false,
    bookings: false,
  },
  notifications: [],
  theme: 'light',
};

/**
 * [Class intent]
 * Configuration du slice Redux pour la gestion de l'état d'interface utilisateur.
 * 
 * [Design principles]
 * Organisation des actions UI par composant fonctionnel.
 * Mutations atomiques pour des changements d'état prévisibles.
 * 
 * [Implementation details]
 * Définit les reducers pour manipuler l'état UI comme la barre latérale,
 * les vues, les indicateurs de chargement, et les notifications.
 */
const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    /**
     * [Function intent]
     * Inverse l'état d'ouverture de la barre latérale.
     * 
     * [Design principles]
     * Action simple avec effet immédiat sur l'interface.
     * 
     * [Implementation details]
     * Bascule la propriété sidebarOpen entre true et false.
     */
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    /**
     * [Function intent]
     * Définit la vue actuellement affichée dans l'application.
     * 
     * [Design principles]
     * Action directe avec paramètre pour spécifier la vue cible.
     * 
     * [Implementation details]
     * Remplace la propriété currentView par la valeur fournie.
     */
    setCurrentView: (state, action: PayloadAction<string>) => {
      state.currentView = action.payload;
    },
    /**
     * [Function intent]
     * Définit l'état de chargement pour une section spécifique de l'application.
     * 
     * [Design principles]
     * Granularité fine permettant des indicateurs de chargement par section.
     * Typage fort pour éviter les erreurs sur les clés de chargement.
     * 
     * [Implementation details]
     * Met à jour une propriété spécifique de l'objet loading avec une valeur booléenne.
     */
    setLoading: (state, action: PayloadAction<{ key: keyof UiState['loading']; value: boolean }>) => {
      const { key, value } = action.payload;
      state.loading[key] = value;
    },
    /**
     * [Function intent]
     * Ajoute une nouvelle notification au système.
     * 
     * [Design principles]
     * Génération automatique des métadonnées pour simplifier l'usage.
     * Types de notifications standardisés pour la cohérence visuelle.
     * 
     * [Implementation details]
     * Crée un ID unique, ajoute un timestamp et définit l'état non lu par défaut.
     */
    addNotification: (state, action: PayloadAction<Omit<Notification, 'id' | 'timestamp' | 'read'>>) => {
      const id = `notification-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
      state.notifications.push({
        ...action.payload,
        id,
        timestamp: Date.now(),
        read: false,
      });
    },
    /**
     * [Function intent]
     * Marque une notification spécifique comme lue.
     * 
     * [Design principles]
     * Tracking de l'interaction utilisateur avec les notifications.
     * Ciblage par ID pour une manipulation précise.
     * 
     * [Implementation details]
     * Recherche la notification par ID et modifie sa propriété read à true.
     */
    markNotificationAsRead: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find(n => n.id === action.payload);
      if (notification) {
        notification.read = true;
      }
    },
    /**
     * [Function intent]
     * Supprime une notification du système.
     * 
     * [Design principles]
     * Nettoyage de l'interface des éléments non pertinents.
     * Ciblage par ID pour une suppression précise.
     * 
     * [Implementation details]
     * Filtre la liste des notifications pour exclure celle avec l'ID spécifié.
     */
    removeNotification: (state, action: PayloadAction<string>) => {
      state.notifications = state.notifications.filter(n => n.id !== action.payload);
    },
    /**
     * [Function intent]
     * Supprime toutes les notifications du système.
     * 
     * [Design principles]
     * Action de nettoyage globale pour réinitialiser l'état des notifications.
     * 
     * [Implementation details]
     * Remplace la liste des notifications par un tableau vide.
     */
    clearNotifications: (state) => {
      state.notifications = [];
    },
    /**
     * [Function intent]
     * Bascule entre les thèmes clair et sombre.
     * 
     * [Design principles]
     * Préférence utilisateur avec persistance entre sessions.
     * Interaction simple avec effet immédiat sur l'interface.
     * 
     * [Implementation details]
     * Inverse la propriété theme et persiste la valeur dans localStorage.
     */
    toggleTheme: (state) => {
      state.theme = state.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem('srr_theme', state.theme);
    },
    /**
     * [Function intent]
     * Définit explicitement un thème spécifique.
     * 
     * [Design principles]
     * Contrôle programmatique du thème avec persistance.
     * Types limités aux valeurs valides uniquement.
     * 
     * [Implementation details]
     * Remplace la propriété theme par la valeur fournie et persiste dans localStorage.
     */
    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload;
      localStorage.setItem('srr_theme', action.payload);
    },
  },
});

export const {
  toggleSidebar,
  setCurrentView,
  setLoading,
  addNotification,
  markNotificationAsRead,
  removeNotification,
  clearNotifications,
  toggleTheme,
  setTheme,
} = uiSlice.actions;

export default uiSlice.reducer;
