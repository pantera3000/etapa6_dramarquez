/**
 * Top Navigation Bar Controller
 * Handles breadcrumb generation and search trigger
 */

(function() {
    'use strict';

    // Breadcrumb configuration
    const breadcrumbConfig = {
        'pacientes': { icon: 'bi-people', label: 'Pacientes' },
        'cumpleanos': { icon: 'bi-cake2', label: 'Cumpleaños' },
        'citas': { icon: 'bi-calendar-week', label: 'Citas' },
        'calendario': { icon: 'bi-calendar-week', label: 'Calendario' },
        'eventos': { icon: 'bi-list-check', label: 'Lista Citas' },
        'historias': { icon: 'bi-journal-medical', label: 'Historias' },
        'notas': { icon: 'bi-sticky', label: 'Notas' },
        'tratamientos': { icon: 'bi-bandaid', label: 'Tratamientos' },
        'pagos': { icon: 'bi-cash-stack', label: 'Pagos' },
        'reportes': { icon: 'bi-graph-up-arrow', label: 'Reportes' },
        'configuracion': { icon: 'bi-gear', label: 'Configuración' },
        'protocolos': { icon: 'bi-clipboard-check', label: 'Protocolos' },
        'usuarios': { icon: 'bi-person', label: 'Usuarios' }
    };

    /**
     * Generate breadcrumbs based on current path
     */
    function generateBreadcrumbs() {
        const breadcrumbNav = document.getElementById('breadcrumbNav');
        if (!breadcrumbNav) return;

        const path = window.location.pathname;
        const segments = path.split('/').filter(s => s && s !== '');
        
        // Clear existing breadcrumbs
        breadcrumbNav.innerHTML = '';

        // Home breadcrumb
        const homeItem = document.createElement('li');
        homeItem.className = 'breadcrumb-item';
        homeItem.innerHTML = '<a href="/"><i class="bi bi-house-door"></i></a>';
        breadcrumbNav.appendChild(homeItem);

        // Generate breadcrumbs for each segment
        let currentPath = '';
        segments.forEach((segment, index) => {
            currentPath += '/' + segment;
            const config = breadcrumbConfig[segment];
            
            const item = document.createElement('li');
            item.className = 'breadcrumb-item';
            
            // Last item is active
            if (index === segments.length - 1) {
                item.classList.add('active');
                item.setAttribute('aria-current', 'page');
                
                if (config) {
                    item.innerHTML = `<i class="${config.icon} me-1"></i>${config.label}`;
                } else if (!isNaN(segment)) {
                    // It's an ID, show as "Detalle"
                    item.innerHTML = 'Detalle';
                } else {
                    item.textContent = capitalize(segment);
                }
            } else {
                // Intermediate items are links
                if (config) {
                    item.innerHTML = `<a href="${currentPath}"><i class="${config.icon} me-1"></i>${config.label}</a>`;
                } else if (!isNaN(segment)) {
                    // Skip numeric IDs in intermediate breadcrumbs
                    return;
                } else {
                    item.innerHTML = `<a href="${currentPath}">${capitalize(segment)}</a>`;
                }
            }
            
            breadcrumbNav.appendChild(item);
        });
    }

    /**
     * Capitalize first letter
     */
    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    /**
     * Initialize sidebar toggle for mobile
     */
    function initSidebarToggle() {
        const toggleBtn = document.getElementById('sidebarToggle');
        const sidebar = document.getElementById('sidebar-wrapper');
        
        if (toggleBtn && sidebar) {
            toggleBtn.addEventListener('click', function() {
                sidebar.classList.toggle('show');
            });
        }
    }

    /**
     * Initialize search trigger
     */
    function initSearchTrigger() {
        const searchBtn = document.getElementById('searchTrigger');
        const searchBtnDesktop = document.getElementById('searchTriggerDesktop');
        
        if (searchBtn) {
            searchBtn.addEventListener('click', function() {
                if (window.openSearchModal) {
                    window.openSearchModal();
                }
            });
        }
        
        if (searchBtnDesktop) {
            searchBtnDesktop.addEventListener('click', function() {
                if (window.openSearchModal) {
                    window.openSearchModal();
                }
            });
        }

        // Keyboard shortcut Ctrl+K / Cmd+K
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                if (window.openSearchModal) {
                    window.openSearchModal();
                }
            }
        });
    }

    /**
     * Initialize tooltips
     */
    function initTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        generateBreadcrumbs();
        initSidebarToggle();
        initSearchTrigger();
        initTooltips();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
