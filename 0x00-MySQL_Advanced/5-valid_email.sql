-- This SQL script creates a trigger that resets the valid_email attribute
-- to 0 whenever the email of a user is updated.

-- Ensure the trigger does not already exist
DROP TRIGGER IF EXISTS reset_valid_email;

-- Set the delimiter to $$ to allow multiple SQL statements within the trigger
DELIMITER $$

-- Create a trigger that resets the valid_email attribute when the email is updated
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users -- Specify that this trigger runs before a row is updated in the 'users' table.
FOR EACH ROW -- The trigger will execute for each row that is updated in the 'users' table.
BEGIN
    -- Check if the email is being updated
    
    -- Compare the new email with the old email to see if it has been changed.
    IF NEW.email != OLD.email THEN
        -- Reset the valid_email attribute to 0
        SET NEW.valid_email = 0; -- If the email has changed, set the valid_email attribute to 0 for the updated row.
    END IF; -- End of the IF statement.
END $$ -- End of the trigger's logic.

-- Reset the delimiter back to the default semicolon (;)
DELIMITER ;
