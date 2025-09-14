```bash
docker build -t pagila-postgres -f db.Dockerfile .
```

```bash
docker run -d \
  --name pagila-db \
  -e POSTGRES_DB=pagila \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  pagila-postgres
```

```bash
docker exec -it pagila-db psql -U postgres -d pagila
```

```bash
docker exec -it pagila-db psql -U llm_user -d pagila
```

```bash
docker compose up --build
```
