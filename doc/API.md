# API - Système de Réservation de Ressources (SRR)

Ce document définit les spécifications de l'API REST du Système de Réservation de Ressources. Il sert de référence pour les développeurs frontend et pour l'intégration avec des systèmes tiers.

## Principes généraux

### Format des échanges

- Toutes les requêtes et réponses utilisent le format JSON
- L'encodage des caractères est UTF-8
- Les dates sont au format ISO 8601 (par exemple: `2025-06-15T14:30:00Z`)
- Les identifiants sont des UUID v4

### Authentification

L'API utilise l'authentification JWT (JSON Web Token) :

1. Le client obtient un token via le endpoint `/auth/login`
2. Le token doit être inclus dans l'en-tête HTTP `Authorization` pour les requêtes ultérieures
3. Format de l'en-tête : `Authorization: Bearer {token}`
4. Les tokens ont une durée de validité limitée (par défaut 1 heure)
5. Un refresh token est fourni pour obtenir un nouveau token sans réauthentification

### Codes de statut HTTP

| Code | Description | Utilisation |
|------|-------------|------------|
| 200 | OK | Requête traitée avec succès |
| 201 | Created | Ressource créée avec succès |
| 204 | No Content | Requête traitée avec succès, pas de contenu retourné |
| 400 | Bad Request | Erreur dans les paramètres de la requête |
| 401 | Unauthorized | Authentification requise ou token invalide |
| 403 | Forbidden | Authentifié mais sans les droits nécessaires |
| 404 | Not Found | Ressource non trouvée |
| 409 | Conflict | Conflit avec l'état actuel de la ressource |
| 422 | Unprocessable Entity | Données de la requête valides mais non traitables |
| 500 | Internal Server Error | Erreur interne du serveur |

### Gestion des erreurs

Format standard des erreurs :

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Message d'erreur lisible par l'utilisateur",
    "details": {
      "field1": ["Message d'erreur spécifique au champ"],
      "field2": ["Message d'erreur spécifique au champ"]
    }
  }
}
```

### Pagination

Pour les endpoints retournant des listes, la pagination est gérée par les paramètres :

- `page` : Numéro de page (par défaut : 1)
- `per_page` : Nombre d'éléments par page (par défaut : 20, maximum : 100)

Format de réponse pour les listes paginées :

```json
{
  "data": [
    { /* élément 1 */ },
    { /* élément 2 */ },
    /* ... */
  ],
  "pagination": {
    "total_items": 327,
    "total_pages": 33,
    "current_page": 1,
    "per_page": 10,
    "next_page": 2,
    "prev_page": null
  }
}
```

### Filtrage, tri et recherche

- Filtrage : `filter[field]=value`
- Tri : `sort=field` (ascendant) ou `sort=-field` (descendant)
- Recherche : `q=terme_recherche`

### Versioning

Le versioning de l'API est géré dans le chemin de l'URL. Par exemple : `/api/v1/resources`

## Endpoints

### Authentification

#### POST /api/v1/auth/login

**Description** : S'authentifier et obtenir un JWT

**Corps de la requête** :
```json
{
  "username": "jdupont",
  "password": "motdepasse"
}
```

**Réponse (200)** :
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "jdupont",
    "email": "jean.dupont@example.com",
    "full_name": "Jean Dupont",
    "roles": ["user"],
    "department": "DSI"
  },
  "expires_at": "2025-04-22T24:00:00Z"
}
```

#### POST /api/v1/auth/refresh

**Description** : Rafraîchir un token JWT expiré

**Corps de la requête** :
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Réponse (200)** :
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-04-22T25:00:00Z"
}
```

#### POST /api/v1/auth/logout

**Description** : Déconnecter l'utilisateur (invalider le token)

**En-têtes** :
- `Authorization: Bearer {token}`

**Réponse (204)** : No Content

### Types de ressources

#### GET /api/v1/resource-types

**Description** : Obtenir la liste des types de ressources

**Paramètres** :
- `filter[name]` : Filtrer par nom
- `sort` : Champ de tri (par défaut : name)
- `page` : Page demandée
- `per_page` : Nombre d'éléments par page

**Réponse (200)** :
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "Salle de réunion",
      "description": "Espace dédié aux réunions et présentations",
      "schema": {
        "properties": {
          "floor": {
            "type": "integer",
            "description": "Étage où se trouve la salle",
            "minimum": 0
          },
          "has_projector": {
            "type": "boolean",
            "description": "Présence d'un projecteur"
          },
          "has_videoconference": {
            "type": "boolean",
            "description": "Équipement pour visioconférence"
          },
          "layout": {
            "type": "string",
            "enum": ["u_shape", "classroom", "boardroom", "theater"],
            "description": "Configuration de la salle"
          },
          "accessibility": {
            "type": "boolean",
            "description": "Accessible PMR"
          }
        },
        "required": ["floor", "layout"]
      },
      "required_properties": ["floor", "layout"],
      "icon": "meeting_room",
      "color": "#4285F4"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "name": "Véhicule",
      "description": "Véhicules de service pour déplacements professionnels",
      "schema": {
        "properties": {
          "model": {
            "type": "string",
            "description": "Modèle du véhicule"
          },
          "registration": {
            "type": "string",
            "description": "Immatriculation"
          },
          "fuel_type": {
            "type": "string",
            "enum": ["gasoline", "diesel", "electric", "hybrid"],
            "description": "Type de carburant"
          },
          "seats": {
            "type": "integer",
            "description": "Nombre de places",
            "minimum": 1
          }
        },
        "required": ["model", "registration", "seats"]
      },
      "required_properties": ["model", "registration", "seats"],
      "icon": "directions_car",
      "color": "#EA4335"
    }
  ],
  "pagination": {
    "total_items": 5,
    "total_pages": 1,
    "current_page": 1,
    "per_page": 10
  }
}
```

#### GET /api/v1/resource-types/{id}

**Description** : Obtenir les détails d'un type de ressource spécifique

**Réponse (200)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Salle de réunion",
  "description": "Espace dédié aux réunions et présentations",
  "schema": {
    "properties": {
      "floor": {
        "type": "integer",
        "description": "Étage où se trouve la salle",
        "minimum": 0
      },
      "has_projector": {
        "type": "boolean",
        "description": "Présence d'un projecteur"
      },
      "has_videoconference": {
        "type": "boolean",
        "description": "Équipement pour visioconférence"
      },
      "layout": {
        "type": "string",
        "enum": ["u_shape", "classroom", "boardroom", "theater"],
        "description": "Configuration de la salle"
      },
      "accessibility": {
        "type": "boolean",
        "description": "Accessible PMR"
      }
    },
    "required": ["floor", "layout"]
  },
  "required_properties": ["floor", "layout"],
  "icon": "meeting_room",
  "color": "#4285F4",
  "created_at": "2025-01-15T08:30:00Z",
  "updated_at": "2025-01-15T08:30:00Z"
}
```

#### POST /api/v1/resource-types

**Description** : Créer un nouveau type de ressource (réservé aux administrateurs)

**Corps de la requête** :
```json
{
  "name": "Matériel audiovisuel",
  "description": "Équipements audiovisuels pour événements",
  "schema": {
    "properties": {
      "type": {
        "type": "string",
        "enum": ["camera", "microphone", "speaker", "projector"],
        "description": "Type d'équipement"
      },
      "model": {
        "type": "string",
        "description": "Modèle de l'équipement"
      },
      "portable": {
        "type": "boolean",
        "description": "Peut être déplacé facilement"
      }
    },
    "required": ["type", "model"]
  },
  "required_properties": ["type", "model"],
  "icon": "videocam",
  "color": "#FBBC04"
}
```

**Réponse (201)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "name": "Matériel audiovisuel",
  "description": "Équipements audiovisuels pour événements",
  "schema": {
    "properties": {
      "type": {
        "type": "string",
        "enum": ["camera", "microphone", "speaker", "projector"],
        "description": "Type d'équipement"
      },
      "model": {
        "type": "string",
        "description": "Modèle de l'équipement"
      },
      "portable": {
        "type": "boolean",
        "description": "Peut être déplacé facilement"
      }
    },
    "required": ["type", "model"]
  },
  "required_properties": ["type", "model"],
  "icon": "videocam",
  "color": "#FBBC04",
  "created_at": "2025-04-22T22:30:00Z",
  "updated_at": "2025-04-22T22:30:00Z"
}
```

#### PUT /api/v1/resource-types/{id}

**Description** : Mettre à jour un type de ressource (réservé aux administrateurs)

**Corps de la requête** :
```json
{
  "name": "Matériel audiovisuel",
  "description": "Équipements audiovisuels pour événements et réunions",
  "schema": {
    "properties": {
      "type": {
        "type": "string",
        "enum": ["camera", "microphone", "speaker", "projector", "mixer"],
        "description": "Type d'équipement"
      },
      "model": {
        "type": "string",
        "description": "Modèle de l'équipement"
      },
      "portable": {
        "type": "boolean",
        "description": "Peut être déplacé facilement"
      }
    },
    "required": ["type", "model"]
  },
  "required_properties": ["type", "model"],
  "icon": "videocam",
  "color": "#FBBC04"
}
```

**Réponse (200)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "name": "Matériel audiovisuel",
  "description": "Équipements audiovisuels pour événements et réunions",
  "schema": {
    "properties": {
      "type": {
        "type": "string",
        "enum": ["camera", "microphone", "speaker", "projector", "mixer"],
        "description": "Type d'équipement"
      },
      "model": {
        "type": "string",
        "description": "Modèle de l'équipement"
      },
      "portable": {
        "type": "boolean",
        "description": "Peut être déplacé facilement"
      }
    },
    "required": ["type", "model"]
  },
  "required_properties": ["type", "model"],
  "icon": "videocam",
  "color": "#FBBC04",
  "created_at": "2025-04-22T22:30:00Z",
  "updated_at": "2025-04-22T22:45:00Z"
}
```

### Ressources

#### GET /api/v1/resources

**Description** : Rechercher et filtrer les ressources disponibles

**Paramètres** :
- `filter[resource_type_id]` : Filtrer par type de ressource
- `filter[location]` : Filtrer par lieu
- `filter[capacity_min]` : Capacité minimale
- `filter[requires_approval]` : Nécessite une validation (true/false)
- `filter[properties]` : Filtrer par propriétés JSON (format: `{"has_projector":true}`)
- `filter[available_between]` : Disponible entre deux dates (format: `2025-06-15T14:00:00Z,2025-06-15T16:00:00Z`)
- `filter[active]` : Filtrer ressources actives/inactives (true/false)
- `q` : Recherche textuelle (nom et description)
- `sort` : Champ de tri
- `page` : Page demandée
- `per_page` : Nombre d'éléments par page

**Réponse (200)** :
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440010",
      "name": "Salle Neptune",
      "description": "Grande salle de réunion avec vue sur le parc",
      "resource_type_id": "550e8400-e29b-41d4-a716-446655440001",
      "resource_type": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Salle de réunion",
        "icon": "meeting_room",
        "color": "#4285F4"
      },
      "properties": {
        "floor": 2,
        "has_projector": true,
        "has_videoconference": true,
        "layout": "boardroom",
        "accessibility": true
      },
      "requires_approval": false,
      "location": "Bâtiment A",
      "capacity": 20,
      "availability_start": "09:00:00",
      "availability_end": "18:00:00",
      "active": true,
      "created_at": "2025-01-15T08:30:00Z",
      "updated_at": "2025-01-15T08:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440011",
      "name": "Salle Mars",
      "description": "Petite salle pour réunions de 4 à 8 personnes",
      "resource_type_id": "550e8400-e29b-41d4-a716-446655440001",
      "resource_type": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Salle de réunion",
        "icon": "meeting_room",
        "color": "#4285F4"
      },
      "properties": {
        "floor": 1,
        "has_projector": true,
        "has_videoconference": false,
        "layout": "boardroom",
        "accessibility": true
      },
      "requires_approval": false,
      "location": "Bâtiment B",
      "capacity": 8,
      "availability_start": "08:00:00",
      "availability_end": "20:00:00",
      "active": true,
      "created_at": "2025-01-15T08:35:00Z",
      "updated_at": "2025-01-15T08:35:00Z"
    }
  ],
  "pagination": {
    "total_items": 42,
    "total_pages": 21,
    "current_page": 1,
    "per_page": 2
  }
}
```

#### GET /api/v1/resources/{id}

**Description** : Obtenir les détails d'une ressource spécifique

**Réponse (200)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440010",
  "name": "Salle Neptune",
  "description": "Grande salle de réunion avec vue sur le parc",
  "resource_type_id": "550e8400-e29b-41d4-a716-446655440001",
  "resource_type": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Salle de réunion",
    "icon": "meeting_room",
    "color": "#4285F4"
  },
  "properties": {
    "floor": 2,
    "has_projector": true,
    "has_videoconference": true,
    "layout": "boardroom",
    "accessibility": true
  },
  "requires_approval": false,
  "location": "Bâtiment A",
  "capacity": 20,
  "availability_start": "09:00:00",
  "availability_end": "18:00:00",
  "active": true,
  "managers": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440100",
      "username": "jmartin",
      "full_name": "Julie Martin"
    }
  ],
  "created_at": "2025-01-15T08:30:00Z",
  "updated_at": "2025-01-15T08:30:00Z",
  "availabilities": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440200",
      "start_time": "2025-05-01T00:00:00Z",
      "end_time": "2025-05-02T23:59:59Z",
      "is_available": false,
      "reason": "Maintenance planifiée"
    }
  ]
}
```

#### GET /api/v1/resources/{id}/availability

**Description** : Vérifier la disponibilité d'une ressource sur une période

**Paramètres** :
- `start_date` : Date de début (obligatoire)
- `end_date` : Date de fin (obligatoire)
- `include_bookings` : Inclure les détails des réservations (true/false)

**Réponse (200)** :
```json
{
  "resource_id": "550e8400-e29b-41d4-a716-446655440010",
  "start_date": "2025-06-15T00:00:00Z",
  "end_date": "2025-06-21T23:59:59Z",
  "availability_slots": [
    {
      "date": "2025-06-15",
      "slots": [
        {
          "start_time": "2025-06-15T09:00:00Z",
          "end_time": "2025-06-15T10:30:00Z",
          "is_available": true
        },
        {
          "start_time": "2025-06-15T10:30:00Z",
          "end_time": "2025-06-15T12:00:00Z",
          "is_available": false,
          "booking_id": "550e8400-e29b-41d4-a716-446655440300"
        },
        {
          "start_time": "2025-06-15T12:00:00Z",
          "end_time": "2025-06-15T14:00:00Z",
          "is_available": true
        }
        // ...autres créneaux
      ]
    }
    // ...autres jours
  ],
  "bookings": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440300",
      "start_time": "2025-06-15T10:30:00Z",
      "end_time": "2025-06-15T12:00:00Z",
      "purpose": "Réunion équipe marketing",
      "user": {
        "id": "550e8400-e29b-41d4-a716-446655440400",
        "full_name": "Sophie Dubois"
      }
    }
    // ...autres réservations
  ]
}
```

#### POST /api/v1/resources

**Description** : Créer une nouvelle ressource (réservé aux administrateurs et gestionnaires)

**Corps de la requête** :
```json
{
  "name": "Salle Jupiter",
  "description": "Salle de conférence pour présentations importantes",
  "resource_type_id": "550e8400-e29b-41d4-a716-446655440001",
  "properties": {
    "floor": 3,
    "has_projector": true,
    "has_videoconference": true,
    "layout": "theater",
    "accessibility": true
  },
  "requires_approval": true,
  "location": "Bâtiment A",
  "capacity": 50,
  "availability_start": "08:00:00",
  "availability_end": "20:00:00",
  "active": true,
  "manager_ids": ["550e8400-e29b-41d4-a716-446655440100"]
}
```

**Réponse (201)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440012",
  "name": "Salle Jupiter",
  "description": "Salle de conférence pour présentations importantes",
  "resource_type_id": "550e8400-e29b-41d4-a716-446655440001",
  "resource_type": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Salle de réunion",
    "icon": "meeting_room",
    "color": "#4285F4"
  },
  "properties": {
    "floor": 3,
    "has_projector": true,
    "has_videoconference": true,
    "layout": "theater",
    "accessibility": true
  },
  "requires_approval": true,
  "location": "Bâtiment A",
  "capacity": 50,
  "availability_start": "08:00:00",
  "availability_end": "20:00:00",
  "active": true,
  "managers": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440100",
      "username": "jmartin",
      "full_name": "Julie Martin"
    }
  ],
  "created_at": "2025-04-22T22:30:00Z",
  "updated_at": "2025-04-22T22:30:00Z"
}
```

#### PUT /api/v1/resources/{id}

**Description** : Mettre à jour une ressource existante (réservé aux administrateurs et gestionnaires)

**Corps de la requête** :
```json
{
  "name": "Salle Jupiter",
  "description": "Salle de conférence pour présentations et formations",
  "resource_type_id": "550e8400-e29b-41d4-a716-446655440001",
  "properties": {
    "floor": 3,
    "has_projector": true,
    "has_videoconference": true,
    "layout": "theater",
    "accessibility": true,
    "has_sound_system": true
  },
  "requires_approval": true,
  "location": "Bâtiment A",
  "capacity": 60,
  "availability_start": "08:00:00",
  "availability_end": "21:00:00",
  "active": true,
  "manager_ids": ["550e8400-e29b-41d4-a716-446655440100"]
}
```

**Réponse (200)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440012",
  "name": "Salle Jupiter",
  "description": "Salle de conférence pour présentations et formations",
  "resource_type_id": "550e8400-e29b-41d4-a716-446655440001",
  "resource_type": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Salle de réunion",
    "icon": "meeting_room",
    "color": "#4285F4"
  },
  "properties": {
    "floor": 3,
    "has_projector": true,
    "has_videoconference": true,
    "layout": "theater",
    "accessibility": true,
    "has_sound_system": true
  },
  "requires_approval": true,
  "location": "Bâtiment A",
  "capacity": 60,
  "availability_start": "08:00:00",
  "availability_end": "21:00:00",
  "active": true,
  "managers": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440100",
      "username": "jmartin",
      "full_name": "Julie Martin"
    }
  ],
  "created_at": "2025-04-22T22:30:00Z",
  "updated_at": "2025-04-22T22:40:00Z"
}
```

#### POST /api/v1/resources/{id}/availabilities

**Description** : Ajouter une période de disponibilité/indisponibilité exceptionnelle (réservé aux gestionnaires)

**Corps de la requête** :
```json
{
  "start_time": "2025-05-01T00:00:00Z",
  "end_time": "2025-05-02T23:59:59Z",
  "is_available": false,
  "reason": "Maintenance planifiée"
}
```

**Réponse (201)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440200",
  "resource_id": "550e8400-e29b-41d4-a716-446655440010",
  "start_time": "2025-05-01T00:00:00Z",
  "end_time": "2025-05-02T23:59:59Z",
  "is_available": false,
  "reason": "Maintenance planifiée",
  "created_by": "550e8400-e29b-41d4-a716-446655440100",
  "created_at": "2025-04-22T22:30:00Z"
}
```

### Réservations

#### GET /api/v1/bookings

**Description** : Obtenir la liste des réservations

**Paramètres** :
- `filter[user_id]` : Filtrer par utilisateur
- `filter[resource_id]` : Filtrer par ressource
- `filter[resource_type_id]` : Filtrer par type de ressource
- `filter[status]` : Filtrer par statut
- `filter[from_date]` : À partir d'une date
- `filter[to_date]` : Jusqu'à une date
- `sort` : Champ de tri (par défaut : -start_time)
- `page` : Page demandée
- `per_page` : Nombre d'éléments par page

**Réponse (200)** :
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440300",
      "resource_id": "550e8400-e29b-41d4-a716-446655440010",
      "resource": {
        "id": "550e8400-e29b-41d4-a716-446655440010",
        "name": "Salle Neptune",
        "location": "Bâtiment A",
        "resource_type": {
          "id": "550e8400-e29b-41d4-a716-446655440001",
          "name": "Salle de réunion",
          "icon": "meeting_room",
          "color": "#4285F4"
        }
      },
      "user_id": "550e8400-e29b-41d4-a716-446655440400",
      "user": {
        "id": "550e8400-e29b-41d4-a716-446655440400",
        "full_name": "Sophie Dubois",
        "email": "sophie.dubois@example.com"
      },
      "start_time": "2025-06-15T10:30:00Z",
      "end_time": "2025-06-15T12:00:00Z",
      "status": "confirmed",
      "purpose": "Réunion équipe marketing",
      "participants": 8,
      "created_at": "2025-04-20T15:30:00Z",
      "updated_at": "2025-04-20T15:35:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440301",
      "resource_id": "550e8400-e29b-41d4-a716-446655440012",
      "resource": {
        "id": "550e8400-e29b-41d4-a716-446655440012",
        "name": "Salle Jupiter",
        "location": "Bâtiment A",
        "resource_type": {
          "id": "550e8400-e29b-41d4-a716-446655440001",
          "name": "Salle de réunion",
          "icon": "meeting_room",
          "color": "#4285F4"
        }
      },
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "full_name": "Jean Dupont",
        "email": "jean.dupont@example.com"
      },
      "start_time": "2025-06-16T14:00:00Z",
      "end_time": "2025-06-16T17:00:00Z",
      "status": "pending",
      "purpose": "Présentation nouveau projet",
      "participants": 25,
      "created_at": "2025-04-22T10:15:00Z",
      "updated_at": "2025-04-22T10:15:00Z"
    }
  ],
  "pagination": {
    "total_items": 14,
    "total_pages": 7,
    "current_page": 1,
    "per_page": 2
  }
}
```

#### GET /api/v1/bookings/{id}

**Description** : Obtenir les détails d'une réservation spécifique

**Réponse (200)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440300",
  "resource_id": "550e8400-e29b-41d4-a716-446655440010",
  "resource": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "name": "Salle Neptune",
    "description": "Grande salle de réunion avec vue sur le parc",
    "location": "Bâtiment A",
    "capacity": 20,
    "resource_type": {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "Salle de réunion",
      "icon": "meeting_room",
      "color": "#4285F4"
    },
    "properties": {
      "floor": 2,
      "has_projector": true,
      "has_videoconference": true,
      "layout": "boardroom",
      "accessibility": true
    }
  },
  "user_id": "550e8400-e29b-41d4-a716-446655440400",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440400",
    "full_name": "Sophie Dubois",
    "email": "sophie.dubois@example.com"
  },
  "start_time": "2025-06-15T10:30:00Z",
  "end_time": "2025-06-15T12:00:00Z",
  "status": "confirmed",
  "purpose": "Réunion équipe marketing",
  "participants": 8,
  "recurrence": null,
  "notes": "Préparer un vidéoprojecteur et des rafraîchissements",
  "created_at": "2025-04-20T15:30:00Z",
  "updated_at": "2025-04-20T15:35:00Z",
  "approvals": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440500",
      "approver": {
        "id": "550e8400-e29b-41d4-a716-446655440100",
        "full_name": "Julie Martin"
      },
      "status": "approved",
      "comment": "Validé",
      "decision_time": "2025-04-20T15:35:00Z"
    }
  ]
}
```

#### POST /api/v1/bookings

**Description** : Créer une nouvelle réservation

**Corps de la requête** :
```json
{
  "resource_id": "550e8400-e29b-41d4-a716-446655440010",
  "start_time": "2025-06-18T14:00:00Z",
  "end_time": "2025-06-18T16:00:00Z",
  "purpose": "Réunion trimestrielle équipe finance",
  "participants": 12,
  "notes": "Besoin du vidéoprojecteur et d'une connexion internet stable",
  "recurrence": {
    "type": "weekly",
    "interval": 1,
    "days_of_week": [2],
    "ends": {
      "type": "count",
      "count": 4
    }
  }
}
```

**Réponse (201)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440302",
  "resource_id": "550e8400-e29b-41d4-a716-446655440010",
  "resource": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "name": "Salle Neptune",
    "location": "Bâtiment A"
  },
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "start_time": "2025-06-18T14:00:00Z",
  "end_time": "2025-06-18T16:00:00Z",
  "status": "confirmed",
  "purpose": "Réunion trimestrielle équipe finance",
  "participants": 12,
  "notes": "Besoin du vidéoprojecteur et d'une connexion internet stable",
  "recurrence": {
    "type": "weekly",
    "interval": 1,
    "days_of_week": [2],
    "ends": {
      "type": "count",
      "count": 4
    }
  },
  "recurrent_bookings": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440303",
      "start_time": "2025-06-25T14:00:00Z",
      "end_time": "2025-06-25T16:00:00Z",
      "status": "confirmed"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440304",
      "start_time": "2025-07-02T14:00:00Z",
      "end_time": "2025-07-02T16:00:00Z",
      "status": "confirmed"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440305",
      "start_time": "2025-07-09T14:00:00Z",
      "end_time": "2025-07-09T16:00:00Z",
      "status": "confirmed"
    }
  ],
  "created_at": "2025-04-22T22:30:00Z",
  "updated_at": "2025-04-22T22:30:00Z"
}
```

#### PUT /api/v1/bookings/{id}

**Description** : Mettre à jour une réservation

**Corps de la requête** :
```json
{
  "start_time": "2025-06-18T14:30:00Z",
  "end_time": "2025-06-18T16:30:00Z",
  "purpose": "Réunion trimestrielle équipe finance - Préparation budget",
  "participants": 15,
  "notes": "Besoin du vidéoprojecteur et d'une connexion internet stable. Prévoir café.",
  "all_recurrences": false
}
```

**Réponse (200)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440302",
  "resource_id": "550e8400-e29b-41d4-a716-446655440010",
  "resource": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "name": "Salle Neptune",
    "location": "Bâtiment A"
  },
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "start_time": "2025-06-18T14:30:00Z",
  "end_time": "2025-06-18T16:30:00Z",
  "status": "confirmed",
  "purpose": "Réunion trimestrielle équipe finance - Préparation budget",
  "participants": 15,
  "notes": "Besoin du vidéoprojecteur et d'une connexion internet stable. Prévoir café.",
  "recurrence": {
    "type": "weekly",
    "interval": 1,
    "days_of_week": [2],
    "ends": {
      "type": "count",
      "count": 4
    }
  },
  "created_at": "2025-04-22T22:30:00Z",
  "updated_at": "2025-04-22T22:45:00Z"
}
```

#### DELETE /api/v1/bookings/{id}

**Description** : Annuler une réservation

**Paramètres** :
- `all_recurrences` : Annuler toutes les récurrences (true/false)
- `reason` : Motif d'annulation (optionnel)

**Réponse (204)** : No Content

#### POST /api/v1/bookings/{id}/approve

**Description** : Approuver une réservation (réservé aux gestionnaires)

**Corps de la requête** :
```json
{
  "comment": "Validation accordée"
}
```

**Réponse (200)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440500",
  "booking_id": "550e8400-e29b-41d4-a716-446655440301",
  "approver_id": "550e8400-e29b-41d4-a716-446655440100",
  "status": "approved",
  "comment": "Validation accordée",
  "decision_time": "2025-04-22T22:30:00Z",
  "created_at": "2025-04-22T22:30:00Z"
}
```

#### POST /api/v1/bookings/{id}/reject

**Description** : Rejeter une réservation (réservé aux gestionnaires)

**Corps de la requête** :
```json
{
  "comment": "Salle non disponible pour cause de maintenance"
}
```

**Réponse (200)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440500",
  "booking_id": "550e8400-e29b-41d4-a716-446655440301",
  "approver_id": "550e8400-e29b-41d4-a716-446655440100",
  "status": "rejected",
  "comment": "Salle non disponible pour cause de maintenance",
  "decision_time": "2025-04-22T22:30:00Z",
  "created_at": "2025-04-22T22:30:00Z"
}
```

### Utilisateurs

#### GET /api/v1/users/profile

**Description** : Récupérer le profil de l'utilisateur connecté

**Réponse (200)** :
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "jdupont",
  "email": "jean.dupont@example.com",
  "full_name": "Jean Dupont",
  "roles": ["user"],
  "department": "DSI",
  "position": "Développeur",
  "phone": "+33123456789",
  "last_login": "2025-04-22T22:00:00Z"
}
```

#### GET /api/v1/users

**Description** : Lister les utilisateurs (réservé aux administrateurs)

**Paramètres** :
- `filter[roles]` : Filtrer par rôle
- `filter[department]` : Filtrer par département
- `q` : Rechercher par nom ou email
- `sort` : Champ de tri (par défaut : full_name)
- `page` : Page demandée
- `per_page` : Nombre d'éléments par page

**Réponse (200)** :
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "jdupont",
      "email": "jean.dupont@example.com",
      "full_name": "Jean Dupont",
      "roles": ["user"],
      "department": "DSI",
      "position": "Développeur",
      "last_login": "2025-04-22T22:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440100",
      "username": "jmartin",
      "email": "julie.martin@example.com",
      "full_name": "Julie Martin",
      "roles": ["resource_manager"],
      "department": "Services Généraux",
      "position": "Responsable Logistique",
      "last_login": "2025-04-22T21:30:00Z"
    }
  ],
  "pagination": {
    "total_items": 32,
    "total_pages": 16,
    "current_page": 1,
    "per_page": 2
  }
}
```

### Statistiques et rapports

#### GET /api/v1/statistics/resources/{id}

**Description** : Obtenir des statistiques sur l'utilisation d'une ressource (réservé aux gestionnaires et administrateurs)

**Paramètres** :
- `period` : Période de statistiques (week, month, quarter, year)
- `start_date` : Date de début (obligatoire)
- `end_date` : Date de fin (obligatoire)

**Réponse (200)** :
```json
{
  "resource_id": "550e8400-e29b-41d4-a716-446655440010",
  "resource_name": "Salle Neptune",
  "period": {
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-03-31T23:59:59Z"
  },
  "usage": {
    "total_bookings": 42,
    "total_hours": 84.5,
    "occupancy_rate": 0.35,
    "average_duration": 2.01
  },
  "by_status": {
    "confirmed": 35,
    "cancelled": 5,
    "rejected": 2
  },
  "by_department": [
    {
      "department": "DSI",
      "bookings": 15,
      "hours": 32.5
    },
    {
      "department": "Finances",
      "bookings": 10,
      "hours": 18.0
    }
  ],
  "by_day_of_week": [
    {
      "day": 1,
      "bookings": 10,
      "hours": 20.0
    },
    {
      "day": 2,
      "bookings": 8,
      "hours": 16.0
    }
  ],
  "by_time": [
    {
      "hour": 9,
      "bookings": 8,
      "hours": 8.0
    },
    {
      "hour": 10,
      "bookings": 12,
      "hours": 12.0
    }
  ]
}
```
