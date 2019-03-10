val taxi = spark.read.format("csv").option("header", true).option("inferSchema", true).load("/user/maria_dev/taxi.csv")

taxi.createOrReplaceTempView("taxiView")

spark.sqlContext.sql("SELECT CASE WHEN fare_amount >= 0 AND fare_amount <= 24.99 THEN '$0 - $24.99'	WHEN fare_amount >= 25 AND fare_amount <= 49.99 THEN '$25 - $49.99' WHEN fare_amount >= 50 AND fare_amount <= 74.99 THEN '$50 - $74.99' ELSE '$75+' END AS fare_group, (avg(tip_amount) / avg(fare_amount)) AS avg_tips FROM taxiView GROUP BY CASE WHEN fare_amount >= 0 AND fare_amount <= 24.99 THEN '$0 - $24.99'	WHEN fare_amount >= 25 AND fare_amount <= 49.99 THEN '$25 - $49.99' WHEN fare_amount >= 50 AND fare_amount <= 74.99 THEN '$50 - $74.99' ELSE '$75+' END").show()