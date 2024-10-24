-- File: 8-index_my_names.sql
-- Task: Create an index on the table 'names' based on the first letter of 'name'.

-- Ensure that the index does not already exist
-- DROP INDEX IF EXISTS idx_name_first ON names;

-- Create an index named 'idx_name_first' on the 'names' table.
-- This index will be created on the first letter of the 'name' column.
CREATE INDEX idx_name_first ON names (name(1));

-- The index will help optimize queries that filter by the first letter of the 'name'.
