# Branchwater web app

The code underlying https://branchwater.jgi.doe.gov/

## Developer install using pixi

Install pixi with `curl -fsSL https://pixi.sh/install.sh | bash`

Then `pixi run flask --app main.py run --debug`


## Developer install using conda

```
mamba create -y -n branchwater_web flask duckdb
mamba activate branchwater_web

pip install pyyaml pandas sentry_sdk urllib3 markdown polars
```

Then:
```
flask --app main.py run --debug
```

