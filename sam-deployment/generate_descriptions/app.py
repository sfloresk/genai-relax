import logging
import json
import boto3
import os
import string
import random 
from datetime import datetime 
import uuid 
import math 
sts_connection = boto3.client('sts')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
role_arn = os.getenv('ROLE_ARN')

bedrock_credentials = sts_connection.assume_role(
    RoleArn=role_arn,
    RoleSessionName=f"lambda-generate-image-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
)

bedrock = boto3.client("bedrock", 'us-east-1',
    aws_access_key_id=bedrock_credentials['Credentials']['AccessKeyId'],
    aws_secret_access_key=bedrock_credentials['Credentials']['SecretAccessKey'],
    aws_session_token=bedrock_credentials['Credentials']['SessionToken'])

dynamodb = boto3.resource('dynamodb','us-east-1')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))

def handler(event, context):
    global bedrock_credentials
    global bedrock
    logger.info(f"event: {event}")
    logger.info(f"context: {context}")
    
    request_json = json.loads(event['body'])
    
    if "message" not in request_json.keys():
        response = {'statusCode':400}
        
    if "High Views" == request_json["message"] or "Sport venues" == request_json['message'] or "Animals" == request_json['message']:
        # Reassume the role only after expiration
        if datetime.now().timestamp() >= bedrock_credentials['Credentials']['Expiration'].timestamp():
            bedrock_credentials = sts_connection.assume_role(
            RoleArn=role_arn,
            RoleSessionName=f"lambda-generate-image-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}")
                
            bedrock = boto3.client("bedrock", 'us-east-1',
                aws_access_key_id=bedrock_credentials['Credentials']['AccessKeyId'],
                aws_secret_access_key=bedrock_credentials['Credentials']['SecretAccessKey'],
                aws_session_token=bedrock_credentials['Credentials']['SessionToken'])
        
        request_message = f"Create 10 positive image descriptions about {request_json['message']}. Do not include a numbers in the list"
        bedrock_body={'prompt': f'Human: \n{request_message}\nAssistant:', 'max_tokens_to_sample': 2048, 'temperature': 1, 'top_k': 250, 'top_p': 0.999, 'stop_sequences': ['\n\nHuman:'], 'anthropic_version': 'bedrock-2023-05-31'}
        logger.info(f"Sending message: {request_json['message']}")
        response = bedrock.invoke_model(body=json.dumps(bedrock_body), modelId='anthropic.claude-v2', accept='*/*',contentType="application/json")
        logger.info(f"Model replied - parsing result")
        response_body = json.loads(response.get('body').read())
        logger.info(f"message: {response_body['completion']}")
        descriptions = response_body['completion'].replace('\n\n','\n').splitlines()[1:]
        uuids = []
        for description in descriptions:
            #add to dynamodb
            item_uuid = str(uuid.uuid4())
            table.put_item(Item={
                'id':item_uuid,
                "description":description,
                "ttl":math.trunc(datetime.now().timestamp())+3600
            })
            uuids.append(item_uuid)
            
        response = {'statusCode': 200,
                    "body": json.dumps(
                        {
                            'descriptions':uuids
                        }
                    )}
    else: 
        response = {'statusCode':400}
    return response