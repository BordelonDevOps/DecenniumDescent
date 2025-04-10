/**
 * Draggable UI functionality for Party UI
 * Allows panels to be moved and resized
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all UI panels
    const panels = document.querySelectorAll('.ui-panel');
    
    panels.forEach(panel => {
        initDraggable(panel);
        initResizable(panel);
        initMinimizable(panel);
    });
    
    // Initialize battle timers
    initBattleTimers();
});

/**
 * Make an element draggable
 * @param {HTMLElement} element - The element to make draggable
 */
function initDraggable(element) {
    const header = element.querySelector('.panel-header');
    let isDragging = false;
    let offsetX, offsetY;
    
    // Mouse events
    header.addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', stopDrag);
    
    // Touch events for mobile/touch screens
    header.addEventListener('touchstart', startDragTouch);
    document.addEventListener('touchmove', dragTouch);
    document.addEventListener('touchend', stopDrag);
    
    function startDrag(e) {
        isDragging = true;
        offsetX = e.clientX - element.getBoundingClientRect().left;
        offsetY = e.clientY - element.getBoundingClientRect().top;
        element.classList.add('dragging');
        
        // Bring panel to front
        bringToFront(element);
    }
    
    function startDragTouch(e) {
        if (e.touches.length === 1) {
            const touch = e.touches[0];
            isDragging = true;
            offsetX = touch.clientX - element.getBoundingClientRect().left;
            offsetY = touch.clientY - element.getBoundingClientRect().top;
            element.classList.add('dragging');
            
            // Bring panel to front
            bringToFront(element);
        }
    }
    
    function drag(e) {
        if (!isDragging) return;
        
        const x = e.clientX - offsetX;
        const y = e.clientY - offsetY;
        
        // Keep panel within viewport
        const maxX = window.innerWidth - element.offsetWidth;
        const maxY = window.innerHeight - element.offsetHeight;
        
        element.style.left = Math.max(0, Math.min(x, maxX)) + 'px';
        element.style.top = Math.max(0, Math.min(y, maxY)) + 'px';
        
        // Remove transform if it exists (for initially centered panels)
        element.style.transform = 'none';
    }
    
    function dragTouch(e) {
        if (!isDragging || e.touches.length !== 1) return;
        
        const touch = e.touches[0];
        const x = touch.clientX - offsetX;
        const y = touch.clientY - offsetY;
        
        // Keep panel within viewport
        const maxX = window.innerWidth - element.offsetWidth;
        const maxY = window.innerHeight - element.offsetHeight;
        
        element.style.left = Math.max(0, Math.min(x, maxX)) + 'px';
        element.style.top = Math.max(0, Math.min(y, maxY)) + 'px';
        
        // Remove transform if it exists (for initially centered panels)
        element.style.transform = 'none';
        
        // Prevent scrolling while dragging
        e.preventDefault();
    }
    
    function stopDrag() {
        isDragging = false;
        element.classList.remove('dragging');
    }
}

/**
 * Make an element resizable
 * @param {HTMLElement} element - The element to make resizable
 */
function initResizable(element) {
    const handle = element.querySelector('.resize-handle');
    let isResizing = false;
    let startX, startY, startWidth, startHeight;
    
    // Mouse events
    handle.addEventListener('mousedown', startResize);
    document.addEventListener('mousemove', resize);
    document.addEventListener('mouseup', stopResize);
    
    // Touch events
    handle.addEventListener('touchstart', startResizeTouch);
    document.addEventListener('touchmove', resizeTouch);
    document.addEventListener('touchend', stopResize);
    
    function startResize(e) {
        isResizing = true;
        startX = e.clientX;
        startY = e.clientY;
        startWidth = element.offsetWidth;
        startHeight = element.offsetHeight;
        element.classList.add('resizing');
        
        // Bring panel to front
        bringToFront(element);
        
        e.preventDefault();
        e.stopPropagation();
    }
    
    function startResizeTouch(e) {
        if (e.touches.length === 1) {
            const touch = e.touches[0];
            isResizing = true;
            startX = touch.clientX;
            startY = touch.clientY;
            startWidth = element.offsetWidth;
            startHeight = element.offsetHeight;
            element.classList.add('resizing');
            
            // Bring panel to front
            bringToFront(element);
            
            e.preventDefault();
            e.stopPropagation();
        }
    }
    
    function resize(e) {
        if (!isResizing) return;
        
        const width = startWidth + e.clientX - startX;
        const height = startHeight + e.clientY - startY;
        
        // Minimum size constraints
        const minWidth = 150;
        const minHeight = 100;
        
        if (width >= minWidth) {
            element.style.width = width + 'px';
        }
        
        if (height >= minHeight) {
            element.style.height = height + 'px';
        }
    }
    
    function resizeTouch(e) {
        if (!isResizing || e.touches.length !== 1) return;
        
        const touch = e.touches[0];
        const width = startWidth + touch.clientX - startX;
        const height = startHeight + touch.clientY - startY;
        
        // Minimum size constraints
        const minWidth = 150;
        const minHeight = 100;
        
        if (width >= minWidth) {
            element.style.width = width + 'px';
        }
        
        if (height >= minHeight) {
            element.style.height = height + 'px';
        }
        
        e.preventDefault();
    }
    
    function stopResize() {
        isResizing = false;
        element.classList.remove('resizing');
    }
}

/**
 * Make an element minimizable
 * @param {HTMLElement} element - The element to make minimizable
 */
function initMinimizable(element) {
    const minimizeBtn = element.querySelector('.minimize-btn');
    const content = element.querySelector('.panel-content');
    
    minimizeBtn.addEventListener('click', function() {
        element.classList.toggle('minimized');
        
        // Update button text
        minimizeBtn.textContent = element.classList.contains('minimized') ? '+' : '_';
    });
}

/**
 * Bring a panel to the front
 * @param {HTMLElement} element - The element to bring to front
 */
function bringToFront(element) {
    // Get all panels
    const panels = document.querySelectorAll('.ui-panel');
    
    // Find the highest z-index
    let maxZ = 0;
    panels.forEach(panel => {
        const zIndex = parseInt(window.getComputedStyle(panel).zIndex) || 0;
        maxZ = Math.max(maxZ, zIndex);
    });
    
    // Set this panel's z-index higher
    element.style.zIndex = maxZ + 1;
}

/**
 * Initialize battle timers
 * Simulates battle timers filling up and changing color
 */
function initBattleTimers() {
    const battleTimers = document.querySelectorAll('.battle-timer');
    
    battleTimers.forEach(timer => {
        // Random starting value between 30% and 90%
        let value = Math.random() * 60 + 30;
        timer.style.width = value + '%';
        
        // Simulate timer progress
        setInterval(() => {
            value += 5;
            if (value > 100) {
                value = 0;
                timer.classList.add('ready');
                
                // Reset to yellow after 2 seconds
                setTimeout(() => {
                    timer.classList.remove('ready');
                }, 2000);
            }
            
            timer.style.width = value + '%';
        }, 1000);
    });
}
