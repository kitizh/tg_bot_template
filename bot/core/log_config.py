from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(
    *,
    log_dir: str = "logs",
    log_file: str = "bot.log",
    level: str = "INFO",
) -> None:
    """Настроить консольный и файловый логгинг с ротацией."""
    # 1) Создаём папку logs/
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # 2) Корневой логгер
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Важно: не плодим хендлеры при перезапуске в IDE
    root.handlers.clear()

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # 3) Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    root.addHandler(ch)

    # 4) File handler (ротация по размеру)
    fh = RotatingFileHandler(
        filename=str(Path(log_dir) / log_file),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,              # 5 файлов: bot.log, bot.log.1 ...
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    root.addHandler(fh)
