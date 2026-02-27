-- ============================================================
-- ACE Avionics Training — Enrollment & Progress Schema
-- Run this in: Supabase Dashboard → SQL Editor → New Query
-- ============================================================

-- ── 1. ENROLLMENTS ───────────────────────────────────────────
-- One row per purchased access code.
-- Created by Stripe webhook; activated when student enters code.
CREATE TABLE ace_enrollments (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  access_code       TEXT UNIQUE NOT NULL,       -- e.g. 'ACE-7K3M-R9PX'
  student_name      TEXT,                        -- filled in on first login
  email             TEXT,                        -- from Stripe
  plan              TEXT NOT NULL DEFAULT '3mo', -- '3mo' | 'lifetime'
  expires_at        TIMESTAMPTZ,                 -- NULL = lifetime
  stripe_session_id TEXT,
  is_active         BOOLEAN DEFAULT TRUE,
  activated_at      TIMESTAMPTZ,                 -- when student first used the code
  theme             TEXT DEFAULT 'dark',
  dashboard_mode    TEXT DEFAULT 'study'
);

-- ── 2. PROGRESS (per student per category) ───────────────────
-- One row per (enrollment × category). Upserted on every activity completion.
CREATE TABLE ace_progress (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  enrollment_id  UUID NOT NULL REFERENCES ace_enrollments(id) ON DELETE CASCADE,
  cat_id         TEXT NOT NULL,          -- 'cat-1' … 'cat-8'
  mastery_pct    SMALLINT DEFAULT 0,
  time_minutes   INT DEFAULT 0,
  practice_score NUMERIC(5,2),
  final_score    NUMERIC(5,2),
  final_attempts SMALLINT DEFAULT 0,
  final_passed   BOOLEAN DEFAULT FALSE,
  updated_at     TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(enrollment_id, cat_id)
);

-- ── 3. COMPLETIONS (activity completion flags) ────────────────
-- Replaces all `ace_cat_${catId}_${key}_complete` localStorage keys.
CREATE TABLE ace_completions (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  enrollment_id UUID NOT NULL REFERENCES ace_enrollments(id) ON DELETE CASCADE,
  cat_id        TEXT NOT NULL,
  item_key      TEXT NOT NULL,  -- e.g. 'training_maintenance-regs', 'practice', 'jeopardy', 'flashcards', 'final'
  completed_at  TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(enrollment_id, cat_id, item_key)
);

-- ── 4. LO MASTERY (per-question answer history) ───────────────
-- Replaces ace_progress_* and ace_lo_* localStorage keys.
CREATE TABLE ace_lo_mastery (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  enrollment_id UUID NOT NULL REFERENCES ace_enrollments(id) ON DELETE CASCADE,
  lesson_id     TEXT NOT NULL,     -- 'cat-4-flight-instruments'
  question_id   TEXT NOT NULL,     -- 'cat4-q001'
  correct_count SMALLINT DEFAULT 0,
  total_count   SMALLINT DEFAULT 0,
  last_correct  BOOLEAN DEFAULT FALSE,
  updated_at    TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(enrollment_id, lesson_id, question_id)
);

-- ── 5. INDEXES ────────────────────────────────────────────────
CREATE INDEX idx_enrollments_code     ON ace_enrollments(access_code);
CREATE INDEX idx_progress_enrollment  ON ace_progress(enrollment_id);
CREATE INDEX idx_completions_enroll   ON ace_completions(enrollment_id);
CREATE INDEX idx_lo_mastery_enroll    ON ace_lo_mastery(enrollment_id);

-- ── 6. ROW LEVEL SECURITY ─────────────────────────────────────
ALTER TABLE ace_enrollments  ENABLE ROW LEVEL SECURITY;
ALTER TABLE ace_progress      ENABLE ROW LEVEL SECURITY;
ALTER TABLE ace_completions   ENABLE ROW LEVEL SECURITY;
ALTER TABLE ace_lo_mastery    ENABLE ROW LEVEL SECURITY;

-- Enrollments: anon can SELECT only to validate a code (read one row by code)
CREATE POLICY "anon validate code"
  ON ace_enrollments FOR SELECT TO anon
  USING (true);  -- RLS enforced via app logic (fetch by specific code only)

-- Enrollments: anon can UPDATE their own row (to set student_name on activation)
CREATE POLICY "anon activate enrollment"
  ON ace_enrollments FOR UPDATE TO anon
  USING (true)
  WITH CHECK (true);

-- Progress: anon can INSERT and UPDATE (app enforces enrollment_id scoping)
CREATE POLICY "anon upsert progress"
  ON ace_progress FOR ALL TO anon
  USING (true) WITH CHECK (true);

-- Completions: anon can INSERT (idempotent)
CREATE POLICY "anon insert completions"
  ON ace_completions FOR ALL TO anon
  USING (true) WITH CHECK (true);

-- LO Mastery: anon can upsert
CREATE POLICY "anon upsert lo_mastery"
  ON ace_lo_mastery FOR ALL TO anon
  USING (true) WITH CHECK (true);

-- Service role has full access to everything (for admin/webhook)
-- (service_role bypasses RLS automatically in Supabase)
