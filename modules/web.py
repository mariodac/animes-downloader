import os
import ntpath
from log import Logger
import sys
from time import ctime
from progress.bar import ChargingBar
from common import Common
import requests
import re

class Web():
    def __init__(self, name_log, binary_location):
        self.log = Logger(name_log)
        self.common = Common(name_log)
        self.binary_location = binary_location
        
      
    def download_archive(self, url, path_archive=None):  
        try:
            freespace = self.common.get_free_space_mb(path_archive)
            if not freespace < 1024:
                response = requests.get(url, headers=self.headers, stream=True)
                content_type = response.headers['content-type']
                if(path_archive):
                    archiveName = os.path.join(path_archive, os.path.basename(response.url.split("/")[-1]))
                    path_archiveName = os.path.join(path_archive, archiveName)
                else:
                    archiveName = os.path.join(self.saida_path, os.path.basename(response.url.split("/")[-1]))
                    path_archiveName = os.path.join(self.saida_path,"{}-{}.{}".format(archiveName, ctime().replace(' ', '_').replace(':','-'), content_type.split('/')[-1]))
                if response.status_code == requests.codes.OK:
                    if os.path.isfile(path_archiveName) is False:
                        # gera barra de progresso
                        chunks = [x for x in response]
                        bar = ChargingBar('Baixando',  suffix='%(percent).1f%% - %(eta)ds', max=len(chunks))
                        with open(path_archiveName, "wb") as f:
                            for chunk in chunks:
                                f.write(chunk)
                                bar.next()
                            bar.finish()
                        print("Download finalizado. Arquivo salvo em: {}".format(path_archiveName))
                    else:
                        print("Arquivo existente")
                        return None
                else:
                    response.raise_for_status()
                    return None
                return path_archiveName
            else:
                print("Sem espaço na memória")
                return None
        except Exception as err:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.log.getLogger().error('ERRO DURANTE EXECUÇÃO na FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.download_archive.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace("\n", " ")))
            if('520 Server Error' in str(err) or '522 Server Error' in str(err) or '404 Client Error' in str(err)):
                self.log.getLogger().error('INTERN ERROR: {0}'.format(err))
            else:
                self.log.getLogger().error('ERROR na linha {}: {}'.format(exc_tb.tb_lineno, err))
            raise
    
    def wait_download_file(self, path_download):
        try:
            files = (os.listdir(path_download))
            check_download = True
            check = True
            common = self.Common()
            t_0 = common.initCountTime()
            while check:
                files = (os.listdir(path_download))
                for file in files:
                    if file.endswith('.crdownload'):
                        check = True
                        file_crd = os.path.join(path_download, file)
                        break
                    else:
                        check = False
                t_f = common.finishCountTime(t_0)
                minutos = int(t_f / 60)
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
            self.log.getLogger().error('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.wait_download_file.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            sys.exit()
            
    def optionsChrome(self, headless=False, download_output=None, crx_extension=None):
        try:
            if(headless):
                self.chrome_options.add_argument("--headless")
            prefs = {}
            self.chrome_options.add_argument("--start-maximized")
            self.chrome_options.add_argument("--disable-gpu")
            self.chrome_options.add_argument("--disable-logging")
            self.chrome_options.add_argument("--log-level=3")
            self.chrome_options.add_argument("--ignore-certificate-errors")
            self.chrome_options.add_argument("--ignore-ssl-errors")
            self.chrome_options.binary_location = self.binary_location
            if download_output:
                download_output = os.path.normpath(download_output)
                download_output = download_output.replace('/',ntpath.sep)
                prefs.update({"download.default_directory" : download_output})
            if crx_extension:
                self.chrome_options.add_extension(crx_extension)
            self.chrome_options.add_experimental_option('prefs', prefs)
            return self.chrome_options
            
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.log.getLogger().error('ERRO DURANTE EXECUÇÃO {}: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(self.optionsChrome.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))
        
    def verify_chrome(self):
        """Verifica se existe navegador chrome instalado e o registra no webbrowser e returna o objeto do browser"""
        results_32 = [x for x in os.listdir(os.environ['PROGRAMFILES']) if re.search(r'(google)', x, re.IGNORECASE)]
        results_64 = [x for x in os.listdir(os.environ['PROGRAMFILES(X86)']) if re.search(r'(google)', x, re.IGNORECASE)]
        if results_32:
            chrome_path = os.path.join(os.environ['PROGRAMFILES'], results_32[0], 'Chrome', 'Application')
            files = [x for x in os.listdir(chrome_path) if re.search(r'.exe$', x)]
            if len(files) == 1:
                file = files[0]
            else:
                file = [x for x in files if re.search(r'chrome.exe', x)][0]
            
            browser_path = os.path.join(chrome_path,file)
            return browser_path
        elif results_64:
            chrome_path = os.path.join(os.environ['PROGRAMFILES(X86)'], results_64[0], 'Chrome', 'Application')
            files = [x for x in os.listdir(chrome_path) if re.search(r'.exe$', x)]
            if len(files) == 1:
                file = files[0]
            else:
                file = [x for x in files if re.search(r'chrome.exe', x)][0]
            browser_path = os.path.join(chrome_path, file)
            return browser_path
        else:
            print("Navegador não instalado")
            return None
