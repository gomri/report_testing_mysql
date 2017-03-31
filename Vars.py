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
	    COUNT(*), MAX(date_interval), SUM(revenue)
	FROM
	    reports_daily_est
	WHERE
	    Actual_Date = CURDATE()
"""