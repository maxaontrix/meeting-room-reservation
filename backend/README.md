# 📅 Meeting Room Reservation System

Микросервисное приложение для бронирования переговорных комнат с подтверждением модератором.

---

## 🚀 Stack

**Backend:**
- Python 3.11
- FastAPI
- SQLAlchemy (async)
- Alembic
- PostgreSQL
- Pydantic v2
- Docker / docker-compose

**Auth:**
- JWT (OAuth2PasswordBearer)
- Роли: `user`, `moderator`

**Testing:**
- pytest / pytest-asyncio
- httpx.AsyncClient
- Изолированная тестовая БД в Docker

---

## 📦 Возможности

- 📋 CRUD для переговорных комнат
- 🧾 Создание брони
- 🔐 Авторизация по JWT
- 👮 Подтверждение/отклонение брони модератором
- 🛡️ Ролевая модель доступа
- 🧪 Полное покрытие тестами
- ☁️ Подготовлено к деплою (Docker)

---

## 🔧 Установка и запуск

```bash
# Клонируем проект
git clone https://github.com/maxaontrix/meeting-room-reservation.git
cd meeting-room-reservation

# Копируем env
cp .env.example .env

# Запускаем через Docker
make up
