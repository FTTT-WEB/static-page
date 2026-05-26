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

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      toggleScrollUp();
      var scrollUp = document.getElementById('scroll-up');
      if (scrollUp) {
        scrollUp.addEventListener('click', scrollToTop);
      }
      window.addEventListener('scroll', toggleScrollUp);
    });
  } else {
    toggleScrollUp();
    var scrollUp = document.getElementById('scroll-up');
    if (scrollUp) {
      scrollUp.addEventListener('click', scrollToTop);
    }
    window.addEventListener('scroll', toggleScrollUp);
  }
})();
