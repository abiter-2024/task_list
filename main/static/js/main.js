// Main JavaScript for Task Progress Manager

document.addEventListener('DOMContentLoaded', function() {
    console.log('Task Progress Manager loaded');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize progress updates
    initializeProgressUpdates();
    
    // Initialize auto-save functionality
    initializeAutoSave();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize page animations
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Add slide-in animation to buttons
    const buttons = document.querySelectorAll('.btn-group .btn');
    buttons.forEach((btn, index) => {
        btn.style.animationDelay = `${index * 0.05}s`;
        btn.classList.add('slide-in');
    });
}

// Initialize progress update functionality
function initializeProgressUpdates() {
    // Real-time progress bar updates
    const progressInputs = document.querySelectorAll('input[type="number"][name="progress"]');
    progressInputs.forEach(input => {
        input.addEventListener('input', function() {
            updateProgressPreview(this);
        });
    });
    
    // Progress slider functionality
    addProgressSliders();
}

// Update progress preview in real-time
function updateProgressPreview(input) {
    const progress = parseInt(input.value) || 0;
    const clampedProgress = Math.max(0, Math.min(100, progress));
    
    // Find associated progress bar
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        if (bar.id === 'progressPreview' || bar.closest('.card') === input.closest('.card')) {
            bar.style.width = clampedProgress + '%';
            bar.textContent = clampedProgress + '%';
            bar.setAttribute('aria-valuenow', clampedProgress);
            
            // Update color based on progress
            bar.className = 'progress-bar';
            if (clampedProgress === 0) {
                bar.classList.add('bg-secondary');
            } else if (clampedProgress < 30) {
                bar.classList.add('bg-danger');
            } else if (clampedProgress < 70) {
                bar.classList.add('bg-warning');
            } else {
                bar.classList.add('bg-success');
            }
        }
    });
    
    // Update input value if needed
    if (input.value !== clampedProgress.toString()) {
        input.value = clampedProgress;
    }
}

// Add progress sliders for better UX
function addProgressSliders() {
    const progressInputs = document.querySelectorAll('input[type="number"][name="progress"]');
    progressInputs.forEach(input => {
        // Create range slider
        const slider = document.createElement('input');
        slider.type = 'range';
        slider.min = '0';
        slider.max = '100';
        slider.value = input.value;
        slider.className = 'form-range mt-2';
        
        // Sync slider with number input
        slider.addEventListener('input', function() {
            input.value = this.value;
            updateProgressPreview(input);
        });
        
        input.addEventListener('input', function() {
            slider.value = this.value;
        });
        
        // Insert slider after input
        input.parentNode.appendChild(slider);
    });
}

// Initialize auto-save functionality for forms
function initializeAutoSave() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                saveFormData(form);
            });
        });
        
        // Restore form data on page load
        restoreFormData(form);
    });
}

// Save form data to localStorage
function saveFormData(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    const formId = form.action || window.location.pathname;
    localStorage.setItem(`formData_${formId}`, JSON.stringify(data));
}

// Restore form data from localStorage
function restoreFormData(form) {
    const formId = form.action || window.location.pathname;
    const savedData = localStorage.getItem(`formData_${formId}`);
    
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const element = form.querySelector(`[name="${key}"]`);
                if (element && !element.value) {
                    element.value = data[key];
                }
            });
        } catch (e) {
            console.warn('Failed to restore form data:', e);
        }
    }
}

// Clear saved form data
function clearFormData(form) {
    const formId = form.action || window.location.pathname;
    localStorage.removeItem(`formData_${formId}`);
}

// Initialize keyboard shortcuts
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + N: New task
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            window.location.href = '/add_task';
        }
        
        // Ctrl/Cmd + H: Home/Dashboard
        if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
            e.preventDefault();
            window.location.href = '/';
        }
        
        // Ctrl/Cmd + T: Tasks page
        if ((e.ctrlKey || e.metaKey) && e.key === 't') {
            e.preventDefault();
            window.location.href = '/tasks';
        }
        
        // Escape: Close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
}

// Utility function to show notifications
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 400px;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Utility function to confirm actions
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// API helper functions
const API = {
    // Base API call function
    async call(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            showNotification('发生错误，请稍后重试。', 'danger');
            throw error;
        }
    },
    
    // Get all tasks
    async getTasks(status = null) {
        const url = status ? `/api/tasks?status=${status}` : '/api/tasks';
        return await this.call(url);
    },
    
    // Get single task
    async getTask(id) {
        return await this.call(`/api/tasks/${id}`);
    },
    
    // Create task
    async createTask(taskData) {
        return await this.call('/api/tasks', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
    },
    
    // Update task
    async updateTask(id, updates) {
        return await this.call(`/api/tasks/${id}`, {
            method: 'PUT',
            body: JSON.stringify(updates)
        });
    },
    
    // Update task progress
    async updateProgress(id, progress) {
        return await this.call(`/api/tasks/${id}/progress`, {
            method: 'PUT',
            body: JSON.stringify({ progress })
        });
    },
    
    // Delete task
    async deleteTask(id) {
        return await this.call(`/api/tasks/${id}`, {
            method: 'DELETE'
        });
    },
    
    // Get statistics
    async getStats() {
        return await this.call('/api/stats');
    }
};

// Export for use in other scripts
window.TaskManager = {
    API,
    showNotification,
    confirmAction,
    updateProgressPreview,
    clearFormData
};

// Add smooth scrolling to anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading states to buttons
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i> 处理中...';
            
            // Re-enable after 5 seconds as fallback
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 5000);
        }
    });
});