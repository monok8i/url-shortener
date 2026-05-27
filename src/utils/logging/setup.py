"""Application logging bootstrap and shutdown helpers."""

import logging
import sys
from logging import Handler
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

from src.utils.logging.config import DEFAULT_LOGGING_LEVEL_DICT, FORMATTER

_queue = Queue()  # pyright: ignore[reportUnknownVariableType]
_listener: QueueListener | None = None


def setup_logging() -> logging.Logger:
    """Configure root logging, console output, and queue-based dispatch.

    Returns:
        The configured root logger.

    The root logger is wired through a queue listener so log emission stays
    consistent even when multiple application components log concurrently.
    """
    handlers: list[Handler] = []

    root_logger = logging.getLogger()
    root_logger.setLevel(DEFAULT_LOGGING_LEVEL_DICT.get("main", logging.INFO))

    # --- Console handler ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(
        DEFAULT_LOGGING_LEVEL_DICT.get("main", logging.INFO)
    )
    console_handler.setFormatter(FORMATTER)

    handlers.append(console_handler)

    # --- uvicorn ---
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = True

    # --- Queue handler ---
    queue_handler = QueueHandler(queue=_queue)  # pyright: ignore[reportUnknownArgumentType]
    queue_handler.setLevel(
        DEFAULT_LOGGING_LEVEL_DICT.get("main", logging.INFO)
    )

    root_logger.addHandler(queue_handler)

    _listener = QueueListener(
        _queue,  # pyright: ignore[reportUnknownArgumentType]
        *handlers,
        respect_handler_level=True,
    )
    _listener.start()

    return root_logger


def stop_logging():
    """Stop the logging listener and flush pending log records.

    The helper is safe to call multiple times and will do nothing if the
    listener has not been started.
    """

    _listener.stop() if _listener else None
