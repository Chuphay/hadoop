import org.apache.SparkContext
import org.apache.sparkContext._
import org.apache.spark.SparkConf

object SimpleApp {
  def main(args: Array[String]){
    val logFile = "dave/*"
    val conf = new SparkConf().setAppName("Simple Application")
    val sc = new SparkContext(conf)
    val logData = sc.textFile(logFile, 2).cache()
    val numAs = logData.filter(l => l.contains("a")).count()
    val numBs = logData.filter(l => l.contains("b")).count()
println("Lines with a: %s, Lines with b: %s".format(numAs,numBs))
  }
}
