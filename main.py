import boto3

# See https://stackoverflow.com/questions/36706512/how-do-you-automate-pyspark-jobs-on-emr-using-boto3-or-otherwise
client = boto3.client('emr', region_name='us-west-1')
S3_BUCKET = 'franco-root'
S3_KEY = 'things.py'
S3_URI = 's3://{bucket}/{key}'.format(bucket=S3_BUCKET, key=S3_KEY)

# upload file to an S3 bucket
print("Uploading file to s3")
s3 = boto3.resource('s3')
s3.meta.client.upload_file("things.py", S3_BUCKET, S3_KEY, ExtraArgs={'ServerSideEncryption': 'AES256',
                                                                      })

# List the EMR Clusters
response = client.list_clusters(ClusterStates=[
    'STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING'
])
print("The following are your clusters")
for position in range(0, len(response['Clusters'])):
    print("{}) {}  {}".format(position, response['Clusters'][position]['Id'], response['Clusters'][position]['Name']))
selected_cluster = input("Select what cluster to use using the number\n")
# JOBFLOWID is clusterid

# Add steps
print("Adding steps")
step_response = client.add_job_flow_steps(
    JobFlowId=response['Clusters'][int(selected_cluster)]['Id'], Steps=[
        {
            'Name': 'Copy Python Script',
            'ActionOnFailure': 'CANCEL_AND_WAIT',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['aws', 's3', 'cp', S3_URI, '/home/hadoop/']
            }
        },
        {
            'Name': 'Run Spark',
            'ActionOnFailure': 'CANCEL_AND_WAIT',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['spark-submit', '/home/hadoop/things.py']
            }
        }
    ])

step_ids = step_response['StepIds']

# print("Step IDs:", step_ids)
