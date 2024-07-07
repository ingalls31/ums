# TODO: Configure your app

import sys


APP_NAME = "UMS"
VERSION = "v1.0.0"


logging_config = {
    "version": 1,
    "formatters": {
        "detailed": {
            "format": (
                "Time: %(asctime)s\n"
                "Process: %(process)s\n"
                "Level: %(levelname)s\n"
                "Logger: %(name)s\n"
                "Module: %(module)s\n"
                "Function: %(funcName)s\n"
                "Line: %(lineno)s\n"
                "Message: %(message)s\n"
                "------------------------------------------------------\n"
            )
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "stream": sys.stderr,
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
        "propagate": True
    }
}