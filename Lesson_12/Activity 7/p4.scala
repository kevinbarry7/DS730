val taxi = spark.read.format("csv").option("header", true).option("inferSchema", true).load("/user/maria_dev/taxi.csv")

taxi.createOrReplaceTempView("taxiView")

spark.sqlContext.sql("SELECT trip_distance, cost FROM (SELECT trip_distance, (avg(fare_amount)/avg(trip_distance)) as cost FROM	taxiView WHERE trip_distance != 0 GROUP BY trip_distance) GROUP BY trip_distance, cost ORDER BY cost DESC LIMIT 10").show()