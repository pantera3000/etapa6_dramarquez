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
     * Initialize bottom navigation
     */
    function init() {
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
        console.log('Menu button found:', menuBtn);
        if (menuBtn) {
            menuBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Menu button clicked!');
                const sidebar = document.getElementById('sidebar-wrapper');
                console.log('Sidebar found:', sidebar);
                if (sidebar) {
                    sidebar.classList.add('show');
                    console.log('Sidebar show class added');
                } else {
                    console.error('Sidebar not found!');
                }
            });
        } else {
            console.error('Menu button not found!');
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
