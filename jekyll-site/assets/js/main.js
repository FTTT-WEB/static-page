// Minimal JavaScript for FTTT Jekyll Site
// Handles scroll-up button visibility and basic interactions

(function() {
  'use strict';

  // Show/hide scroll-up button based on scroll position
  function toggleScrollUp() {
    var scrollUp = document.getElementById('scroll-up');
    if (!scrollUp) return;

    if (window.pageYOffset > 300) {
      scrollUp.style.display = 'block';
    } else {
      scrollUp.style.display = 'none';
    }
  }

  // Smooth scroll to top
  function scrollToTop(e) {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  }

  // Toggle mobile navigation
  function initMobileNav() {
    var toggle = document.querySelector('.menu-toggle');
    var nav = document.getElementById('site-navigation');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', function() {
      var isOpen = nav.classList.contains('nav-open');
      nav.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', String(!isOpen));
      toggle.innerHTML = isOpen ? '&#9776;' : '&#10005;';
    });

    // Sub-menu click toggle on mobile
    nav.querySelectorAll('.menu-item-has-children > a').forEach(function(link) {
      link.addEventListener('click', function(e) {
        if (window.innerWidth < 768) {
          e.preventDefault();
          var parent = this.parentElement;
          var sub = parent.querySelector('.sub-menu');
          if (sub) {
            parent.classList.toggle('sub-menu-open');
            sub.classList.toggle('sub-menu-open');
          }
        }
      });
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      toggleScrollUp();
      var scrollUp = document.getElementById('scroll-up');
      if (scrollUp) {
        scrollUp.addEventListener('click', scrollToTop);
      }
      window.addEventListener('scroll', toggleScrollUp);
      initMobileNav();
    });
  } else {
    toggleScrollUp();
    var scrollUp = document.getElementById('scroll-up');
    if (scrollUp) {
      scrollUp.addEventListener('click', scrollToTop);
    }
    window.addEventListener('scroll', toggleScrollUp);
    initMobileNav();
  }
})();
