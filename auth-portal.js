/**
 * auth-portal.js — Google SSO gate for Account Management Portal
 * Same pattern as Newsletter Hub auth.js
 */
(function () {
  'use strict';

  var SESSION_HOURS = 24;

  function getStoredUser() {
    try {
      var stored = localStorage.getItem('fermat_portal_user');
      if (!stored) return null;
      var user = JSON.parse(stored);
      if (Date.now() - (user.loginTime || 0) > SESSION_HOURS * 60 * 60 * 1000) {
        localStorage.removeItem('fermat_portal_user');
        return null;
      }
      return user;
    } catch (e) {
      localStorage.removeItem('fermat_portal_user');
      return null;
    }
  }

  // Check for SSO callback params
  function checkSSOCallback() {
    var params = new URLSearchParams(window.location.search);
    var ssoEmail = params.get('sso_email');
    var ssoName = params.get('sso_name');
    var ssoToken = params.get('sso_token');
    var ssoError = params.get('sso_error');

    if (ssoEmail || ssoError) {
      window.history.replaceState({}, document.title, window.location.pathname);
    }

    if (ssoError) {
      if (ssoError === 'domain_not_allowed') return 'Only @fermatcommerce.com accounts allowed.';
      if (ssoError === 'access_denied') return 'Access denied.';
      return 'Sign-in failed. Please try again.';
    }

    if (ssoEmail && ssoToken) {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '/api/verify-sso?email=' + encodeURIComponent(ssoEmail) + '&token=' + ssoToken, false);
      xhr.send();
      try {
        var resp = JSON.parse(xhr.responseText);
        if (resp.valid) {
          localStorage.setItem('fermat_portal_user', JSON.stringify({
            email: ssoEmail, name: ssoName || '', loginTime: Date.now()
          }));
          return null;
        }
      } catch (e) {}
      return 'Verification failed. Try again.';
    }
    return null;
  }

  // Update sidebar footer with user profile
  function showUserProfile(user) {
    var sbf = document.querySelector('.sbf');
    if (!sbf) return;

    var name = user.name || user.email.split('@')[0];
    var initial = name[0].toUpperCase();

    sbf.innerHTML =
      '<div style="cursor:pointer;display:flex;align-items:center;gap:10px" onclick="document.getElementById(\'portalUserMenu\').classList.toggle(\'show\')">' +
        '<div style="width:32px;height:32px;border-radius:8px;background:rgba(62,214,96,0.15);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#3ED660;flex-shrink:0">' + initial + '</div>' +
        '<div style="flex:1;min-width:0"><div class="sbft" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + name + '</div><div class="sbfr" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + user.email + '</div></div>' +
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>' +
      '</div>' +
      '<div id="portalUserMenu" class="portal-user-menu">' +
        '<div style="padding:12px 16px;border-bottom:1px solid rgba(255,255,255,0.08)">' +
          '<div style="font-size:12px;font-weight:600;color:#fff">' + name + '</div>' +
          '<div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:2px">' + user.email + '</div>' +
        '</div>' +
        '<a href="/auth/logout" onclick="localStorage.removeItem(\'fermat_portal_user\')" style="display:flex;align-items:center;gap:8px;padding:10px 16px;font-size:12px;color:rgba(255,255,255,0.6);text-decoration:none;transition:background .15s" onmouseover="this.style.background=\'rgba(255,255,255,0.05)\'" onmouseout="this.style.background=\'none\'">' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/></svg>' +
          'Sign out' +
        '</a>' +
      '</div>';

    // Add popup CSS
    if (!document.getElementById('portal-menu-css')) {
      var style = document.createElement('style');
      style.id = 'portal-menu-css';
      style.textContent = '.portal-user-menu{display:none;position:absolute;bottom:100%;left:10px;right:10px;background:#1a3a28;border-radius:10px;box-shadow:0 -4px 20px rgba(0,0,0,0.3);overflow:hidden;margin-bottom:8px;border:1px solid rgba(255,255,255,0.08)}.portal-user-menu.show{display:block}';
      document.head.appendChild(style);
    }

    // Close on outside click
    document.addEventListener('click', function (e) {
      var menu = document.getElementById('portalUserMenu');
      if (menu && !sbf.contains(e.target)) menu.classList.remove('show');
    });
  }

  // Login overlay
  function showLoginOverlay(errorMsg) {
    var overlay = document.createElement('div');
    overlay.id = 'portal-login-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;background:#F4F3F0;z-index:99999;display:flex;align-items:center;justify-content:center;font-family:Space Grotesk,sans-serif';
    overlay.innerHTML =
      '<div style="text-align:center;max-width:380px;padding:40px">' +
        '<img src="https://cdn.prod.website-files.com/63f5f201b1f212a5c76681f0/63f6319f0b6d0beeffa89a24_Logo.svg" height="32" style="margin-bottom:24px" onerror="this.outerHTML=\'<div style=font-size:24px;font-weight:700;color:#072C1B;margin-bottom:24px>FERM\\u00c0T</div>\'">' +
        '<h1 style="font-family:Cormorant Garamond,serif;font-size:28px;font-weight:400;color:#072C1B;margin-bottom:8px">Account Management Portal</h1>' +
        '<p style="color:#9E9E9E;font-size:13px;margin-bottom:28px">Sign in with your FERM\u00c0T Google account</p>' +
        '<a href="/auth/google" style="display:inline-flex;align-items:center;gap:10px;padding:12px 28px;background:#072C1B;color:#fff;border-radius:10px;text-decoration:none;font-size:13px;font-weight:600;transition:background .15s" onmouseover="this.style.background=\'#0d4a2f\'" onmouseout="this.style.background=\'#072C1B\'">' +
          '<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>' +
          'Sign in with Google' +
        '</a>' +
        (errorMsg ? '<p style="color:#C84632;font-size:12px;margin-top:16px">' + errorMsg + '</p>' : '') +
        '<p style="color:#9E9E9E;font-size:10px;margin-top:20px">Restricted to @fermatcommerce.com</p>' +
      '</div>';
    document.body.appendChild(overlay);
  }

  // ── INIT ──
  function init() {
    var ssoError = checkSSOCallback();
    var user = getStoredUser();
    var info = window.__PORTAL_USER__ || {};

    if (user) {
      showUserProfile(user);
      return;
    }

    // If SSO is configured, show login gate
    if (info.ssoConfigured) {
      showLoginOverlay(ssoError);
      return;
    }

    // SSO not configured — show default name, no gate
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
