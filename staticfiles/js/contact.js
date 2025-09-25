    // Form submission handling
    document.getElementById('contactForm').addEventListener('submit', function(e) {
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Show loading state
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Sending...';
        submitBtn.disabled = true;
        
        // Set a timeout to reset button if something goes wrong
        const resetTimeout = setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 10000); // Reset after 10 seconds if no response
        
        // The form will submit normally, Django will handle the redirect
        // The button state will be reset by page reload/redirect
    });

    // Live chat button
    document.getElementById('liveChatBtn').addEventListener('click', function() {
        alert('Live chat feature will be available soon! Please use our contact form or call us directly.');
    });

    // Location alert
    document.getElementById('location-alert').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default link behavior
        alert("This feature is available soon!");
    });

    // Scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Initialize scroll animations
    document.addEventListener('DOMContentLoaded', () => {
        const elements = document.querySelectorAll('.glass-morphism');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = `opacity 0.6s ease-out ${index * 0.1}s, transform 0.6s ease-out ${index * 0.1}s`;
            observer.observe(el);
        });
        
        // Enhanced hover effects
        document.querySelectorAll('.hover-scale').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.1)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.boxShadow = '';
            });
        });
    });

    // Form validation feedback
    const inputs = document.querySelectorAll('input[required], select[required], textarea[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.style.borderColor = '#ef4444';
                this.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
            } else {
                this.style.borderColor = '#10b981';
                this.style.boxShadow = '0 0 0 3px rgba(16, 185, 129, 0.1)';
            }
        });
        
        input.addEventListener('focus', function() {
            this.style.borderColor = '#6366f1';
            this.style.boxShadow = '0 0 0 3px rgba(99, 102, 241, 0.1)';
        });
    });

    // // Real-time form validation
    // function validateForm() {
    //     const form = document.getElementById('contactForm');
    //     const submitBtn = form.querySelector('button[type="submit"]');
    //     const requiredFields = form.querySelectorAll('input[required], select[required], textarea[required]');
        
    //     let allValid = true;
    //     requiredFields.forEach(field => {
    //         if (!field.value.trim()) {
    //             allValid = false;
    //         }
    //     });
        
    //     // Enable/disable submit button based on validation
    //     submitBtn.disabled = !allValid;
    //     if (allValid) {
    //         submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    //     } else {
    //         submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
    //     }
    // }

    // // Add input listeners for real-time validation
    // document.addEventListener('DOMContentLoaded', () => {
    //     const form = document.getElementById('contactForm');
    //     const inputs = form.querySelectorAll('input, select, textarea');
        
    //     inputs.forEach(input => {
    //         input.addEventListener('input', validateForm);
    //         input.addEventListener('change', validateForm);
    //     });
        
    //     // Initial validation
    //     validateForm();
    // });