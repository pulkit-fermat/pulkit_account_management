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

// ── MAIN ROUTE — serve dashboard with auth gate injected ────────────────────
app.get('/', function (req, res) {
  var html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
  var userEmail = checkAuth(req);
  var ssoConfigured = GOOGLE_CLIENT_ID !== 'PLACEHOLDER_CLIENT_ID';

  // Inject auth.js before </body>
  var authScript = '<script>' + fs.readFileSync(path.join(__dirname, 'auth-portal.js'), 'utf8') + '</script>';
  html = html.replace('</body>', authScript + '</body>');

  // Pass user info to client
  var userMeta = '<script>window.__PORTAL_USER__=' + JSON.stringify({
    email: userEmail,
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
