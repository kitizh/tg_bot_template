# tg_bot_template

Универсальный шаблон для Telegram‑ботов на Python с упором на OOP, масштабируемость и чистую архитектуру.

## Стек
- Python 3.12+
- aiogram 3.x
- Redis (FSM storage)
- SQLAlchemy 2.x (async) + asyncpg
- Alembic (миграции)
- FastAPI + Uvicorn (опционально, убрано в пользу polling)
- Ruff, MyPy, Pytest (dev‑tooling)

## Быстрый старт
1. Установить зависимости
2. Создать и заполнить `.env`
3. Запустить бота в polling
4. Проверить бота в Telegram

## Конфигурация (.env)
Минимум для запуска:
- `BOT_TOKEN` — токен бота.
- `REDIS_URL` — Redis для FSM/ratelimit.
- `DB_URL` — Postgres для хранения пользователей (опционально, но рекомендуется).

Полный список:
- `BOT_TOKEN` — токен бота.
- `DB_URL` — строка подключения к Postgres (SQLAlchemy async).
- `REDIS_URL` — строка подключения к Redis.
- `USE_WEBHOOK` — использовать webhook вместо polling (`True/False`).
- `LOG_LEVEL` — уровень логов (`INFO` по умолчанию).
- `RATE_LIMIT_LIMIT` — лимит сообщений.
- `RATE_LIMIT_PERIOD` — период для лимита сообщений.
- `RATE_LIMIT_NOTIFY` — уведомлять пользователя при превышении лимита (`True/False`).
- `COMMAND_RATE_LIMIT_LIMIT` — лимит команд.
- `COMMAND_RATE_LIMIT_PERIOD` — период для лимита команд.

Пример:
```env
BOT_TOKEN=your_token_here
DB_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
USE_WEBHOOK=False
LOG_LEVEL=INFO
RATE_LIMIT_LIMIT=5
RATE_LIMIT_PERIOD=1.0
RATE_LIMIT_NOTIFY=True
COMMAND_RATE_LIMIT_LIMIT=3
COMMAND_RATE_LIMIT_PERIOD=5.0
```

## Установка и запуск (uv)
Установка `uv` (официальный способ через `curl`):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Установить зависимости и запустить бота через `uv`:

```
uv sync
uv run python -m bot.main
```

## Архитектура
**Идея**: логика разделена на слои, всё управляется через контейнер зависимостей и фабрику приложения.

Поток обработки:
`Container` → `AppFactory` → `Dispatcher` → `middlewares` → `routers` → `handlers` → `services` → `repositories` → `DB/Redis`

### Ключевые элементы
- `Container` — единая точка создания и закрытия ресурсов (bot, dispatcher, redis, storage, сервисы и т.д.).
- `AppFactory` — фабрика сборки приложения: создаёт контейнер, подключает middleware и роутеры.
- `router_registry` (`bot/routers.py`) — центральный список активных роутеров.
- `BaseHandlers` — базовый класс для группировки хендлеров в OOP‑стиле.
- `BaseService` / `BaseRepository` — базовые классы для бизнес‑логики и доступа к данным.

### Принцип DI (dependency injection)
- Middleware кладёт зависимости в `data`, aiogram подставляет их в параметры обработчиков.
- В хендлеры передаются **только нужные сервисы**, контейнер передаётся **только когда нужен доступ к множеству ресурсов**.

Пример:
```python
async def start(message: Message, user_service: UserService) -> None:
    await message.answer(user_service.get_welcome_text())
```

Доступные зависимости:
- `user_service` — сервис пользователей (из `ContainerMiddleware`).
- `db_session` — `AsyncSession` (из `DbSessionMiddleware`).

### Middleware: уровень подключения
В проекте middleware подключаются на уровне `dispatcher.update`. Это означает, что их `event` всегда `Update`.
Если потребуется вешать middleware на уровне `router.message` или `router.callback_query`, нужно вернуть обработку `Message`/`CallbackQuery` в коде.

### Middleware стек и порядок
Подключается в `bot/core/app_factory.py`:
1. `ErrorHandlerMiddleware` — перехват ошибок и ответ пользователю.
2. `LoggingMiddleware` — логирование входящих апдейтов и времени обработки.
3. `ContainerMiddleware` — DI контейнер и сервисы.
4. `RateLimitMiddleware` — глобальные лимиты на команды и сообщения.
5. `DbSessionMiddleware` — открывает сессию БД и коммитит/роллбэчит.
6. `UserActivityMiddleware` — создание пользователя и обновление активности.

## Структура проекта
- `bot/core/` — ядро приложения: `Settings`, `Container`, `AppFactory`, `BotApp`, типы DI.
- `bot/handlers/` — OOP‑хендлеры, регистрация обработчиков внутри `register`.
- `bot/services/` — бизнес‑логика.
- `bot/repositories/` — репозитории доступа к данным.
- `bot/models/` — ORM‑модели SQLAlchemy.
- `bot/infra/` — подключения к БД/Redis и общая ORM‑база.
- `bot/middlewares/` — middleware (DI, DB session, rate‑limit, logging, error‑handler).
- `bot/filters/` — фильтры aiogram, включая `RateLimit`, `IsAdmin`, `TextPrefix`.
- `bot/ui/` — клавиатуры и UI‑утилиты.
- `bot/states/` — FSM состояния и сценарии.
- `bot/routers.py` — единая точка подключения всех роутеров.
- `bot/rate_limits/` — реализация лимитера (Redis).

## Паттерны и соглашения
- Обработчики должны быть «тонкими» — только вход/выход, логика в сервисах.
- Сервисы не зависят от aiogram.
- Все зависимости создаются в `Container`.
- Все роутеры подключаются через `bot/routers.py`.
- При необходимости `DbSessionMiddleware` можно подключать точечно (к конкретным роутерам), если не всем обработчикам нужна БД.

## Rate limit
Глобальный rate limit включён через `RateLimitMiddleware`:
- команды и обычные сообщения имеют разные лимиты;
- параметры берутся из `.env`;
- команда `/broadcast` исключена из глобального лимита и регулируется локально.

Локальный rate limit (через фильтр на хэндлере):
```python
@router.message(Command("broadcast"), IsAdmin(), RateLimit(key_prefix="rate:cmd:broadcast", limit=1, per=30))
async def admin_broadcast(message: Message) -> None:
    ...
```

Чтобы исключить команду из глобального лимита, добавьте её в `RateLimitMiddleware._is_exempt_command(...)` в файле `bot/middlewares/rate_limit.py`.

## База данных и репозитории
Сессия БД создаётся в `DbSessionMiddleware` и передаётся в хэндлеры как `db_session`.
Коммит/роллбэк выполняются автоматически в этом же middleware.

Репозитории принимают `AsyncSession` и инкапсулируют доступ к данным.
Пример (упрощённо):
```python
repo = UserRepository(db_session)
user = await repo.get_or_create_user(user_id=message.from_user.id, username=message.from_user.username)
await repo.last_user_activity(user, username=message.from_user.username)
```

## Логирование и ошибки
- Логирование апдейтов и времени обработки выполняет `LoggingMiddleware`.
- `ErrorHandlerMiddleware` ловит необработанные исключения и отвечает пользователю коротким сообщением.

## Как расширять шаблон
1. Добавьте новый класс хэндлеров в `bot/handlers/` и зарегистрируйте обработчики внутри `register`.
2. При необходимости создайте сервис в `bot/services/` и репозиторий в `bot/repositories/`.
3. Подключите роутер в `bot/routers.py`.
4. Если нужен доступ к БД, используйте `db_session` в сигнатуре хэндлера.

## Примеры
Добавление команды:
```python
class CustomHandlers(BaseHandlers):
    def register(self) -> None:
        @self.router.message(Command("ping"))
        async def ping(message: Message) -> None:
            await message.answer("pong")
```

Подключение роутера:
```python
from bot.handlers.custom import router as custom_router

ROUTERS = [
    custom_router,
    # ...
]
```

## Docker
Для Redis используется `docker-compose.yml`.

Запуск Redis:
```
docker compose up -d
```

Остановка:
```
docker compose down
```

