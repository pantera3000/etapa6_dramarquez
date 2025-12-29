/**
 * Global Search Modal Controller
 * Handles Ctrl+K search with keyboard navigation and AJAX results
 */

(function() {
    'use strict';

    let searchModal = null;
    let searchInput = null;
    let searchResults = null;
    let currentResults = [];
    let selectedIndex = -1;
    let searchTimeout = null;

    /**
     * Initialize search modal
     */
    function init() {
        searchModal = document.getElementById('searchModal');
        searchInput = document.getElementById('searchInput');
        searchResults = document.querySelector('.search-results-container');
        
        if (!searchModal || !searchInput) return;

        // Keyboard shortcuts
        document.addEventListener('keydown', handleGlobalKeydown);
        
        // Modal controls
        document.getElementById('searchBackdrop')?.addEventListener('click', closeModal);
        document.getElementById('searchClose')?.addEventListener('click', closeModal);
        
        // Search input
        searchInput.addEventListener('input', handleSearchInput);
        searchInput.addEventListener('keydown', handleSearchKeydown);
        
        // Connect to topbar search button
        const searchTrigger = document.getElementById('searchTrigger');
        if (searchTrigger) {
            searchTrigger.addEventListener('click', openModal);
        }
    }

    /**
     * Handle global keyboard shortcuts
     */
    function handleGlobalKeydown(e) {
        // Ctrl+K or Cmd+K to open
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            openModal();
        }
        
        // Escape to close
        if (e.key === 'Escape' && searchModal.classList.contains('show')) {
            closeModal();
        }
    }

    /**
     * Open search modal
     */
    function openModal() {
        searchModal.classList.add('show');
        searchInput.value = '';
        searchInput.focus();
        selectedIndex = -1;
        showEmptyState();
        document.body.style.overflow = 'hidden';
    }

    /**
     * Close search modal
     */
    function closeModal() {
        searchModal.classList.remove('show');
        document.body.style.overflow = '';
        searchInput.value = '';
        currentResults = [];
    }

    /**
     * Handle search input
     */
    function handleSearchInput(e) {
        const query = e.target.value.trim();
        
        // Clear previous timeout
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }
        
        if (query.length === 0) {
            showEmptyState();
            return;
        }
        
        if (query.length < 2) {
            return; // Wait for at least 2 characters
        }
        
        // Debounce search
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    }

    /**
     * Handle keyboard navigation in search
     */
    function handleSearchKeydown(e) {
        if (currentResults.length === 0) return;
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, currentResults.length - 1);
                updateSelection();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                updateSelection();
                break;
                
            case 'Enter':
                e.preventDefault();
                if (selectedIndex >= 0 && currentResults[selectedIndex]) {
                    navigateToResult(currentResults[selectedIndex]);
                }
                break;
        }
    }

    /**
     * Perform AJAX search
     */
    function performSearch(query) {
        showLoadingState();
        
        fetch(`/api/search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displayResults(data, query);
            })
            .catch(error => {
                console.error('Search error:', error);
                showNoResults();
            });
    }

    /**
     * Display search results
     */
    function displayResults(data, query) {
        currentResults = [];
        selectedIndex = -1;
        
        let html = '';
        let hasResults = false;
        
        // Pacientes
        if (data.pacientes && data.pacientes.length > 0) {
            hasResults = true;
            html += createCategorySection('pacientes', 'Pacientes', data.pacientes);
            currentResults.push(...data.pacientes.map(p => ({...p, type: 'paciente'})));
        }
        
        // Tratamientos
        if (data.tratamientos && data.tratamientos.length > 0) {
            hasResults = true;
            html += createCategorySection('tratamientos', 'Tratamientos', data.tratamientos);
            currentResults.push(...data.tratamientos.map(t => ({...t, type: 'tratamiento'})));
        }
        
        // Notas
        if (data.notas && data.notas.length > 0) {
            hasResults = true;
            html += createCategorySection('notas', 'Notas', data.notas);
            currentResults.push(...data.notas.map(n => ({...n, type: 'nota'})));
        }
        
        // Historias
        if (data.historias && data.historias.length > 0) {
            hasResults = true;
            html += createCategorySection('historias', 'Historias Clínicas', data.historias);
            currentResults.push(...data.historias.map(h => ({...h, type: 'historia'})));
        }
        
        if (hasResults) {
            searchResults.innerHTML = html;
            showResultsState();
            
            // Add click handlers
            document.querySelectorAll('.search-result-item').forEach((item, index) => {
                item.addEventListener('click', () => navigateToResult(currentResults[index]));
                item.addEventListener('mouseenter', () => {
                    selectedIndex = index;
                    updateSelection();
                });
            });
        } else {
            showNoResults();
        }
    }

    /**
     * Create category section HTML
     */
    function createCategorySection(type, title, items) {
        const icons = {
            'pacientes': 'bi-people',
            'tratamientos': 'bi-bandaid',
            'notas': 'bi-sticky',
            'historias': 'bi-journal-medical'
        };
        
        let html = `
            <div class="search-category">
                <div class="search-category-title">
                    <i class="bi ${icons[type]}"></i>
                    ${title}
                </div>
        `;
        
        items.forEach(item => {
            html += createResultItem(item, type);
        });
        
        html += '</div>';
        return html;
    }

    /**
     * Create result item HTML
     */
    function createResultItem(item, type) {
        const icons = {
            'pacientes': 'bi-person-circle',
            'tratamientos': 'bi-bandaid',
            'notas': 'bi-sticky-fill',
            'historias': 'bi-journal-medical'
        };
        
        let title = '';
        let subtitle = '';
        let url = '';
        
        switch(type) {
            case 'pacientes':
                title = item.nombre_completo || item.nombre;
                subtitle = `DNI: ${item.dni || 'N/A'}`;
                url = `/pacientes/${item.id}/`;
                break;
            case 'tratamientos':
                title = item.descripcion || 'Tratamiento';
                subtitle = `Paciente: ${item.paciente_nombre || 'N/A'}`;
                url = `/tratamientos/${item.id}/`;
                break;
            case 'notas':
                title = item.titulo || 'Nota';
                subtitle = item.contenido ? item.contenido.substring(0, 60) + '...' : '';
                url = `/notas/${item.id}/`;
                break;
            case 'historias':
                title = item.motivo || 'Historia Clínica';
                subtitle = `Paciente: ${item.paciente_nombre || 'N/A'}`;
                url = `/historias/${item.id}/`;
                break;
        }
        
        return `
            <div class="search-result-item" data-url="${url}">
                <div class="search-result-icon ${type.slice(0, -1)}">
                    <i class="bi ${icons[type]}"></i>
                </div>
                <div class="search-result-content">
                    <div class="search-result-title">${title}</div>
                    <div class="search-result-subtitle">${subtitle}</div>
                </div>
                <i class="bi bi-arrow-right search-result-arrow"></i>
            </div>
        `;
    }

    /**
     * Update selection highlight
     */
    function updateSelection() {
        document.querySelectorAll('.search-result-item').forEach((item, index) => {
            if (index === selectedIndex) {
                item.classList.add('active');
                item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            } else {
                item.classList.remove('active');
            }
        });
    }

    /**
     * Navigate to selected result
     */
    function navigateToResult(result) {
        const item = document.querySelector(`.search-result-item[data-url="${getResultUrl(result)}"]`);
        if (item) {
            const url = item.dataset.url;
            window.location.href = url;
        }
    }

    /**
     * Get URL for result
     */
    function getResultUrl(result) {
        switch(result.type) {
            case 'paciente':
                return `/pacientes/${result.id}/`;
            case 'tratamiento':
                return `/tratamientos/${result.id}/`;
            case 'nota':
                return `/notas/${result.id}/`;
            case 'historia':
                return `/historias/${result.id}/`;
            default:
                return '#';
        }
    }

    /**
     * Show empty state
     */
    function showEmptyState() {
        document.querySelector('.search-empty-state').style.display = 'flex';
        document.querySelector('.search-loading').style.display = 'none';
        document.querySelector('.search-results-container').style.display = 'none';
        document.querySelector('.search-no-results').style.display = 'none';
    }

    /**
     * Show loading state
     */
    function showLoadingState() {
        document.querySelector('.search-empty-state').style.display = 'none';
        document.querySelector('.search-loading').style.display = 'flex';
        document.querySelector('.search-results-container').style.display = 'none';
        document.querySelector('.search-no-results').style.display = 'none';
    }

    /**
     * Show results state
     */
    function showResultsState() {
        document.querySelector('.search-empty-state').style.display = 'none';
        document.querySelector('.search-loading').style.display = 'none';
        document.querySelector('.search-results-container').style.display = 'block';
        document.querySelector('.search-no-results').style.display = 'none';
    }

    /**
     * Show no results state
     */
    function showNoResults() {
        document.querySelector('.search-empty-state').style.display = 'none';
        document.querySelector('.search-loading').style.display = 'none';
        document.querySelector('.search-results-container').style.display = 'none';
        document.querySelector('.search-no-results').style.display = 'flex';
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose openModal globally for topbar
    window.openSearchModal = openModal;

})();
