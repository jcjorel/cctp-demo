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
 * Gestion de l'état d'authentification de l'application avec Redux.
 * Ce fichier centralise toute la logique liée à l'authentification, y compris
 * la connexion, déconnexion, rafraîchissement de token, et la gestion des états
 * d'authentification dans l'application.
 *
 * [Source file design principles]
 * - Séparation claire des préoccupations entre état, actions et services
 * - Validation et gestion des tokens JWT
 * - Persistance locale de l'état d'authentification
 * - Gestion immutable de l'état via Redux Toolkit
 * - Opérations asynchrones avec feedback d'état (loading, error)
 *
 * [Source file constraints]
 * - Dépend d'un service d'authentification pour les appels API
 * - Utilise localStorage pour la persistence entre rechargements
 * - Doit gérer les tokens expirés et les erreurs d'authentification
 *
 * [Dependencies]
 * - @reduxjs/toolkit: Gestion d'état Redux simplifiée
 * - jwt-decode: Décodage et validation des tokens JWT
 * - src/services/authService.ts: Service d'API pour l'authentification
 *
 * [GenAI tool change history]
 * 2025-04-23T10:57:00Z : Ajout du header GenAI et des commentaires de documentation par CodeAssistant
 * * Ajout du header de fichier conforme aux directives
 * * Ajout des commentaires de fonction avec les 3 sections requises
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { jwtDecode } from 'jwt-decode';
import authService from '../../services/authService';

/**
 * [Class intent]
 * Types et interfaces pour la gestion de l'authentification.
 * 
 * [Design principles]
 * Typage fort pour éviter les erreurs et assurer la cohérence des données.
 * 
 * [Implementation details]
 * Définition des interfaces utilisateur, payload JWT et état d'authentification.
 */
// Types
export interface User {
  username: string;
  email: string;
  full_name: string;
  role: string;
  department: string;
  groups: string[];
}

interface JwtPayload {
  sub: string;
  exp: number;
  role: string;
  groups: string[];
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

/**
 * [Function intent]
 * État initial du slice d'authentification.
 * 
 * [Design principles]
 * Restauration de l'état depuis le stockage local pour la persistance.
 * 
 * [Implementation details]
 * Vérifie la présence d'un token dans le localStorage pour déterminer l'état d'authentification initial.
 */
// État initial
const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('srr_token'),
  isAuthenticated: !!localStorage.getItem('srr_token'),
  loading: false,
  error: null,
};

/**
 * [Function intent]
 * Action asynchrone pour authentifier un utilisateur avec ses identifiants.
 * 
 * [Design principles]
 * Gestion des erreurs et informations d'état centralisée.
 * Interface unifiée pour toutes les opérations d'authentification.
 * 
 * [Implementation details]
 * Utilise le service d'authentification pour faire une requête API,
 * stocke le token et les informations utilisateur en cas de succès.
 */
// Thunks
export const login = createAsyncThunk(
  'auth/login',
  async (credentials: { username: string; password: string }, { rejectWithValue }) => {
    try {
      const response = await authService.login(credentials.username, credentials.password);
      return response;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Une erreur est survenue lors de la connexion' });
    }
  }
);

/**
 * [Function intent]
 * Action asynchrone pour déconnecter l'utilisateur.
 * 
 * [Design principles]
 * Opération simple et directe sans état complexe.
 * 
 * [Implementation details]
 * Appelle le service de déconnexion et nettoie l'état d'authentification.
 */
export const logout = createAsyncThunk('auth/logout', async () => {
  await authService.logout();
  return null;
});

/**
 * [Function intent]
 * Action asynchrone pour rafraîchir un token d'authentification expiré.
 * 
 * [Design principles]
 * Renouvellement transparent du token sans déconnecter l'utilisateur.
 * Gestion robuste des cas d'erreur.
 * 
 * [Implementation details]
 * Vérifie l'existence d'un token, demande son renouvellement via le service
 * et met à jour le stockage local en cas de succès.
 */
export const refreshToken = createAsyncThunk('auth/refreshToken', async (_, { getState, rejectWithValue }) => {
  try {
    // @ts-ignore
    const { auth } = getState();
    if (!auth.token) {
      return rejectWithValue('Aucun token à rafraîchir');
    }
    
    const response = await authService.refreshToken();
    return response;
  } catch (error: any) {
    return rejectWithValue('Échec du rafraîchissement du token');
  }
});

/**
 * [Class intent]
 * Configuration du slice Redux pour la gestion de l'état d'authentification.
 * 
 * [Design principles]
 * Organisation de l'état par domaine fonctionnel.
 * Mutations immutables de l'état pour tracer les changements.
 * 
 * [Implementation details]
 * Définit les reducers pour manipuler l'état et les extraReducers
 * pour gérer les résultats des opérations asynchrones.
 */
// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    /**
     * [Function intent]
     * Réinitialise l'état d'erreur du slice.
     * 
     * [Design principles]
     * Simple reset d'un état spécifique.
     * 
     * [Implementation details]
     * Met la propriété error à null.
     */
    clearError: (state) => {
      state.error = null;
    },
    /**
     * [Function intent]
     * Vérifie si le token JWT actuel est expiré.
     * 
     * [Design principles]
     * Validation proactive pour éviter les requêtes avec un token invalide.
     * 
     * [Implementation details]
     * Décode le token, compare son timestamp d'expiration avec l'heure actuelle,
     * et réinitialise l'état d'authentification si nécessaire.
     */
    checkTokenExpiration: (state) => {
      if (state.token) {
        try {
          const decoded = jwtDecode<JwtPayload>(state.token);
          const currentTime = Date.now() / 1000;
          
          if (decoded.exp < currentTime) {
            // Token expiré
            state.token = null;
            state.user = null;
            state.isAuthenticated = false;
            localStorage.removeItem('srr_token');
            localStorage.removeItem('srr_user');
          }
        } catch (error) {
          // Token invalide
          state.token = null;
          state.user = null;
          state.isAuthenticated = false;
          localStorage.removeItem('srr_token');
          localStorage.removeItem('srr_user');
        }
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action: PayloadAction<{ token: string; user: User }>) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.token = action.payload.token;
        state.user = action.payload.user;
        localStorage.setItem('srr_token', action.payload.token);
        localStorage.setItem('srr_user', JSON.stringify(action.payload.user));
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Identifiants invalides';
      })
      .addCase(logout.fulfilled, (state) => {
        state.user = null;
        state.token = null;
        state.isAuthenticated = false;
        localStorage.removeItem('srr_token');
        localStorage.removeItem('srr_user');
      })
      .addCase(refreshToken.fulfilled, (state, action: PayloadAction<{ token: string }>) => {
        state.token = action.payload.token;
        localStorage.setItem('srr_token', action.payload.token);
      })
      .addCase(refreshToken.rejected, (state) => {
        state.user = null;
        state.token = null;
        state.isAuthenticated = false;
        localStorage.removeItem('srr_token');
        localStorage.removeItem('srr_user');
      });
  },
});

export const { clearError, checkTokenExpiration } = authSlice.actions;
export default authSlice.reducer;
