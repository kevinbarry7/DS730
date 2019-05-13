DROP TABLE IF EXISTS batting;
CREATE EXTERNAL TABLE IF NOT EXISTS batting(id STRING, year INT,
team STRING, league STRING, games INT, ab INT, runs INT, hits
INT, doubles INT, triples INT, homeruns INT, rbi INT, sb INT, cs
INT, walks INT, strikeouts INT, ibb INT, hbp INT, sh INT, sf
INT, gidp INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/hivetest/batting';
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
		calc,
		rank() over(order by calc desc) as ranking
	FROM
		(
		SELECT
			f.id,
			round(((SUM(hits)/SUM(ab))-(SUM(errors)/SUM(G))),3) as calc
		FROM
			fielding f
		JOIN
			batting b
		ON
			f.id = b.id
		WHERE
			f.year >= 2005 AND 
			f.year <= 2009 AND
			b.year >= 2005 AND 
			b.year <= 2009 AND
			NOT (f.GS IS NULL AND
			f.InnOuts IS NULL AND
			f.PO IS NULL AND
			f.A IS NULL AND
			f.errors IS NULL AND
			f.DP IS NULL AND
			f.PB IS NULL AND
			f.WB IS NULL AND
			f.SB IS NULL AND
			f.CS IS NULL AND
			f.ZR IS NULL)
		GROUP BY
			f.id
		HAVING
			SUM(ab) >= 40 AND
			SUM(G) >= 20
			) sub
	ORDER BY
		calc DESC
	) sub2
WHERE
	ranking <= 3