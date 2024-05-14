## Docker-command
```
docker run -d --name dogs -e POSTGRES_USER=dog -e POSTGRES_PASSWORD=gavgav -e POSTGRES_DB=konura -p 2525:5432 postgres
```
## Installing
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## env 
```
PG_HOST=127.0.0.1
PG_PORT=2525
PG_PASSWORD=gavgav
PG_USER=dog
PG_DBNAME=konura
FLASK_PORT=5555
API_KEY=<your api key>
```
