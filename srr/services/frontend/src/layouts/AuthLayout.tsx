import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { useAppSelector } from '../hooks';
import { Box, Container, Paper, Typography } from '@mui/material';

/**
 * [Function intent]
 * Layout pour les pages d'authentification non protégées.
 * 
 * [Design principles]
 * Interface épurée centrée sur les fonctionnalités d'authentification.
 * Redirection automatique si l'utilisateur est déjà authentifié.
 * 
 * [Implementation details]
 * Utilise Material UI avec une mise en page centrée et simplifiée.
 * Vérifie l'état d'authentification via Redux.
 */
const AuthLayout: React.FC = () => {
  const { isAuthenticated } = useAppSelector(state => state.auth);
  
  // Si l'utilisateur est déjà authentifié, rediriger vers le tableau de bord
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: (theme) => theme.palette.background.default,
        py: 4,
      }}
    >
      <Container maxWidth="xs">
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            borderRadius: 2,
          }}
        >
          <Typography
            component="h1"
            variant="h4"
            align="center"
            color="primary"
            gutterBottom
          >
            SRR
          </Typography>
          <Typography variant="h6" align="center" gutterBottom>
            Système de Réservation de Ressources
          </Typography>
          
          <Box sx={{ width: '100%', mt: 2 }}>
            <Outlet />
          </Box>
        </Paper>
      </Container>
      
      <Typography variant="body2" color="text.secondary" sx={{ mt: 4 }}>
        © {new Date().getFullYear()} Mairie de Saint-Denis
      </Typography>
    </Box>
  );
};

export default AuthLayout;
