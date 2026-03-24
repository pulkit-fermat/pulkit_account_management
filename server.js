const express = require('express');
const session = require('express-session');
const passport = require('passport');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const SSO_ENABLED = !!(process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET);

if (SSO_ENABLED) {
  const GoogleStrategy = require('passport-google-oauth20').Strategy;

  app.use(session({
    secret: process.env.SESSION_SECRET || 'fermat-portal-secret',
    resave: false,
    saveUninitialized: false,
    cookie: { secure: process.env.NODE_ENV === 'production', maxAge: 24 * 60 * 60 * 1000 }
  }));

  app.use(passport.initialize());
  app.use(passport.session());

  passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: process.env.CALLBACK_URL || '/auth/google/callback'
  }, (accessToken, refreshToken, profile, done) => {
    const email = profile.emails && profile.emails[0] && profile.emails[0].value;
    if (email && email.endsWith('@fermatcommerce.com')) {
      return done(null, { id: profile.id, name: profile.displayName, email });
    }
    return done(null, false, { message: 'Only @fermatcommerce.com accounts allowed' });
  }));

  passport.serializeUser((user, done) => done(null, user));
  passport.deserializeUser((user, done) => done(null, user));

  console.log('SSO enabled — @fermatcommerce.com only');
} else {
  console.log('SSO disabled — GOOGLE_CLIENT_ID not set. Serving without auth.');
}

// Auth middleware
function ensureAuth(req, res, next) {
  if (!SSO_ENABLED) return next();
  if (req.isAuthenticated()) return next();
  res.redirect('/auth/google');
}

// Auth routes
app.get('/auth/google', passport.authenticate('google', {
  scope: ['profile', 'email'],
  hd: 'fermatcommerce.com'
}));

app.get('/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/auth/denied' }),
  (req, res) => res.redirect('/')
);

app.get('/auth/denied', (req, res) => {
  res.status(403).send(`
    <div style="font-family:Space Grotesk,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;background:#F4F3F0">
      <div style="text-align:center;max-width:400px">
        <div style="font-size:48px;margin-bottom:16px">🔒</div>
        <h1 style="color:#072C1B;font-size:24px;margin-bottom:8px">Access Denied</h1>
        <p style="color:#9E9E9E;font-size:14px">Only @fermatcommerce.com accounts can access this portal.</p>
        <a href="/auth/google" style="display:inline-block;margin-top:20px;padding:10px 24px;background:#072C1B;color:#fff;border-radius:8px;text-decoration:none;font-size:13px;font-weight:600">Try Again</a>
      </div>
    </div>
  `);
});

app.get('/auth/logout', (req, res) => {
  req.logout(() => res.redirect('/'));
});

// API: current user info
app.get('/api/me', (req, res) => {
  res.json({ user: req.user || null, sso: SSO_ENABLED });
});

// Serve dashboard behind auth — inject user info
app.get('/', ensureAuth, (req, res) => {
  const fs = require('fs');
  let html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');

  const user = req.user || { name: 'Pulkit Srivastava', email: 'pulkit@fermatcommerce.com' };
  const userName = user.name || 'User';
  const userEmail = user.email || '';
  const initials = userName.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();

  // Replace the static sidebar footer with dynamic user profile + logout
  const oldFooter = /<div class="sbf">.*?<\/div><\/div>/s;
  const newFooter = `<div class="sbf" style="position:relative">
<div class="sbf-profile" onclick="document.getElementById('userPopup').classList.toggle('show')" style="cursor:pointer;display:flex;align-items:center;gap:10px">
<div style="width:32px;height:32px;border-radius:8px;background:rgba(62,214,96,0.15);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#3ED660;flex-shrink:0">${initials}</div>
<div><div class="sbft">${userName}</div><div class="sbfr">${userEmail}</div></div>
<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2" style="flex-shrink:0"><path d="M6 9l6 6 6-6"/></svg>
</div>
<div id="userPopup" class="user-popup">
<div style="padding:12px 16px;border-bottom:1px solid rgba(255,255,255,0.08)">
<div style="font-size:12px;font-weight:600;color:#fff">${userName}</div>
<div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:2px">${userEmail}</div>
</div>
${SSO_ENABLED ? '<a href="/auth/logout" style="display:block;padding:10px 16px;font-size:12px;color:rgba(255,255,255,0.6);text-decoration:none;transition:background .15s" onmouseover="this.style.background=\'rgba(255,255,255,0.05)\'" onmouseout="this.style.background=\'none\'">Sign out</a>' : '<div style="padding:10px 16px;font-size:10px;color:rgba(255,255,255,0.3)">SSO not configured</div>'}
</div>
</div>`;

  // Add popup CSS
  const popupCSS = `<style>
.user-popup{display:none;position:absolute;bottom:100%;left:10px;right:10px;background:#1a3a28;border-radius:10px;box-shadow:0 -4px 20px rgba(0,0,0,0.3);overflow:hidden;margin-bottom:8px;border:1px solid rgba(255,255,255,0.08)}
.user-popup.show{display:block}
</style>`;

  html = html.replace(oldFooter, newFooter);
  html = html.replace('</head>', popupCSS + '</head>');
  res.send(html);
});

// Health check
app.get('/health', (req, res) => res.json({ status: 'ok', user: req.user || null, sso: SSO_ENABLED }));

app.listen(PORT, () => {
  console.log(`FERMÀT Account Portal running on port ${PORT}`);
});
