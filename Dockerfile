FROM ubuntu:latest
RUN apt-get update -y && apt-get install -y python3-pip python3-dev
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY . /app
RUN pip install -r requirements.txt
ENV HOST=0.0.0.0
ENTRYPOINT ["python3"]
CMD ["app.py"]
EXPOSE 5000