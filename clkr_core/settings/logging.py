LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "%(asctime)s - [%(levelname)s] - %(name)s "
            "- (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "WARNING",
            "formatter": "basic",
            "class": "logging.StreamHandler",
            # 'stream': 'ext://sys.stdout',  # Default is stderr
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "WARNING",
            "formatter": "basic",
            "filename": "/src/logs/clkr-service.log",
            "maxBytes": 1048576,
            "backupCount": 10,
            "mode": "a",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console, file"],
            "propagate": True,
            "level": "WARNING",
        }
    },
}
