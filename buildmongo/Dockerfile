FROM docker.io/mongo:latest

# Install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get -y install python3-dev
RUN pip3 install pymongo pandas google-cloud-bigquery pyarrow pyyaml

# Copy the contents of the current directory to the container's entrypoint directory
COPY . /docker-entrypoint-initdb.d/
