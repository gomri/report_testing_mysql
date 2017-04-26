testing = """
SELECT 
    entity_name, date_interval, SUM(imps) imps, SUM(revenue) rev
FROM
    onetag.reports_daily_est
WHERE
    date_interval BETWEEN '2017-03-28' AND '2017-03-31'
and entity_name = 'AOL-america'
GROUP BY date_interval , entity_name
"""

query_serving_24_hours ="""
SELECT 
    HOUR(date_interval), SUM(imps)
FROM
    reports
WHERE
    date_interval BETWEEN '{0}' AND '{1}'
GROUP BY 1
"""
# date format = '2017-04-15'

query_imps_rev_last_days_5 ="""
SELECT 
    entity_id, date_interval, SUM(imps), SUM(revenue)
FROM
    onetag.reports_daily_est
WHERE
    date_interval BETWEEN '{0}' AND '{1}'
AND entity_id in {2}
GROUP BY date_interval , entity_name
"""
# date format = '2017-04-15'


query_rtb_imps_rev_last_days_5 ="""
SELECT 
    DAY(date_interval), SUM(imps), SUM(revenue)
FROM
    reports
WHERE
    date_interval BETWEEN {start_date} AND {end_date}
        AND entity_id > 200
        AND entity_id <= 300
GROUP BY 1
"""
# date format = '2017-04-15 00:00:00'

#has to stay tuple in order for the query to work
entity_ids = (11, 101, 102, 105, 109, 110, 120, 125, 117, 7)


min_delta = 0.3

