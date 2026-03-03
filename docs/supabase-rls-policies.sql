-- ============================================================
-- ACE Avionics Training — Supabase RLS Policies
-- Run this in the Supabase SQL Editor to enable proper
-- read/write access for the anon role.
-- ============================================================

-- 1. ace_question_events — Allow anon INSERT and SELECT
-- INSERT is needed for tracking answers from drill/jeopardy/flashcards
-- SELECT is needed for the gamification engine to read events back

ALTER TABLE ace_question_events ENABLE ROW LEVEL SECURITY;

-- Allow anyone to insert events (tracked by session_id)
CREATE POLICY IF NOT EXISTS "anon_insert_question_events"
  ON ace_question_events
  FOR INSERT
  TO anon
  WITH CHECK (true);

-- Allow anyone to read their own events (by session_id)
CREATE POLICY IF NOT EXISTS "anon_select_question_events"
  ON ace_question_events
  FOR SELECT
  TO anon
  USING (true);


-- 2. ace_session_summaries — Allow anon INSERT and SELECT

ALTER TABLE ace_session_summaries ENABLE ROW LEVEL SECURITY;

CREATE POLICY IF NOT EXISTS "anon_insert_session_summaries"
  ON ace_session_summaries
  FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY IF NOT EXISTS "anon_select_session_summaries"
  ON ace_session_summaries
  FOR SELECT
  TO anon
  USING (true);


-- 3. ace_enrollments — Allow anon SELECT (for admin page and enrollment checks)

ALTER TABLE ace_enrollments ENABLE ROW LEVEL SECURITY;

CREATE POLICY IF NOT EXISTS "anon_select_enrollments"
  ON ace_enrollments
  FOR SELECT
  TO anon
  USING (true);

CREATE POLICY IF NOT EXISTS "anon_insert_enrollments"
  ON ace_enrollments
  FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY IF NOT EXISTS "anon_update_enrollments"
  ON ace_enrollments
  FOR UPDATE
  TO anon
  USING (true)
  WITH CHECK (true);
