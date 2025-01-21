FROM ghcr.io/prefix-dev/pixi:0.39.5-noble AS build

COPY . /app
WORKDIR /app

#RUN pixi run -e web postinstall-prod
RUN pixi shell-hook -e web > /shell-hook-web
RUN echo 'exec "$@"' >> /shell-hook-web
#RUN pixi run -e worker postinstall-prod
RUN pixi shell-hook -e prepare > /shell-hook-prepare
RUN echo 'exec "$@"' >> /shell-hook-prepare
RUN pixi shell-hook -e mongo > /shell-hook-mongo
RUN echo 'exec "$@"' >> /shell-hook-mongo

#--------------------

FROM build AS rust_build

# Need this to avoid SSL errors. Can this be done only with pixi?
RUN apt-get update && apt-get -y install ca-certificates

RUN pixi run build-server

#--------------------

FROM ubuntu:24.04 AS web

# only copy the production environment into prod container
COPY --from=build /app/.pixi/envs/web /app/.pixi/envs/web
COPY --from=build /shell-hook-web /shell-hook

RUN groupadd user && \
    useradd --create-home --home-dir /home/user -g user -s /bin/bash user

COPY app/ /app/web/

WORKDIR /app/web

#USER user 

ENTRYPOINT ["/bin/bash", "/shell-hook"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--access-logfile", "-", "main:app"]

#--------------------

FROM ubuntu:24.04 AS index

COPY --from=rust_build /app/target/release/branchwater-server /app/bin/branchwater-server

WORKDIR /data

EXPOSE 80/tcp

CMD ["/app/bin/branchwater-server", "--port", "80", "-k21", "--location", "/data/sigs.zip", "/data/index"]

#--------------------

FROM docker.io/mongo:latest AS mongo

COPY --from=build /app/.pixi/envs/mongo /app/.pixi/envs/mongo
COPY --from=build /shell-hook-mongo /shell-hook

# Copy the contents of the current directory to the container's entrypoint directory
COPY ./metadata/load_parquet.py /docker-entrypoint-initdb.d/load_parquet.py
