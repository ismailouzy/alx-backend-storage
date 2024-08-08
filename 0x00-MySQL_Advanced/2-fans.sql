-- Script to rank country origins of bands by the number of fans

-- Selecting the origin and the sum of the number of fans
-- Grouping by origin and ordering by the number of fans in descending order
SELECT origin, SUM(fans) as nb_fans FROM metal_bands
GROUP BY origin ORDER BY nb_fans DESC;
