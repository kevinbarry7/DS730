import org.apache.spark.sql.expressions.Window;

// ------------ Setup ------------

val data = spark.read.format("csv").option("header", "true").option("inferSchema", true).load("s3a://ebfp3/flight_data/*.csv");

val carriers = spark.read.format("csv").option("header", "true").option("inferSchema", true).load("s3a://ebfp3/supp_data/carriers.csv");

val airports = spark.read.format("csv").option("header", "true").option("inferSchema", true).load("s3a://ebfp3/supp_data/airports.csv");

data.write.parquet("data_p");
carriers.write.parquet("carriers_p");
airports.write.parquet("airports_p");

val df_p = spark.read.option("header","true").option("inferSchema", true).parquet("data_p");
val df_carriers = spark.read.option("header","true").option("inferSchema", true).parquet("carriers_p");
val df_airports = spark.read.option("header","true").option("inferSchema", true).parquet("airports_p");

df_p.createOrReplaceTempView("ap");
df_carriers.createOrReplaceTempView("ap_carriers");
df_airports.createOrReplaceTempView("ap_airports");

// ------------ Question 1 ------------

val view_data = spark.sqlContext.sql("SELECT Year, UniqueCarrier, sum(cast(DepDelay as INT)) as sum_dep_delay FROM ap GROUP BY Year, UniqueCarrier");

val view_carriers = spark.sqlContext.sql("SELECT Code, Description FROM ap_carriers");

val joined_data = view_data.join(view_carriers, view_data.col("UniqueCarrier") === view_carriers.col("Code")).drop("Code");

val window = Window.partitionBy("year").orderBy($"sum_dep_delay".desc);
val ranked_data = joined_data.withColumn("delay_rank", rank over window).where($"delay_rank" === 1).orderBy($"year").drop("delay_rank");

val final_output = ranked_data.groupBy($"Description").agg(count($"Description").alias("Count")).sort($"Count".desc);

// ------------ Question 2 ------------

val view_data = spark.sqlContext.sql("SELECT Year, Month, UniqueCarrier, sum(cast(Distance as INT)) as sum_distance FROM ap GROUP BY Year, Month, UniqueCarrier");

val view_carriers = spark.sqlContext.sql("SELECT Code, Description FROM ap_carriers");

val joined_data = view_data.join(view_carriers, view_data.col("UniqueCarrier") === view_carriers.col("Code")).drop("Code");

val window = Window.partitionBy("year");
val data_with_avg = joined_data.withColumn("yearly_avg", avg($"sum_distance") over window).withColumn("percent_diff", round(($"sum_distance" - $"yearly_avg") / $"yearly_avg", 4)).drop($"yearly_avg");

val window2 = Window.partitionBy("year").orderBy("percent_diff");
val ranked_data = data_with_avg.withColumn("ranking", rank over window2).where($"ranking" === 1).drop("UniqueCarrier").drop("sum_distance").drop("ranking").sort($"Year");

// ------------ Question 3 ------------

val view_data = spark.sqlContext.sql("SELECT Origin, Month, sum(cast(CarrierDelay as INT)+ cast(WeatherDelay as INT) + cast(NASDelay as INT) + cast(SecurityDelay as INT) + cast(LateAircraftDelay as INT)) as sum_delays FROM ap WHERE Month != 11 and Month != 12 GROUP BY Origin, Month");

val view_airports = spark.sqlContext.sql("SELECT iata, airport, city FROM ap_airports");

val joined_data = view_data.join(view_airports, view_data.col("Origin") === view_airports.col("iata")).drop("Origin","iata").filter("sum_delays is not null");

val window = Window.partitionBy("airport").orderBy($"sum_delays".desc);
val ranked_data = joined_data.withColumn("ranking", rank over window).where($"ranking" === 1).sort($"sum_delays".desc).drop("ranking").select("airport","city","Month","sum_delays");


// ------------ Question 4 ------------

val view_data = spark.sqlContext.sql("SELECT UniqueCarrier as Carrier, Origin, Dest, count(*) as count_flights FROM ap GROUP BY UniqueCarrier, Origin, Dest");

val view_carriers = spark.sqlContext.sql("SELECT Code, Description as Airline FROM ap_carriers");

val joined_data = view_data.join(view_carriers, view_data.col("Carrier") === view_carriers.col("Code")).drop("Code","Carrier");

val window = Window.partitionBy("Airline").orderBy($"count_flights".desc);
val ranked_data = joined_data.withColumn("ranking", rank over window).where($"ranking" === 1).sort($"count_flights".desc).drop("ranking").select("Airline","Origin","Dest","Count_flights");


