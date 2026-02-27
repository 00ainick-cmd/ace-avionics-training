-- ============================================================
-- ACE Admin Queries — run in Supabase SQL Editor
-- ============================================================

-- List all active enrollments
SELECT access_code, student_name, email, plan, expires_at, activated_at, is_active
FROM ace_enrollments
ORDER BY created_at DESC;

-- Find a specific student by code
SELECT * FROM ace_enrollments WHERE access_code = 'ACE-XXXX-XXXX';

-- Revoke a student's access
UPDATE ace_enrollments SET is_active = FALSE WHERE access_code = 'ACE-XXXX-XXXX';

-- See a student's category progress
SELECT p.cat_id, p.mastery_pct, p.practice_score, p.final_score, p.final_passed
FROM ace_progress p
JOIN ace_enrollments e ON e.id = p.enrollment_id
WHERE e.access_code = 'ACE-XXXX-XXXX';

-- See what a student has completed
SELECT c.cat_id, c.item_key, c.completed_at
FROM ace_completions c
JOIN ace_enrollments e ON e.id = c.enrollment_id
WHERE e.access_code = 'ACE-XXXX-XXXX'
ORDER BY c.completed_at;

-- Count enrollments by plan
SELECT plan, COUNT(*) as count FROM ace_enrollments GROUP BY plan;

-- Count enrollments by month
SELECT DATE_TRUNC('month', created_at) as month, COUNT(*) as signups
FROM ace_enrollments
GROUP BY 1 ORDER BY 1 DESC;

-- Students who have not activated yet (bought but have not logged in)
SELECT access_code, email, plan, created_at
FROM ace_enrollments
WHERE activated_at IS NULL AND is_active = TRUE
ORDER BY created_at DESC;

-- Extend a 3-month enrollment by 30 days
UPDATE ace_enrollments
SET expires_at = expires_at + INTERVAL '30 days'
WHERE access_code = 'ACE-XXXX-XXXX';

-- Upgrade student to lifetime
UPDATE ace_enrollments
SET plan = 'lifetime', expires_at = NULL
WHERE access_code = 'ACE-XXXX-XXXX';
