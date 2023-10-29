from unidecode import unidecode
import os
import re
import platform
import ctypes
import sys
from time import ctime, time
sys.path.append(os.path.join(os.path.split(os.path.dirname(__file__))[0], "modules"))
sys.path.append(os.path.join(os.path.split(os.path.dirname(__file__))[0], "utils"))
import constants as cnst


class Common():
        
    def normalize_name(self, name:str):
        """Normalizar um string para padrão aceitável no windows

        Args:
            name (str): texto a ser normalizado

        Returns:
            str: texto normalizado
        """
        # Lista de caracteres proibidos no Windows
        caracteres_proibidos = r'[<>:"/\\|?*]'
        # retira caracters acentuados
        name = unidecode(name)
        # substitui caracteres proibidos do windows por vazio
        name = re.sub(caracteres_proibidos, '', name)
        return name

    def get_free_space_mb(self, dirname:str):
        """Obter espaço livre em MB para um diretório.

        Args:
            dirname (str): Nome do diretório a verificar

        Returns:
            float: Espaço livre em MB ou 0 em erro (não encontrado ou grande demais para ser considerado um espaço livre
        """
        try:
            # Espaço total livre em bytes do arquivo.
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
            print('ERRO DURANTE EXECUÇÃO na FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_free_space_mb.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace("\n", " ")))
              
    def create_folder(self, name:str, dirname:str):
        """Verifica se a diretório existe e se não existe, realiza a criação da diretório

        Args:
            name (str): Nome da diretório a criar
            dirname (str): Diretório onde a diretório será criada. É usado para criar a diretório

        Returns:
            str: O caminho da diretório
        """
        
        try:
            name = name.replace(':', ' - ')
            directory = os.listdir(dirname)
            complete = os.path.join(dirname, name)
            # print(complete)
            # Verifique se o diretorio com este nome existe no diretório ou não
            if(name not in directory):
                # Crie um diretório se não existir.
                if not os.path.isdir(complete):
                    os.mkdir(complete)
                    return complete
                return complete
            else:
                return complete
        except Exception as err:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO na FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.create_folder.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace("\n", " ")))
            
    def print_time(self,t_f:float):    
        """Imprime o tempo de execução para o terminal. Exibe dias, horas, minutos e segundos

        Args:
            t_f (float): Tempo em segundos
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
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO {}: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(self.print_time.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))
        
    def only_read_int(self, string:str=None):
        """Leia apenas um número inteiro do usuário. Se o usuário não inserir nada, uma mensagem será exibida

        Args:
            string (str, optional): Mensagem a ser exibida no terminal. Defaults to None.

        Returns:
            int or None: Numero informado pelo usuário. None se nada foi informado. 
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
        """Retorna o tempo atual no formato Sun Jun 20 23:21:05 1993

        Returns:
            str: Retorna o tempo atual em segundos
        """
        t = time ()
        return ctime (t)

    def initCountTime(self, print_time:bool=False):
        """Inicializa o contador de tempo a partir deste método

        Args:
            print_time (bool, optional): Indica se pode imprimir o tempo. Defaults to False.

        Returns:
            float: Retorna a quantidade de tempo em segundos
        """
        # Imprime o tempo atual
        if print_time:
            print(self.timestamp())
        t_o = time() 
        return t_o

    def finishCountTime(self, t_i:float, print_time=False):
        """Finaliza o contador de tempo a partir deste método

        Args:
            t_i (float): É o tempo inicial
            print_time (bool, optional): Indica se pode imprimir o tempo. Defaults to False.

        Returns:
            float: Quantidade de tempo em segundos
        """        
        """
         
         
         @param t_i - É o tempo inicial
         @param print_time - Indica se pode imprimir o tempo
         
         @return Retorna a quantidade de tempo em segundos
        """
        # Imprima o tempo atual.
        if print_time:
            print(self.timestamp())
        t_f = int(time () - t_i)
        return t_f