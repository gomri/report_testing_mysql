max_time_stamp = """
   SELECT 
     MAX(id),
     MAX(Date_interval)
   FROM
     onetag.reports
  """

min_time_stamp = """
   SELECT 
     MAX(id),
     MIN(Date_interval)
   FROM
     onetag.reports
  """

query_serving_24_hours = """
SELECT 
    HOUR(date_interval), SUM(imps)
FROM
    reports
WHERE
    date_interval BETWEEN '{0}' AND '{1}'
GROUP BY 1
"""

query_imps_rev_last_days_5 = """
    SELECT 
    entity_name, date_interval, SUM(imps), SUM(revenue)
FROM
    onetag.reports_daily_est
WHERE
    date_interval BETWEEN '{0}' AND '{1}'
AND entity_name = '{2}'
GROUP BY date_interval , entity_name
"""

entity_names = [
    "OpenX",
    "Admeta PWF",
    "Adx",
    "AOL-America"
]
