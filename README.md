# Gen AI Relax 

A GenAI serverless application example built with Amazon API Gateway, Amazon Lambda, Amazon DynamoDB and Amazon Bedrock.

The solution has two main components:

1. relaxing-ui: a simple web interface written in VueJS.

2. sam-deployment: SAM application that creates 3 lambda functions (one to generate descriptions with Claude, another to generate images with Stable Diffusion and a third one to generate audio from the description using Polly), a dynamodb table to keep track of the descriptions and an API Gateway as entry point

## Use cases

The application is able to create positive image descriptions for topics selected by the users (the example UI goes over three different topics: High Views, Animals and Sport Venues), this descriptions are then processed one by one to generate an image and audio representations. 

Uses can go from helping users to relaxing and reduce anxiety (concentrating on the images being displayed), to creating memory games (which can be used to evaluate cognitive decline) and even for education (e.g., showing geometric images and asking children to identify which shape is in the screen). An audio description plays per image as an example of how to make a website more accessible.

## Installation

This application uses the Amazon Bedrock service which is, at the time of this commmit, in preview. The libraries for this service are not included in the public boto3 libraries, so it is needed to manually add the following files into an installers directory within the folders sam-deployment/generate_descriptions and sam-deployment/generate_image:

1. awscli-1.27.162-py3-none-any.whl
2. boto3-1.26.162-py3-none-any.whl
3. botocore-1.29.162-py3-none-any.whl

Without these files, the docker build will fail for those functions. If you don't have access to Bedrock's libraries, please contact your AWS account team. 

## Issues

Please open bugs for any questions or issues.
