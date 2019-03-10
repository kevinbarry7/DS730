import java.io.PrintWriter;
​val wapFile = sc.textFile("/user/zeppelin/wap.txt");
val flattenMap = wapFile.flatMap(line => line.split("\\s+"));
val mapreduce = flattenMap.map(word => (word, 1)).reduceByKey((a,b) => a+b);
val result = mapreduce.filter{case (key, value) => value >= 5 && value <= 7};
result foreach {case (key, value) => println (key)};