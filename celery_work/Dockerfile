FROM python:3.9

# Copies every file and directory to '/reddit-stock-sentiment-analyzer' docker image
COPY . . 

# runs requirements.txt copied in the docker image
RUN pip3 install --no-cache-dir -r celery_work/requirements.txt


