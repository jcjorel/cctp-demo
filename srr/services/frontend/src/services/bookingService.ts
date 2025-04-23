import apiClient from '../api/apiClient';
import { Booking, BookingRequest, AvailabilityResponse } from '../store/slices/bookingsSlice';

/**
 * [Class intent]
 * Service de gestion des réservations de ressources dans le SRR.
 * 
 * [Design principles]
 * Interface claire et fonctionnelle pour simplifier l'intégration avec Redux.
 * Séparation des responsabilités pour une meilleure maintenabilité.
 * 
 * [Implementation details]
 * Utilise le client API centralisé pour toutes les requêtes liées aux réservations.
 */
const bookingService = {
  /**
   * [Function intent]
   * Récupère la liste de toutes les réservations.
   * 
   * [Design principles]
   * Interface flexible avec filtrage optionnel.
   * 
   * [Implementation details]
   * Effectue une requête GET vers l'API des réservations avec gestion des filtres optionnels.
   */
  getBookings: async (filters?: Record<string, any>): Promise<Booking[]> => {
    const params = filters || {};
    const response = await apiClient.get<Booking[]>('/exchange/bookings', { params });
    return response.data;
  },

  /**
   * [Function intent]
   * Récupère une réservation spécifique par son identifiant.
   * 
   * [Design principles]
   * Interface simple basée sur l'identifiant unique de la réservation.
   * 
   * [Implementation details]
   * Effectue une requête GET vers l'API des réservations avec l'ID spécifié.
   */
  getBookingById: async (id: string): Promise<Booking> => {
    const response = await apiClient.get<Booking>(`/exchange/bookings/${id}`);
    return response.data;
  },

  /**
   * [Function intent]
   * Récupère les réservations d'un utilisateur spécifique.
   * 
   * [Design principles]
   * Interface simple pour filtrer les réservations par utilisateur.
   * 
   * [Implementation details]
   * Effectue une requête GET vers l'API avec le filtre utilisateur.
   */
  getUserBookings: async (userId: string): Promise<Booking[]> => {
    const response = await apiClient.get<Booking[]>('/exchange/bookings', { 
      params: { user_id: userId }
    });
    return response.data;
  },

  /**
   * [Function intent]
   * Récupère les réservations pour une ressource spécifique.
   * 
   * [Design principles]
   * Interface simple pour filtrer les réservations par ressource.
   * 
   * [Implementation details]
   * Effectue une requête GET vers l'API avec le filtre ressource.
   */
  getResourceBookings: async (resourceId: string): Promise<Booking[]> => {
    const response = await apiClient.get<Booking[]>('/exchange/bookings', { 
      params: { resource_id: resourceId } 
    });
    return response.data;
  },

  /**
   * [Function intent]
   * Vérifie la disponibilité d'une ressource sur une plage horaire.
   * 
   * [Design principles]
   * Interface claire pour la vérification des conflits de réservation.
   * 
   * [Implementation details]
   * Effectue une requête POST vers l'API de vérification de disponibilité.
   */
  checkAvailability: async (
    resourceId: string,
    startTime: Date,
    endTime: Date
  ): Promise<AvailabilityResponse> => {
    const response = await apiClient.post<AvailabilityResponse>('/exchange/availability', {
      resource_id: resourceId,
      start_time: startTime.toISOString(),
      end_time: endTime.toISOString(),
    });
    return response.data;
  },

  /**
   * [Function intent]
   * Crée une nouvelle réservation de ressource.
   * 
   * [Design principles]
   * Interface claire avec validations appropriées.
   * 
   * [Implementation details]
   * Effectue une requête POST vers l'API de création de réservation.
   */
  createBooking: async (bookingRequest: BookingRequest): Promise<Booking> => {
    const response = await apiClient.post<Booking>('/exchange/bookings', {
      resource_id: bookingRequest.resource_id,
      title: bookingRequest.title,
      start_time: bookingRequest.start_time.toISOString(),
      end_time: bookingRequest.end_time.toISOString(),
      attendees: bookingRequest.attendees,
      description: bookingRequest.description || undefined,
    });
    return response.data;
  },

  /**
   * [Function intent]
   * Met à jour le statut d'une réservation existante.
   * 
   * [Design principles]
   * Interface simple pour confirmer ou annuler une réservation.
   * 
   * [Implementation details]
   * Effectue une requête PUT vers l'API de mise à jour de statut.
   */
  updateBookingStatus: async (
    bookingId: string,
    status: 'confirmed' | 'cancelled'
  ): Promise<Booking> => {
    const response = await apiClient.put<Booking>(
      `/exchange/bookings/${bookingId}/status`,
      { status }
    );
    return response.data;
  },

  /**
   * [Function intent]
   * Recherche des réservations selon des critères multiples.
   * 
   * [Design principles]
   * Interface flexible avec multiples critères de recherche.
   * 
   * [Implementation details]
   * Effectue une requête GET avec paramètres de filtrage avancés.
   */
  searchBookings: async (searchParams: {
    startDate?: Date;
    endDate?: Date;
    resourceId?: string;
    userId?: string;
    status?: string;
  }): Promise<Booking[]> => {
    // Convertir les dates en ISO string si elles sont présentes
    const params: Record<string, any> = {};
    
    if (searchParams.startDate) {
      params.start_date = searchParams.startDate.toISOString();
    }
    
    if (searchParams.endDate) {
      params.end_date = searchParams.endDate.toISOString();
    }
    
    if (searchParams.resourceId) {
      params.resource_id = searchParams.resourceId;
    }
    
    if (searchParams.userId) {
      params.user_id = searchParams.userId;
    }
    
    if (searchParams.status) {
      params.status = searchParams.status;
    }
    
    const response = await apiClient.get<Booking[]>('/exchange/bookings', { params });
    return response.data;
  },
};

export default bookingService;
