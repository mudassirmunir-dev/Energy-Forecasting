-- Name: Mudassir Munir
-- Roll No: PSEB-2026-010784
-- Date: 2026-11-18

-- Average electricity consumption by building usage category.

SELECT
    m.primaryspaceusage AS building_usage,
    COUNT(*) AS building_count,
    ROUND(AVG(e.average_consumption), 2) AS average_consumption,
    ROUND(SUM(e.total_consumption), 2) AS total_consumption
FROM building_energy_summary AS e
INNER JOIN building_metadata AS m
    ON e.building_id = m.building_id
WHERE m.primaryspaceusage IS NOT NULL
GROUP BY m.primaryspaceusage
ORDER BY average_consumption DESC;
