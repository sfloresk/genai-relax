FROM public.ecr.aws/lambda/python:3.9
COPY requirements.txt  .
COPY installers ./installers
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" && rm -rf requirements.txt installers

COPY app.py ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]