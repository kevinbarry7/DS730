%spark
import sqlContext.implicits._
import org.apache.spark.sql.expressions.Window

// Oshkosh

// Load data
val oshkosh_weather = spark.read.format("csv").option("header", true).option("inferSchema", true).load("/user/maria_dev/final/Oshkosh/OshkoshWeather.csv")
oshkosh_weather.createOrReplaceTempView("okw")

// Pull various columns. Create timestamp from dates.
val updated_view = spark.sqlContext.sql("SELECT to_timestamp(CONCAT(Year,'-',Month,'-',Day,' ',TimeCST), 'yyyy-MM-dd h:m a') as from_dt, to_timestamp(CONCAT(Year,'-',Month,'-',Day,' ',TimeCST), 'yyyy-MM-dd h:m a') + INTERVAL 24 HOURS as to_dt, CAST(to_timestamp(CONCAT(Year,'-',Month,'-',Day,' ',TimeCST), 'yyyy-MM-dd h:m a') AS Long) dt_long, TemperatureF as temp FROM okw WHERE TemperatureF != -9999")

// Setup window for window function
val window = Window.orderBy("dt_long").rangeBetween(0, 86400)

// Run query that takes max-min difference of 24 hour window for every row (time)
val temp_diff_view = updated_view.withColumn("dt_long", $"dt_long").withColumn("temp_diff", max($"temp").over(window)-min($"temp").over(window)).drop("dt_long").drop("temp")

// Rank temp differences
val rank_window = Window.orderBy('temp_diff.desc)
val ranked_output = temp_diff_view.withColumn("rank", rank over rank_window)

// Produce final answer
val final_output = ranked_output.filter($"rank" === 1).drop("rank").show(1)

// IowaCity

// Load data
val iowacity_weather = spark.read.format("csv").option("header", true).option("inferSchema", true).load("/user/maria_dev/final/IowaCity/IowaCityWeather.csv")
iowacity_weather.createOrReplaceTempView("iow")

// Pull various columns. Create timestamp from dates.
val updated_view_io = spark.sqlContext.sql("SELECT to_timestamp(CONCAT(Year,'-',Month,'-',Day,' ',TimeCST), 'yyyy-MM-dd h:m a') as from_dt, to_timestamp(CONCAT(Year,'-',Month,'-',Day,' ',TimeCST), 'yyyy-MM-dd h:m a') + INTERVAL 24 HOURS as to_dt, CAST(to_timestamp(CONCAT(Year,'-',Month,'-',Day,' ',TimeCST), 'yyyy-MM-dd h:m a') AS Long) dt_long, TemperatureF as temp FROM iow WHERE TemperatureF != -9999")

// Setup window for window function
val window_io = Window.orderBy("dt_long").rangeBetween(0, 86400)

// Run query that takes max-min difference of 24 hour window for every row (time)
val temp_diff_view_io = updated_view_io.withColumn("dt_long", $"dt_long").withColumn("temp_diff", max($"temp").over(window_io)-min($"temp").over(window_io)).drop("dt_long").drop("temp")

// Rank temp differences
val rank_window_io = Window.orderBy('temp_diff.desc)
val ranked_output_io = temp_diff_view_io.withColumn("rank", rank over rank_window_io)

// Produce final answer
val final_output_io = ranked_output_io.filter($"rank" === 1).drop("rank").show(1)