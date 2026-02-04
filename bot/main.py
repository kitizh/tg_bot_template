import asyncio

from bot.core.log_config import setup_logging
from bot.core.app import BotApp
from bot.routers import ROUTERS


async def main() -> None:
    setup_logging()
    app = BotApp(routers=ROUTERS)
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
