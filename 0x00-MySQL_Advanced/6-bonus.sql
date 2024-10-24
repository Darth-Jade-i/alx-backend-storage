-- This SQL script creates a stored procedure named AddBonus that takes three inputs:
-- user_id, project_name, and score. It adds a correction entry for a student.
-- If the project doesn't exist in the projects table, it creates the project first.

-- Ensure the procedure does not already exist
DROP PROCEDURE IF EXISTS AddBonus;

-- Set the delimiter to $$ to allow multiple SQL statements within the procedure
DELIMITER $$

-- Start creating the stored procedure named AddBonus
CREATE PROCEDURE AddBonus(
    IN user_id INT,               -- Input parameter: ID of the user (student)
    IN project_name VARCHAR(255), -- Input parameter: Name of the project
    IN score INT                  -- Input parameter: Score for the correction
)
BEGIN
    -- Declare a local variable to store the project ID
    DECLARE project_id INT;

    -- Attempt to find the project ID based on the given project_name
    -- If the project exists, its ID will be stored in the project_id variable
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;

    -- Check if the project_id is NULL, meaning the project doesn't exist
    IF project_id IS NULL THEN
        -- If the project doesn't exist, insert a new record into the projects table
        INSERT INTO projects (name) VALUES (project_name);

        -- Retrieve the ID of the newly inserted project and store it in project_id
        SET project_id = LAST_INSERT_ID();
    END IF; -- End of the IF statement that checks for the project's existence

    -- Insert the correction record into the corrections table
    -- using the user_id, the found or newly created project_id, and the given score
    INSERT INTO corrections (user_id, project_id, score) 
    VALUES (user_id, project_id, score);
END $$ -- End of the stored procedure definition

-- Reset the delimiter back to the default semicolon (;)
DELIMITER ;
