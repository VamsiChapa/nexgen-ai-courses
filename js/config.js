// ═══════════════════════════════════════════════════════════════════
// NexGen AI Trainer Portal — Shared Configuration
// Fill in your Supabase + EmailJS values here.
// This file is loaded by every app page.
// ═══════════════════════════════════════════════════════════════════

// ── Supabase ─────────────────────────────────────────────────────────
// Get these from: Supabase Dashboard → Project Settings → API
const SUPABASE_URL      = 'https://mugfmtyierkevpjytfec.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im11Z2ZtdHlpZXJrZXZwanl0ZmVjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxMjcwMzYsImV4cCI6MjA5MTcwMzAzNn0.zFD6iEypMGzSIcRGz6t9zIMHARIQZmNJkLc713TVpU8';

// ── EmailJS ───────────────────────────────────────────────────────────
// Get these from: https://www.emailjs.com/ (free: 200 emails/month)
// Create 2 email templates:
//   1. template_signup_notify → sent to admin when trainer signs up
//   2. template_approved      → sent to trainer when approved
const EMAILJS_PUBLIC_KEY          = 'YOUR_EMAILJS_PUBLIC_KEY';
const EMAILJS_SERVICE_ID          = 'YOUR_EMAILJS_SERVICE_ID';
const EMAILJS_TEMPLATE_NOTIFY     = 'template_signup_notify';
const EMAILJS_TEMPLATE_APPROVED   = 'template_approved';
const EMAILJS_TEMPLATE_INVITE     = 'template_invite';

// ── App constants ─────────────────────────────────────────────────────
const ADMIN_EMAIL      = 'chapavamsi1731@gmail.com';
const SITE_URL         = 'https://vamsichapa.github.io/nexgen-ai-courses';
const QUIZ_PASS_SCORE  = 6;
const QUIZ_TOTAL       = 10;

// ── Route helpers ─────────────────────────────────────────────────────
const ROUTES = {
  login:     'login.html',
  signup:    'signup.html',
  dashboard: 'dashboard.html',
  admin:     'admin.html',
};

// ── Shared Supabase client (created once) ────────────────────────────
// Loaded after supabase CDN script
function getSupabase() {
  if (!window._sb) {
    window._sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  }
  return window._sb;
}

// ── Auth helpers ──────────────────────────────────────────────────────
async function requireAuth(allowedStatuses = ['approved','direct'], adminOnly = false) {
  const sb = getSupabase();
  const { data: { session } } = await sb.auth.getSession();
  if (!session) { window.location.href = ROUTES.login; return null; }

  const { data: profile } = await sb.from('profiles').select('*').eq('id', session.user.id).single();
  if (!profile) { window.location.href = ROUTES.login; return null; }

  if (adminOnly && profile.role !== 'admin') {
    window.location.href = ROUTES.dashboard; return null;
  }
  if (!adminOnly && !allowedStatuses.includes(profile.status)) {
    // Still logged in but not approved — show them a holding page
    return { session, profile, blocked: true };
  }

  // Touch last_seen
  await sb.rpc('touch_last_seen', { uid: session.user.id }).catch(() => {});
  return { session, profile, blocked: false };
}

async function logout() {
  await getSupabase().auth.signOut();
  window.location.href = ROUTES.login;
}

// ── EmailJS helpers ───────────────────────────────────────────────────
function sendEmail(templateId, params) {
  if (!window.emailjs || EMAILJS_PUBLIC_KEY === 'YOUR_EMAILJS_PUBLIC_KEY') {
    console.warn('EmailJS not configured — skipping email:', templateId, params);
    return Promise.resolve();
  }
  return emailjs.send(EMAILJS_SERVICE_ID, templateId, params, EMAILJS_PUBLIC_KEY)
    .catch(e => console.warn('EmailJS error:', e));
}

function notifyAdminSignup(trainerName, trainerEmail, quizScore) {
  return sendEmail(EMAILJS_TEMPLATE_NOTIFY, {
    to_email:     ADMIN_EMAIL,
    trainer_name: trainerName,
    trainer_email:trainerEmail,
    quiz_score:   quizScore + ' / ' + QUIZ_TOTAL,
    admin_url:    SITE_URL + '/' + ROUTES.admin,
  });
}

function notifyTrainerApproved(trainerEmail, trainerName) {
  return sendEmail(EMAILJS_TEMPLATE_APPROVED, {
    to_email:   trainerEmail,
    to_name:    trainerName,
    login_url:  SITE_URL + '/' + ROUTES.login,
    portal_url: SITE_URL + '/' + ROUTES.dashboard,
  });
}

function notifyTrainerInvite(inviteEmail, inviteName) {
  return sendEmail(EMAILJS_TEMPLATE_INVITE, {
    to_email:   inviteEmail,
    to_name:    inviteName || 'Trainer',
    signup_url: SITE_URL + '/' + ROUTES.signup,
  });
}

// ── Shared CSS vars string (injected into each page's <style>) ────────
// Each page imports this via: <script src="js/config.js"></script>
