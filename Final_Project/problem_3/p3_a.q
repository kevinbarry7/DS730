DROP TABLE IF EXISTS ccd;
CREATE EXTERNAL TABLE ccd (level STRING, projected_hour FLOAT, x INT, y INT, value FLOAT)
PARTITIONED BY (category STRING, area STRING, element STRING, reference_year INT, reference_month INT, reference_day INT, reference_hour INT, reference_minute INT)
LOCATION 's3a://cornell-eas-data-lake/v1/ncep/ndfd-ndgd/';

SELECT
	concat(reference_year, reference_month),
	avg(temp)
FROM
	ndfd_ndgd
WHERE
	reference_month == 6 OR reference_month == 12 and reference_day == 21 AND reference_year >= 2019 and
	element = 'temp' and
	area = 'conus'
GROUP BY
	concat(reference_year, reference_month)