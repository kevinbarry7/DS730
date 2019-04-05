%spark
import sqlContext.implicits._
import org.apache.spark.sql.expressions.Window

// Load data
val oshkosh_weather = spark.read.format("csv").option("header", true).option("inferSchema", true).load("/user/maria_dev/final/Oshkosh/OshkoshWeather.csv")
val iowacity_weather = spark.read.format("csv").option("header", true).option("inferSchema", true).load("/user/maria_dev/final/IowaCity/IowaCityWeather.csv")

iowacity_weather.createOrReplaceTempView("iow")
oshkosh_weather.createOrReplaceTempView("okw")

// Pull various columns. Create timestamp from dates.
val ok_view = spark.sqlContext.sql("SELECT month, CONCAT(split(TimeCST, ':')[0], split(TimeCST, ' ')[1]) as hour, 'Oshkosh' as city, abs(avg(TemperatureF)-50) as temp_diff, avg(`Wind SpeedMPH`) as avg_wind FROM okw WHERE TemperatureF IS NOT NULL AND TemperatureF != -9999 AND `Wind SpeedMPH` IS NOT NULL AND `Wind SpeedMPH` != -9999 AND `Wind SpeedMPH` != 'Calm' GROUP BY month, CONCAT(split(TimeCST, ':')[0], split(TimeCST, ' ')[1]), 'Oshkosh'")

val io_view = spark.sqlContext.sql("SELECT month, CONCAT(split(TimeCST, ':')[0], split(TimeCST, ' ')[1]) as hour, 'IowaCity' as city, abs(avg(TemperatureF)-50) as temp_diff, avg(`Wind SpeedMPH`) as avg_wind FROM iow WHERE TemperatureF IS NOT NULL AND TemperatureF != -9999 AND `Wind SpeedMPH` IS NOT NULL AND `Wind SpeedMPH` != -9999 AND `Wind SpeedMPH` != 'Calm' GROUP BY month, CONCAT(split(TimeCST, ':')[0], split(TimeCST, ' ')[1]), 'IowaCity'")

val unioned_data = ok_view.union(io_view)
unioned_data.createOrReplaceTempView("combined")

val combined_view = spark.sqlContext.sql("SELECT month, hour, city, round(temp_diff, 2) as temp_diff, round(avg_wind,2) as avg_wind FROM combined")

// Setup window for window function
val window_temp = Window.partitionBy("month").orderBy("temp_diff")
val ranked_data = combined_view.withColumn("temp_rank", rank over window_temp)

val window_wind = Window.partitionBy("month").orderBy("avg_wind")
val filtered_data = ranked_data.where($"temp_rank" === 1).withColumn("wind_rank", rank over window_wind).orderBy($"month").drop("temp_diff").drop("avg_wind").drop("temp_rank").drop("wind_rank").show()