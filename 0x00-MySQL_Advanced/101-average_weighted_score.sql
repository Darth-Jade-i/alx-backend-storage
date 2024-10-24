-- File: 101-average_weighted_score.sql
-- Task: Creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and stores
-- the average weighted score for all students.

-- Script to create a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and stores the average weighted score for all students

-- Drop the stored procedure if it already exists to avoid conflicts
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Change the delimiter to allow multiple SQL statements in the procedure
DELIMITER $$

-- Create the stored procedure ComputeAverageWeightedScoreForUsers
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Update each user in the `users` table
    UPDATE users AS U,
        -- Subquery to calculate the weighted average score for each user
        (SELECT 
            U.id,  -- Select the user ID
            SUM(C.score * P.weight) / SUM(P.weight) AS w_avg  -- Calculate the weighted average score
         FROM 
            users AS U  -- From the `users` table
         JOIN 
            corrections AS C ON U.id = C.user_id  -- Join with `corrections` to match user scores
         JOIN 
            projects AS P ON C.project_id = P.id  -- Join with `projects` to get the weight of each project
         GROUP BY 
            U.id  -- Group by user ID to calculate the average for each user
        ) AS WA
    -- Set the `average_score` of the user to the calculated weighted average
    SET U.average_score = WA.w_avg 
    -- Ensure that the update is applied to the correct user by matching IDs
    WHERE U.id = WA.id;
END $$

-- Reset the delimiter back to the default
DELIMITER ;
