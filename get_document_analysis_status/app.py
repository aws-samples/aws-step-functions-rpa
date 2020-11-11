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

textract_client = boto3.client('textract')
stepfunctions_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print("Processing Event:")
    print(json.dumps(event))
    body = event["Records"][0]["body"]
    bodyAsJson = json.loads(body)
    inputAsJson = bodyAsJson["Input"] 
    job_id = inputAsJson["JobId"]
    task_token = bodyAsJson["TaskToken"]

    response = textract_client.get_document_analysis(
        JobId=job_id
    )

    job_status = response["JobStatus"]
    inputAsJson["JobStatus"]=job_status 

    if job_status in ["SUCCEEDED"]:
        stepfunctions_client.send_task_success(
            taskToken=task_token,
            output=json.dumps(inputAsJson)
        )
    elif job_status == ["FAILED","PARTIAL_SUCCESS"]:
        stepfunctions_client.send_task_failure(
            taskToken=task_token
        )
    else:
        raise Exception("Document Analysis in progress")
    return inputAsJson