# set the base image. Since we're running 
# a Python application a Python base image is used
FROM python:3.8
# set a key-value label for the Docker image
LABEL maintainer="Tech Trends"
# copy files from the host to the container filesystem. 
#  defines the working directory within the container
WORKDIR /techtrends

COPY ./project/techtrends/requirements.txt .

# run commands within the container. 
# For example, invoke a pip command 
# to install dependencies defined in the requirements.txt file. 
RUN pip install -r requirements.txt

COPY ./project/techtrends .
# Run the init_db.py script to initialize the database
RUN python3 init_db.py

# Expose the application port
EXPOSE 3111

# provide a command to run on container start. 
# For example, start the `app.py` application.
CMD [ "python", "app.py" ]
