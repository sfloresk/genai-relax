import boto3
import sys
import base64
from boto3.dynamodb.conditions import Key
import logging
import json 
import os

polly_c = boto3.client('polly','us-east-1')
dynamodb = boto3.resource('dynamodb','us-east-1')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f"event: {event}")
    logger.info(f"context: {context}")
    request_json = json.loads(event['body'])
    description = table.query(KeyConditionExpression=Key('id').eq(request_json['message_id']))['Items'][0]['description']
    voice = 'Matthew'
    text = description
    speech = convert_text_to_speech(voice, text)
    response = {
        'statusCode': 200,
        'headers': { 'Content-Type': 'audio/mpeg' },
        'body': base64.b64encode(speech),
        'isBase64Encoded': True}
    return response

def convert_text_to_speech(voice, text):
    response = polly_c.synthesize_speech(
                   VoiceId=voice,
                   OutputFormat='mp3',
                   Text = text)
    return response['AudioStream'].read()