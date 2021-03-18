import logging.config
import os

import structlog

LOG_FILE_NAME = os.environ.get('LOG_FILE_PATH', '/var/log/swipe-food-api.log')

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simpleFormatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=True),
        },
        "jsonFormatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
    },
    "handlers": {
        "consoleHandler": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simpleFormatter",
        },
        "fileHandler": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "jsonFormatter",
            "filename": LOG_FILE_NAME,
            "when": "midnight",
            "interval": 10,
            "backupCount": 7
        },
    },
    "loggers": {
        "": {
            "handlers": ["consoleHandler", "fileHandler"],
            "level": "DEBUG",
        },
    }
})

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


class Logger:

    @classmethod
    def create(cls, name: str, **kwargs):
        return structlog.getLogger(name=name, **kwargs)
