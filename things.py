from pyspark.sql import SparkSession
def le_pi():
    # Introduces memory errors on m1.large
    k = 1
    s = 0
    how_many = 100000
    for i in range(how_many):
        #if i % 100000000 == 0:
        #    print("{}/{} iterations".format(i, how_many))
        if i % 2 == 0:
            s += 4 / k
        else:
            s -= 4 / k
        k += 2
    print(s)

def big_file():
    #import boto3
    #s3 = boto3.resource('s3')
    #s3.download_file('franco-test-emr-data', 'FINAL_USO.csv', 'FINAL_USO.csv')
    big_text = ""
    size_in_mb = 1024
    with open('s3://franco-test-emr-data/FINAL_USO.csv') as file:
        for i in range(1, size_in_mb):
            big_text = big_text + file.read()
        with open('bigfile.csv') as bigfile:
            bigfile.write(big_text)


spark = SparkSession.builder \
    .master("local[*]") \
    .appName("spark_test") \
    .getOrCreate()
#big_file()
input_file = "bigfile.csv"
for i in range(1, 1000):
    df = spark.read.csv("s3://franco-test-emr-data/files/*.csv")
    print(df.count(), len(df.columns))
df = spark.read.csv(input_file)

# le_pi()