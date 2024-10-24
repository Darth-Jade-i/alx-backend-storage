-- File: 11-need_meeting.sql
-- Task: Creates a view `need_meeting` that lists all students with a score under 80 (strict) and no `last_meeting` or more than 1 month ago.
-- Script that creates a view `need_meeting` listing students with a score under 80
-- and either no `last_meeting` date or a `last_meeting` date more than 1 month old.

-- Drop the view `need_meeting` if it already exists to prevent errors when creating it anew
DROP VIEW IF EXISTS need_meeting;

-- Create a new view named `need_meeting`
CREATE VIEW need_meeting AS
-- Select the `name` column from the `students` table
SELECT name
FROM students
-- Apply filtering conditions
WHERE score < 80  -- Include students whose score is strictly less than 80
AND (
    last_meeting IS NULL  -- Include students who do not have a recorded `last_meeting` date
    OR last_meeting < DATE(CURDATE() - INTERVAL 1 MONTH)  -- Include students whose `last_meeting` date is more than 1 month before the current date
);
