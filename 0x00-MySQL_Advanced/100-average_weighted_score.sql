-- File: 100-average_weighted_score.sql
-- Task: Creates a stored procedure `ComputeAverageWeightedScoreForUser` that computes 
-- and stores the average weighted score for a student based on their project scores.

-- Drop the stored procedure if it already exists to avoid errors when recreating it
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Change the delimiter to $$ to avoid conflicts with semicolons inside the procedure
DELIMITER $$

-- Create the stored procedure `ComputeAverageWeightedScoreForUser`
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    -- Declare variables to hold the sum of weighted scores and the sum of weights
    DECLARE weighted_sum FLOAT DEFAULT 0;
    DECLARE weight_total INT DEFAULT 0;
    
    -- Calculate the sum of weighted scores for the given user
    -- SUM(c.score * p.weight) multiplies each project score by its weight and sums them up
    SELECT SUM(c.score * p.weight) 
    INTO weighted_sum  -- Store the result in `weighted_sum`
    FROM corrections c
    JOIN projects p ON c.project_id = p.id  -- Join `corrections` with `projects` to access weights
    WHERE c.user_id = user_id;  -- Filter by the input `user_id`
    
    -- Calculate the total sum of weights for the given user
    -- SUM(p.weight) sums up all the weights of the projects associated with the user
    SELECT SUM(p.weight) 
    INTO weight_total  -- Store the result in `weight_total`
    FROM corrections c
    JOIN projects p ON c.project_id = p.id  -- Join `corrections` with `projects` to access weights
    WHERE c.user_id = user_id;  -- Filter by the input `user_id`
    
    -- Update the `average_score` field for the user in the `users` table
    -- The average weighted score is calculated by dividing `weighted_sum` by `weight_total`
    -- If `weight_total` is 0 (to avoid division by zero), `average_score` will be set to 0
    UPDATE users
    SET average_score = IF(weight_total = 0, 0, weighted_sum / weight_total)  -- Set the `average_score` based on the calculation
    WHERE id = user_id;  -- Filter by the input `user_id`
END $$

-- Change the delimiter back to the default semicolon
DELIMITER ;
