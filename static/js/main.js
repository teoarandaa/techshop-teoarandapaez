// TechShop - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('TechShop loaded successfully!');
    
    // Initialize cart badge
    updateCartBadge();
    
    // Add to cart forms with AJAX
    initAddToCartForms();
    
    // Quantity update forms
    initQuantityForms();
    
    // Remove from cart forms
    initRemoveForms();
});

/**
 * Update cart badge count
 */
function updateCartBadge() {
    const badge = document.getElementById('cart-badge');
    if (badge) {
        // Badge is already rendered by the server
        // This function can be used to update it via AJAX
    }
}

/**
 * Initialize add to cart forms with AJAX support
 */
function initAddToCartForms() {
    const forms = document.querySelectorAll('.add-to-cart-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const button = form.querySelector('button[type="submit"]');
            const originalText = button.textContent;
            
            // Disable button and show loading state
            button.disabled = true;
            button.textContent = 'Afegint...';
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update cart badge
                    const badge = document.getElementById('cart-badge');
                    if (badge && data.cart_count !== undefined) {
                        badge.textContent = data.cart_count;
                    }
                    
                    // Show success message
                    showNotification(data.message, 'success');
                    
                    // Reset form
                    form.reset();
                } else {
                    showNotification(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error en afegir al carretó', 'error');
            })
            .finally(() => {
                // Re-enable button
                button.disabled = false;
                button.textContent = originalText;
            });
        });
    });
}

/**
 * Initialize quantity update forms
 */
function initQuantityForms() {
    const forms = document.querySelectorAll('.quantity-form');
    
    forms.forEach(form => {
        const input = form.querySelector('input[type="number"]');
        
        // Auto-submit on change
        input.addEventListener('change', function() {
            form.dispatchEvent(new Event('submit'));
        });
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reload page to update totals
                    location.reload();
                } else {
                    showNotification(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error en actualitzar quantitat', 'error');
            });
        });
    });
}

/**
 * Initialize remove from cart forms
 */
function initRemoveForms() {
    const forms = document.querySelectorAll('.remove-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (!confirm('Estàs segur que vols eliminar aquest producte?')) {
                return;
            }
            
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reload page
                    location.reload();
                } else {
                    showNotification(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error en eliminar producte', 'error');
            });
        });
    });
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background-color: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

/**
 * Form validation helper
 */
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let valid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            valid = false;
            input.style.borderColor = '#ef4444';
        } else {
            input.style.borderColor = '';
        }
    });
    
    return valid;
}

