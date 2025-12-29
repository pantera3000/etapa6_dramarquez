/**
 * Mobile Gestures Controller
 * Handles touch gestures for sidebar and other mobile interactions
 */

(function() {
    'use strict';

    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;
    let isSwiping = false;

    const SWIPE_THRESHOLD = 50; // Minimum distance for swipe
    const SWIPE_VELOCITY_THRESHOLD = 0.3; // Minimum velocity
    const sidebar = document.getElementById('sidebar-wrapper');
    const wrapper = document.getElementById('wrapper');

    /**
     * Initialize mobile gestures
     */
    function init() {
        if (!sidebar || !wrapper) return;

        // Only enable on mobile/tablet
        if (window.innerWidth <= 992) {
            enableSwipeGestures();
        }

        // Re-enable on resize
        window.addEventListener('resize', function() {
            if (window.innerWidth <= 992) {
                enableSwipeGestures();
            } else {
                disableSwipeGestures();
            }
        });
    }

    /**
     * Enable swipe gestures
     */
    function enableSwipeGestures() {
        document.addEventListener('touchstart', handleTouchStart, { passive: true });
        document.addEventListener('touchmove', handleTouchMove, { passive: false });
        document.addEventListener('touchend', handleTouchEnd, { passive: true });
    }

    /**
     * Disable swipe gestures
     */
    function disableSwipeGestures() {
        document.removeEventListener('touchstart', handleTouchStart);
        document.removeEventListener('touchmove', handleTouchMove);
        document.removeEventListener('touchend', handleTouchEnd);
    }

    /**
     * Handle touch start
     */
    function handleTouchStart(e) {
        touchStartX = e.changedTouches[0].screenX;
        touchStartY = e.changedTouches[0].screenY;
        isSwiping = false;
    }

    /**
     * Handle touch move
     */
    function handleTouchMove(e) {
        if (!isSwiping) {
            const deltaX = Math.abs(e.changedTouches[0].screenX - touchStartX);
            const deltaY = Math.abs(e.changedTouches[0].screenY - touchStartY);
            
            // Only start swiping if horizontal movement is greater than vertical
            if (deltaX > deltaY && deltaX > 10) {
                isSwiping = true;
            }
        }

        if (isSwiping) {
            // Prevent scrolling while swiping
            e.preventDefault();
        }
    }

    /**
     * Handle touch end
     */
    function handleTouchEnd(e) {
        if (!isSwiping) return;

        touchEndX = e.changedTouches[0].screenX;
        touchEndY = e.changedTouches[0].screenY;

        handleSwipe();
        isSwiping = false;
    }

    /**
     * Handle swipe gesture
     */
    function handleSwipe() {
        const deltaX = touchEndX - touchStartX;
        const deltaY = touchEndY - touchStartY;
        const distance = Math.abs(deltaX);
        
        // Check if it's a horizontal swipe
        if (Math.abs(deltaY) > Math.abs(deltaX)) {
            return; // Vertical swipe, ignore
        }

        if (distance < SWIPE_THRESHOLD) {
            return; // Swipe too short
        }

        // Swipe right (open sidebar)
        if (deltaX > 0 && touchStartX < 50) {
            // Only open if swipe started from left edge
            openSidebar();
        }
        // Swipe left (close sidebar)
        else if (deltaX < 0 && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    }

    /**
     * Open sidebar
     */
    function openSidebar() {
        sidebar.classList.add('show');
        wrapper.classList.add('sidebar-open');
        
        // Add backdrop
        let backdrop = document.querySelector('.mobile-backdrop');
        if (!backdrop) {
            backdrop = document.createElement('div');
            backdrop.className = 'mobile-backdrop';
            document.body.appendChild(backdrop);
        }
        
        // Remove old listener and add new one
        backdrop.removeEventListener('click', closeSidebar);
        backdrop.addEventListener('click', closeSidebar);
        
        // Trigger animation
        setTimeout(() => backdrop.classList.add('show'), 10);
    }

    /**
     * Close sidebar
     */
    function closeSidebar() {
        sidebar.classList.remove('show');
        wrapper.classList.remove('sidebar-open');
        
        // Remove backdrop
        const backdrop = document.querySelector('.mobile-backdrop');
        if (backdrop) {
            backdrop.classList.remove('show');
            setTimeout(() => {
                backdrop.removeEventListener('click', closeSidebar);
                backdrop.remove();
            }, 300);
        }
    }

    /**
     * Handle sidebar toggle button
     */
    function initSidebarToggle() {
        const toggleBtn = document.getElementById('sidebarToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function() {
                if (sidebar.classList.contains('show')) {
                    closeSidebar();
                } else {
                    openSidebar();
                }
            });
        }

        // Close button in sidebar
        const closeBtn = document.getElementById('sidebarClose');
        if (closeBtn) {
            closeBtn.addEventListener('click', closeSidebar);
        }
    }

    /**
     * Add ripple effect to buttons
     */
    function addRippleEffect() {
        const buttons = document.querySelectorAll('.btn, .list-group-item-action, .topbar-btn');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });
    }

    /**
     * Optimize touch targets
     */
    function optimizeTouchTargets() {
        // Ensure minimum 44x44px touch targets
        const smallButtons = document.querySelectorAll('button, a, .btn');
        
        smallButtons.forEach(btn => {
            const rect = btn.getBoundingClientRect();
            if (rect.height < 44 || rect.width < 44) {
                btn.style.minHeight = '44px';
                btn.style.minWidth = '44px';
            }
        });
    }

    /**
     * Initialize on DOM ready
     */
    function initAll() {
        init();
        initSidebarToggle();
        
        // Only add ripple and optimize on touch devices
        if ('ontouchstart' in window) {
            addRippleEffect();
            optimizeTouchTargets();
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAll);
    } else {
        initAll();
    }

})();
