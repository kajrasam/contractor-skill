-- Add eval_year column to user_actuals
ALTER TABLE user_actuals ADD COLUMN IF NOT EXISTS eval_year INTEGER;

-- Set existing records to the current year (2026) so they are not orphaned
UPDATE user_actuals SET eval_year = 2026 WHERE eval_year IS NULL;
