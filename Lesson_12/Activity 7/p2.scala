import scala.util.matching.Regex;
​val wapFile = sc.textFile("/user/zeppelin/wap.txt");
val flattenMap = wapFile.flatMap(line => line.split("\\s+"));
val pattern = new Regex("a|e|i|o|u");
def matchVowels(word: String) : String = {
	var vowels: String = "";
	val matches = pattern.findAllIn(word);
	if(!matches.isEmpty) matches.foreach {vowels += _};
	return vowels;
};
val mapreduce = flattenMap.map(word => (matchVowels(word), 1)).reduceByKey((a,b) => a+b);
val max_val = mapreduce.max()(Ordering[Int].on(x=>x._2));
println(max_val);