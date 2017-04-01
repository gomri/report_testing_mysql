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

test = """
    SELECT 
    entity_name, date_interval, SUM(imps), SUM(revenue)
FROM
    onetag.reports_daily_est
WHERE
    date_interval BETWEEN CURDATE() - 5 AND CURDATE() - 1
and entity_id = 102
GROUP BY date_interval , entity_name
"""