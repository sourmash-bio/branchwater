load_data:
	podman-compose exec mongodb python3 /docker-entrypoint-initdb.d/bqtomongo.py	
