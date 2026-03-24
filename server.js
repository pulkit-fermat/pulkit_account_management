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

// Serve dashboard behind auth
app.get('/', ensureAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Health check (no auth needed)
app.get('/health', (req, res) => res.json({ status: 'ok', user: req.user || null }));

app.listen(PORT, () => {
  console.log(`FERMÀT Account Portal running on port ${PORT}`);
});
