python3 -m uvicorn core.main:app --host 0.0.0.0 --port 8080

docker-compose -f .\deploy\docker-compose.yml up -d

docker-compose -f .\deploy\docker-compose.yml down