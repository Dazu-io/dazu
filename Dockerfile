FROM ubuntu:latest

## Instaling python and build-essential
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev build-essential

WORKDIR /app

## Copy only requirements file for build a base image with major dependencies and reduce time of build 
COPY requirements.txt /app

RUN pip install -r requirements.txt

## Copy rest of code
COPY david /app

ENTRYPOINT ["python"]

CMD ["app.py"]