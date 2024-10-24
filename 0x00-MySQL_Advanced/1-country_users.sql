-- File: 1-country_users.sql
-- Task: Create a 'users' table with specific constraints including an enumeration for the country.

-- Check if the 'users' table exists; if it doesn't, create it.
CREATE TABLE IF NOT EXISTS users (
    -- 'id' is an integer, auto-incremented, never null, and serves as the primary key.
    id INT NOT NULL AUTO_INCREMENT,

    -- 'email' is a string with a maximum of 255 characters, never null, and must be unique.
    email VARCHAR(255) NOT NULL UNIQUE,

    -- 'name' is a string with a maximum of 255 characters.
    name VARCHAR(255),

    -- 'country' is an enumeration with possible values 'US', 'CO', 'TN', never null, defaulting to 'US'.
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US',

    -- Set 'id' as the primary key for the table.
    PRIMARY KEY (id)
);
