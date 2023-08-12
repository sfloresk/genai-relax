import logging
import json
import boto3
import os
import string
import random 
from datetime import datetime 
from boto3.dynamodb.conditions import Key

sts_connection = boto3.client('sts')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
role_arn = os.getenv('ROLE_ARN')
dynamodb = boto3.resource('dynamodb','us-east-1')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))

bedrock_credentials = sts_connection.assume_role(
    RoleArn=role_arn,
    RoleSessionName=f"lambda-generate-image-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
)
bedrock = boto3.client("bedrock", 'us-east-1',
    aws_access_key_id=bedrock_credentials['Credentials']['AccessKeyId'],
    aws_secret_access_key=bedrock_credentials['Credentials']['SecretAccessKey'],
    aws_session_token=bedrock_credentials['Credentials']['SessionToken'])

def handler(event, context):
    global bedrock_credentials
    global bedrock
    logger.info(f"event: {event}")
    logger.info(f"context: {context}")
    
    request_json = json.loads(event['body'])
    
    # Reassume the role only if it after expiration
    if datetime.now().timestamp() >= bedrock_credentials['Credentials']['Expiration'].timestamp():
        bedrock_credentials = sts_connection.assume_role(
        RoleArn=role_arn,
        RoleSessionName=f"lambda-generate-image-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}")
        
        bedrock = boto3.client("bedrock", 'us-east-1',
        aws_access_key_id=bedrock_credentials['Credentials']['AccessKeyId'],
        aws_secret_access_key=bedrock_credentials['Credentials']['SecretAccessKey'],
        aws_session_token=bedrock_credentials['Credentials']['SessionToken'])
    
    # Get description from dynamodb
    logger.info(f"Getting description for uuid: {request_json['message_id']}")
    description = table.query(KeyConditionExpression=Key('id').eq(request_json['message_id']))['Items'][0]['description']
    
    logger.info(f"message: {description}")
    
    
    bedrock_body={'text_prompts': [{'text': description}], 'cfg_scale': 10, 'seed': 0, 'steps': 50}
    bedrock_response = bedrock.invoke_model(body=json.dumps(bedrock_body), modelId='stability.stable-diffusion-xl', accept='application/json',contentType="application/json")
    response_body = json.loads(bedrock_response.get('body').read())
    if response_body['result'] == 'success':
        image_b64 = response_body['artifacts'][0]['base64']
        logger.info(f"message result: {response_body['result']}")
        response = {'statusCode': 200,
                    "body": json.dumps({
                        'image_b64':image_b64, 
                        'description':description
                        })
                    }
    else:
        response = {'statusCode': 500 }
    return response