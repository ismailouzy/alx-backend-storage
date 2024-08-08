-- Script to list Glam Rock bands ranked by their longevity
-- Selecting band name and calculating lifespan based on 'formed' and 'split'
-- We assume bands that haven't split yet will be considered as active in 2022

SELECT band_name, COALESCE(split, 2022) - formed as lifespan FROM metal_bands
WHERE style LIKE '%Glam rock%' ORDER BY lifespan DESC;
