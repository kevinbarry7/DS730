DROP TABLE IF EXISTS fielding;
CREATE EXTERNAL TABLE IF NOT EXISTS fielding(id STRING, year INT,
team STRING, igid STRING, position STRING, G INT, GS INT, InnOuts
INT, PO INT, A INT, errors INT, DP INT, PB INT, WB
INT, SB INT, CS INT, ZR INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/hivetest/fielding';

SELECT
	id
FROM
	(
	SELECT
		id,
		sum_errors
	FROM
		(
		SELECT
			id,
			SUM(errors) as sum_errors
		FROM
			fielding
		GROUP BY
			id
		) sub
	ORDER BY
		sum_errors DESC
	) sub2
LIMIT 1