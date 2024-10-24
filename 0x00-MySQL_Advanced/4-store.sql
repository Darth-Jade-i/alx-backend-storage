-- File: 4-store.sql
-- Task: Create a trigger that decreases the quantity of an item after a new order is added.

-- Ensure the trigger does not already exist
DROP TRIGGER IF EXISTS decrease_quantity_after_order;

-- Set the delimiter to // to allow multiple SQL statements within the trigger
DELIMITER //

-- Create a trigger that is executed after a new row is inserted into the 'orders' table.
CREATE TRIGGER decrease_quantity_after_order
AFTER INSERT ON orders -- Specify that this trigger runs after a row is inserted into the 'orders' table.
FOR EACH ROW -- The trigger will execute for each row that is inserted into the 'orders' table.
BEGIN
    -- Update the 'items' table by decreasing the quantity of the ordered item.
    
    -- Perform an update operation on the 'items' table.
    UPDATE items
    -- Set the new quantity to be the current quantity minus the number of items ordered.
    SET quantity = quantity - NEW.number -- On each row insert in the 'orders' table, decrease the quantity of the item by the number of items ordered.
    -- Apply this update only to the row where the item name matches the one in the new order.
    WHERE name = NEW.item_name; -- Update the item where the name matches the item name in the new order.
END;
//

-- Reset the delimiter back to the default semicolon (;)
DELIMITER ;
