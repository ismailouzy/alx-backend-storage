-- Script to list Glam Rock bands ranked by their longevity
-- Selecting band name and calculating lifespan based on 'formed' and 'split'
-- We assume bands that haven't split yet will be considered as active in 2022


SELECT
    band_name,
    CASE
        WHEN split IS NULL THEN 2022 - formed
        ELSE split - formed
    END AS lifespan
FROM
    metal_bands
WHERE
    main_style = 'Glam Rock'
ORDER BY
    lifespan DESC;
