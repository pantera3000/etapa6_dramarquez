/**
 * Pacientes List - Filtros y Ordenamiento
 * Maneja filtrado en tiempo real y ordenamiento de tabla
 */

(function() {
    'use strict';

    let currentSort = { column: null, direction: 'asc' };

    /**
     * Inicializar filtros
     */
    function initFilters() {
        const searchInput = document.querySelector('input[name="q"]');
        const ageFilter = document.getElementById('ageFilter');
        const genderFilter = document.getElementById('genderFilter');
        const statusFilter = document.getElementById('statusFilter');

        if (searchInput) {
            searchInput.addEventListener('input', debounce(applyFilters, 300));
        }

        if (ageFilter) {
            ageFilter.addEventListener('change', applyFilters);
        }

        if (genderFilter) {
            genderFilter.addEventListener('change', applyFilters);
        }

        if (statusFilter) {
            statusFilter.addEventListener('change', applyFilters);
        }
    }

    /**
     * Aplicar filtros a las filas de la tabla
     */
    function applyFilters() {
        const searchTerm = document.querySelector('input[name="q"]')?.value.toLowerCase() || '';
        const ageRange = document.getElementById('ageFilter')?.value || 'all';
        const gender = document.getElementById('genderFilter')?.value || 'all';
        const status = document.getElementById('statusFilter')?.value || 'all';

        const rows = document.querySelectorAll('.table-saas tbody tr');
        let visibleCount = 0;

        rows.forEach(row => {
            const name = row.querySelector('.patient-name')?.textContent.toLowerCase() || '';
            const dni = row.querySelector('.patient-meta')?.textContent.toLowerCase() || '';
            const age = parseInt(row.dataset.age) || 0;
            const rowGender = row.dataset.gender || '';
            const rowStatus = row.dataset.status || '';

            // Filtro de búsqueda
            const matchesSearch = searchTerm === '' || name.includes(searchTerm) || dni.includes(searchTerm);

            // Filtro de edad
            let matchesAge = true;
            if (ageRange !== 'all') {
                const [min, max] = ageRange.split('-').map(Number);
                if (max) {
                    matchesAge = age >= min && age <= max;
                } else {
                    matchesAge = age >= min;
                }
            }

            // Filtro de género
            const matchesGender = gender === 'all' || rowGender === gender;

            // Filtro de estado
            const matchesStatus = status === 'all' || rowStatus === status;

            // Mostrar/ocultar fila
            if (matchesSearch && matchesAge && matchesGender && matchesStatus) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });

        // Mostrar mensaje si no hay resultados
        updateEmptyState(visibleCount);
    }

    /**
     * Actualizar mensaje de estado vacío
     */
    function updateEmptyState(count) {
        let emptyState = document.getElementById('emptyState');
        
        if (count === 0) {
            if (!emptyState) {
                emptyState = document.createElement('tr');
                emptyState.id = 'emptyState';
                emptyState.innerHTML = `
                    <td colspan="100%" class="text-center py-5 text-muted">
                        <i class="bi bi-search fs-1 opacity-25"></i>
                        <p class="mb-0 mt-2">No se encontraron pacientes con los filtros aplicados</p>
                    </td>
                `;
                document.querySelector('.table-saas tbody').appendChild(emptyState);
            }
            emptyState.style.display = '';
        } else if (emptyState) {
            emptyState.style.display = 'none';
        }
    }

    /**
     * Inicializar ordenamiento de tabla
     */
    function initSorting() {
        const headers = document.querySelectorAll('.sortable');
        
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                const column = header.dataset.sort;
                sortTable(column);
            });
        });
    }

    /**
     * Ordenar tabla por columna
     */
    function sortTable(column) {
        const tbody = document.querySelector('.table-saas tbody');
        const rows = Array.from(tbody.querySelectorAll('tr:not(#emptyState)'));

        // Determinar dirección
        if (currentSort.column === column) {
            currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
        } else {
            currentSort.column = column;
            currentSort.direction = 'asc';
        }

        // Ordenar filas
        rows.sort((a, b) => {
            let aVal, bVal;

            switch(column) {
                case 'nombre':
                    aVal = a.querySelector('.patient-name')?.textContent || '';
                    bVal = b.querySelector('.patient-name')?.textContent || '';
                    break;
                case 'edad':
                    aVal = parseInt(a.dataset.age) || 0;
                    bVal = parseInt(b.dataset.age) || 0;
                    break;
                case 'telefono':
                    aVal = a.dataset.telefono || '';
                    bVal = b.dataset.telefono || '';
                    break;
                case 'fecha':
                    aVal = new Date(a.dataset.fecha || 0);
                    bVal = new Date(b.dataset.fecha || 0);
                    break;
                default:
                    return 0;
            }

            if (typeof aVal === 'string') {
                return currentSort.direction === 'asc' 
                    ? aVal.localeCompare(bVal)
                    : bVal.localeCompare(aVal);
            } else {
                return currentSort.direction === 'asc'
                    ? aVal - bVal
                    : bVal - aVal;
            }
        });

        // Reordenar DOM
        rows.forEach(row => tbody.appendChild(row));

        // Actualizar indicadores visuales
        updateSortIndicators(column);
    }

    /**
     * Actualizar indicadores de ordenamiento
     */
    function updateSortIndicators(column) {
        document.querySelectorAll('.sortable').forEach(header => {
            const icon = header.querySelector('.sort-icon');
            if (icon) {
                if (header.dataset.sort === column) {
                    icon.className = currentSort.direction === 'asc' 
                        ? 'bi bi-arrow-up sort-icon'
                        : 'bi bi-arrow-down sort-icon';
                } else {
                    icon.className = 'bi bi-arrow-down-up sort-icon opacity-25';
                }
            }
        });
    }

    /**
     * Debounce helper
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Inicializar todo
     */
    function init() {
        initFilters();
        initSorting();
    }

    // Ejecutar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
