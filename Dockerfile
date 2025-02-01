FROM ghcr.io/prefix-dev/pixi:0.39.5-noble AS install

WORKDIR /app

COPY pyproject.toml .
COPY pixi.lock .

RUN --mount=type=cache,target=/root/.cache/rattler/cache,sharing=private pixi install

RUN pixi shell-hook -e web > /shell-hook-web
RUN echo 'exec "$@"' >> /shell-hook-web

RUN pixi shell-hook -e prepare > /shell-hook-prepare
RUN echo 'exec "$@"' >> /shell-hook-prepare

RUN pixi shell-hook -e mongo > /shell-hook-mongo
RUN echo 'exec "$@"' >> /shell-hook-mongo

RUN pixi shell-hook -e mongod > /shell-hook-mongod
RUN echo 'exec "$@"' >> /shell-hook-mongod

#--------------------

FROM install AS rust_build

COPY . .

# Need this to avoid SSL errors. Can this be done only with pixi?
RUN apt-get update && apt-get -y install ca-certificates

RUN pixi run build-server

#--------------------

FROM ubuntu:24.04 AS web

# only copy the production environment into prod container
COPY --from=install /app/.pixi/envs/web /app/.pixi/envs/web
COPY --from=install /shell-hook-web /shell-hook

RUN groupadd user && \
    useradd --create-home --home-dir /home/user -g user -s /bin/bash user

COPY app/ /app/web/

WORKDIR /app/web

USER user

ENTRYPOINT ["/bin/bash", "/shell-hook"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--timeout", "120", "--workers", "4", "--access-logfile", "-", "main:app"]

#--------------------

FROM ubuntu:24.04 AS index

COPY --from=rust_build /app/target/release/branchwater-server /app/bin/branchwater-server

WORKDIR /data

EXPOSE 80/tcp

CMD ["/app/bin/branchwater-server", "--port", "80", "-k21", "--location", "/data/sigs.zip", "/data/index"]

#--------------------

FROM ubuntu:24.04 AS mongo

# only copy the production environment into prod container
COPY --from=install /app/.pixi/envs/mongod /app/.pixi/envs/mongod
COPY --from=install /shell-hook-mongod /shell-hook

RUN groupadd user && \
    useradd --create-home --home-dir /home/user -g user -s /bin/bash user

USER user

ENTRYPOINT ["/bin/bash", "/shell-hook"]
CMD ["mongod", "--dbpath", "/data/db", "--bind_ip_all"]
