/**
 * auth-portal.js — Sidebar user profile + logout
 * Auth is enforced SERVER-SIDE. This script only handles the UI.
 */
(function () {
  'use strict';

  function init() {
    var info = window.__PORTAL_USER__ || {};
    var email = info.email || '';
    var name = info.name || email.split('@')[0] || 'User';
    var initials = name.split(' ').filter(Boolean).map(function(w){return w[0]}).join('').substring(0,2).toUpperCase() || 'U';

    var sbf = document.querySelector('.sbf');
    if (!sbf) return;

    sbf.style.position = 'relative';
    sbf.innerHTML =
      '<div id="portalProfileBtn" style="cursor:pointer;display:flex;align-items:center;gap:10px">' +
        '<div style="width:34px;height:34px;border-radius:9px;background:rgba(62,214,96,0.15);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#3ED660;flex-shrink:0">' + initials + '</div>' +
        '<div style="flex:1;min-width:0"><div class="sbft" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + name + '</div><div class="sbfr" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + email + '</div></div>' +
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2.5" style="flex-shrink:0"><path d="M6 9l6 6 6-6"/></svg>' +
      '</div>' +
      '<div id="portalUserMenu" style="display:none;position:absolute;bottom:100%;left:0;right:0;background:#1a3a28;border-radius:12px;box-shadow:0 -6px 24px rgba(0,0,0,0.35);overflow:hidden;margin-bottom:10px;border:1px solid rgba(255,255,255,0.1)">' +
        '<div style="padding:14px 16px;border-bottom:1px solid rgba(255,255,255,0.08)">' +
          '<div style="font-size:13px;font-weight:600;color:#fff">' + name + '</div>' +
          '<div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:3px">' + email + '</div>' +
        '</div>' +
        (info.ssoConfigured ?
          '<a href="/auth/logout" style="display:flex;align-items:center;gap:8px;padding:12px 16px;font-size:12px;font-weight:500;color:rgba(255,255,255,0.65);text-decoration:none;transition:all .15s" onmouseover="this.style.background=\'rgba(255,255,255,0.06)\';this.style.color=\'#fff\'" onmouseout="this.style.background=\'none\';this.style.color=\'rgba(255,255,255,0.65)\'">' +
            '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/></svg>' +
            'Sign out</a>'
          : '<div style="padding:10px 16px;font-size:10px;color:rgba(255,255,255,0.25)">SSO not configured</div>') +
      '</div>';

    var btn = document.getElementById('portalProfileBtn');
    var menu = document.getElementById('portalUserMenu');
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    });
    document.addEventListener('click', function() { menu.style.display = 'none'; });
    menu.addEventListener('click', function(e) { e.stopPropagation(); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
