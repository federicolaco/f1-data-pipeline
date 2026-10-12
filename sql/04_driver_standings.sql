SELECT
  dim_drivers.driver_id,
  dim_drivers.given_name,
  dim_drivers.family_name,
  SUM(fact_results.points) AS total_points
FROM analytics.fact_results
JOIN analytics.dim_drivers
  ON fact_results.driver_id = dim_drivers.driver_id
GROUP BY dim_drivers.driver_id
ORDER BY total_points DESC;