SELECT * 
FROM (
  SELECT
    'drivers' AS tabla,
    (SELECT COUNT(*) FROM staging.drivers) AS staging,
    (SELECT COUNT(*) FROM analytics.dim_drivers) AS analytics
  UNION ALL
  SELECT
    'constructors',
    (SELECT COUNT(*) FROM staging.constructors),
    (SELECT COUNT(*) FROM analytics.dim_constructors)
  UNION ALL
  SELECT 
    'circuits' AS tabla,
    (SELECT COUNT(*) FROM staging.circuits) AS staging,
    (SELECT COUNT(*) FROM analytics.dim_circuits) AS analytics
  UNION ALL
  SELECT
    'races' AS tabla,
    (SELECT COUNT(*) FROM staging.races) AS staging,
    (SELECT COUNT(*) FROM analytics.dim_races) AS analytics
  UNION ALL
  SELECT
    'results' AS tabla,
    (SELECT COUNT(*) FROM staging.results) AS staging,
    (SELECT COUNT(*) FROM analytics.fact_results) AS analytics
  ) AS checks 
WHERE staging <> analytics;

SELECT season, round, driver_id, points, position
FROM analytics.fact_results
WHERE points IS NULL OR position IS NULL;