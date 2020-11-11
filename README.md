## Getting started with RPA using AWS Step Functions and Amazon Textract

[AWS Step
Functions](https://aws.amazon.com/step-functions/) is a serverless function 
orchestrator and workflow automation tool. [Amazon Textract](https://aws.amazon.com/textract/) 
is a fully managed machine learning service that automatically extracts text 
and data from scanned documents. Combining these services, you can create an RPA bot 
to automate the processing of documents.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

## Prerequisites

Before you get started with deploying the solution, you must install the
following prerequisites:

1.  [Python](https://www.python.org/)

2.  [AWS Command Line Interface (AWS CLI)](https://aws.amazon.com/cli/)
    -- for instructions, see [Installing the AWS
    CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)

3.  [AWS Serverless Application Model Command Line Interface (AWS
    SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)
    -- for instructions, see [Installing the AWS SAM
    CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

## Deploying the solution

The solution will create the following three Amazon Simple Storage
Service (S3) buckets with names suffixed by your AWS Account ID to
prevent a global namespace collision of your S3 bucket names:

-   scanned-invoices-\<YOUR AWS ACCOUNT ID\>

-   invoice-analyses-\<YOUR AWS ACCOUNT ID\>

-   processed-invoices-\<YOUR AWS ACCOUNT ID\>

The below steps deploy the reference implementation in your AWS account.
The solution deploys several components including an AWS Step Functions
state machine, AWS Lambda functions, Amazon Simple Storage Service (S3)
buckets, an Amazon DynamoDB table for payment information, and AWS
Simple Notification Service (SNS) topics. You will need an Amazon S3
bucket to be used by AWS CloudFormation for deploying the solution. You
will also need a stack name, e.g., Getting-Started-with-RPA, for
deploying the solution. To deploy run the following commands from a
terminal session:

1.  Download code from GitHub repo
    (<https://github.com/aws-samples/aws-step-functions-rpa>).

2.  Run the following command to build the artifacts locally on your
    workstation:

        sam build

3.  Run the following command to create a CloudFormation stack and
    deploy your resources:
    
        sam deploy --guided --capabilities CAPABILITY_NAMED_IAM

Monitor the progress and wait for the completion of the stack creation
process from the [AWS CloudFormation
console](https://console.aws.amazon.com/cloudformation/home) before
proceeding.

## Testing the solution

To test the solution, upload the .PDF test invoices from the invoices
folder of the downloaded solution to the S3 bucket named
scanned-invoices-\<Your AWS Account ID\> created during deployment.

An AWS Step Functions state machine with the name \<YOUR STACK
NAME\>-ProcessedScannedInvoiceWorkflow will execute the workflow. Amazon
Textract document analyses will be stored in the S3 bucket named
invoice-analyses-\<YOUR AWS ACCOUNT ID\>, and processed invoices will be
stored in the S3 bucket named processed-invoices-\<YOUR AWS ACCOUNT
ID\>. Processed payments will be found in the DynamoDB table named
\<YOUR STACK NAME\>-invoices.

You can monitor the execution status of the workflows from the [AWS Step
Functions console](https://console.aws.amazon.com/states/home).

Upon completion of the workflow executions, review the items added to
DynamoDB from the [Amazon DynamoDB
console](https://console.aws.amazon.com/dynamodb/home).

## Cleanup

To avoid ongoing charges for resources you created,
follow the below steps which will delete the stack of resources
deployed:

1.  Empty the three S3 buckets created during deployment using the
    [Amazon S3 Console](https://s3.console.aws.amazon.com/s3/home):
    
    - scanned-invoices-\<YOUR AWS ACCOUNT ID\>
    - invoice-analyses-\<YOUR AWS ACCOUNT ID\>
    - processed-invoices-\<YOUR AWS ACCOUNT ID\>

2.  Delete the CloudFormation stack created during deployment using the
    [AWS CloudFormation
    console](https://console.aws.amazon.com/cloudformation/home).
