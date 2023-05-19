from log import Logger
import os
import platform
import ctypes
import sys
from time import ctime, time
sys.path.append(os.path.join(os.path.split(os.path.dirname(__file__))[0], "modules"))

class Common():
    def __init__(self, log_name:str):
        """
         Iniciar o log
         
         @param log_name -Nome do log
        """
        self.log = Logger(log_name)
        
    def get_free_space_mb(self, dirname):
        """
         Obter espaço livre em MB para um diretório.
         
         @param dirname -Nome do diretório a verificar
         
         @return Espaço livre em MB ou 0 em erro (não encontrado ou grande demais para ser considerado um espaço livre
        """
        try:
            # Total free space in bytes of the file.
            if platform.system() == 'Windows':
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
                return free_bytes.value / 1024 / 1024
            else:
                st = os.statvfs(dirname)
                return st.f_bavail * st.f_frsize / 1024 / 1024
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.log.getLogger().error('ERRO DURANTE EXECUÇÃO na FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_free_space_mb.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace("\n", " ")))
            
        
    def create_folder(self, name, dirname):
        """
         Cria uma pasta se não existe. Verifica se a pasta existe e se não existe, cria-a
         
         @param name -Nome da pasta a criar
         @param dirname -Directório onde a pasta será criada. É usado para criar a pasta
         
         @return O caminho total da pasta criada
        """
        
        try:
            name = name.replace(':', ' - ')
            directory = os.listdir(dirname)
            complete = os.path.join(dirname, name)
            # print(complete)
            # Check if file exists in directory or not
            if(name not in directory):
                # Create a directory if it doesn t exist.
                if not os.path.isdir(complete):
                    os.mkdir(complete)
                    return complete
                return complete
            else:
                return complete
        except Exception as err:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.log.getLogger().error('ERRO DURANTE EXECUÇÃO na FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.create_folder.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace("\n", " ")))
            
    def print_time(self,t_f):    
        """
         Imprime a hora para o console. Este é um método a ser usado em conjunto com
         
         @param t_f - Tempo em segundos para
        """
        try:
            segundos = t_f % 60 
            # (//) utiliza para divisão exata
            minutos  = t_f // 60
            # minutos é o número de minutos
            if minutos > 60:
                horas = minutos // 60
                # Calcule os dias caso tenha horas tem mais que 24.
                if horas > 24:
                    dias = horas // 24
                    horas = horas % 24
                else:
                    dias = 0
                minutos = horas % 60
            else:
                horas = 0
                dias = 0
            print('{} dias, {} horas, {} minutos e {} segundos'.format(dias,horas,minutos,segundos))
            self.log.getLogger().info('Executado em: {} dias, {} horas, {} minutos e {} segundos'.format(dias, horas, minutos, segundos))
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO {}: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(self.print_time.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))
            self.log.getLogger().error('ERRO DURANTE EXECUÇÃO {}: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(self.print_time.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))
        
    def only_read_int(self, string=None):
        """
         Leia apenas um número inteiro do usuário. Se o usuário não inserir nada, um prompt é impresso
         
         @param string - Mensagem a ser exibida no prompt
         
         @return Integra leitura do usuário ou None se nada foi informado
        """
        entrada = None
        try:
            entrada = int(input(string))
        except Exception:
            # Loop para leitura de apenas inteiro
            while type(entrada) != int:
                print('Opção invalida')
                entrada = input(string)
                try:
                    entrada = int(entrada)
                except ValueError:
                    continue
        return entrada
            
    def timestamp (self):    
        """ Retorna tempo  atual em segundos"""       
        t = time ()
        return ctime (t)

    def initCountTime(self, print_time=False):
        """ Inicia contagem de tempo """
        if print_time:
            print(self.timestamp())
        t_o = time() 
        return t_o

    def finishCountTime(self, t_o, print_time=False):
        """ Encerra a contagem """
        if print_time:
            print(self.timestamp())
        t_f = int(time () - t_o)
        return t_f