import os
import ntpath
import sys
import urllib.parse 
sys.path.append(os.path.join(os.path.split(os.path.dirname(__file__))[0], "modules"))
sys.path.append(os.path.join(os.path.split(os.path.dirname(__file__))[0], "utils"))
import constants as cnst
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from progress.bar import ChargingBar
from progress.spinner import Spinner
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import common
import requests
import re

class Web():
    def __init__(self, binary_location:str=None):
        """Inicia classe Web

        Configura localização do binário do chrome

        Args:
            binary_location (str, optional): Localização do binário do chrome. Defaults to None.
        """
        self.common = common.Common()
        if binary_location:
            self.binary_location = binary_location
        else:
            self.binary_location =self.verify_chrome()  
      
    def download_archive(self, url:str, path_archive:str):  
        """Baixe o arquivo e retorne caminho para ele. Se o path_archive é None defina automático nome para baixar arquivo 

        Args:
            url (str): URL do arquivo para download
            path_archive (str): Caminho para arquivo para download

        Returns:
            boolean: status de download
        """
        try:
            freespace = self.common.get_free_space_mb(path_archive)
            # Verifique espaço livre.
            if not freespace < 1024:
                response = requests.get(url, stream=True)
                content_type = response.headers['content-type']
                # Verifica se houve sucesso na requisição da url do arquivo
                if response.status_code == requests.codes.OK:
                    # Verifica se caminho do arquivo foi passado.
                    filename_header = response.headers.get('content-disposition')
                    # Extrair o valor do header "filename"
                    filename = filename_header.split("filename=")[1]
                    # Decodificar o valor do cabeçalho
                    filename_decoded = urllib.parse.unquote(filename)
                    filename_decoded = self.common.normalize_name(filename_decoded)
                    path_archiveName = os.path.join(path_archive, filename_decoded)
                    # Verifica se arquivo existe
                    if os.path.isfile(path_archiveName) is False:
                        chunks = []
                        spinner = Spinner('Loading ')
                        for x in response:
                            chunks.append(x)
                            spinner.next()
                        # gera barra de progresso
                        bar = ChargingBar('Baixando',  suffix='%(percent).1f%% - %(eta)ds', max=len(chunks))
                        with open(path_archiveName, "wb") as f:
                            # Escreva cada pedaço no arquivo.
                            for chunk in chunks:
                                f.write(chunk)
                                bar.next()
                            bar.finish()
                        print("Download finalizado. Arquivo salvo em: {}".format(path_archiveName))
                        return True
                    else:
                        print("Arquivo existente")
                        return False
                else:
                    response.raise_for_status()
                return path_archiveName
            else:
                print("Sem espaço na memória")
                return False
        except Exception as err:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO na FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.download_archive.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace("\n", " ")))
            # O erro é 520 Erro de servidor 522 Erro de servidor 522 Erro de servidor 520 Erro de servidor
            if('520 Server Error' in str(err) or '522 Server Error' in str(err) or '404 Client Error' in str(err) or '403 Client Error' in str(err)):
                print('INTERN ERROR: {0}'.format(err))
            else:
                print('ERROR na linha {}: {}'.format(exc_tb.tb_lineno, err))
            return False
    
    def wait_download_file(self, path_download):
        """Aguarde o termino do download

        Args:
            path_download (str): caminho do download

        Returns:
            boolean: status de download
        """        

        """
         Espera para o arquivo de download terminar. Esta é uma função de bloqueio para voltar após 30 minutos
         
         @param path_download - caminho de downloads
         
         @return Verdadeiro se o download terminou Falso se ainda há arquivo crdownload
        """
        try:
            files = (os.listdir(path_download))
            check_download = True
            check = True
            common = self.Common()
            t_0 = common.initCountTime()
            # Verifique se o download está no diretório de download.
            while check:
                files = (os.listdir(path_download))
                # Verifique se o arquivo é um crdownload.
                for file in files:
                    # Verifique se o arquivo termina com. crdownload
                    if file.endswith('.crdownload'):
                        check = True
                        file_crd = os.path.join(path_download, file)
                        break
                    else:
                        check = False
                t_f = common.finishCountTime(t_0)
                minutos = int(t_f / 60)
                # Verifique se o arquivo existe a mais de 30 minutos
                if minutos > 30:
                    check_download = False
                    os.remove(file_crd)
                    break
                else:
                    check_download = True
            return check_download
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.wait_download_file.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            sys.exit()

    def init_webdriver(self,default=True, headless=False, output:str=None):
        """Inicia navegador automatizado google chrome

        Args:
            default (bool, optional): Define se navegador será aberto com opções padrão. Defaults to True.
            headless (bool, optional): Define se navegador abrirá com interface. Defaults to False.
            saida (str, optional): Diretório para downloads. Defaults to None.

        Returns:
            webdriver: navegador automatizado google chrome configurado
        """
        try:
            print('Iniciando navegador automatizado google chrome')
            s=Service(ChromeDriverManager().install())
            if default:
                if headless:
                    driver = webdriver.Chrome(service=s, options=self.optionsChrome(headless=True, download_output=output))
                else:    
                    driver = webdriver.Chrome(service=s, options=self.optionsChrome(headless=False, download_output=output))    
            else:
                # caminho das extensões
                extension_path = os.path.join(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0], 'extensions')
                extensions = [os.path.join(extension_path, 'popup_blocker.crx'), os.path.join(extension_path, 'enable_right_click.crx')]
                # extension = [os.path.join(extension_path, 'adblock.crx'), os.path.join(extension_path, 'enable_right_click.crx')]
                # extension = [os.path.join(extension_path, 'enable_right_click.crx')]
                try:
                    if headless:
                        driver = webdriver.Chrome(service=s, options=self.optionsChrome(headless=True, download_output=output, crx_extension=extensions))
                    else:
                        driver = webdriver.Chrome(service=s, options=self.optionsChrome(headless=False, download_output=output, crx_extension=extensions))
                except:
                    if headless:
                        driver = webdriver.Chrome(service=s, options=self.optionsChrome(headless=True, download_output=output))
                    else:
                        driver = webdriver.Chrome(service=s, options=self.optionsChrome(headless=False, download_output=output))
            return driver
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.init_webdriver.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            sys.exit()

    def optionsChrome(self, headless=False, download_output=None, crx_extension:list=None):
        """Configura opções do navegador chrome

        Args:
            headless (bool, optional): Define se navegador irá iniciar sem interface. Defaults to False.
            download_output (str, optional): Define diretorio para downloads. Defaults to None.
            crx_extension (list, optional): Listas de extensões para instalar no navegador. Defaults to None.

        Returns:
            Options: objeto contendo todas as opções configuradas do navegador
        """
        # Criar uma instância dr opções Chrome e devolvê-lo. Esta é a primeira chamada que você quer executar
        try:
            chrome_options = Options()
            if(headless):
                chrome_options.add_argument("--headless")
            prefs = {}
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--ignore-ssl-errors")
            # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0")
            chrome_options.binary_location = self.binary_location
            if download_output:
                download_output = os.path.normpath(download_output)
                download_output = download_output.replace('/',ntpath.sep)
                prefs.update({"download.default_directory" : download_output})
            if crx_extension:
                for extension in crx_extension:
                    chrome_options.add_extension(extension)
            chrome_options.add_experimental_option('prefs', prefs)
            return chrome_options
            
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO {}: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(self.optionsChrome.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))
        
    def verify_chrome(self):
        """Verifica se existe navegador chrome instalado e retorna o binario do navegador

        Returns:
            str: caminho do binário do navegador chrome
        """
        # Retorna o caminho para o executável mais recente do Chrome x32 ou X86. Isso é baseado na presença de um arquivo
        results_32 = [x for x in os.listdir(os.environ['PROGRAMFILES']) if re.search(r'(google)', x, re.IGNORECASE)]
        results_64 = [x for x in os.listdir(os.environ['PROGRAMFILES(X86)']) if re.search(r'(google)', x, re.IGNORECASE)]
        # Retorna o navegador da base de dados.
        if results_32:
            chrome_path = os.path.join(os.environ['PROGRAMFILES'], results_32[0], 'Chrome', 'Application')
            files = [x for x in os.listdir(chrome_path) if re.search(r'.exe$', x)]
            # Retorna o primeiro arquivo na lista de arquivos.
            if len(files) == 1:
                file = files[0]
            else:
                file = [x for x in files if re.search(r'chrome.exe', x)][0]
            
            browser_path = os.path.join(chrome_path,file)
            return browser_path
        elif results_64:
            chrome_path = os.path.join(os.environ['PROGRAMFILES(X86)'], results_64[0], 'Chrome', 'Application')
            files = [x for x in os.listdir(chrome_path) if re.search(r'.exe$', x)]
            # Retorna o primeiro arquivo na lista de arquivos.
            if len(files) == 1:
                file = files[0]
            else:
                file = [x for x in files if re.search(r'chrome.exe', x)][0]
            browser_path = os.path.join(chrome_path, file)
            return browser_path
        else:
            print("Navegador não instalado")
            return None
        
    def web_scrap(self, url:str=None, markup:str=None):
        """Realiza requisição em site e/ou obtem o conteudo do HTML

        Args:
            url (str, optional): URL a ser requisitada. Defaults to None.
            markup (str, optional): conteudo HTML. Defaults to None.

        Returns:
            bs4.BeautifulSoup: objeto BeautifulSoup
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        soup = None
        feature = 'html.parser'
        # cria instancia do BeautifulSoup com html informado
        if markup:
            soup = BeautifulSoup(markup, feature)
        # cria instancia do BeautifulSoup com html obtido pela requisição
        elif url:
            request = requests.get(url, headers=headers)
            soup = BeautifulSoup(request.content, feature)
        return soup
    
    def try_quit_webdriver(self, driver:webdriver):
        """Fecha navegador se tiver aberto

        Args:
            driver (webdriver): instancia do navegador automatizado
        """        
        try:
            driver.quit()
        except:
            print("Navegador fechado")

    def check_driver(self, driver:webdriver):
        """Verifique se há mais de uma janela para mudar.

        Args:
            driver (webdriver): navegador a verificar
        """
        # Passe para a ultima janela.
        while len(driver.window_handles)>1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            sleep(1)
            # Passe para a primeira janela.
            driver.switch_to.window(driver.window_handles[0])

    def check_crdownload(self, save_path:str):
        """
            Verifique se o crdownload está presente em save_path. Este é um hack para evitar o download que não termina ou ocorra um erro
            
            @param save_path - Caminho para salvar arquivos
        """
        # Esta loop é usado para verificar se há quaisquer crdownloads no save_path.
        while True:
            files = os.listdir(save_path)
            files = [x for x in files if x.endswith('.crdownload')]
            # Se não houver arquivos na lista, encerre o loop.
            if len(files) == 0:
                break

if __name__ == '__main__':
    Web('animes_downloads')
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
