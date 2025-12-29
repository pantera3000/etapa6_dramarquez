/**
 * Mobile Bottom Navigation Controller
 * Handles FAB menu, active states, and navigation
 */

(function() {
    'use strict';

    let fabButton = null;
    let fabMenu = null;
    let fabBackdrop = null;
    let bottomNav = null;

    /**
     * CRITICAL FIX: Eliminar menú flotante del DOM en desktop
     */
    function removeBottomNavOnDesktop() {
        if (window.innerWidth >= 768) {
            const bottomNav = document.getElementById('bottomNav');
            const fabMenu = document.getElementById('fabMenu');
            
            if (bottomNav) {
                bottomNav.remove();
                console.log('Bottom nav removed from DOM (desktop detected)');
            }
            if (fabMenu) {
                fabMenu.remove();
                console.log('FAB menu removed from DOM (desktop detected)');
            }
            return true; // Desktop detected, elements removed
        }
        return false; // Mobile, keep elements
    }

    /**
     * Initialize bottom navigation
     */
    function init() {
        // CRITICAL: Remove bottom nav on desktop BEFORE any initialization
        if (removeBottomNavOnDesktop()) {
            console.log('Desktop detected - bottom nav initialization skipped');
            return; // Exit early, don't initialize
        }
        
        fabButton = document.getElementById('fabButton');
        fabMenu = document.getElementById('fabMenu');
        fabBackdrop = fabMenu?.querySelector('.fab-backdrop');
        bottomNav = document.getElementById('bottomNav');
        
        if (fabButton && fabMenu) {
            // FAB button click
            fabButton.addEventListener('click', toggleFabMenu);
            
            // Backdrop click to close
            if (fabBackdrop) {
                fabBackdrop.addEventListener('click', closeFabMenu);
            }
        }
        
        // Navigation buttons
        initNavigationButtons();
        
        // Set active button based on current page
        setActiveButton();
        
        // Search button
        const searchBtn = document.getElementById('searchBottomNav');
        if (searchBtn) {
            searchBtn.addEventListener('click', function(e) {
                e.preventDefault();
                if (window.openSearchModal) {
                    window.openSearchModal();
                }
            });
        }
        
        // Menu button (open sidebar)
        const menuBtn = document.getElementById('menuBottomNav');
        if (menuBtn) {
            menuBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                openSidebar();
            });
        }
        
        // Sidebar close button
        const sidebarCloseBtn = document.getElementById('sidebarClose');
        if (sidebarCloseBtn) {
            sidebarCloseBtn.addEventListener('click', function(e) {
                e.preventDefault();
                closeSidebar();
            });
        }
    }

    /**
     * Open sidebar with backdrop
     */
    function openSidebar() {
        const sidebar = document.getElementById('sidebar-wrapper');
        if (sidebar) {
            sidebar.classList.add('show');
            
            // Create backdrop if it doesn't exist
            let backdrop = document.getElementById('sidebar-backdrop');
            if (!backdrop) {
                backdrop = document.createElement('div');
                backdrop.id = 'sidebar-backdrop';
                backdrop.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0, 0, 0, 0.5);
                    z-index: 999;
                    display: none;
                `;
                document.body.appendChild(backdrop);
                
                // Close sidebar when clicking backdrop
                backdrop.addEventListener('click', closeSidebar);
            }
            
            backdrop.style.display = 'block';
        }
    }

    /**
     * Close sidebar and remove backdrop
     */
    function closeSidebar() {
        const sidebar = document.getElementById('sidebar-wrapper');
        const backdrop = document.getElementById('sidebar-backdrop');
        
        if (sidebar) {
            sidebar.classList.remove('show');
        }
        
        if (backdrop) {
            backdrop.style.display = 'none';
        }
    }

    /**
     * Toggle FAB menu
     */
    function toggleFabMenu(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const isActive = fabMenu.classList.contains('active');
        
        if (isActive) {
            closeFabMenu();
        } else {
            openFabMenu();
        }
    }

    /**
     * Open FAB menu
     */
    function openFabMenu() {
        fabMenu.classList.add('active');
        fabButton.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    /**
     * Close FAB menu
     */
    function closeFabMenu() {
        fabMenu.classList.remove('active');
        fabButton.classList.remove('active');
        document.body.style.overflow = '';
    }

    /**
     * Initialize navigation buttons
     */
    function initNavigationButtons() {
        const navButtons = document.querySelectorAll('.bottom-nav-item[data-url]');
        
        navButtons.forEach(button => {
            button.addEventListener('click', function() {
                const url = this.dataset.url;
                if (url) {
                    window.location.href = url;
                }
            });
        });
    }

    /**
     * Set active button based on current page
     */
    function setActiveButton() {
        const currentPath = window.location.pathname;
        const navButtons = document.querySelectorAll('.bottom-nav-item[data-action]');
        
        // Remove all active states
        navButtons.forEach(btn => btn.classList.remove('active'));
        
        // Determine which button should be active
        if (currentPath === '/' || currentPath.includes('/pacientes/') && currentPath.split('/').length === 3) {
            // Home or root pacientes list
            const homeBtn = document.querySelector('[data-action="home"]');
            if (homeBtn) homeBtn.classList.add('active');
        } else if (currentPath.includes('/pacientes/')) {
            const patientsBtn = document.querySelector('[data-action="patients"]');
            if (patientsBtn) patientsBtn.classList.add('active');
        } else if (currentPath.includes('/citas/')) {
            // Could add a citas button if needed
            const homeBtn = document.querySelector('[data-action="home"]');
            if (homeBtn) homeBtn.classList.add('active');
        }
    }

    /**
     * Handle window resize
     */
    function handleResize() {
        if (window.innerWidth >= 768) {
            // Desktop - close FAB menu if open
            closeFabMenu();
        }
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Handle resize
    window.addEventListener('resize', handleResize);

    // Close FAB menu on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && fabMenu?.classList.contains('active')) {
            closeFabMenu();
        }
    });

})();
