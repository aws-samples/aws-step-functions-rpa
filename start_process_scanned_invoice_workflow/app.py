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

client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print("Processing Event:")
    print(json.dumps(event))
    body = json.loads(event["Records"][0]["body"])
    message = json.loads(body["Message"])
    document_location = message["DocumentLocation"]
    bucket_name = document_location["S3Bucket"]
    key = document_location["S3ObjectName"]
    key_split_on_slash = key.split("/")
    join_with_dash = "-".join(key_split_on_slash)
    join_split_on_colon = join_with_dash.split(":")
    job_name = "_".join(join_split_on_colon)
    job_id = message["JobId"]
    status = message["Status"]
    response = client.start_execution(
        stateMachineArn = os.environ['STATE_MACHINE_ARN'],
        input="{\"bucket_name\": \"" + bucket_name + 
            "\",\"key\": \"" + key + 
            "\",\"job_name\": \"" + job_name +
            "\",\"job_id\": \"" + job_id + 
            "\",\"status\": \"" + status + "\"}"
    )
    return response["executionArn"]
