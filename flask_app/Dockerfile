FROM --platform=linux/amd64 python:3.9-slim-buster as build


# Copies requirements.txt to /app directory
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
# Installs requirements
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]

# CMD ["python3", "-um", "run.py"]
# CMD ["waitress-serve", "--port=8080", "--call", "run:create_app"]

