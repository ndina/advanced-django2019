import logging

logging.basicConfig(
    filename='out.log',
    filemode='w',
    format='%(asctime)s -- %(levelno)s:%(levelname)s -- %(message)s',
    level=logging.DEBUG
)

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')
