-- File: 9-index_name_score.sql
-- Task: Create an index on the table 'names' for the first letter of 'name' and the 'score'.

-- Ensure that the index does not already exist
-- DROP INDEX IF EXISTS idx_name_first_score ON names;

-- Create an index named 'idx_name_first_score' on the 'names' table.
-- This index will be created on the first letter of the 'name' column and the 'score' column.
CREATE INDEX idx_name_first_score ON names (name(1), score);

-- The index will help optimize queries that filter by the first letter of the 'name' and the 'score'.
