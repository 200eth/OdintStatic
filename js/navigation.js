// Navigation Management System
class NavigationManager {
  constructor() {
    this.activeDropdown = null;
    this.isScrolled = false;
    this.mobileMenuOpen = false;
    this.init();
  }

  init() {
    this.setupHeaderScroll();
    this.setupDropdowns();
    this.setupMobileMenu();
    this.setupKeyboardNavigation();
    this.setupOverlay();
  }

  setupHeaderScroll() {
    const header = document.querySelector('.header');
    if (!header) return;

    window.addEventListener('scroll', () => {
      const scrolled = window.scrollY > 10;
      if (scrolled !== this.isScrolled) {
        this.isScrolled = scrolled;
        header.classList.toggle('scrolled', scrolled);
      }
    });
  }

  setupDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
      const trigger = dropdown.querySelector('.dropdown-trigger');
      const menu = dropdown.querySelector('.dropdown-menu');
      
      if (!trigger || !menu) return;

      // Desktop hover events
      dropdown.addEventListener('mouseenter', () => {
        this.openDropdown(dropdown);
      });

      dropdown.addEventListener('mouseleave', () => {
        this.closeDropdown(dropdown);
      });

      // Click events for mobile and keyboard
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        if (dropdown.classList.contains('active')) {
          this.closeDropdown(dropdown);
        } else {
          this.closeAllDropdowns();
          this.openDropdown(dropdown);
        }
      });

      // Handle clicks on dropdown links
      const links = menu.querySelectorAll('.dropdown-link');
      links.forEach(link => {
        link.addEventListener('click', () => {
          this.closeDropdown(dropdown);
        });
      });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
      this.closeAllDropdowns();
    });
  }

  openDropdown(dropdown) {
    if (this.activeDropdown && this.activeDropdown !== dropdown) {
      this.closeDropdown(this.activeDropdown);
    }
    
    dropdown.classList.add('active');
    const trigger = dropdown.querySelector('.dropdown-trigger');
    if (trigger) trigger.classList.add('active');
    
    this.activeDropdown = dropdown;
    this.showOverlay();
  }

  closeDropdown(dropdown) {
    dropdown.classList.remove('active');
    const trigger = dropdown.querySelector('.dropdown-trigger');
    if (trigger) trigger.classList.remove('active');
    
    if (this.activeDropdown === dropdown) {
      this.activeDropdown = null;
      this.hideOverlay();
    }
  }

  closeAllDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown.active');
    dropdowns.forEach(dropdown => {
      this.closeDropdown(dropdown);
    });
  }

  setupMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileDropdownTriggers = document.querySelectorAll('.mobile-dropdown-trigger');

    if (!toggle || !mobileMenu) return;

    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleMobileMenu();
    });

    // Mobile dropdown triggers
    mobileDropdownTriggers.forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        const dropdown = trigger.closest('.mobile-dropdown');
        const menu = dropdown.querySelector('.mobile-dropdown-menu');
        
        if (dropdown.classList.contains('active')) {
          this.closeMobileDropdown(dropdown);
        } else {
          this.closeAllMobileDropdowns();
          this.openMobileDropdown(dropdown);
        }
      });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!mobileMenu.contains(e.target) && !toggle.contains(e.target)) {
        this.closeMobileMenu();
      }
    });
  }

  toggleMobileMenu() {
    if (this.mobileMenuOpen) {
      this.closeMobileMenu();
    } else {
      this.openMobileMenu();
    }
  }

  openMobileMenu() {
    const mobileMenu = document.querySelector('.mobile-menu');
    const toggle = document.querySelector('.mobile-menu-toggle');
    
    mobileMenu.classList.add('active');
    toggle.classList.add('active');
    this.mobileMenuOpen = true;
    this.showOverlay();
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
  }

  closeMobileMenu() {
    const mobileMenu = document.querySelector('.mobile-menu');
    const toggle = document.querySelector('.mobile-menu-toggle');
    
    mobileMenu.classList.remove('active');
    toggle.classList.remove('active');
    this.mobileMenuOpen = false;
    this.hideOverlay();
    
    // Restore body scroll
    document.body.style.overflow = '';
    
    // Close all mobile dropdowns
    this.closeAllMobileDropdowns();
  }

  openMobileDropdown(dropdown) {
    dropdown.classList.add('active');
    const trigger = dropdown.querySelector('.mobile-dropdown-trigger');
    const menu = dropdown.querySelector('.mobile-dropdown-menu');
    
    if (trigger) trigger.classList.add('active');
    if (menu) menu.classList.add('active');
  }

  closeMobileDropdown(dropdown) {
    dropdown.classList.remove('active');
    const trigger = dropdown.querySelector('.mobile-dropdown-trigger');
    const menu = dropdown.querySelector('.mobile-dropdown-menu');
    
    if (trigger) trigger.classList.remove('active');
    if (menu) menu.classList.remove('active');
  }

  closeAllMobileDropdowns() {
    const dropdowns = document.querySelectorAll('.mobile-dropdown.active');
    dropdowns.forEach(dropdown => {
      this.closeMobileDropdown(dropdown);
    });
  }

  setupKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
      // ESC key closes dropdowns and mobile menu
      if (e.key === 'Escape') {
        if (this.mobileMenuOpen) {
          this.closeMobileMenu();
        } else if (this.activeDropdown) {
          this.closeDropdown(this.activeDropdown);
        }
      }

      // Tab navigation for dropdowns
      if (e.key === 'Tab') {
        const activeElement = document.activeElement;
        const dropdown = activeElement.closest('.dropdown');
        
        if (dropdown && this.activeDropdown !== dropdown) {
          this.closeAllDropdowns();
          this.openDropdown(dropdown);
        }
      }
    });
  }

  setupOverlay() {
    const overlay = document.querySelector('.overlay');
    if (!overlay) return;

    overlay.addEventListener('click', () => {
      this.closeAllDropdowns();
      this.closeMobileMenu();
    });
  }

  showOverlay() {
    const overlay = document.querySelector('.overlay');
    if (overlay) {
      overlay.classList.add('active');
    }
  }

  hideOverlay() {
    const overlay = document.querySelector('.overlay');
    if (overlay && !this.mobileMenuOpen && !this.activeDropdown) {
      overlay.classList.remove('active');
    }
  }
}

// Initialize navigation when DOM is loaded
function injectHeader() {
  return fetch('/partials/header.html')
    .then(r => r.text())
    .then(html => {
      const existing = document.querySelector('header.header');
      if (existing) {
        existing.outerHTML = html;
      } else {
        const container = document.createElement('div');
        container.innerHTML = html;
        const headerEl = container.firstElementChild;
        if (headerEl) document.body.insertBefore(headerEl, document.body.firstChild);
      }
    })
    .catch(() => {});
}

document.addEventListener('DOMContentLoaded', async () => {
  await injectHeader();
  new NavigationManager();
  setActiveNavLink();
  initIcons();
});

// Smooth scroll for anchor links
document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('a[href^="#"]');
  
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      
      if (href === '#') return;
      
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        
        const header = document.querySelector('.header');
        const headerHeight = header ? header.offsetHeight : 0;
        const targetPosition = target.offsetTop - headerHeight;
        
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
});

// Active link highlighting based on current page
function setActiveNavLink() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link, .dropdown-link, .mobile-nav-link, .mobile-dropdown-link');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && (currentPath === href || currentPath === '/' + href)) {
      link.classList.add('active');
      
      // If it's in a dropdown, open the parent dropdown
      const dropdown = link.closest('.dropdown');
      if (dropdown) {
        const trigger = dropdown.querySelector('.dropdown-trigger');
        if (trigger) trigger.classList.add('active');
      }
    }
  });
}

// Set active links when page loads
// setActiveNavLink is called after header injection
function initIcons() {
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }
  document.querySelectorAll('.lucide-fallback').forEach(el => {
    const parent = el.parentElement;
    const hasSvg = parent && parent.querySelector('svg');
    el.style.display = hasSvg ? 'none' : 'inline-flex';
  });
}

function injectFooter() {
  fetch('/partials/footer.html')
    .then(r => r.text())
    .then(html => {
      const existing = document.querySelector('footer');
      if (existing) {
        existing.outerHTML = html;
      } else {
        const container = document.createElement('div');
        container.innerHTML = html;
        const footerEl = container.firstElementChild;
        if (footerEl) document.body.appendChild(footerEl);
      }
      initIcons();
    })
    .catch(() => {});
}

document.addEventListener('DOMContentLoaded', injectFooter);
window.addEventListener('load', initIcons);
let __iconsObserverInitialized = false;
function observeIcons() {
  if (__iconsObserverInitialized) return;
  const obs = new MutationObserver(mutations => {
    for (const m of mutations) {
      for (const n of m.addedNodes) {
        if (n && n.nodeType === 1) {
          if ((n.matches && n.matches('[data-lucide]')) || (n.querySelector && n.querySelector('[data-lucide]'))) {
            initIcons();
            return;
          }
        }
      }
    }
  });
  obs.observe(document.body, { childList: true, subtree: true });
  __iconsObserverInitialized = true;
}
document.addEventListener('DOMContentLoaded', observeIcons);

function setupAccordion() {
  const headers = document.querySelectorAll('.accordion .accordion-header');
  headers.forEach(header => {
    header.addEventListener('click', () => {
      const item = header.closest('.accordion-item');
      const expanded = header.getAttribute('aria-expanded') === 'true';
      header.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      item.classList.toggle('active', !expanded);
    });
  });
}

document.addEventListener('DOMContentLoaded', setupAccordion);
