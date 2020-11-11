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
import copy
import json
import os

texttract_client = boto3.client('textract')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print("Processing Event:")
    print(json.dumps(event))
    blocks = []
    analysis = {}
    response = texttract_client.get_document_analysis(
        JobId=event["job_id"]
    )
    analysis = copy.deepcopy(response)
    while True:
        for block in response["Blocks"]:
            blocks.append(block)
        if ("NextToken" not in response.keys()):
            break
        next_token = response["NextToken"]
        response = texttract_client.get_document_analysis(
            JobId=event["job_id"],
            NextToken=next_token
        )
    analysis.pop("NextToken", None)
    analysis["Blocks"] = blocks
    invoice_analyses_bucket_name = os.environ["ANALYSES_BUCKET_NAME"]
    invoice_analyses_bucket_key = "{}.json".format(event["key"])
    s3_client.put_object(
        Bucket=invoice_analyses_bucket_name,  
        Key=invoice_analyses_bucket_key,
        Body=json.dumps(analysis).encode('utf-8')
    )
    event["invoice_analyses_bucket_name"] = invoice_analyses_bucket_name
    event["invoice_analyses_bucket_key"] = invoice_analyses_bucket_key
    return event
