-- File: 10-div.sql
-- Task: Create a function SafeDiv that divides the first number by the second number or returns 0 if the second number is 0.
-- Script that creates a function SafeDiv that divides
-- (and returns) the first number by the second number or returns
-- 0 if the second number is equal to 0.

-- Drop the function if it already exists to avoid conflicts
DROP FUNCTION IF EXISTS SafeDiv;

-- Change the delimiter to $$ to allow the use of semicolons within the function
DELIMITER $$ 

-- Create the SafeDiv function
CREATE FUNCTION SafeDiv(
    a INT,        -- First integer parameter (numerator)
    b INT         -- Second integer parameter (denominator)
)
RETURNS FLOAT   -- Specifies that the function will return a floating-point number
DETERMINISTIC  -- Indicates that the function always returns the same result for the same inputs
BEGIN
    DECLARE result FLOAT;  -- Declare a variable to store the result of the division
    
    -- Check if the denominator is 0
    IF b = 0 THEN
        RETURN 0;  -- If b is 0, return 0 to avoid division by zero
    END IF;
    
    -- Perform the division. Multiplying 'a' by 1.0 converts it to a float for accurate division
    SET result = (a * 1.0) / b;
    
    RETURN result;  -- Return the result of the division
END $$

-- Reset the delimiter to the default semicolon
DELIMITER ;
