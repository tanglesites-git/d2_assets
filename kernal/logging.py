import logging
import logging.config


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {
            'format': '[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(module)s - %(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
        'file_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': f'logs/app-info',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
            'encoding': 'utf8',
        },
        'file_debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': f'logs/app-debug',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
            'encoding': 'utf8',
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'simple',
            'filename': f'logs/app-error',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
            'encoding': 'utf8',
        },
    },
    'loggers': {
        '': {  # root logger
            'level': 'DEBUG',
            'handlers': ['console', 'file_info', 'file_debug', 'file_error'],
        },
        'infrastructure.httpio': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_info', 'file_debug', 'file_error'],
        },
        'infrastructure.fileio': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_info', 'file_debug', 'file_error'],
        },
        'kernal.filepath': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_info', 'file_debug', 'file_error'],
        }
    },
})


if __name__ == "__main__":
    pass
