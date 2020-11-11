# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import boto3
import json
import os

client = boto3.client('textract')

def lambda_handler(event, context):
    print("Processing Event:")
    print(json.dumps(event))
    s3 = event["Records"][0]["s3"]
    bucket_name = s3["bucket"]["name"]
    key = s3["object"]["key"]
    document_location={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': key
        }
    }
    response = client.start_document_analysis(
        DocumentLocation=document_location,
        FeatureTypes=[
            'TABLES','FORMS'
        ],
        NotificationChannel={
            'SNSTopicArn': os.environ["DOCUMENT_ANALYIS_COMPLETED_SNS_TOPIC_ARN"],
            'RoleArn': os.environ["TEXTRACT_PUBLISH_TO_SNS_ROLE_ARN"]
        }
    )
    event["job_id"]=response["JobId"] 
    return event
