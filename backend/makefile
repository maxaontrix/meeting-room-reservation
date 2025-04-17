up:
	docker-compose up --build -d

rebuild:
	docker-compose build --no-cache backend

migrate:
	docker-compose exec backend alembic upgrade head

makemigrations:
	docker-compose exec backend alembic revision --autogenerate -m

psql:
	docker-compose exec db psql -U postgres -d meeting_room
