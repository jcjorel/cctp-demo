import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { useAppSelector, useAppDispatch } from '../hooks';
import { toggleSidebar } from '../store/slices/uiSlice';
import { 
  Box, 
  CssBaseline, 
  Drawer, 
  AppBar, 
  Toolbar, 
  Typography, 
  Divider, 
  IconButton, 
  Container,
  Menu,
  MenuItem,
  Avatar,
  Tooltip
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  ChevronLeft as ChevronLeftIcon,
  Notifications as NotificationsIcon,
  AccountCircle as AccountCircleIcon
} from '@mui/icons-material';

import MainNavigation from '../components/navigation/MainNavigation';
import NotificationList from '../components/notifications/NotificationList';

const drawerWidth = 240;

/**
 * [Function intent]
 * Layout principal de l'application pour les pages authentifiées.
 * 
 * [Design principles]
 * Interface commune avec barre de navigation et menu latéral.
 * Maintien de la cohérence visuelle entre les différentes pages.
 * 
 * [Implementation details]
 * Utilise Material UI avec un design responsive.
 * Intègre la gestion d'état via Redux pour le contrôle du menu latéral.
 */
const MainLayout: React.FC = () => {
  const dispatch = useAppDispatch();
  const { sidebarOpen } = useAppSelector(state => state.ui);
  const { user } = useAppSelector(state => state.auth);
  
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [notificationsOpen, setNotificationsOpen] = useState(false);

  // Gestionnaires du menu utilisateur
  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  // Gestionnaire du menu de notifications
  const handleNotificationsToggle = () => {
    setNotificationsOpen(!notificationsOpen);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      
      {/* Barre d'application supérieure */}
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="ouvrir le tiroir"
            onClick={() => dispatch(toggleSidebar())}
            edge="start"
            sx={{ mr: 2 }}
          >
            {sidebarOpen ? <ChevronLeftIcon /> : <MenuIcon />}
          </IconButton>
          
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Système de Réservation de Ressources
          </Typography>
          
          {/* Icône de notifications */}
          <IconButton color="inherit" onClick={handleNotificationsToggle}>
            <NotificationsIcon />
          </IconButton>
          
          {/* Profil utilisateur */}
          <Tooltip title={user?.full_name || 'Profil'}>
            <IconButton
              onClick={handleMenuOpen}
              color="inherit"
            >
              <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                {user?.full_name ? user.full_name.charAt(0).toUpperCase() : <AccountCircleIcon />}
              </Avatar>
            </IconButton>
          </Tooltip>
          
          {/* Menu utilisateur */}
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={handleMenuClose}>Mon profil</MenuItem>
            <MenuItem onClick={handleMenuClose}>Mes réservations</MenuItem>
            <Divider />
            <MenuItem onClick={handleMenuClose}>Déconnexion</MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
      
      {/* Menu latéral */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { 
            width: drawerWidth, 
            boxSizing: 'border-box',
            transform: sidebarOpen ? 'translateX(0)' : 'translateX(-100%)',
            transition: (theme) => theme.transitions.create('transform', {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.enteringScreen,
            }),
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto', mt: 2 }}>
          <MainNavigation />
        </Box>
      </Drawer>
      
      {/* Contenu principal */}
      <Box component="main" sx={{ 
        flexGrow: 1, 
        p: 3,
        ml: sidebarOpen ? `${drawerWidth}px` : 0,
        transition: (theme) => theme.transitions.create('margin', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.enteringScreen,
        }),
      }}>
        <Toolbar /> {/* Espace pour compenser la AppBar */}
        <Container maxWidth="xl" sx={{ mt: 2 }}>
          <Outlet />
        </Container>
      </Box>
      
      {/* Menu de notifications (à côté) */}
      <Drawer
        anchor="right"
        open={notificationsOpen}
        onClose={handleNotificationsToggle}
      >
        <Box sx={{ width: 320, p: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Notifications
          </Typography>
          <NotificationList />
        </Box>
      </Drawer>
    </Box>
  );
};

export default MainLayout;
