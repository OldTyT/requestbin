import logging
import sys
from loguru import logger  # noqa: F811

from .models.configs import GlobalConfigs


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        logging.CRITICAL: 'CRITICAL',
        logging.ERROR: 'ERROR',
        logging.WARNING: 'WARNING',
        logging.INFO: 'INFO',
        logging.DEBUG: 'DEBUG',
        logging.NOTSET: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        cfg = GlobalConfigs()
        log.opt(
            depth=depth,
            colors=True,
            exception=record.exc_info
        ).log(level, cfg.delete_secrets(record.getMessage()))


def formatter(record):
    cfg = GlobalConfigs()
    record['message'] = cfg.delete_secrets(record['message'])
    return "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>" \
           " <level>{level}</level> <cyan>{name}:{function}:{line}</cyan>" \
           " - <level>{message}</level>\n"


class CustomizeLogger:
    @classmethod
    def customize_logging(cls):
        cfg = GlobalConfigs()
        logger.remove()
        logger.add(
            sys.stderr,
            enqueue=True,
            backtrace=True,
            colorize=True,
            level=cfg.log_level.upper(),
            format=formatter,
            serialize=cfg.log_format_json
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        #logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['gunicorn',
                     'gunicorn.error',
                     #'uvicorn',
                     'uvicorn.access',
                     'uvicorn.error',
                     'flask'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)


logger = CustomizeLogger.customize_logging()  # noqa: F811
