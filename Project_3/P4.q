DROP TABLE IF EXISTS fielding;
CREATE EXTERNAL TABLE IF NOT EXISTS fielding(id STRING, year INT,
team STRING, igid STRING, position STRING, G INT, GS INT, InnOuts
INT, PO INT, A INT, errors INT, DP INT, PB INT, WB
INT, SB INT, CS INT, ZR INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/hivetest/fielding';

SELECT
	team
FROM
	(
	SELECT
		team,
		count_errors,
		rank() over(order by count_errors desc) as ranking
	FROM
		(
		SELECT
			team,
			SUM(errors) count_errors
		FROM
			fielding
		WHERE
			year = 2001
		GROUP BY
			team
		) sub
	ORDER BY
		count_errors DESC
	) sub2
WHERE
	ranking = 1