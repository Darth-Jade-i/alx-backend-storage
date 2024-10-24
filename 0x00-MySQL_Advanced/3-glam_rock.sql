-- File: 3-glam_rock.sql
-- Task: List all bands with Glam rock as their main style, ranked by their longevity (lifespan).

-- Select band names and calculate lifespan, filtering by Glam rock and ordering by lifespan in descending order.
SELECT 
    band_name,
    -- (IFNULL(split, '2022') - formed) AS `lifespan`
    CASE
        WHEN split IS NULL THEN (2022 - formed)
        ELSE (split - formed)
    END AS `lifespan`
FROM 
    metal_bands
WHERE 
    style LIKE '%Glam rock%'
ORDER BY 
    `lifespan` DESC;
