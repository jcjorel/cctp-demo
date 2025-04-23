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
 * Composant racine de l'application SRR qui définit la structure de routage
 * complète et fournit les contextes globaux comme le thème et l'authentification.
 *
 * [Source file design principles]
 * - Organisation hiérarchique des routes avec protection d'authentification
 * - Séparation des layouts par contexte d'utilisation (authentifié, non authentifié)
 * - Vérification périodique de la validité de l'authentification
 * - Structure de navigation reflétant les fonctionnalités principales du système
 *
 * [Source file constraints]
 * - Dépend des contextes Redux pour l'état d'authentification
 * - Fonctionne avec React Router v6+ uniquement
 * - Doit intégrer MUI pour le système de thème cohérent
 *
 * [Dependencies]
 * - react-router-dom: Système de routage et navigation
 * - @mui/material: Framework UI pour le thème et composants
 * - src/hooks/index.ts: Hooks personnalisés pour accéder à Redux
 * - src/store/slices/authSlice.ts: Gestion de l'authentification
 * - src/layouts/* et src/pages/*: Composants de structure et de page
 *
 * [GenAI tool change history]
 * 2025-04-23T11:04:00Z : Ajout du header GenAI par CodeAssistant
 * * Ajout du header de fichier conforme aux directives
 */

import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { useAppDispatch, useAppSelector } from './hooks';
import { checkTokenExpiration } from './store/slices/authSlice';

import theme from './styles/theme';

// Layouts
import MainLayout from './layouts/MainLayout';
import AuthLayout from './layouts/AuthLayout';

// Pages
import LoginPage from './pages/auth/LoginPage';
import DashboardPage from './pages/dashboard/DashboardPage';
import ResourcesPage from './pages/resources/ResourcesPage';
import ResourceDetailPage from './pages/resources/ResourceDetailPage';
import BookingsPage from './pages/bookings/BookingsPage';
import BookingDetailPage from './pages/bookings/BookingDetailPage';
import CreateBookingPage from './pages/bookings/CreateBookingPage';
import ProfilePage from './pages/user/ProfilePage';
import NotFoundPage from './pages/NotFoundPage';

// Route Guards
import ProtectedRoute from './components/auth/ProtectedRoute';

/**
 * [Function intent]
 * Composant racine de l'application SRR définissant la structure globale de l'interface.
 * 
 * [Design principles]
 * Organisation des routes selon les fonctionnalités principales du système.
 * Protection des routes nécessitant une authentification.
 * 
 * [Implementation details]
 * Utilise React Router pour la navigation et MUI pour le thème d'interface.
 * Intègre la vérification périodique de validité du token d'authentification.
 */
const App: React.FC = () => {
  const dispatch = useAppDispatch();
  
  // Vérifier l'expiration du token périodiquement
  useEffect(() => {
    dispatch(checkTokenExpiration());
    
    const tokenCheckInterval = setInterval(() => {
      dispatch(checkTokenExpiration());
    }, 60000); // Vérification toutes les minutes
    
    return () => {
      clearInterval(tokenCheckInterval);
    };
  }, [dispatch]);

  return (
    <ThemeProvider theme={theme}>
      <Routes>
        {/* Routes publiques */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
        </Route>
        
        {/* Routes protégées */}
        <Route element={<ProtectedRoute />}>
          <Route element={<MainLayout />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            
            <Route path="/dashboard" element={<DashboardPage />} />
            
            <Route path="/resources">
              <Route index element={<ResourcesPage />} />
              <Route path=":resourceId" element={<ResourceDetailPage />} />
            </Route>
            
            <Route path="/bookings">
              <Route index element={<BookingsPage />} />
              <Route path="create" element={<CreateBookingPage />} />
              <Route path=":bookingId" element={<BookingDetailPage />} />
            </Route>
            
            <Route path="/profile" element={<ProfilePage />} />
          </Route>
        </Route>
        
        {/* Route par défaut (404) */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </ThemeProvider>
  );
};

export default App;
