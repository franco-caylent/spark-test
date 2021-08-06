'''
Using a list of letters and words creates a dataframe with a schema
Then creates a new dataframe with the rows where letter is 'a' or 'r'
Saves the new dataframe to S3.
'''
import datetime
from pyspark.sql import SparkSession, functions
import socket


spark = SparkSession.builder.appName('test-paralel').getOrCreate()
sc = spark.sparkContext
data = [
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
]
schema = ["letter", "word"]
words = spark.createDataFrame(data=data, schema=schema)
results = words.select("word").where(((words.letter == 'a') | (words.letter == 'r')))
# Write to S3
S3_BUCKET = "franco-root"
# This will be the masters hostname
S3_KEY = "{hostname}".format(hostname=socket.gethostname())
results.write.mode("overwrite").csv('s3://{bucket}/{key}'.format(bucket=S3_BUCKET, key=S3_KEY))


print("{time} finished processing for node {hostname}".format(time=datetime.datetime.now(), hostname=socket.gethostname()))

# VERY important to stop SparkSession
# Otherwise, the job will keep running indefinitely
spark.stop()
