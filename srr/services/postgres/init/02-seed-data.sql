-- Script d'insertion de données de test pour le SRR
-- Exécuté automatiquement après la création des tables

-- Insertion des utilisateurs de test
INSERT INTO users (username, email, full_name, password_hash, role, department, is_active)
VALUES 
  -- Mot de passe = 'password' pour tous les utilisateurs (bcrypt hash)
  ('admin', 'admin@mairie-saint-denis.fr', 'Administrateur Système', '$2b$12$tZS.5QASbKAKD0P/p3qhs.CZ.LUzJ.vS5Yggg7jFJCxQSOq0P6FtW', 'admin', 'DSI', TRUE),
  ('jdupont', 'jean.dupont@mairie-saint-denis.fr', 'Jean Dupont', '$2b$12$tZS.5QASbKAKD0P/p3qhs.CZ.LUzJ.vS5Yggg7jFJCxQSOq0P6FtW', 'manager', 'Urbanisme', TRUE),
  ('smartin', 'sophie.martin@mairie-saint-denis.fr', 'Sophie Martin', '$2b$12$tZS.5QASbKAKD0P/p3qhs.CZ.LUzJ.vS5Yggg7jFJCxQSOq0P6FtW', 'user', 'RH', TRUE),
  ('plegrand', 'pierre.legrand@mairie-saint-denis.fr', 'Pierre Legrand', '$2b$12$tZS.5QASbKAKD0P/p3qhs.CZ.LUzJ.vS5Yggg7jFJCxQSOq0P6FtW', 'user', 'Finances', TRUE),
  ('cmoreau', 'claire.moreau@mairie-saint-denis.fr', 'Claire Moreau', '$2b$12$tZS.5QASbKAKD0P/p3qhs.CZ.LUzJ.vS5Yggg7jFJCxQSOq0P6FtW', 'manager', 'Culture', TRUE),
  ('inactif', 'user.inactif@mairie-saint-denis.fr', 'Utilisateur Inactif', '$2b$12$tZS.5QASbKAKD0P/p3qhs.CZ.LUzJ.vS5Yggg7jFJCxQSOq0P6FtW', 'user', 'DSI', FALSE)
ON CONFLICT (username) DO NOTHING;

-- Insertion des caractéristiques de ressources
INSERT INTO features (name, icon)
VALUES
  ('projecteur', 'projector'),
  ('tableau', 'whiteboard'),
  ('visioconference', 'video-camera'),
  ('sonorisation', 'microphone'),
  ('ordinateurs', 'computer')
ON CONFLICT (name) DO NOTHING;

-- Récupération des IDs pour les managers
DO $$
DECLARE
  jdupont_id INTEGER;
  cmoreau_id INTEGER;
BEGIN
  SELECT id INTO jdupont_id FROM users WHERE username = 'jdupont';
  SELECT id INTO cmoreau_id FROM users WHERE username = 'cmoreau';
  
  -- Insertion des ressources
  INSERT INTO resources (resource_id, name, type, capacity, location, email, calendar_id, status, manager_id)
  VALUES
    ('salle-a101', 'Salle A101', 'salle_reunion', 12, 'Hôtel de Ville - Aile A - 1er étage', 'salle-a101@mairie-saint-denis.fr', 'salle-a101', 'active', jdupont_id),
    ('salle-b205', 'Salle B205', 'salle_reunion', 8, 'Hôtel de Ville - Aile B - 2ème étage', 'salle-b205@mairie-saint-denis.fr', 'salle-b205', 'active', cmoreau_id),
    ('salle-conseil', 'Salle du Conseil', 'salle_reunion', 50, 'Hôtel de Ville - Rez-de-chaussée', 'salle-conseil@mairie-saint-denis.fr', 'salle-conseil', 'active', jdupont_id),
    ('salle-c310', 'Salle C310', 'salle_reunion', 6, 'Annexe - Aile C - 3ème étage', 'salle-c310@mairie-saint-denis.fr', 'salle-c310', 'active', cmoreau_id),
    ('amphitheatre', 'Amphithéâtre', 'salle_reunion', 120, 'Centre culturel - Rez-de-chaussée', 'amphitheatre@mairie-saint-denis.fr', 'amphitheatre', 'active', cmoreau_id),
    ('salle-formation', 'Salle de Formation', 'salle_reunion', 15, 'Annexe - Aile B - 1er étage', 'salle-formation@mairie-saint-denis.fr', 'salle-formation', 'maintenance', jdupont_id)
  ON CONFLICT (resource_id) DO NOTHING;
END $$;

-- Associations entre ressources et caractéristiques
DO $$
DECLARE
  salle_a101_id INTEGER;
  salle_b205_id INTEGER;
  salle_conseil_id INTEGER;
  salle_c310_id INTEGER;
  amphitheatre_id INTEGER;
  salle_formation_id INTEGER;
  projecteur_id INTEGER;
  tableau_id INTEGER;
  visioconf_id INTEGER;
  sono_id INTEGER;
  ordi_id INTEGER;
BEGIN
  -- Récupération des IDs des ressources
  SELECT id INTO salle_a101_id FROM resources WHERE resource_id = 'salle-a101';
  SELECT id INTO salle_b205_id FROM resources WHERE resource_id = 'salle-b205';
  SELECT id INTO salle_conseil_id FROM resources WHERE resource_id = 'salle-conseil';
  SELECT id INTO salle_c310_id FROM resources WHERE resource_id = 'salle-c310';
  SELECT id INTO amphitheatre_id FROM resources WHERE resource_id = 'amphitheatre';
  SELECT id INTO salle_formation_id FROM resources WHERE resource_id = 'salle-formation';
  
  -- Récupération des IDs des caractéristiques
  SELECT id INTO projecteur_id FROM features WHERE name = 'projecteur';
  SELECT id INTO tableau_id FROM features WHERE name = 'tableau';
  SELECT id INTO visioconf_id FROM features WHERE name = 'visioconference';
  SELECT id INTO sono_id FROM features WHERE name = 'sonorisation';
  SELECT id INTO ordi_id FROM features WHERE name = 'ordinateurs';
  
  -- Association des caractéristiques aux ressources
  INSERT INTO resource_features (resource_id, feature_id)
  VALUES
    (salle_a101_id, projecteur_id),
    (salle_a101_id, visioconf_id),
    (salle_a101_id, tableau_id),
    (salle_b205_id, projecteur_id),
    (salle_b205_id, tableau_id),
    (salle_conseil_id, projecteur_id),
    (salle_conseil_id, visioconf_id),
    (salle_conseil_id, sono_id),
    (salle_conseil_id, tableau_id),
    (salle_c310_id, tableau_id),
    (amphitheatre_id, projecteur_id),
    (amphitheatre_id, visioconf_id),
    (amphitheatre_id, sono_id),
    (salle_formation_id, projecteur_id),
    (salle_formation_id, ordi_id),
    (salle_formation_id, tableau_id)
  ON CONFLICT DO NOTHING;
END $$;

-- Insertion des groupes d'utilisateurs
INSERT INTO user_groups (name, description)
VALUES
  ('SRR_Admins', 'Administrateurs du système SRR'),
  ('SRR_Managers', 'Gestionnaires de ressources SRR'),
  ('SRR_Users', 'Utilisateurs standard SRR'),
  ('Urbanisme', 'Service Urbanisme'),
  ('RH', 'Service Ressources Humaines'),
  ('Finances', 'Service Finances'),
  ('Culture', 'Service Culture'),
  ('DSI', 'Direction des Systèmes d''Information')
ON CONFLICT (name) DO NOTHING;

-- Association des utilisateurs aux groupes
DO $$
DECLARE
  admin_id INTEGER;
  jdupont_id INTEGER;
  smartin_id INTEGER;
  plegrand_id INTEGER;
  cmoreau_id INTEGER;
  inactif_id INTEGER;
  
  srr_admins_id INTEGER;
  srr_managers_id INTEGER;
  srr_users_id INTEGER;
  urbanisme_id INTEGER;
  rh_id INTEGER;
  finances_id INTEGER;
  culture_id INTEGER;
  dsi_id INTEGER;
BEGIN
  -- Récupération des IDs utilisateurs
  SELECT id INTO admin_id FROM users WHERE username = 'admin';
  SELECT id INTO jdupont_id FROM users WHERE username = 'jdupont';
  SELECT id INTO smartin_id FROM users WHERE username = 'smartin';
  SELECT id INTO plegrand_id FROM users WHERE username = 'plegrand';
  SELECT id INTO cmoreau_id FROM users WHERE username = 'cmoreau';
  SELECT id INTO inactif_id FROM users WHERE username = 'inactif';
  
  -- Récupération des IDs des groupes
  SELECT id INTO srr_admins_id FROM user_groups WHERE name = 'SRR_Admins';
  SELECT id INTO srr_managers_id FROM user_groups WHERE name = 'SRR_Managers';
  SELECT id INTO srr_users_id FROM user_groups WHERE name = 'SRR_Users';
  SELECT id INTO urbanisme_id FROM user_groups WHERE name = 'Urbanisme';
  SELECT id INTO rh_id FROM user_groups WHERE name = 'RH';
  SELECT id INTO finances_id FROM user_groups WHERE name = 'Finances';
  SELECT id INTO culture_id FROM user_groups WHERE name = 'Culture';
  SELECT id INTO dsi_id FROM user_groups WHERE name = 'DSI';
  
  -- Association des utilisateurs aux groupes
  INSERT INTO user_group_members (group_id, user_id)
  VALUES
    (srr_admins_id, admin_id),
    (srr_managers_id, jdupont_id),
    (srr_managers_id, cmoreau_id),
    (srr_users_id, smartin_id),
    (srr_users_id, plegrand_id),
    (srr_users_id, inactif_id),
    (urbanisme_id, jdupont_id),
    (rh_id, smartin_id),
    (finances_id, plegrand_id),
    (culture_id, cmoreau_id),
    (dsi_id, admin_id),
    (dsi_id, inactif_id)
  ON CONFLICT DO NOTHING;
END $$;

-- Création de quelques réservations de test
DO $$
DECLARE
  salle_a101_id INTEGER;
  salle_b205_id INTEGER;
  salle_conseil_id INTEGER;
  
  jdupont_id INTEGER;
  smartin_id INTEGER;
  cmoreau_id INTEGER;
  plegrand_id INTEGER;
  admin_id INTEGER;
  
  booking1_id INTEGER;
  booking2_id INTEGER;
  booking3_id INTEGER;
  booking4_id INTEGER;
BEGIN
  -- Récupération des IDs des ressources
  SELECT id INTO salle_a101_id FROM resources WHERE resource_id = 'salle-a101';
  SELECT id INTO salle_b205_id FROM resources WHERE resource_id = 'salle-b205';
  SELECT id INTO salle_conseil_id FROM resources WHERE resource_id = 'salle-conseil';
  
  -- Récupération des IDs utilisateurs
  SELECT id INTO jdupont_id FROM users WHERE username = 'jdupont';
  SELECT id INTO smartin_id FROM users WHERE username = 'smartin';
  SELECT id INTO cmoreau_id FROM users WHERE username = 'cmoreau';
  SELECT id INTO plegrand_id FROM users WHERE username = 'plegrand';
  SELECT id INTO admin_id FROM users WHERE username = 'admin';
  
  -- Création des réservations
  INSERT INTO bookings (booking_id, resource_id, user_id, title, description, start_time, end_time, status)
  VALUES
    ('booking-001', salle_a101_id, jdupont_id, 'Réunion Urbanisme', 'Discussion sur le PLU', '2025-04-24 09:00:00+00', '2025-04-24 10:30:00+00', 'confirmed'),
    ('booking-002', salle_b205_id, smartin_id, 'Entretiens RH', 'Entretiens nouveaux recrutements', '2025-04-24 14:00:00+00', '2025-04-24 17:00:00+00', 'confirmed'),
    ('booking-003', salle_conseil_id, cmoreau_id, 'Conseil Municipal', 'Séance mensuelle du conseil', '2025-04-25 18:00:00+00', '2025-04-25 20:00:00+00', 'confirmed'),
    ('booking-004', salle_a101_id, plegrand_id, 'Réunion Budget', 'Préparation budget 2026', '2025-04-26 10:00:00+00', '2025-04-26 12:00:00+00', 'pending')
  ON CONFLICT (booking_id) DO NOTHING
  RETURNING id INTO booking1_id;
  
  SELECT id INTO booking1_id FROM bookings WHERE booking_id = 'booking-001';
  SELECT id INTO booking2_id FROM bookings WHERE booking_id = 'booking-002';
  SELECT id INTO booking3_id FROM bookings WHERE booking_id = 'booking-003';
  SELECT id INTO booking4_id FROM bookings WHERE booking_id = 'booking-004';
  
  -- Association des participants aux réservations
  INSERT INTO booking_attendees (booking_id, user_id, response)
  VALUES
    (booking1_id, jdupont_id, 'accepted'),
    (booking1_id, smartin_id, 'accepted'),
    (booking2_id, smartin_id, 'accepted'),
    (booking3_id, jdupont_id, 'accepted'),
    (booking3_id, cmoreau_id, 'accepted'),
    (booking3_id, admin_id, 'tentative'),
    (booking4_id, plegrand_id, 'accepted'),
    (booking4_id, jdupont_id, 'none')
  ON CONFLICT DO NOTHING;
END $$;
