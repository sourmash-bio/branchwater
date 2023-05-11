FROM mongo:latest

# Install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get -y install python3-dev
RUN pip3 install pymongo pandas google-cloud-bigquery pyarrow

# Set environment variables for MongoDB
ENV MONGO_INITDB_ROOT_USERNAME=root \
    MONGO_INITDB_ROOT_PASSWORD=rootpassword

# Copy the contents of the current directory to the container's entrypoint directory
COPY . /docker-entrypoint-initdb.d/


# Build the database
CMD mongod --fork --logpath /var/log/mongodb.log && python3 /docker-entrypoint-initdb.d/bqtomongo.py

