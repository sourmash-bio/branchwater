# Branchwater web app

The code underlying https://branchwater.jgi.doe.gov/

## Developer install using conda

```
mamba create -y -n branchwater_web flask mongodb
mamba activate branchwater_web

pip install pymongo pyyaml pandas sentry_sdk urllib3 markdown
```

Then:
```
flask --app main.py run --debug
```

