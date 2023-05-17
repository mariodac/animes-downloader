import logging
from os import path, environ, name
class Logger:
    def __init__(self, log_name):
        """
         Iniciar o log. Isto é chamado por __init__ e não deve ser chamado diretamente
         
         @param log_name - O nome do log
        """
        self.log_name = log_name
        self.loggers = {}
        
    def getLogger(self):
        """
         Retorna o objeto de log. Verificação para não criar vários instãncias  e gerar linhas duplicadas no log 
         
         
         @return Objeto de log aqui estable
        """
        # verificação para não criar vários objetos e gerar linhas duplicadas no log 
        # Verifica se já existe instancia de logger
        if self.loggers.get(name):
            return self.loggers.get(name)
        else:
            # nome que irá aparece no log'
            logger = logging.getLogger(self.log_name)
            # configura nivel de log
            logger.setLevel('DEBUG')
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
            # especificando nome do arquivo de log 
            file_handler = logging.FileHandler("{}.log".format(path_log))
            file_handler.setFormatter(formatter)
            # adiciona arquivo ao manipulador de arquivo de log
            logger.addHandler(file_handler)
            self.loggers[name] = logger
            return logger
    
    