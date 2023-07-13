-- lists all bands with Gam rock main style, ranked by longevity
SELECT band_name, ifnull(split, 2022)-ifnull(formed, 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
