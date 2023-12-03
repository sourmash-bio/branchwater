FROM condaforge/mambaforge:23.1.0-4

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV PATH /opt/conda/bin:$PATH
WORKDIR /app

#install packages
RUN mamba install -c conda-forge flask=2.3.2 pandas=2.0.3 pymongo=4.4.1 urllib3=2.0.4 pyyaml=6.0 && \
    pip install --upgrade "sentry-sdk[flask]" && \
    mamba clean -afy && \
    rm -rf /opt/conda/pkgs/* && \
    rm -rf /root/.cache/pip/* /root/.cache/conda/*

COPY . /app

EXPOSE 8000

#run app
CMD ["python3", "main.py"]



# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info,  refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser
