param([string]$Target)

switch ($Target) {
    "up"             { docker-compose up --build }
    "rebuild"        { docker-compose build --no-cache backend }
    "migrate"        { docker-compose exec backend alembic upgrade head }
    "makemigrations" { docker-compose exec backend alembic revision --autogenerate -m "Manual" }
    "psql"           { docker-compose exec db psql -U postgres -d meeting_room }
    "test"           { docker-compose exec backend poetry run pytest }
    default          { Write-Output "Unknown command: $Target" }
}
