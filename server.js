/**
 * server.js — Express server for Account Management Portal
 * Google OAuth SSO (same pattern as Newsletter Hub)
 */

const express = require('express');
const path = require('path');
const crypto = require('crypto');
const querystring = require('querystring');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// ── GOOGLE OAUTH CONFIG ─────────────────────────────────────────────────────
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID || 'PLACEHOLDER_CLIENT_ID';
const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET || 'PLACEHOLDER_CLIENT_SECRET';
const SSO_SIGNING_SECRET = process.env.SSO_SIGNING_SECRET || crypto.randomBytes(32).toString('hex');
const ALLOWED_DOMAIN = 'fermatcommerce.com';

function getCallbackUrl(req) {
  var proto = req.headers['x-forwarded-proto'] || req.protocol || 'http';
  var host = req.headers['x-forwarded-host'] || req.headers.host;
  return proto + '://' + host + '/auth/google/callback';
}

function signEmail(email) {
  return crypto.createHmac('sha256', SSO_SIGNING_SECRET).update(email).digest('hex').substring(0, 32);
}

// ── AUTH MIDDLEWARE ──────────────────────────────────────────────────────────
function checkAuth(req) {
  var cookie = req.headers.cookie || '';
  var match = cookie.match(/fermat_portal_auth=([^;]+)/);
  if (!match) return null;
  var parts = match[1].split('_');
  var token = parts[0];
  var email = parts.slice(1).join('_');
  if (!email || signEmail(email) !== token) return null;
  return email;
}

// ── STATIC FILES (CSS/JS if needed) ─────────────────────────────────────────
app.use(express.static(__dirname, {
  index: false,  // don't auto-serve index.html — we gate it
  extensions: ['css', 'js', 'png', 'jpg', 'svg', 'ico', 'json']
}));

// ── LOGIN PAGE (served when not authenticated) ──────────────────────────────
function loginPage(errorMsg) {
  return '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FERMÀT — Sign In</title>' +
    '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Cormorant+Garamond:wght@400;500&display=swap" rel="stylesheet">' +
    '<style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:"Space Grotesk",sans-serif;background:#F4F3F0;display:flex;align-items:center;justify-content:center;min-height:100vh}</style></head><body>' +
    '<div style="text-align:center;max-width:380px;padding:40px">' +
      '<img src="https://cdn.prod.website-files.com/63f5f201b1f212a5c76681f0/63f6319f0b6d0beeffa89a24_Logo.svg" height="32" style="margin-bottom:28px;opacity:0.85">' +
      '<h1 style="font-family:Cormorant Garamond,serif;font-size:32px;font-weight:400;color:#072C1B;margin-bottom:6px">Account Management</h1>' +
      '<p style="color:#9E9E9E;font-size:13px;margin-bottom:32px">Sign in with your FERMÀT Google account to continue</p>' +
      '<a href="/auth/google" style="display:inline-flex;align-items:center;gap:10px;padding:13px 32px;background:#072C1B;color:#fff;border-radius:12px;text-decoration:none;font-size:14px;font-weight:600;box-shadow:0 2px 8px rgba(7,44,27,0.2)">' +
        '<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>' +
        'Sign in with Google</a>' +
      (errorMsg ? '<p style="color:#C84632;font-size:12px;margin-top:16px">' + errorMsg + '</p>' : '') +
      '<p style="color:#bbb;font-size:10px;margin-top:24px">Restricted to @fermatcommerce.com</p>' +
    '</div></body></html>';
}

// ── MAIN ROUTE — server-side auth enforcement ───────────────────────────────
app.get('/', function (req, res) {
  var ssoConfigured = GOOGLE_CLIENT_ID !== 'PLACEHOLDER_CLIENT_ID';
  var userEmail = checkAuth(req);

  // SSO is configured but user is NOT authenticated → block completely
  if (ssoConfigured && !userEmail) {
    var error = req.query.sso_error;
    var errorMsg = null;
    if (error === 'domain_not_allowed') errorMsg = 'Only @fermatcommerce.com accounts allowed.';
    else if (error === 'access_denied') errorMsg = 'Access denied.';
    else if (error) errorMsg = 'Sign-in failed. Please try again.';
    return res.send(loginPage(errorMsg));
  }

  // Authenticated (or SSO not configured) → serve dashboard
  var html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');

  // Inject user profile script
  var authScript = '<script>' + fs.readFileSync(path.join(__dirname, 'auth-portal.js'), 'utf8') + '</script>';
  html = html.replace('</body>', authScript + '</body>');

  var userMeta = '<script>window.__PORTAL_USER__=' + JSON.stringify({
    email: userEmail || 'pulkit@fermatcommerce.com',
    name: userEmail ? '' : 'Pulkit Srivastava',
    ssoConfigured: ssoConfigured
  }) + ';</script>';
  html = html.replace('</head>', userMeta + '</head>');

  res.send(html);
});

// ── GOOGLE OAUTH SSO ────────────────────────────────────────────────────────

app.get('/auth/google', function (req, res) {
  if (GOOGLE_CLIENT_ID === 'PLACEHOLDER_CLIENT_ID') {
    return res.status(503).send('Google SSO not configured yet.');
  }
  var callbackUrl = getCallbackUrl(req);
  var params = querystring.stringify({
    client_id: GOOGLE_CLIENT_ID,
    redirect_uri: callbackUrl,
    response_type: 'code',
    scope: 'openid email profile',
    hd: ALLOWED_DOMAIN,
    prompt: 'select_account',
  });
  res.redirect('https://accounts.google.com/o/oauth2/v2/auth?' + params);
});

app.get('/auth/google/callback', function (req, res) {
  var code = req.query.code;
  var error = req.query.error;

  if (error) return res.redirect('/?sso_error=' + encodeURIComponent(error));
  if (!code) return res.redirect('/?sso_error=no_code');

  var callbackUrl = getCallbackUrl(req);

  (async function() {
    try {
      var tokenRes = await fetch('https://oauth2.googleapis.com/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: querystring.stringify({
          code: code,
          client_id: GOOGLE_CLIENT_ID,
          client_secret: GOOGLE_CLIENT_SECRET,
          redirect_uri: callbackUrl,
          grant_type: 'authorization_code',
        }),
      });

      var data = await tokenRes.json();

      if (!data.id_token) {
        return res.redirect('/?sso_error=no_token&detail=' + encodeURIComponent(data.error_description || data.error || ''));
      }

      var parts = data.id_token.split('.');
      var payload = JSON.parse(Buffer.from(parts[1].replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString());

      var email = (payload.email || '').toLowerCase();
      var name = payload.name || '';

      if (!email.endsWith('@' + ALLOWED_DOMAIN)) {
        return res.redirect('/?sso_error=domain_not_allowed');
      }

      var token = signEmail(email);
      res.set('Set-Cookie', 'fermat_portal_auth=' + token + '_' + email + '; Path=/; HttpOnly; SameSite=Lax; Max-Age=86400');
      res.redirect('/?sso_email=' + encodeURIComponent(email) + '&sso_name=' + encodeURIComponent(name) + '&sso_token=' + token);

    } catch (e) {
      res.redirect('/?sso_error=network_error&detail=' + encodeURIComponent(e.message));
    }
  })();
});

app.get('/api/verify-sso', function (req, res) {
  var email = (req.query.email || '').toLowerCase();
  var token = req.query.token || '';
  if (!email || !token) return res.json({ valid: false });
  res.json({ valid: token === signEmail(email) });
});

app.get('/auth/logout', function (req, res) {
  res.set('Set-Cookie', 'fermat_portal_auth=; Path=/; HttpOnly; Max-Age=0');
  res.redirect('/');
});

// Health check
app.get('/health', function (req, res) {
  res.json({ status: 'ok', sso: GOOGLE_CLIENT_ID !== 'PLACEHOLDER_CLIENT_ID' });
});

app.listen(PORT, function () {
  console.log('FERMÀT Account Portal on port ' + PORT);
  console.log('SSO: ' + (GOOGLE_CLIENT_ID !== 'PLACEHOLDER_CLIENT_ID' ? 'ENABLED' : 'disabled (no credentials)'));
});
