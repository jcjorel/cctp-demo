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
 * Gestion de l'état des réservations dans l'application via Redux.
 * Ce fichier centralise la logique de réservation, incluant la création,
 * modification, consultation et vérification de disponibilité des ressources.
 *
 * [Source file design principles]
 * - Organisation par catégories de réservations (toutes, utilisateur, ressource)
 * - Gestion atomique des opérations asynchrones (loading, error)
 * - Vérification de disponibilité avant création
 * - Mise à jour cohérente dans toutes les listes après modification
 * - Manipulation immutable via Redux Toolkit
 *
 * [Source file constraints]
 * - Dépend d'un service de réservation pour les appels API
 * - Doit maintenir la cohérence entre les différentes vues de réservation
 * - Doit gérer les cas d'erreur réseau et serveur
 * - Maintient plusieurs représentations des mêmes données (par ressource, par utilisateur)
 *
 * [Dependencies]
 * - @reduxjs/toolkit: Gestion d'état Redux simplifiée
 * - src/services/bookingService.ts: Service d'API pour les réservations
 *
 * [GenAI tool change history]
 * 2025-04-23T11:01:00Z : Ajout du header GenAI et des commentaires de documentation par CodeAssistant
 * * Ajout du header de fichier conforme aux directives
 * * Ajout des commentaires de fonction/classe avec les 3 sections requises
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import bookingService from '../../services/bookingService';

/**
 * [Class intent]
 * Types et interfaces pour la gestion des réservations.
 * 
 * [Design principles]
 * Typage fort pour garantir la cohérence des données de réservation.
 * 
 * [Implementation details]
 * Déclaration des interfaces pour les réservations et l'état associé.
 */
// Types
/**
 * [Class intent]
 * Interface définissant une réservation de ressource dans le système.
 * 
 * [Design principles]
 * Structure complète avec tous les attributs nécessaires au cycle de vie d'une réservation.
 * 
 * [Implementation details]
 * Inclut identifiants, plages horaires, participants, statut et métadonnées.
 */
export interface Booking {
  id: string;
  resource_id: string;
  user_id: string;
  title: string;
  start_time: string;
  end_time: string;
  status: 'pending' | 'confirmed' | 'cancelled';
  attendees: string[];
  created_at: string;
  description?: string;
}

/**
 * [Class intent]
 * Interface définissant la réponse à une vérification de disponibilité.
 * 
 * [Design principles]
 * Structure informative incluant les causes d'indisponibilité.
 * 
 * [Implementation details]
 * Indique la disponibilité, la raison si indisponible et le conflit éventuel.
 */
export interface AvailabilityResponse {
  available: boolean;
  reason?: string;
  conflicting_booking?: Booking;
}

/**
 * [Class intent]
 * Interface définissant une demande de réservation.
 * 
 * [Design principles]
 * Structure contenant les informations minimales requises pour créer une réservation.
 * 
 * [Implementation details]
 * Inclut ressource cible, titre, horaires, participants et description optionnelle.
 */
export interface BookingRequest {
  resource_id: string;
  title: string;
  start_time: Date;
  end_time: Date;
  attendees: string[];
  description?: string;
}

/**
 * [Class intent]
 * Interface définissant l'état complet des réservations dans l'application.
 * 
 * [Design principles]
 * Organisation multi-vues pour accéder aux réservations selon différents contextes.
 * 
 * [Implementation details]
 * Inclut listes globale, par utilisateur, par ressource, et état des vérifications de disponibilité.
 */
interface BookingsState {
  bookings: Booking[];
  userBookings: Booking[];
  resourceBookings: Record<string, Booking[]>;
  selectedBooking: Booking | null;
  availabilityChecks: Record<string, AvailabilityResponse>;
  loading: boolean;
  error: string | null;
}

/**
 * [Function intent]
 * État initial du slice de réservations.
 * 
 * [Design principles]
 * Structure complète avec collections vides et états neutres.
 * 
 * [Implementation details]
 * Initialise toutes les collections de réservations et les indicateurs d'état.
 */
// État initial
const initialState: BookingsState = {
  bookings: [],
  userBookings: [],
  resourceBookings: {},
  selectedBooking: null,
  availabilityChecks: {},
  loading: false,
  error: null,
};

/**
 * [Function intent]
 * Action asynchrone pour récupérer toutes les réservations.
 * 
 * [Design principles]
 * Action de base pour charger la vue globale des réservations.
 * 
 * [Implementation details]
 * Utilise le service de réservation avec gestion d'erreurs adaptée.
 */
// Thunks
export const fetchBookings = createAsyncThunk(
  'bookings/fetchBookings',
  async (_, { rejectWithValue }) => {
    try {
      const response = await bookingService.getBookings();
      return response;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Erreur lors de la récupération des réservations' });
    }
  }
);

/**
 * [Function intent]
 * Action asynchrone pour récupérer les réservations d'un utilisateur spécifique.
 * 
 * [Design principles]
 * Action ciblée pour afficher l'historique ou les réservations à venir d'un utilisateur.
 * 
 * [Implementation details]
 * Utilise le service de réservation avec filtrage par utilisateur.
 */
export const fetchUserBookings = createAsyncThunk(
  'bookings/fetchUserBookings',
  async (userId: string, { rejectWithValue }) => {
    try {
      const response = await bookingService.getUserBookings(userId);
      return response;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Erreur lors de la récupération des réservations utilisateur' });
    }
  }
);

/**
 * [Function intent]
 * Action asynchrone pour récupérer les réservations d'une ressource spécifique.
 * 
 * [Design principles]
 * Action ciblée pour afficher le planning d'une ressource.
 * 
 * [Implementation details]
 * Utilise le service de réservation avec filtrage par ressource et structure de retour enrichie.
 */
export const fetchResourceBookings = createAsyncThunk(
  'bookings/fetchResourceBookings',
  async (resourceId: string, { rejectWithValue }) => {
    try {
      const response = await bookingService.getResourceBookings(resourceId);
      return {
        resourceId,
        bookings: response,
      };
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Erreur lors de la récupération des réservations de la ressource' });
    }
  }
);

/**
 * [Function intent]
 * Action asynchrone pour vérifier la disponibilité d'une ressource sur une période.
 * 
 * [Design principles]
 * Validation préalable avant de permettre une réservation.
 * 
 * [Implementation details]
 * Vérifie les conflits potentiels et génère une clé unique pour stocker le résultat.
 */
export const checkAvailability = createAsyncThunk(
  'bookings/checkAvailability',
  async (params: { resourceId: string, startTime: Date, endTime: Date }, { rejectWithValue }) => {
    try {
      const { resourceId, startTime, endTime } = params;
      const response = await bookingService.checkAvailability(resourceId, startTime, endTime);
      return {
        resourceId,
        availabilityCheck: response,
        key: `${resourceId}-${startTime.toISOString()}-${endTime.toISOString()}`,
      };
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Erreur lors de la vérification de disponibilité' });
    }
  }
);

/**
 * [Function intent]
 * Action asynchrone pour créer une nouvelle réservation.
 * 
 * [Design principles]
 * Opération principale du module avec mise à jour immédiate de l'état.
 * 
 * [Implementation details]
 * Crée la réservation via le service et met à jour les différentes listes.
 */
export const createBooking = createAsyncThunk(
  'bookings/createBooking',
  async (bookingRequest: BookingRequest, { rejectWithValue }) => {
    try {
      const response = await bookingService.createBooking(bookingRequest);
      return response;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Erreur lors de la création de la réservation' });
    }
  }
);

/**
 * [Function intent]
 * Action asynchrone pour modifier le statut d'une réservation existante.
 * 
 * [Design principles]
 * Gestion du cycle de vie des réservations (confirmation, annulation).
 * 
 * [Implementation details]
 * Met à jour le statut via le service et propage la modification dans toutes les vues.
 */
export const updateBookingStatus = createAsyncThunk(
  'bookings/updateBookingStatus',
  async (params: { bookingId: string, status: 'confirmed' | 'cancelled' }, { rejectWithValue }) => {
    try {
      const { bookingId, status } = params;
      const response = await bookingService.updateBookingStatus(bookingId, status);
      return response;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({ message: 'Erreur lors de la mise à jour de la réservation' });
    }
  }
);

/**
 * [Class intent]
 * Configuration du slice Redux pour la gestion des réservations.
 * 
 * [Design principles]
 * Organisation claire des reducers et traitement des actions asynchrones.
 * 
 * [Implementation details]
 * Définit les reducers pour les opérations locales et les extraReducers pour les actions API.
 */
// Slice
const bookingsSlice = createSlice({
  name: 'bookings',
  initialState,
  reducers: {
    /**
     * [Function intent]
     * Sélectionne une réservation par son ID ou annule la sélection.
     * 
     * [Design principles]
     * Action simple pour la navigation et l'affichage des détails.
     * 
     * [Implementation details]
     * Trouve la réservation correspondante ou définit null pour annuler la sélection.
     */
    selectBooking: (state, action: PayloadAction<string | null>) => {
      if (action.payload === null) {
        state.selectedBooking = null;
      } else {
        state.selectedBooking = state.bookings.find(b => b.id === action.payload) || null;
      }
    },
    /**
     * [Function intent]
     * Supprime une vérification de disponibilité spécifique.
     * 
     * [Design principles]
     * Nettoyage ciblé des vérifications obsolètes.
     * 
     * [Implementation details]
     * Supprime l'entrée correspondant à la clé fournie du dictionnaire des vérifications.
     */
    clearAvailabilityCheck: (state, action: PayloadAction<string>) => {
      delete state.availabilityChecks[action.payload];
    },
    /**
     * [Function intent]
     * Supprime toutes les vérifications de disponibilité.
     * 
     * [Design principles]
     * Nettoyage global des vérifications au changement de contexte.
     * 
     * [Implementation details]
     * Réinitialise le dictionnaire des vérifications à un objet vide.
     */
    clearAllAvailabilityChecks: (state) => {
      state.availabilityChecks = {};
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
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch all bookings
      .addCase(fetchBookings.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchBookings.fulfilled, (state, action: PayloadAction<Booking[]>) => {
        state.loading = false;
        state.bookings = action.payload;
      })
      .addCase(fetchBookings.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Erreur lors de la récupération des réservations';
      })
      
      // Fetch user bookings
      .addCase(fetchUserBookings.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUserBookings.fulfilled, (state, action: PayloadAction<Booking[]>) => {
        state.loading = false;
        state.userBookings = action.payload;
      })
      .addCase(fetchUserBookings.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Erreur lors de la récupération des réservations utilisateur';
      })
      
      // Fetch resource bookings
      .addCase(fetchResourceBookings.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchResourceBookings.fulfilled, (state, action: PayloadAction<{ resourceId: string; bookings: Booking[] }>) => {
        state.loading = false;
        state.resourceBookings[action.payload.resourceId] = action.payload.bookings;
      })
      .addCase(fetchResourceBookings.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Erreur lors de la récupération des réservations de la ressource';
      })
      
      // Check availability
      .addCase(checkAvailability.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(checkAvailability.fulfilled, (state, action: PayloadAction<{ resourceId: string; availabilityCheck: AvailabilityResponse; key: string }>) => {
        state.loading = false;
        state.availabilityChecks[action.payload.key] = action.payload.availabilityCheck;
      })
      .addCase(checkAvailability.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Erreur lors de la vérification de disponibilité';
      })
      
      // Create booking
      .addCase(createBooking.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createBooking.fulfilled, (state, action: PayloadAction<Booking>) => {
        state.loading = false;
        state.bookings.push(action.payload);
        state.userBookings.push(action.payload);
        
        // Mise à jour des réservations par ressource si elles existent déjà
        if (state.resourceBookings[action.payload.resource_id]) {
          state.resourceBookings[action.payload.resource_id].push(action.payload);
        }
      })
      .addCase(createBooking.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Erreur lors de la création de la réservation';
      })
      
      // Update booking status
      .addCase(updateBookingStatus.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateBookingStatus.fulfilled, (state, action: PayloadAction<Booking>) => {
        state.loading = false;
        
        // Mise à jour de la réservation dans toutes les listes
        const updatedBooking = action.payload;
        
        // Mise à jour dans la liste générale
        const bookingIndex = state.bookings.findIndex(b => b.id === updatedBooking.id);
        if (bookingIndex !== -1) {
          state.bookings[bookingIndex] = updatedBooking;
        }
        
        // Mise à jour dans la liste des réservations utilisateur
        const userBookingIndex = state.userBookings.findIndex(b => b.id === updatedBooking.id);
        if (userBookingIndex !== -1) {
          state.userBookings[userBookingIndex] = updatedBooking;
        }
        
        // Mise à jour dans la liste des réservations par ressource
        if (state.resourceBookings[updatedBooking.resource_id]) {
          const resourceBookingIndex = state.resourceBookings[updatedBooking.resource_id].findIndex(b => b.id === updatedBooking.id);
          if (resourceBookingIndex !== -1) {
            state.resourceBookings[updatedBooking.resource_id][resourceBookingIndex] = updatedBooking;
          }
        }
        
        // Mise à jour de la réservation sélectionnée si applicable
        if (state.selectedBooking && state.selectedBooking.id === updatedBooking.id) {
          state.selectedBooking = updatedBooking;
        }
      })
      .addCase(updateBookingStatus.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string || 'Erreur lors de la mise à jour de la réservation';
      });
  },
});

export const {
  selectBooking,
  clearAvailabilityCheck,
  clearAllAvailabilityChecks,
  clearError,
} = bookingsSlice.actions;

export default bookingsSlice.reducer;
