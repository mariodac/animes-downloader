import logging
from logging.handlers import RotatingFileHandler
from os import path, environ, name
import sys
sys.path.append(path.join(path.split(path.dirname(__file__))[0], "modules"))

loggers = {} 

class DuplicateFilter(logging.Filter):

    def filter(self, record):
        # add other fields if you need more granular comparison, depends on your app
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False
class Logger:
    def __init__(self, log_name):
        """
         Iniciar o log. Isto é chamado por __init__ e não deve ser chamado diretamente
         
         @param log_name - O nome do log
        """
        self.log_name = log_name
    def get_logger(self):
        global loggers
        """
         Retorna o objeto de log. Verificação para não criar vários instãncias  e gerar linhas duplicadas no log 
         
         
         @return Objeto de log aqui estable
        """
        # verificação para não criar vários objetos e gerar linhas duplicadas no log 
        # Verifica se já existe instancia de logger
        if loggers.get(self.log_name):
            return loggers.get(self.log_name)
        else:
            # nome que irá aparece no log'
            logger = logging.getLogger(self.log_name)
            logger.addFilter(DuplicateFilter())
            # configura nivel de log
            logger.setLevel(logging.DEBUG)
            # verifica sistema operacional
            if name == 'nt':
                path_log = environ['TEMP']
                log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                # aplica formato 
                formatter = logging.Formatter(log_format)
            else:
                path_log = environ['HOME']
                # formato do log
                log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                formatter = logging.Formatter(log_format)
            path_log = path.join(path_log, '.{}'.format(self.log_name))
            # especificando nome do arquivo de log e configurando log rotativo
            file_handler = RotatingFileHandler("{}.log".format(path_log), maxBytes=10000, backupCount=1) 
            file_handler.setLevel(logging.DEBUG)
            # file_handler = logging.FileHandler("{}.log".format(path_log))
            file_handler.setFormatter(formatter)
            # adiciona arquivo ao manipulador de arquivo de log
            logger.addHandler(file_handler)
            loggers.update(dict(name=logger))
            return logger
    
    