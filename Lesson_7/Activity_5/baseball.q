DROP TABLE IF EXISTS batting;
CREATE EXTERNAL TABLE IF NOT EXISTS batting(id STRING, year INT,
team STRING, league STRING, games INT, ab INT, runs INT, hits
INT, doubles INT, triples INT, homeruns INT, rbi INT, sb INT, cs
INT, walks INT, strikeouts INT, ibb INT, hbp INT, sh INT, sf
INT, gidp INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 's3://aws-hivescripts-eb/batters';
DROP TABLE IF EXISTS master;
CREATE EXTERNAL TABLE IF NOT EXISTS master(id STRING, byear INT,
bmonth INT, bday INT, bcountry STRING, bstate STRING, bcity
STRING, dyear INT, dmonth INT, dday INT, dcountry STRING, dstate
STRING, dcity STRING, fname STRING, lname STRING, name STRING,
weight INT, height INT, bats STRING, throws STRING, debut
STRING, finalgame STRING, retro STRING, bbref STRING) ROW FORMAT
DELIMITED FIELDS TERMINATED BY ',' LOCATION
's3://aws-hivescripts-eb/master';
INSERT OVERWRITE DIRECTORY 's3://aws-hivescripts-eb/output/' SELECT
n.fname, n.lname, x.year, x.runs FROM master n JOIN (SELECT b.id
as id, b.year as year, b.runs as runs FROM batting b JOIN
(SELECT year, max(runs) AS best FROM batting GROUP BY year) o
WHERE b.runs=o.best AND b.year=o.year) x ON x.id=n.id ORDER BY
x.runs DESC;