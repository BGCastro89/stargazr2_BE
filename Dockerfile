FROM python:3.7

# ENV IMG_DIR=

#Copy files into docker image dir, and make that the current working dir
COPY . /docker-image
WORKDIR /docker-image

RUN pip install -r requirements.txt


CMD ["flask", "run", "--host", "0.0.0.0"]

# FROM python:3.7

# ENV APP_HOME /app #just sets a var named APP_HOME for later use
# WORKDIR $APP_HOME
# COPY . .

# RUN pip install -r requirements.txt

# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:main





######
# FROM python:3.9-slim

# # Allow statements and log messages to immediately appear in the Knative logs
# ENV PYTHONUNBUFFERED True


# # Copy local code to the container image.
# COPY . /src
# WORKDIR /src

# # Install Python Requirements
# RUN pip install -r requirements.txt

# # Run the web service on container startup. Here we use the gunicorn
# # webserver, with one worker process and 8 threads.
# # For environments with multiple CPU cores, increase the number of workers
# # to be equal to the cores available.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app




######Go
# FROM golang:alpine
# ENV CGO_ENABLED=0

# WORKDIR /app
# COPY . .

# RUN go mod download
# RUN go build -o main .

# EXPOSE $PORT

# CMD [ "./main" ]