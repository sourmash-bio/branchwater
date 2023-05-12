FROM continuumio/miniconda3:4.10.3

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV PATH /opt/conda/bin:$PATH
WORKDIR /app
#install packages
RUN conda install -c conda-forge flask=2.3.2 pandas=1.3.3 pymongo=4.3.3 urllib3=1.26.7 && \
    conda clean -afy && \
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
