/**
 * navigation.js - Script de navigation entre les mockups du SRR
 * Système de Réservation de Ressources - Plaine Commune & Saint-Denis
 *
 * Ce script gère la navigation entre les mockups et assure une expérience cohérente
 * tout en facilitant la démonstration des parcours utilisateurs.
 */

document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    highlightActiveLink();
    setupMockupControls();
    initNotifications();
    setupSearchForm();
});

/**
 * Initialise les éléments de navigation
 */
function initNavigation() {
    // Gestion du menu mobile (hamburger)
    const menuToggle = document.querySelector('.menu-toggle');
    const navList = document.querySelector('.nav-list');
    
    if (menuToggle && navList) {
        menuToggle.addEventListener('click', function() {
            navList.classList.toggle('nav-list--visible');
            menuToggle.classList.toggle('menu-toggle--active');
        });
    }
    
    // Gestion du menu utilisateur
    const userMenuToggle = document.querySelector('.user-avatar');
    const userMenu = document.querySelector('.user-menu');
    
    if (userMenuToggle && userMenu) {
        userMenuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            userMenu.classList.toggle('user-menu--visible');
        });
        
        // Fermer le menu utilisateur lorsqu'on clique à l'extérieur
        document.addEventListener('click', function(e) {
            if (!userMenuToggle.contains(e.target) && !userMenu.contains(e.target)) {
                userMenu.classList.remove('user-menu--visible');
            }
        });
    }
}

/**
 * Met en surbrillance le lien actif dans la navigation
 */
function highlightActiveLink() {
    // Obtenir le chemin de la page actuelle
    const currentPath = window.location.pathname;
    const currentPageName = currentPath.substring(currentPath.lastIndexOf('/') + 1);
    
    // Parcourir tous les liens de navigation et trouver celui qui correspond à la page actuelle
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        if (linkHref === currentPageName || 
            (currentPageName === '' && linkHref === 'index.html') ||
            (currentPageName === 'home.html' && linkHref === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Configure les contrôles spécifiques aux mockups
 */
function setupMockupControls() {
    // Gestion des modals
    const modalTriggers = document.querySelectorAll('[data-toggle="modal"]');
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const targetModalId = this.getAttribute('data-target');
            const targetModal = document.getElementById(targetModalId);
            
            if (targetModal) {
                targetModal.style.display = 'flex';
                
                // Gestion de la fermeture du modal
                const closeButtons = targetModal.querySelectorAll('.modal-close, [data-dismiss="modal"]');
                closeButtons.forEach(button => {
                    button.addEventListener('click', function() {
                        targetModal.style.display = 'none';
                    });
                });
                
                // Fermer le modal en cliquant sur l'overlay
                targetModal.addEventListener('click', function(e) {
                    if (e.target === targetModal) {
                        targetModal.style.display = 'none';
                    }
                });
            }
        });
    });
    
    // Boutons de déconnexion
    const logoutButtons = document.querySelectorAll('[data-action="logout"]');
    logoutButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '../../screens/user/login.html';
        });
    });
    
    // Simulation de soumission de formulaires
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Déterminer l'action basée sur l'ID ou la classe du formulaire
            if (form.id === 'login-form' || form.classList.contains('login-form')) {
                window.location.href = '../../screens/user/home.html';
            } else if (form.id === 'search-form' || form.classList.contains('search-form')) {
                // Si présent sur la page de recherche, simuler une recherche
                if (window.location.pathname.includes('search.html')) {
                    const resultsSection = document.querySelector('.search-results');
                    if (resultsSection) {
                        resultsSection.style.display = 'block';
                        window.scrollTo(0, resultsSection.offsetTop - 20);
                    }
                } else {
                    // Sinon, rediriger vers la page de recherche
                    window.location.href = '../../screens/user/search.html';
                }
            } else if (form.id === 'booking-form' || form.classList.contains('booking-form')) {
                window.location.href = '../../screens/user/booking-confirmation.html';
            }
        });
    });
}

/**
 * Initialise les comportements des notifications
 */
function initNotifications() {
    // Fermer les notifications
    const notificationCloseButtons = document.querySelectorAll('.notification-close');
    notificationCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const notification = this.closest('.notification');
            if (notification) {
                notification.style.opacity = '0';
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 300);
            }
        });
    });
}

/**
 * Configure le formulaire de recherche
 */
function setupSearchForm() {
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('.search-input');
        
        // Suggestions de recherche (simulation)
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                const value = this.value.trim().toLowerCase();
                
                // Afficher des suggestions si la valeur n'est pas vide
                if (value.length > 0) {
                    // Créer ou récupérer le conteneur de suggestions
                    let suggestionsContainer = document.querySelector('.search-suggestions');
                    
                    if (!suggestionsContainer) {
                        suggestionsContainer = document.createElement('div');
                        suggestionsContainer.className = 'search-suggestions';
                        searchForm.appendChild(suggestionsContainer);
                    }
                    
                    // Suggestions exemple basées sur la saisie
                    let suggestions = [];
                    
                    if (value.includes('salle') || value.includes('réunion')) {
                        suggestions.push('Salle Pleyel', 'Salle du Conseil', 'Salle de réunion A102');
                    } else if (value.includes('voiture') || value.includes('véhicule')) {
                        suggestions.push('Renault Zoé', 'Citroën C3', 'Peugeot 208');
                    } else if (value.includes('projecteur') || value.includes('équipement')) {
                        suggestions.push('Projecteur Epson', 'Écran interactif', 'Système de sonorisation');
                    } else {
                        // Suggestions génériques
                        suggestions.push(
                            'Salle de réunion',
                            'Véhicule de service',
                            'Équipement audiovisuel'
                        );
                    }
                    
                    // Limiter à 5 suggestions
                    suggestions = suggestions.slice(0, 5);
                    
                    // Afficher les suggestions
                    suggestionsContainer.innerHTML = '';
                    suggestions.forEach(suggestion => {
                        const item = document.createElement('div');
                        item.className = 'search-suggestion-item';
                        item.textContent = suggestion;
                        item.addEventListener('click', function() {
                            searchInput.value = suggestion;
                            suggestionsContainer.innerHTML = '';
                            suggestionsContainer.style.display = 'none';
                        });
                        suggestionsContainer.appendChild(item);
                    });
                    
                    suggestionsContainer.style.display = 'block';
                } else {
                    // Cacher les suggestions si la valeur est vide
                    const suggestionsContainer = document.querySelector('.search-suggestions');
                    if (suggestionsContainer) {
                        suggestionsContainer.style.display = 'none';
                    }
                }
            });
            
            // Cacher les suggestions quand on clique ailleurs
            document.addEventListener('click', function(e) {
                if (!searchInput.contains(e.target)) {
                    const suggestionsContainer = document.querySelector('.search-suggestions');
                    if (suggestionsContainer) {
                        suggestionsContainer.style.display = 'none';
                    }
                }
            });
        }
    }
}

/**
 * Fonctions utilitaires pour la démo des mockups
 */
const MockupDemo = {
    // Simuler une notification
    showNotification: function(type, title, message) {
        const notificationsContainer = document.querySelector('.notifications-container') || document.body;
        
        const notification = document.createElement('div');
        notification.className = `notification notification-${type} mb-md`;
        
        const icon = document.createElement('span');
        icon.className = 'notification-icon';
        
        // Définir l'icône en fonction du type
        switch (type) {
            case 'success': icon.textContent = '✓'; break;
            case 'info': icon.textContent = 'i'; break;
            case 'warning': icon.textContent = '!'; break;
            case 'error': icon.textContent = '⚠'; break;
            default: icon.textContent = 'i';
        }
        
        const content = document.createElement('div');
        content.className = 'notification-content';
        
        const titleElement = document.createElement('h4');
        titleElement.className = 'notification-title';
        titleElement.textContent = title;
        
        const messageElement = document.createElement('p');
        messageElement.className = 'notification-message';
        messageElement.textContent = message;
        
        const closeButton = document.createElement('button');
        closeButton.className = 'notification-close';
        closeButton.innerHTML = '&times;';
        closeButton.addEventListener('click', function() {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        });
        
        content.appendChild(titleElement);
        content.appendChild(messageElement);
        
        notification.appendChild(icon);
        notification.appendChild(content);
        notification.appendChild(closeButton);
        
        // Ajouter au conteneur et configurer l'auto-disparition
        notificationsContainer.appendChild(notification);
        
        // Disparaître après 5 secondes
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    },
    
    // Toggle la visibilité d'une section
    toggleSection: function(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            const isVisible = section.style.display !== 'none';
            section.style.display = isVisible ? 'none' : 'block';
            return !isVisible;
        }
        return false;
    }
};

// Exposer les fonctions utilitaires globalement pour la démo
window.MockupDemo = MockupDemo;
