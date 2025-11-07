from __future__ import annotations

import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict

import orjson


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if record.__dict__.get("extra_data"):
            payload.update(record.__dict__["extra_data"])
        return orjson.dumps(payload).decode("utf-8")


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
