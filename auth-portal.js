/**
 * auth-portal.js — SSO gate for Account Management Portal
 * If SSO is configured: must sign in with @fermatcommerce.com
 * If not configured: shows dashboard with default profile
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
      return 'Sign-in failed. Please try again.';
    }

    if (ssoEmail && ssoToken) {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '/api/verify-sso?email=' + encodeURIComponent(ssoEmail) + '&token=' + ssoToken, false);
      xhr.send();
      try {
        if (JSON.parse(xhr.responseText).valid) {
          localStorage.setItem('fermat_portal_user', JSON.stringify({
            email: ssoEmail, name: ssoName || '', loginTime: Date.now()
          }));
          return null;
        }
      } catch (e) {}
      return 'Verification failed.';
    }
    return null;
  }

  // ── SIDEBAR PROFILE + LOGOUT POPUP ──
  function showUserProfile(user) {
    var sbf = document.querySelector('.sbf');
    if (!sbf) return;

    var name = user.name || user.email.split('@')[0];
    var initials = name.split(' ').filter(Boolean).map(function(w){return w[0]}).join('').substring(0,2).toUpperCase();

    sbf.style.position = 'relative';
    sbf.innerHTML =
      '<div id="portalProfileBtn" style="cursor:pointer;display:flex;align-items:center;gap:10px;padding:0">' +
        '<div style="width:34px;height:34px;border-radius:9px;background:rgba(62,214,96,0.15);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#3ED660;flex-shrink:0">' + initials + '</div>' +
        '<div style="flex:1;min-width:0"><div class="sbft" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + name + '</div><div class="sbfr" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + user.email + '</div></div>' +
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2.5" style="flex-shrink:0"><path d="M6 9l6 6 6-6"/></svg>' +
      '</div>' +
      '<div id="portalUserMenu" style="display:none;position:absolute;bottom:100%;left:0;right:0;background:#1a3a28;border-radius:12px;box-shadow:0 -6px 24px rgba(0,0,0,0.35);overflow:hidden;margin-bottom:10px;border:1px solid rgba(255,255,255,0.1)">' +
        '<div style="padding:14px 16px;border-bottom:1px solid rgba(255,255,255,0.08)">' +
          '<div style="font-size:13px;font-weight:600;color:#fff">' + name + '</div>' +
          '<div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:3px">' + user.email + '</div>' +
        '</div>' +
        '<a id="portalLogoutBtn" href="/auth/logout" style="display:flex;align-items:center;gap:8px;padding:12px 16px;font-size:12px;font-weight:500;color:rgba(255,255,255,0.65);text-decoration:none;transition:all .15s">' +
          '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/></svg>' +
          'Sign out' +
        '</a>' +
      '</div>';

    // Toggle popup
    var btn = document.getElementById('portalProfileBtn');
    var menu = document.getElementById('portalUserMenu');
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    });
    document.addEventListener('click', function() { menu.style.display = 'none'; });
    menu.addEventListener('click', function(e) { e.stopPropagation(); });

    // Hover effect on logout
    var logoutBtn = document.getElementById('portalLogoutBtn');
    logoutBtn.addEventListener('mouseover', function() { this.style.background = 'rgba(255,255,255,0.06)'; this.style.color = '#fff'; });
    logoutBtn.addEventListener('mouseout', function() { this.style.background = 'none'; this.style.color = 'rgba(255,255,255,0.65)'; });
    logoutBtn.addEventListener('click', function() { localStorage.removeItem('fermat_portal_user'); });
  }

  // ── LOGIN OVERLAY (blocks entire page) ──
  function showLoginOverlay(errorMsg) {
    // Hide everything
    document.body.style.overflow = 'hidden';

    var overlay = document.createElement('div');
    overlay.id = 'portal-login-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;background:#F4F3F0;z-index:99999;display:flex;align-items:center;justify-content:center;font-family:Space Grotesk,sans-serif';
    overlay.innerHTML =
      '<div style="text-align:center;max-width:380px;padding:40px">' +
        '<img src="https://cdn.prod.website-files.com/63f5f201b1f212a5c76681f0/63f6319f0b6d0beeffa89a24_Logo.svg" height="32" style="margin-bottom:28px;opacity:0.85" onerror="this.outerHTML=\'<div style=font-size:22px;font-weight:700;color:#072C1B;margin-bottom:28px>FERM\\u00c0T</div>\'">' +
        '<h1 style="font-family:Cormorant Garamond,serif;font-size:32px;font-weight:400;color:#072C1B;margin-bottom:6px;letter-spacing:-0.5px">Account Management</h1>' +
        '<p style="color:#9E9E9E;font-size:13px;margin-bottom:32px">Sign in with your FERM\u00c0T Google account to continue</p>' +
        '<a href="/auth/google" style="display:inline-flex;align-items:center;gap:10px;padding:13px 32px;background:#072C1B;color:#fff;border-radius:12px;text-decoration:none;font-size:14px;font-weight:600;transition:all .2s;box-shadow:0 2px 8px rgba(7,44,27,0.2)" onmouseover="this.style.background=\'#0d4a2f\';this.style.transform=\'translateY(-1px)\'" onmouseout="this.style.background=\'#072C1B\';this.style.transform=\'none\'">' +
          '<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>' +
          'Sign in with Google' +
        '</a>' +
        (errorMsg ? '<p style="color:#C84632;font-size:12px;margin-top:16px">' + errorMsg + '</p>' : '') +
        '<p style="color:#bbb;font-size:10px;margin-top:24px">Restricted to @fermatcommerce.com</p>' +
      '</div>';
    document.body.appendChild(overlay);
  }

  // ── INIT ──
  function init() {
    var ssoError = checkSSOCallback();
    var user = getStoredUser();
    var info = window.__PORTAL_USER__ || {};

    if (user) {
      // Logged in — show profile, no gate
      showUserProfile(user);
      return;
    }

    if (info.ssoConfigured) {
      // SSO active but not logged in — BLOCK with login overlay
      showLoginOverlay(ssoError);
      return;
    }

    // SSO not configured — show default sidebar (no changes)
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
