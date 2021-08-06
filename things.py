'''
from pyspark.ml.regression import LinearRegression

# Load training data
from pyspark.shell import spark

#training = spark.read.format("csv")\
#    .load("s3://franco-root/FINAL_USO.csv")
training = spark.read.format("libsvm")\
    .load("s3://franco-root/sample_data.txt")
lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(training)

# Print the coefficients and intercept for linear regression
print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))

# Summarize the model over the training set and print out some metrics
trainingSummary = lrModel.summary
print("numIterations: %d" % trainingSummary.totalIterations)
print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
trainingSummary.residuals.show()
print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
print("r2: %f" % trainingSummary.r2)

# More iterations

lr = LinearRegression(maxIter=1000000, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(training)

# Print the coefficients and intercept for linear regression
print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))

# Summarize the model over the training set and print out some metrics
trainingSummary = lrModel.summary
print("numIterations: %d" % trainingSummary.totalIterations)
print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
trainingSummary.residuals.show()
print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
print("r2: %f" % trainingSummary.r2)

'''
import datetime
from pyspark.sql import SparkSession, dataframe
import socket
import boto3


def big_list(number):
    # not used for now
    import random
    import string
    le_big_list = []
    for le_num in range(0, number):
        le_big_list.append((le_num, random.choice(string.ascii_letters)))
    return le_big_list

spark = SparkSession.builder.appName('test-paralel').getOrCreate()
sc = spark.sparkContext
rdd = sc.parallelize(big_list(1000))
words = sc.parallelize([
    ('a', 'abracadabra'),
    ('b', 'ball'),
    ('c', 'cousin'),
    ('d', 'data'),
    ('e', 'ernest'),
    ('f', 'failure'),
    ('g', 'grill'),
    ('h', 'hills'),
    ('i', 'inventor'),
    ('j', 'jay'),
    ('k', 'kale'),
    ('l', 'lumberjack'),
    ('m', 'minas tirith'),
    ('n', 'name'),
    ('o', 'orthopedic'),
    ('p', 'poland'),
    ('q', 'quebec'),
    ('r', 'raisin'),
    ('s', 'stain'),
    ('t', 'trouble'),
    ('u', 'university'),
    ('v', 'violon'),
    ('w', 'wazausky'),
    ('x', 'xavier'),
    ('y', 'yall'),
    ('z', 'zebra')
])
# rddCollect = rdd.collect()
dataframe = words.toDF()
S3_BUCKET = "franco-root"
# This will be the masters hostname
S3_KEY = "{hostname}".format(hostname=socket.gethostname())
dataframe.append(('hostname', "{hostname}".format(hostname=socket.gethostname())))
dataframe.write.mode("overwrite").csv('s3://{bucket}/{key}'.format(bucket=S3_BUCKET, key=S3_KEY))


print("{time} finished processing for node {hostname}".format(time=datetime.datetime.now(), hostname=socket.gethostname()))

# VERY important to stop SparkSession
# Otherwise, the job will keep running indefinitely
spark.stop()
