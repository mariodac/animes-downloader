import sys
import os
import re
import shutil
import wx
import utils.constants as cnst
from time import sleep
from modules.web import Web
from modules.common import Common
from modules.log import Logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



class DownloaderAnime():
    def __init__(self):
        self.logger = Logger(cnst.NAME_LOG)
        self.web = Web
        self.common = Common(cnst.NAME_LOG)
    def init_webdriver(self,default=True, headless=False, saida:os.PathLike=None):
        try:
            s=Service(ChromeDriverManager().install())
            if default:
                if headless:
                    driver = webdriver.Chrome(service=s, options=self.web.optionsChrome(headless=True))
                else:    
                    driver = webdriver.Chrome(service=s, options=self.web.optionsChrome(headless=False))    
            else:
                extension = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'extension', 'adblock.crx')
                try:
                    if headless:
                        driver = webdriver.Chrome(service=s, options=self.web.optionsChrome(headless=True, download_output=saida, crx_extension_pathname=extension))
                    else:
                        driver = webdriver.Chrome(service=s, options=self.web.optionsChrome(headless=False, download_output=saida, crx_extension_pathname=extension))
                except:
                    if headless:
                        driver = webdriver.Chrome(service=s, options=self.web.optionsChrome(headless=True, download_output=saida))
                    else:
                        driver = webdriver.Chrome(service=s, options=self.web.optionsChrome(headless=False, download_output=saida))
            return driver
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.getLogger().error('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.init_webdriver.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            sys.exit()

    def download_animes_episodes_fenix(self, url:str, save_path:os.PathLike):
        try:
            
            site = self.web.webScraping(url=url)
            episodes = site.find_all('div', class_='ep d-flex')
            series = site.find('span', class_='cat-series')
            if series:
                name = series.next_sibling
                name = name.strip()
                name = re.sub(r'[\\/:"*?!<>|]+', '', name)
                saida = self.common.create_folder(name, save_path)
            links = []
            for item in episodes:
                if item.find('a', title="mfire"):
                    links.append(item.find('a', title="mfire"))
            if links is None:
                print("Impossível baixar episódios")
                return
            links = [x.get('href') for x in links]
            file_name = r'{}/{}.txt'.format(saida.replace("\\", r"/"), name)
            if not os.path.isfile(file_name):
                file_get = open(file_name, 'x', encoding='utf-8')
                file_get.close()
            file_get = open(file_name, 'r+', encoding='utf-8')
            texts_file = file_get.readlines()
            texts_file = [x.replace('\n', '') for x in texts_file]
            driver = self.init_webdriver(True, saida=saida)
            for index,link in enumerate(links):
                print("Baixando episodio {} de {}".format(index+1, len(links)))
                driver.get(link)
                # obtem site de download
                site = self.web.webScraping(markup=driver.page_source)
                # busca elemento
                elements = site.find('font', text="Name:")
                if elements:
                    # busca do elemento com o nome do arquivo
                    elements = [x for x in elements.next_elements if x.name == 'font' if re.search("\.[0-9a-z]+$", x.text)]
                    # se achar o elemento pega a string com o nome
                    if elements:
                        file_name = elements[0].text
                    else:
                        file_name = "None - {}".format(index)
                # verifica se o nome do arquivo está na lista do arquivo txt
                if file_name in texts_file:
                    continue
                # verifica se o link está na lista do arquivo txt
                if link in texts_file:
                    continue
                lrbox = site.find(id="lrbox")
                if lrbox:
                    if re.search('File has expired and does not exist anymore on this server', lrbox.text):
                        print("Arquivo {} não disponível neste link {}".format(file_name, link))
                        continue
                try:
                    new_link = driver.find_element(By.ID, 'dlbutton')
                except:
                    new_link = None
                if new_link:
                    new_link = new_link.get_attribute('href')
                file_down = self.web.downloadArchive(url=new_link, path_archive=saida)
                if file_down:
                    file_get.write('{} - {}\n'.format(link, file_down))
            file_get.close() 
            driver.quit()
        except:
            exc_type,exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.getLogger().error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.download_animes_episodes_fenix.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

    def get_anime_saiko(self, search:str):
        try:
            driver = self.init_webdriver(headless=False)
            driver.get("https://saikoanimes.net")
            driver.quit()
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.getLogger().error('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_anime_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

    def down_episodes_saiko(self, url:str, save_path:os.PathLike, name:str=None, limit:int=1):
        try:
            driver = self.init_webdriver(default=False,headless=False, saida=save_path)
            driver.get(url)
            sleep(3)
            try:
                SCROLL_PAUSE_TIME = 2
                # Pega tamanho do scroll
                scroll_height = driver.execute_script("return document.evaluate('//table', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                # pressiona pgup
                element = driver.find_elements(By.TAG_NAME, 'td')
                element[-1].send_keys(Keys.END)
                # Define o tamanho de rolagem
                scroll_old = scroll_height
                while True:
                    # Pega tamanho do scroll
                    scroll_height = driver.execute_script("return document.evaluate('//table', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                    # armazena tamanho antigo antes da rolagem
                    scroll_old = scroll_height
                    # pressiona pgup
                    element = driver.find_elements(By.TAG_NAME, 'td')
                    element[-1].send_keys(Keys.END)
                    # Espera página carregar
                    sleep(SCROLL_PAUSE_TIME)
                    # Verifica se chegou no fim
                    scroll_height = driver.execute_script("return document.evaluate('//table', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                    if scroll_old >= scroll_height:
                        break
            except Exception as err:
                exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                self.log.getLogger().error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.down_episodes_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            # define a quantidade de downloads a ser realizada
            downloads_count = 1
            # classificar lista de objetos com base em atributo do objeto
            lines_table = sorted(lines_table, key=lambda x: x.text, reverse=False)
            # ignora as linhas da table com icone de pasta
            lines_table = [x for x in lines_table if "folder-file-color" not in x.find_element(By.TAG_NAME, 'svg').get_attribute('class')]
            [print(index+1, '-', item.text.split('\n')[0]) for index,item in enumerate(lines_table)]
            while True:
                print('Exemplos:\nUm itervalo de episódios 1-10\nDeterminados episódios 1,3,4\nTodos os episódios*')
                print('Digite os intervalos dos episódios')
                text = input('>> ')
                search = re.search('[0-9\-\,]+|[aA\*]', text)
                if search != None: break
            if '-' in text:
                nums = [int(x)-1 for x in text.split('-')]
                lines_table = lines_table[nums[0]:nums[1]+1]
            elif ',' in text:
                nums = [int(x)-1 for x in text.split(',')]
                lines_table = [lines_table[x] for x in nums]
            for index, item in enumerate(lines_table):
                # nome do arquivo
                if index == downloads_count:
                    self.common.check_crdownload(save_path)
                    downloads_count += limit
                if not name:
                    name = item.find_element(By.XPATH, '//td[@data-testid="col-name"]')
                    name = name.text
                    search_name = re.search(r'\[Saiko\-Animes\]_([A-Za-z0-9_]+)_|\[Saiko\-Animes\]_([\-A-Za-z0-9]+)_', name)
                    if search_name:
                        name_dir = search_name.group()
                        name_dir = name_dir.replace('[Saiko-Animes]_', '')
                        dir_name = self.common  (name_dir, save_path)
                else:
                    dir_name = self.common.create_folder(name, save_path)
                actions = ActionChains(driver)
                actions.move_to_element(item).perform()
                item.click()
                sleep(2)
                try:
                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
                except:
                    exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    self.log.getLogger().error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.down_episodes_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
                # buscando video
                element = driver.find_elements(By.TAG_NAME, 'video')
                if element:
                    element[0].click()
                
                # buscando link do arquivo1
                # element = driver.find_elements(By.TAG_NAME, 'source')
                # if element:
                #     url = element[0].get_attribute('src')
                # buscando botões da pagina
                element = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME,'button')))
                if element:
                    # filtrando botão de download
                    download = [x for x in element if x.text=="Download"]
                    download[0].click()
                else:
                    # filtrando botão de download
                    download = [x for x in element if x.text=="Download"]
                    download[0].click()
                sleep(2)
                name_log = item.text.split('\n')[0]
                self.logger.getLogger().info('Iniciado download {}'.format(name_log))
                if element:
                    if len(element) == 7:
                        element[-1].click()
                    else:
                        element[-2].click()
                    sleep(2)
            self.common.check_crdownload(save_path)
            downs = os.listdir(save_path)
            for item in downs:
                if os.path.isfile(os.path.join(save_path, item)):
                    print(os.path.join(save_path, item), "->", os.path.join(dir_name, item))
                    shutil.move(os.path.join(save_path, item), dir_name)
            driver.quit()
            print()
            r'\[Saiko\-Animes\]_([A-Za-z0-9])\w+'
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.getLogger().error('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.down_episodes_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
        
if __name__ == "__main__":
    # possiveis sites para baixar animes pelo script
    # https://www.hinatasoul.com
    # https://animefire.net
    # https://animesaria.com
    # https://animesorionvip.com
    # https://animeq.blog
    
    downloader = DownloaderAnime()
    common = downloader.common
    
    
    while True:
        # cria instancia da tela que não tera um pai (janela principal)
        app = wx.App(None)
        # cria um objeto de dialog de diretório sem um pai
        dialog = wx.DirDialog (None, "Escolha um diretório", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        #verifica se o usuário clicou em ok
        if dialog.ShowModal() == wx.ID_OK: 
            # diretorio selecionado para criar diretório onde salvar imagens
            save_path = dialog.GetPath()
            break
        else:
            print("Escolha o diretorio")

    # destroi os objetos para liberar a memória
    dialog.Destroy()
    app.Destroy()
    
    option = -1
    list_episodes = []
    
    sleep(2)
    regex = re.compile('((?:https\:\/\/)|(?:http\:\/\/)|(?:www\.))?([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(?:\??)[a-zA-Z0-9\-\._\?\,\'\/\\\+&%\$#\=~]+)')
    while option != '0':
        
        print("0 - SAIR\n1 - baixar todos episodios - Fenixsub\n2 - Baixar todos os episódios Saiko Animes")
        option = input("Digite -> ")
        if option == '2':
            while True:
                t_i = common.initCountTime(True)
                url = input("Digite o URL -> ")
                if regex.match(url):
                    name = input("Nome -> ")
                    if name:
                        downloader.down_episodes_saiko(url, common.criarPasta("- Downloaded -", save_path), name)
                    else:
                        downloader.down_episodes_saiko(url, common.criarPasta("- Downloaded -", save_path))
                    break
                else:
                    print('URL inválida')
                    continue
            t_f = common.finishCountTime(t_i, True)
            common.print_time(t_f)
            
                