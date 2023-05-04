FROM python:3.9

WORKDIR /reddit-stock-sentiment-analyzer

# Copies every file and directory to '/reddit-stock-sentiment-analyzer' docker image
COPY . . 

# runs requirements.txt copied in the docker image
RUN pip3 install --no-cache-dir -r requirements.txt

# used to run flask 
CMD ["python3" "-u" "run.py"]