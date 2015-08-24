import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object pca {
  def main(args: Array[String]){
    val logFile = "pca/*"
    val conf = new SparkConf().setAppName("Simple Application")
    val sc = new SparkContext(conf)
    val data = sc.textFile(logFile, 2).cache()
    val totalData = data.map(line => line.split(" ").map(z => z.toDouble))
    val gee = totalData.reduce((a,b) => Array(a(0)+b(0),a(1)+b(1),a(2)+b(2)))
    //    val numAs = logData.filter(l => l.contains("a")).count()
    //    val numBs = logData.filter(l => l.contains("b")).count()
    println("sum of x: %s,count: %s".format(gee(0),totalData.count()))
  }
}
