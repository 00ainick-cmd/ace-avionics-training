// shared/js/ace-auth.js
// =============================================
// ACE Platform Auth Guard & Logout
// =============================================
// Include this script on any page that requires login.
// Usage:
//   <script src="shared/js/ace-auth.js"></script>
//   -- automatically checks for enrollment on load
//   -- provides aceLogout() function
//   -- provides aceGetProfile() function

(function () {
  'use strict';

  const ENROLLMENT_KEY = 'ace_enrollment';
  const SESSION_KEY = 'ace_session_id';
  const LOGIN_PAGE = '/enrollment.html';

  // Pages that don't require auth
  const PUBLIC_PAGES = ['enrollment.html', 'checkout.html', 'checkout-success.html', 'index.html'];

  function isPublicPage() {
    const path = window.location.pathname.toLowerCase();
    return PUBLIC_PAGES.some(p => path.endsWith(p) || path === '/');
  }

  function getProfile() {
    try {
      const raw = localStorage.getItem(ENROLLMENT_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function isLoggedIn() {
    const profile = getProfile();
    return profile && profile.code;
  }

  function logout() {
    // Clear auth-related data
    localStorage.removeItem(ENROLLMENT_KEY);
    localStorage.removeItem(SESSION_KEY);
    localStorage.removeItem('caet-onboarding-complete');
    sessionStorage.clear();
    // Redirect to login
    var base = window.location.pathname.includes('/shared/') ? '../enrollment.html' : 'enrollment.html';
    window.location.href = base;
  }

  // Auth guard: redirect to login if not authenticated (skip public pages)
  if (!isPublicPage() && !isLoggedIn()) {
    var base = window.location.pathname.includes('/shared/') ? '../enrollment.html' : 'enrollment.html';
    window.location.href = base;
  }

  // Inject logout button into navigation
  function injectLogoutButton() {
    // Don't inject on public pages
    if (isPublicPage()) return;
    // Don't inject if already present
    if (document.getElementById('aceLogoutBtn')) return;

    // Look for common nav containers — try multiple selectors
    var topbar = document.querySelector('.topbar-right, .topbar-end, .nav-right, .header-right');
    if (!topbar) {
      topbar = document.querySelector('.topbar, .top-bar, header, .site-header');
    }
    if (!topbar) return false; // Signal not found yet

    var btn = document.createElement('button');
    btn.id = 'aceLogoutBtn';
    btn.textContent = 'Sign Out';
    btn.title = 'Sign out of ACE Training';
    btn.style.cssText = 'background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);color:#ef4444;padding:6px 14px;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;font-family:Inter,system-ui,sans-serif;transition:all 0.2s;margin-left:12px;';
    btn.onmouseenter = function () { btn.style.background = 'rgba(239,68,68,0.2)'; };
    btn.onmouseleave = function () { btn.style.background = 'rgba(239,68,68,0.1)'; };
    btn.onclick = function () {
      if (confirm('Sign out of ACE Avionics Training?')) {
        logout();
      }
    };

    topbar.appendChild(btn);
    return true; // Signal success
  }

  // Wait for DOM, then inject with retry
  function tryInject() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { retryInject(0); });
    } else {
      retryInject(0);
    }
  }

  function retryInject(attempt) {
    if (injectLogoutButton()) return; // Success
    if (attempt < 6) {
      setTimeout(function () { retryInject(attempt + 1); }, 500);
    }
  }

  tryInject();

  // Expose globally
  window.aceLogout = logout;
  window.aceGetProfile = getProfile;
  window.aceIsLoggedIn = isLoggedIn;
})();
