import logging

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )

error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_logger_handler = logging.FileHandler('../logs/app/errors.log')
error_logger_formatter = logging.Formatter(u'%(filename)s [LINE:%(lineno)d] [%(asctime)s]  %(message)s')
error_logger_handler.setFormatter(error_logger_formatter)
error_logger.addHandler(error_logger_handler)
