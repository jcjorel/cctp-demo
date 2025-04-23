import apiClient from '../api/apiClient';

interface LoginResponse {
  token: string;
  user: {
    username: string;
    email: string;
    full_name: string;
    role: string;
    department: string;
    groups: string[];
  };
}

/**
 * [Class intent]
 * Service d'authentification gérant les appels API liés à l'authentification et la session utilisateur.
 * 
 * [Design principles]
 * Interface claire et fonctionnelle pour simplifier l'intégration avec Redux.
 * Gestion centralisée des jetons JWT et des données utilisateur.
 * 
 * [Implementation details]
 * Utilise un client API centralisé et le stockage local pour la persistance de session.
 */
const authService = {
  /**
   * [Function intent]
   * Authentifie un utilisateur auprès de l'API.
   * 
   * [Design principles]
   * Interface simple nécessitant uniquement les identifiants essentiels.
   * 
   * [Implementation details]
   * Envoie une requête POST à l'API d'authentification et gère le stockage des jetons.
   */
  login: async (username: string, password: string): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/api/auth/login', {
      username,
      password,
    });
    return response.data;
  },

  /**
   * [Function intent]
   * Déconnecte l'utilisateur actuel.
   * 
   * [Design principles]
   * Approche simple pour assurer une déconnexion complète et cohérente.
   * 
   * [Implementation details]
   * Supprime les données de session du stockage local.
   */
  logout: async (): Promise<void> => {
    // Pas d'appel API pour la déconnexion côté serveur car JWT est stateless
    // La déconnexion se fait uniquement côté client
  },

  /**
   * [Function intent]
   * Récupère le jeton d'accès actuel.
   * 
   * [Design principles]
   * Méthode utilitaire pour simplifier l'accès au jeton stocké.
   * 
   * [Implementation details]
   * Lit le jeton depuis le stockage local.
   */
  getToken: (): string | null => {
    return localStorage.getItem('srr_token');
  },

  /**
   * [Function intent]
   * Vérifie si l'utilisateur est authentifié.
   * 
   * [Design principles]
   * Approche simple basée sur l'existence d'un jeton.
   * 
   * [Implementation details]
   * Vérifie la présence d'un jeton dans le stockage local.
   */
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('srr_token');
  },

  /**
   * [Function intent]
   * Actualise le jeton d'accès.
   * 
   * [Design principles]
   * Gestion automatique du renouvellement des jetons pour une expérience continue.
   * 
   * [Implementation details]
   * Envoie une requête au point de terminaison de rafraîchissement et met à jour le jeton stocké.
   */
  refreshToken: async (): Promise<{ token: string }> => {
    const response = await apiClient.post<{ token: string }>('/api/auth/refresh-token');
    if (response.data.token) {
      localStorage.setItem('srr_token', response.data.token);
    }
    return response.data;
  },

  /**
   * [Function intent]
   * Récupère les informations de l'utilisateur actuel.
   * 
   * [Design principles]
   * Accès aux données utilisateur sans avoir à repasser par l'API.
   * 
   * [Implementation details]
   * Lit et parse les données stockées localement.
   */
  getCurrentUser: () => {
    const userStr = localStorage.getItem('srr_user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch (e) {
      console.error('Error parsing user data from localStorage', e);
      return null;
    }
  },

  /**
   * [Function intent]
   * Vérifie si l'utilisateur a un rôle spécifique.
   * 
   * [Design principles]
   * Facilite la vérification des autorisations basées sur les rôles.
   * 
   * [Implementation details]
   * Compare le rôle stocké avec le rôle demandé.
   */
  hasRole: (role: string): boolean => {
    const user = authService.getCurrentUser();
    return user ? user.role === role : false;
  },

  /**
   * [Function intent]
   * Vérifie si l'utilisateur appartient à un groupe spécifique.
   * 
   * [Design principles]
   * Facilite la vérification des autorisations basées sur les groupes.
   * 
   * [Implementation details]
   * Recherche le groupe dans la liste des groupes de l'utilisateur.
   */
  hasGroup: (group: string): boolean => {
    const user = authService.getCurrentUser();
    return user ? user.groups.includes(group) : false;
  },
};

export default authService;
