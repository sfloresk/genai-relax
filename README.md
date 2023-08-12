# Gen AI Relax 

A GenAI serverless application example built with API Gateway, Lambda, DynamoDB and Bedrock.

The solution has to main components:

1. relaxing-ui: a simple web interface written in VueJS.

2. sam-deployment: SAM application that creates 3 lambda functions (one to generate descriptions with Claude, another to generate images with Stable Diffusion and a third one to generate audio from the description using Polly), a dynamodb table to keep track of the descriptions and an API Gateway as entry point

## Use cases

The application is able to create positive image descriptions for topics selected by the users (the example UI goes over three different topics: High Views, Animals and Sport Venues), this descriptions are then processed one by one to generate an image and audio representations. 

Uses can go from helping users to relaxing and reduce anxiety (concentrating on the images being displayed), to creating memory games (which can be used to evaluate cognitive decline) and even for education (e.g., showing geometric images and asking children to identify which shape is in the screen). An audio description plays per image as an example of how to make a website more accessible.


## Issues

Please open bugs for any questions or issues.