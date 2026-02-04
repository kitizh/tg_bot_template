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
2. Заполнить `.env`
3. Запустить polling

Пример `.env`:
```
BOT_TOKEN=your_token_here
DB_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
USE_WEBHOOK=False
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

## Структура проекта
- `bot/core/` — запуск приложения, конфигурация, контейнер, фабрика
- `bot/handlers/` — обработчики (OOP)
- `bot/services/` — бизнес‑логика
- `bot/repositories/` — доступ к данным (заготовка)
- `bot/infra/` — низкоуровневые подключения (DB, Redis и т.д.)
- `bot/middlewares/` — middleware
- `bot/states/` — FSM состояния
- `bot/routers.py` — список активных роутеров
## Модули (актуально, подробнее)
- `bot/core/` — ядро приложения. Тут живут `Settings`, `Container`, `AppFactory`, `BotApp`, логирование и `types.py` с типизированным DI‑контекстом. Это место, где собирается runtime и управляются ресурсы.
- `bot/handlers/` — OOP‑хендлеры. Каждый класс наследуется от `BaseHandlers` и сам регистрирует свои обработчики в `Router`.
- `bot/services/` — слой бизнес‑логики. Сервисы не зависят от aiogram, используют репозитории и возвращают чистые данные.
- `bot/models/` — ORM‑модели SQLAlchemy: сейчас есть `User`, `Admin`, `Subscription`.
- `bot/repositories/` — репозитории доступа к данным. Есть `BaseRepository` и примеры репозиториев с CRUD и выборками.
- `bot/infra/` — низкоуровневые подключения. Сюда вынесены engine/session и `Base` для ORM.
- `bot/middlewares/` — middleware для DI и сессии БД. Сюда будут добавлены error‑handler, rate‑limit, i18n и т.д.
- `bot/states/` — FSM состояния и сценарии.
- `bot/filters/` — фильтры (заготовка), включая кастомные фильтры и MagicFilter.
- `bot/ui/` — клавиатуры и UI‑утилиты (заготовка).
- `bot/admin/` — админский модуль (заготовка) с командами, фильтрами и сервисами.
- `bot/rate_limits/` — лимиты запросов (заготовка) и middleware.
- `bot/subscriptions/` — подписки и платежи (заготовка) с сервисом проверки подписки.
- `bot/queues/` — очереди и фоновые задачи (заготовка) на Redis.
- `bot/routers.py` — единая точка подключения всех роутеров.

## Паттерны и соглашения
- Обработчики должны быть «тонкими» — только вход/выход, логика в сервисах.
- Сервисы не зависят от aiogram.
- Все зависимости создаются в `Container`.
- Все роутеры подключаются через `bot/routers.py`.
- `DbSessionMiddleware` можно подключать точечно (к конкретным роутерам), если не всем обработчикам нужна БД. Это уменьшает накладные расходы.

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

## Режим работы
Проект рассчитан на polling‑режим как для локальной разработки, так и для продакшена.

## Тестирование
Планируется базовый набор тестов:
- проверки обработчиков (pytest‑asyncio)
- тесты сервисов
- тесты FSM‑сценариев

Запуск (когда появятся тесты):
```
pytest
```

## Ближайшие задачи (roadmap)
- Подключение БД и миграций
- Готовые middleware: i18n, rate‑limit, error‑handler
- Примеры репозиториев и сервисов

---
Если хочешь, я могу расширить README с конкретными командами установки, настройкой Poetry/uv и примерами запуска в Docker.
