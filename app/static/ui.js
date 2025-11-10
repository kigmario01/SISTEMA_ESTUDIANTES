(() => {
  // Modern UI Interactions with Ripple Effects and Advanced Animations
  const supportsReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pressClass = 'is-pressed';
  const loadingClass = 'is-loading';
  const rippleClass = 'ripple';
  
  // Utility functions
  const disablePress = (el) => el.classList.remove(pressClass);
  const enableLoading = (el) => el.classList.add(loadingClass);
  const disableLoading = (el) => el.classList.remove(loadingClass);
  
  // Create ripple effect
  const createRipple = (event, button) => {
    if (supportsReducedMotion) return;
    
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.classList.add(rippleClass);
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    
    button.appendChild(ripple);
    
    // Remove ripple after animation
    setTimeout(() => {
      if (ripple.parentNode) {
        ripple.parentNode.removeChild(ripple);
      }
    }, 600);
  };
  
  // Loading state management
  const handleLoading = (button) => {
    const autoLoading = button.dataset.autoLoading === 'true';
    if (!autoLoading) return;
    
    enableLoading(button);
    
    // Simulate loading (can be replaced with actual async operations)
    setTimeout(() => {
      disableLoading(button);
    }, 2000);
  };
  
  // Modern button interactions
  const onPointerDown = (e) => {
    const btn = e.target.closest('.btn-modern, .btn');
    if (!btn || btn.disabled || btn.classList.contains('is-disabled')) return;
    
    btn.classList.add(pressClass);
    createRipple(e, btn);
    
    // Add haptic feedback if available
    if ('vibrate' in navigator) {
      navigator.vibrate(10);
    }
  };
  
  const onPointerUp = (e) => {
    const btn = e.target.closest('.btn-modern, .btn');
    if (!btn) return;
    
    setTimeout(() => disablePress(btn), 80);
    
    // Handle loading state
    if (btn.dataset.autoLoading === 'true') {
      handleLoading(btn);
    }
  };
  
  const onKeyDown = (e) => {
    const btn = e.target.closest('.btn-modern, .btn');
    if (!btn) return;
    
    if (e.key === ' ' || e.key === 'Enter') {
      btn.classList.add(pressClass);
      if (e.key === 'Enter') {
        createRipple(e, btn);
      }
    }
  };
  
  const onKeyUp = (e) => {
    const btn = e.target.closest('.btn-modern, .btn');
    if (!btn) return;
    
    if (e.key === ' ' || e.key === 'Enter') {
      disablePress(btn);
      if (e.key === 'Enter' && btn.dataset.autoLoading === 'true') {
        handleLoading(btn);
      }
    }
  };
  
  // Form input animations
  const setupFormAnimations = () => {
    const inputs = document.querySelectorAll('.form-input, .form-textarea');
    
    inputs.forEach(input => {
      input.addEventListener('focus', function() {
        this.parentElement?.classList.add('form-group-focused');
      });
      
      input.addEventListener('blur', function() {
        this.parentElement?.classList.remove('form-group-focused');
        
        // Add filled state for styling
        if (this.value) {
          this.parentElement?.classList.add('form-group-filled');
        } else {
          this.parentElement?.classList.remove('form-group-filled');
        }
      });
    });
  };
  
  // Card hover effects
  const setupCardAnimations = () => {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
      card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px)';
      });
      
      card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
      });
    });
  };
  
  // Table row animations
  const setupTableAnimations = () => {
    const rows = document.querySelectorAll('.table-modern tbody tr');
    
    rows.forEach((row, index) => {
      row.style.animationDelay = `${index * 50}ms`;
      row.classList.add('animate-slide-up');
    });
  };
  
  // Smooth page transitions
  const setupPageTransitions = () => {
    const links = document.querySelectorAll('a[href^="/"]');
    
    links.forEach(link => {
      link.addEventListener('click', function(e) {
        // Add transition class to body
        document.body.classList.add('page-transitioning');
        
        // Remove class after transition
        setTimeout(() => {
          document.body.classList.remove('page-transitioning');
        }, 300);
      });
    });
  };
  
  // Loading states for forms
  const setupFormLoading = () => {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
      form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn && submitBtn.dataset.autoLoading === 'true') {
          enableLoading(submitBtn);
          
          // Re-enable after form submission (adjust timing as needed)
          setTimeout(() => {
            disableLoading(submitBtn);
          }, 3000);
        }
      });
    });
  };
  
  // Alert animations
  const setupAlertAnimations = () => {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
      alert.classList.add('animate-slide-in');
      
      // Auto-dismiss after 5 seconds
      if (alert.dataset.autoDismiss !== 'false') {
        setTimeout(() => {
          alert.style.transition = 'all 0.3s ease-out';
          alert.style.opacity = '0';
          alert.style.transform = 'translateY(-10px)';
          
          setTimeout(() => {
            if (alert.parentNode) {
              alert.parentNode.removeChild(alert);
            }
          }, 300);
        }, 5000);
      }
    });
  };
  
  // Progress indicators
  const setupProgressIndicators = () => {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
      const width = bar.dataset.progress || '0%';
      
      // Animate progress after a short delay
      setTimeout(() => {
        bar.style.width = width;
        bar.style.transition = 'width 1s ease-out';
      }, 100);
    });
  };
  
  // Initialize all modern interactions
  const initModernUI = () => {
    if (!supportsReducedMotion) {
      document.addEventListener('pointerdown', onPointerDown);
      document.addEventListener('pointerup', onPointerUp);
      document.addEventListener('keydown', onKeyDown);
      document.addEventListener('keyup', onKeyUp);
    }
    
    // Setup all animations
    setupFormAnimations();
    setupCardAnimations();
    setupTableAnimations();
    setupPageTransitions();
    setupFormLoading();
    setupAlertAnimations();
    setupProgressIndicators();
    
    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Add CSS for loading states
    const style = document.createElement('style');
    style.textContent = `
      .btn-modern.is-loading,
      .btn.is-loading {
        position: relative;
        pointer-events: none;
      }

      .btn-modern.is-loading {
        padding-right: calc(var(--space-4) + 1.75rem);
      }

      .btn-modern.btn-sm.is-loading {
        padding-right: calc(var(--space-3) + 1.5rem);
      }

      .btn-modern.btn-lg.is-loading {
        padding-right: calc(var(--space-6) + 1.75rem);
      }

      .btn.is-loading {
        padding-right: 2.5rem;
        opacity: 0.9;
      }

      .btn-modern.is-loading::after,
      .btn.is-loading::after {
        content: '';
        position: absolute;
        width: 1rem;
        height: 1rem;
        top: 50%;
        right: 0.75rem;
        margin-top: -0.5rem;
        border: 2px solid currentColor;
        border-radius: 50%;
        border-top-color: transparent;
        animation: spin 0.8s linear infinite;
      }

      .page-transitioning {
        opacity: 0.8;
        transition: opacity 0.3s ease-out;
      }
      
      .form-group-focused .form-label {
        color: var(--primary-600);
        transform: translateY(-2px);
      }
      
      .form-group-filled .form-label {
        font-size: var(--text-xs);
        color: var(--neutral-600);
      }
    `;
    document.head.appendChild(style);
  };
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initModernUI);
  } else {
    initModernUI();
  }
  
  // Re-initialize on dynamic content changes (for SPAs)
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        // Re-setup animations for new content
        setupTableAnimations();
        setupAlertAnimations();
        setupProgressIndicators();
      }
    });
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
})();