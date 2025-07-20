// KDS - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Loading button states
    const loadingButtons = document.querySelectorAll('[data-loading-text]');
    loadingButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const originalText = button.innerHTML;
            const loadingText = button.getAttribute('data-loading-text');
            
            button.innerHTML = loadingText;
            button.disabled = true;
            
            // Re-enable after form submission or 10 seconds
            setTimeout(function() {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 10000);
        });
    });

    // Confirm dialogs
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const message = button.getAttribute('data-confirm');
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // Auto-focus first input in modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = modal.querySelector('input, select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });
});

// Utility functions
const KDS = {
    // Show flash message
    showFlash: function(message, category = 'info') {
        const alertContainer = document.querySelector('.container .alert') ? 
            document.querySelector('.container .alert').parentNode : 
            document.querySelector('.container');
        
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${category} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    },

    // Format date for Serbian locale
    formatDate: function(date, includeTime = false) {
        const options = {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        };
        
        if (includeTime) {
            options.hour = '2-digit';
            options.minute = '2-digit';
        }
        
        return new Date(date).toLocaleString('sr-RS', options);
    },

    // Validate email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    // Loading state for buttons
    setButtonLoading: function(button, loading = true) {
        if (loading) {
            button.disabled = true;
            const originalText = button.innerHTML;
            button.setAttribute('data-original-text', originalText);
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Učitava...';
        } else {
            button.disabled = false;
            const originalText = button.getAttribute('data-original-text');
            if (originalText) {
                button.innerHTML = originalText;
            }
        }
    }
};
