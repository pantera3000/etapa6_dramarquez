/**
 * DARK MODE CONTROLLER
 * Maneja el toggle entre light/dark mode con persistencia
 */

(function() {
    'use strict';

    const DarkMode = {
        // Configuración
        STORAGE_KEY: 'theme-preference',
        THEME_ATTR: 'data-theme',
        
        // Estado actual
        currentTheme: null,

        /**
         * Inicializar dark mode
         */
        init() {
            // Cargar tema guardado o detectar preferencia del sistema
            this.currentTheme = this.getSavedTheme() || this.getSystemPreference();
            
            // Aplicar tema inicial
            this.applyTheme(this.currentTheme);
            
            // Configurar event listeners
            this.setupListeners();
            
            // Escuchar cambios en preferencia del sistema
            this.watchSystemPreference();
            
            console.log('🌓 Dark Mode initialized:', this.currentTheme);
        },

        /**
         * Obtener tema guardado en localStorage
         */
        getSavedTheme() {
            return localStorage.getItem(this.STORAGE_KEY);
        },

        /**
         * Detectar preferencia del sistema
         */
        getSystemPreference() {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                return 'dark';
            }
            return 'light';
        },

        /**
         * Aplicar tema
         */
        applyTheme(theme) {
            document.documentElement.setAttribute(this.THEME_ATTR, theme);
            this.currentTheme = theme;
            
            // Guardar preferencia
            localStorage.setItem(this.STORAGE_KEY, theme);
            
            // Actualizar icono del toggle
            this.updateToggleIcon();
            
            // Disparar evento personalizado
            window.dispatchEvent(new CustomEvent('themeChanged', { 
                detail: { theme } 
            }));
        },

        /**
         * Toggle entre light y dark
         */
        toggle() {
            const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
            this.applyTheme(newTheme);
        },

        /**
         * Actualizar icono del botón toggle
         */
        updateToggleIcon() {
            const toggleBtn = document.querySelector('.dark-mode-toggle');
            if (!toggleBtn) return;

            const sunIcon = toggleBtn.querySelector('.icon-sun');
            const moonIcon = toggleBtn.querySelector('.icon-moon');

            if (this.currentTheme === 'dark') {
                if (sunIcon) sunIcon.style.display = 'inline-block';
                if (moonIcon) moonIcon.style.display = 'none';
                toggleBtn.setAttribute('aria-label', 'Cambiar a modo claro');
                toggleBtn.setAttribute('title', 'Modo claro');
            } else {
                if (sunIcon) sunIcon.style.display = 'none';
                if (moonIcon) moonIcon.style.display = 'inline-block';
                toggleBtn.setAttribute('aria-label', 'Cambiar a modo oscuro');
                toggleBtn.setAttribute('title', 'Modo oscuro');
            }
        },

        /**
         * Configurar event listeners
         */
        setupListeners() {
            // Click en botón toggle
            document.addEventListener('click', (e) => {
                if (e.target.closest('.dark-mode-toggle')) {
                    e.preventDefault();
                    this.toggle();
                }
            });

            // Atajo de teclado: Ctrl+Shift+D
            document.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.shiftKey && e.key === 'D') {
                    e.preventDefault();
                    this.toggle();
                }
            });
        },

        /**
         * Escuchar cambios en preferencia del sistema
         */
        watchSystemPreference() {
            if (!window.matchMedia) return;

            const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            // Listener para cambios
            darkModeQuery.addEventListener('change', (e) => {
                // Solo aplicar si el usuario no ha establecido preferencia manual
                if (!this.getSavedTheme()) {
                    const newTheme = e.matches ? 'dark' : 'light';
                    this.applyTheme(newTheme);
                }
            });
        }
    };

    // Aplicar tema INMEDIATAMENTE para evitar flash
    // (antes de que el DOM esté listo)
    const savedTheme = localStorage.getItem('theme-preference');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => DarkMode.init());
    } else {
        DarkMode.init();
    }

    // Exponer globalmente para debugging
    window.DarkMode = DarkMode;

})();
