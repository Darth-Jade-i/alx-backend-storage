-- File: 7-average_score.sql
-- Task: Create a stored procedure that computes and stores the average score for a student.

-- Ensure the procedure does not already exist
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Start by setting a delimiter to allow the procedure to contain multiple SQL statements.
DELIMITER $$

-- Create the stored procedure named 'ComputeAverageScoreForUser'.
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
-- The procedure takes one input parameter 'user_id', which is an integer representing the ID of the user whose average score will be computed.

BEGIN
    -- Declare a variable to hold the computed average score.
    DECLARE avg_score FLOAT;

    -- Calculate the average score for the given user by selecting the average score from the 'corrections' table.
    -- This query computes the average of the 'score' column for the specified 'user_id'.
    SELECT AVG(score)
    INTO avg_score -- Store the result of the average score calculation in the 'avg_score' variable.
    FROM corrections
    WHERE corrections.user_id = user_id; -- Filter the scores by the specified user ID.

    -- Update the 'users' table with the computed average score.
    -- This updates the 'average_score' column for the user with the specified 'user_id'.
    UPDATE users
    SET average_score = avg_score -- Set the 'average_score' column to the value of 'avg_score'.
    WHERE id = user_id; -- Ensure the update is applied only to the row where 'id' matches the given 'user_id'.

END $$ -- End the procedure and the block of code for the procedure.

-- Reset the delimiter back to the default semicolon (;).
DELIMITER ;
