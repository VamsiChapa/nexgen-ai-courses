-- ═══════════════════════════════════════════════════════════════════
-- NexGen AI Trainer Portal — Supabase Schema
-- Run this entire file in the Supabase SQL Editor (one shot).
-- ═══════════════════════════════════════════════════════════════════

-- ── Extensions ──────────────────────────────────────────────────────
create extension if not exists "uuid-ossp";
create extension if not exists "pg_stat_statements";

-- ── Profiles ────────────────────────────────────────────────────────
-- One row per authenticated user. Linked to auth.users via trigger.
create table if not exists public.profiles (
  id           uuid         references auth.users(id) on delete cascade primary key,
  email        text         not null,
  full_name    text,
  phone        text,
  institution  text,
  role         text         not null default 'trainer'
                            check (role in ('admin','trainer')),
  status       text         not null default 'pending'
                            check (status in ('pending','approved','rejected','direct')),
  quiz_score   integer,
  quiz_passed  boolean      default false,
  notes        text,                          -- admin notes
  created_at   timestamptz  default now(),
  approved_at  timestamptz,
  approved_by  uuid,                          -- profiles.id of admin who approved
  last_seen    timestamptz
);
comment on table public.profiles is 'Extended trainer/admin user info';

-- ── Quiz Attempts ────────────────────────────────────────────────────
create table if not exists public.quiz_attempts (
  id          uuid         default gen_random_uuid() primary key,
  user_id     uuid         references public.profiles(id) on delete cascade,
  email       text,                           -- stored pre-auth for reference
  answers     jsonb        not null default '{}',
  score       integer      not null,
  passed      boolean      not null,
  created_at  timestamptz  default now()
);
comment on table public.quiz_attempts is 'Python aptitude quiz attempts during signup';

-- ── Day Progress ─────────────────────────────────────────────────────
-- One row per (user, context, day). Upsert on mark-complete.
create table if not exists public.day_progress (
  id           uuid         default gen_random_uuid() primary key,
  user_id      uuid         references public.profiles(id) on delete cascade,
  context      text         not null
               check (context in ('prep','track1','track2','track3')),
  day_number   integer      not null check (day_number >= 1),
  completed_at timestamptz  default now(),
  unique(user_id, context, day_number)
);
comment on table public.day_progress is 'Per-trainer daily progress across prep plan and all 3 tracks';

-- ── Direct Invites (Backfill) ─────────────────────────────────────────
-- Admin adds emails here. When that email signs up → auto-approved, no quiz.
create table if not exists public.direct_invites (
  id           uuid         default gen_random_uuid() primary key,
  email        text         not null unique,
  full_name    text,
  notes        text,
  invited_by   uuid         references public.profiles(id),
  created_at   timestamptz  default now(),
  used         boolean      default false,
  used_at      timestamptz
);
comment on table public.direct_invites is 'Pre-approved emails — skip quiz on signup';

-- ── Activity Log ──────────────────────────────────────────────────────
create table if not exists public.activity_log (
  id          uuid         default gen_random_uuid() primary key,
  user_id     uuid         references public.profiles(id) on delete cascade,
  action      text         not null,  -- 'login','progress_update','quiz_attempt', etc.
  metadata    jsonb        default '{}',
  created_at  timestamptz  default now()
);
comment on table public.activity_log is 'Audit trail of trainer actions';


-- ═══════════════════════════════════════════════════════════════════
-- Row Level Security
-- ═══════════════════════════════════════════════════════════════════
alter table public.profiles       enable row level security;
alter table public.quiz_attempts  enable row level security;
alter table public.day_progress   enable row level security;
alter table public.direct_invites enable row level security;
alter table public.activity_log   enable row level security;

-- ── Helper functions ──────────────────────────────────────────────────
create or replace function public.is_admin()
returns boolean language sql security definer stable as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role = 'admin'
  );
$$;

create or replace function public.is_approved()
returns boolean language sql security definer stable as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and status in ('approved','direct')
  );
$$;

-- ── Profiles policies ────────────────────────────────────────────────
drop policy if exists "profiles_select" on public.profiles;
create policy "profiles_select" on public.profiles
  for select using (auth.uid() = id or public.is_admin());

drop policy if exists "profiles_insert" on public.profiles;
create policy "profiles_insert" on public.profiles
  for insert with check (auth.uid() = id or public.is_admin());

drop policy if exists "profiles_update" on public.profiles;
create policy "profiles_update" on public.profiles
  for update using (auth.uid() = id or public.is_admin());

-- ── Quiz policies ────────────────────────────────────────────────────
drop policy if exists "quiz_all" on public.quiz_attempts;
create policy "quiz_all" on public.quiz_attempts
  for all using (auth.uid() = user_id or public.is_admin());

-- Also allow insert without auth (pre-signup quiz grading)
drop policy if exists "quiz_insert_anon" on public.quiz_attempts;
create policy "quiz_insert_anon" on public.quiz_attempts
  for insert with check (true);

-- ── Day progress policies ─────────────────────────────────────────────
drop policy if exists "progress_own" on public.day_progress;
create policy "progress_own" on public.day_progress
  for all using (auth.uid() = user_id or public.is_admin());

-- ── Direct invites: admin only ────────────────────────────────────────
drop policy if exists "invites_admin" on public.direct_invites;
create policy "invites_admin" on public.direct_invites
  for all using (public.is_admin());

-- Allow anon to check if email is invited (for signup flow)
drop policy if exists "invites_check" on public.direct_invites;
create policy "invites_check" on public.direct_invites
  for select using (true);

-- ── Activity log policies ─────────────────────────────────────────────
drop policy if exists "activity_read" on public.activity_log;
create policy "activity_read" on public.activity_log
  for select using (auth.uid() = user_id or public.is_admin());

drop policy if exists "activity_insert" on public.activity_log;
create policy "activity_insert" on public.activity_log
  for insert with check (auth.uid() = user_id or public.is_admin());


-- ═══════════════════════════════════════════════════════════════════
-- Triggers
-- ═══════════════════════════════════════════════════════════════════

-- Auto-create profile on new auth user
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer as $$
declare
  invite_row public.direct_invites%rowtype;
begin
  -- Check if this email has a direct invite
  select * into invite_row
  from public.direct_invites
  where lower(email) = lower(new.email) and used = false
  limit 1;

  insert into public.profiles (id, email, full_name, status, quiz_passed)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'full_name', ''),
    case when invite_row.id is not null then 'direct' else 'pending' end,
    case when invite_row.id is not null then true else false end
  );

  -- Mark invite used
  if invite_row.id is not null then
    update public.direct_invites
    set used = true, used_at = now()
    where id = invite_row.id;
  end if;

  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Update last_seen on login (called from client)
create or replace function public.touch_last_seen(uid uuid)
returns void language sql security definer as $$
  update public.profiles set last_seen = now() where id = uid;
$$;


-- ═══════════════════════════════════════════════════════════════════
-- Views (admin reads these)
-- ═══════════════════════════════════════════════════════════════════
create or replace view public.trainer_stats as
select
  p.id,
  p.email,
  p.full_name,
  p.phone,
  p.institution,
  p.status,
  p.role,
  p.quiz_score,
  p.quiz_passed,
  p.created_at,
  p.approved_at,
  p.last_seen,
  p.notes,
  coalesce(count(dp.id) filter (where dp.context = 'prep'),  0)::int as prep_days_done,
  coalesce(count(dp.id) filter (where dp.context = 'track1'),0)::int as t1_days_done,
  coalesce(count(dp.id) filter (where dp.context = 'track2'),0)::int as t2_days_done,
  coalesce(count(dp.id) filter (where dp.context = 'track3'),0)::int as t3_days_done,
  coalesce(count(dp.id), 0)::int                                       as total_days_done,
  -- Activity in last 7 days
  coalesce(count(dp.id) filter (where dp.completed_at > now() - interval '7 days'), 0)::int as active_last_7d
from public.profiles p
left join public.day_progress dp on dp.user_id = p.id
where p.role = 'trainer'
group by p.id;

comment on view public.trainer_stats is 'Admin-facing aggregate view of all trainer progress';


-- ═══════════════════════════════════════════════════════════════════
-- Seed: Make first admin (replace email before running)
-- ═══════════════════════════════════════════════════════════════════
-- After you sign up with chapavamsi1731@gmail.com, run this:
--
--   update public.profiles
--   set role = 'admin', status = 'approved'
--   where email = 'chapavamsi1731@gmail.com';
--
-- ═══════════════════════════════════════════════════════════════════
