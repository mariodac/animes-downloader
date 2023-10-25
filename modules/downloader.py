import sys
import os
import re
import shutil
import wx
import pyautogui
import pygetwindow as gw
sys.path.append(os.path.join(os.path.split(os.path.dirname(__file__))[0], "utils"))
sys.path.append(os.path.join(os.path.split(os.path.dirname(__file__))[0], "modules"))
import constants as cnst
from time import sleep
from web import Web
from common import Common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import getpass



class DownloaderAnime():
    def __init__(self):
        self.web = Web()
        self.common = Common()

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
            driver = self.web.init_webdriver(True, saida=saida)
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
            print('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.download_animes_episodes_fenix.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

    def login_saiko(self, save_path, web_driver:webdriver=None):
        try:
            if web_driver is None:
                    web_driver = self.web.init_webdriver(headless=False, saida=save_path)
            # acessa url de login da saiko
            web_driver.get("{}login".format(cnst.SAIKO_URL))
            sleep(3)
            # busca elemento de login
            elements = web_driver.find_elements(By.NAME, 'user_login')
            if elements:
                # obtem email digitado pelo usuário e envia para o elemento
                elements[0].send_keys(input('Digite seu email >> '))
                # busca elemento de senha
                elements = web_driver.find_elements(By.NAME, 'user_pass')
                if elements:
                    # envia senha digitada pelo usuário e envia para o elemento
                    elements[0].send_keys(getpass.getpass())
                    # busca pelo botão de login
                    elements = web_driver.find_elements(By.NAME, 'armFormSubmitBtn')
                    if elements:
                        elements[0].click()
                        # buscar elemento do avatar para verificar se logou com sucesso
                        elements = web_driver.find_elements(By.CSS_SELECTOR, '.avatar-content')
                        if elements:
                            print("Login efetuado com sucesso")
                        
            sleep(4)
            return web_driver
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.login_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            
    def logout_saiko(self, web_driver:webdriver):
        try:
            # busca elemento do avatar
            elements = web_driver.find_elements(By.ID, 'btn2')
            if elements:
                # clica no elemento
                elements[0].click()
                sleep(2)
                # busca o elemento de logout
                elements = web_driver.find_elements(By.CLASS_NAME, 'logout-btn')
                if elements:
                    elements[0].click()
                    # buscar elemento do avatar para verificar se deslogou com sucesso
                    elements = web_driver.find_elements(By.CSS_SELECTOR, '.avatar-content')
                    if len(elements) == 0:
                        print("Logout efetuado com sucesso")

        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_anime_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

    def get_anime_saiko(self, search:str, save_path, web_driver:webdriver=None):
        """
         Esta é uma função de web scrap para obter a lista de animações e seus nomes
         
         @param search - Uma termo para procurar
         @param save_path - Caminho para salvar os animes.
         @param web_driver - Selenium webdriver para usar se None novo será criado
         
         @return Instancia do driver e nome do anime escolhido
        """
        try:
            # Iniciar o driver web. Se nenhum driver web estiver configurado, o driver web padrão é usado.
            if web_driver is None:
                driver = self.web.init_webdriver(headless=False, saida=save_path)
            else:
                driver = web_driver
            sleep(4)
            driver.get("{}multimidia/?fwp_pesquisa={}".format(cnst.SAIKO_URL,search))
            site = self.web.web_scrap(markup=driver.page_source)
            # Lista de animes
            animes = site.find_all("div", "anilist")
            animes_names = []
            for item in animes:
                name = item.find("div", class_="title-list").text
                # Obtem o nome do anime
                if name:
                    audio = item.find('div', class_='audio-list')
                    # Verifica se anime é legendado ou dublado
                    if audio:
                        # Adicionado legendado ao nome do anime
                        if 'legendado' in audio.text.lower():
                            name = "{} - {}".format(name, audio.text)
                animes_names.append(name)
            index = -1
            if len(animes_names) == 1:
                index = 1
            elif len(animes_names) > 0:
                print("A pesquisa obteu os seguintes animes:")
                # Imprime os nomes de todos os animes na busca e obtem a escolha do usuario.
                index = self.get_anime_index(animes_names)
            else:
                print("Não foi encontrado nenhum resultado")
                return None,  None
            # Obter o índice do elemento da lista de anime
            if index in range(1, len(animes_names) + 1):
                driver.get(animes[index-1].a.get('href'))
                element = driver.find_elements(By.CLASS_NAME, 'info')
                # Verificar se anime está com acesso bloqueado
                if element:
                    sleep(3)
                    actions = ActionChains(driver)
                    actions.move_to_element(element[0]).perform()
                    element[0].click()
                    sleep(3)
                    element = driver.find_elements(By.ID, 'blockModalLabel')
                    # Se estiver com acesso bloqueado exibe mensagem
                    if element:
                        # Returnar o elemento da lista de proibição pelo seguinte motivo
                        if element[0].is_displayed():
                            print("Entrada proibido pelo seguinte motivo:")
                            print(element[0].text) 
                else:
                    print("Opção inválida")
                return driver, animes_names[index-1]
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_anime_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            return None, None

    def down_episodes_saiko(self,save_path:os.PathLike, url:str=None, web_driver:webdriver=None, name:str=None, limit:int=1):
        try:
            if webdriver is None:
                driver = self.web.init_webdriver(default=False,headless=False, saida=save_path)
                driver.get(url)
            else:
                driver = web_driver
            sleep(3)
            try:
                SCROLL_PAUSE_TIME = 2
                # Pega tamanho do scroll
                scroll_height = driver.execute_script("return document.evaluate('//div[@class=\"list-body\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                # obtem os episódios e rola até o ultimo episódio que está visível
                element = driver.find_elements(By.CLASS_NAME, 'container-down')
                ActionChains(driver).move_to_element(element[-1]).perform()
                # Define o tamanho de rolagem
                scroll_old = scroll_height
                while True:
                    # Pega tamanho do scroll
                    scroll_height = driver.execute_script("return document.evaluate('//div[@class=\"list-body\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                    # armazena tamanho antigo antes da rolagem
                    scroll_old = scroll_height
                    # obtem os episódios e rola até o ultimo episódio que está visível
                    element = driver.find_elements(By.CLASS_NAME, 'container-down')
                    ActionChains(driver).move_to_element(element[-1]).perform()
                    # Espera página carregar
                    sleep(SCROLL_PAUSE_TIME)
                    # Verifica se chegou no fim
                    scroll_height = driver.execute_script("return document.evaluate('//div[@class=\"list-body\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                    if scroll_old >= scroll_height:
                        break
            except Exception as err:
                exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.down_episodes_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            # define a quantidade de downloads a ser realizada
            downloads_count = 1
            # obtem itens da tabela
            lines_table = driver.find_elements(By.CLASS_NAME, 'container-down')
            # classificar lista de objetos com base em atributo do objeto
            lines_table = sorted(lines_table, key=lambda x: x.text, reverse=False)
            # ignora as linhas da tabela com os nomes das colunas
            lines_table = lines_table[1:]
            eps_names = [item.text.split('\n')[0] for index,item in enumerate(lines_table)]
            select_eps = self.get_anime_ep_index(eps_names)
            lines_table = self.select_range_episodes(select_eps, lines_table)
            
            for index, item in enumerate(lines_table):
                # incrementa a quantidade de downloads
                if index == downloads_count:
                    self.web.check_crdownload(save_path)
                    downloads_count += limit
                dir_name = None
                # nome da pasta
                if not name:
                    name = item.find_element(By.XPATH, '//td[@data-testid="col-name"]')
                    name = name.text
                    search_name = re.search(r'\[Saiko\-Animes\]_([A-Za-z0-9_]+)_|\[Saiko\-Animes\]_([\-A-Za-z0-9]+)_', name)
                    if search_name:
                        name_dir = search_name.group()
                        name_dir = name_dir.replace('[Saiko-Animes]_', '')
                        dir_name = self.common  (name_dir, save_path)
                else:
                    
                    dest_anime_dir = os.path.join(save_path, name)
                    new_dest_dir = (os.path.join(os.path.split(save_path)[0], os.path.split(dest_anime_dir)[-1]))
                    if os.path.isdir(new_dest_dir) is False:
                        dir_name = self.common.create_folder(name, save_path)
                # clica no episodio
                actions = ActionChains(driver)
                actions.move_to_element(item).perform()
                item.click()
                sleep(2)
                name_log = item.text.split('\n')[0]
                print('Iniciado download {}'.format(name_log))
            self.web.check_crdownload(save_path)
            downs = os.listdir(save_path)
            if dir_name:
                for item in downs:
                    if os.path.isfile(os.path.join(save_path, item)):
                        print(os.path.join(save_path, item), "->", os.path.join(dir_name, item))
                        shutil.move(os.path.join(save_path, item), dir_name)
            
                shutil.move(dir_name, os.path.split(save_path)[0])
            else:
                for item in downs:
                    if os.path.isfile(os.path.join(save_path, item)):
                        print(os.path.join(save_path, item), "->", os.path.join(new_dest_dir, item))
                        shutil.move(os.path.join(save_path, item), new_dest_dir)
            # logout = input("Deseja realizar o logout? (S)sim/(n)não\n-> ")
            # if 's' in logout.lower() or 'sim' in logout.lower() or 'si' in logout.lower() or 'yes' in logout.lower() or 'y' in logout.lower():
            self.logout_saiko(driver)
            driver.quit()
        except Exception as err:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.down_episodes_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, err))
            if driver:
                driver.quit()
    
    def get_anime_animefire_net(self, search:str):
        try:
            # formata busca para forma utilizada na url
            search = search.replace(' ', '-')
            search = search.lower()
            site = self.web.web_scrap(url='{}pesquisar/{}'.format(cnst.ANIMEFIRENET_URL, search))
            # obtem resultados da busca
            articles = site.find_all('article')
            # imprime nomes dos animes da busca
            if len(articles) == 1:
                index = 1
            elif len(articles) > 0:
                print("A pesquisa obteu os seguintes animes:")
                animes = [x.h3.text for x in articles if x.h3]
                index = self.get_anime_index(animes)
                # obtem o link do anime e o seu nome
            else:
                print("Nenhum anime encontrado")
                return None, None
            if index in range(1, len(articles) + 1):
                link = articles[index-1].a.get('href')
                anime_name = articles[index-1].h3.text      
            return link, anime_name
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_anime_animefire_net.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
     
    def down_episodes_animefire_net(self, url:str, anime_name:str, save_path:os.PathLike):
        try:
            dest_dir = self.common.create_folder(anime_name, save_path)
            site = self.web.web_scrap(url=url)
            # obtem lista com os episódios
            div_eps = site.find('div', class_='div_video_list')
            eps = div_eps.find_all('a')
            name_eps = [x.text for x in eps]
            select_eps = self.get_anime_ep_index(name_eps)
            # para selecionar o intervalo de episódios
            eps = self.select_range_episodes(select_eps, eps)
            print("Digite o numero da qualidade: ")
            for ep in eps:
                # abre o link do episodio
                site = self.web.web_scrap(url=ep.get('href'))
                # obtem o botão de download
                link = site.find('a', id='dw')
                site = self.web.web_scrap(url=link.get('href'))
                qualidades = site.find_all('a', class_='mb-1')
                qualidades_name = [x.text for x in qualidades]
                index = self.get_anime_index(qualidades_name)
                if index-1 in range(0, len(qualidades)):
                    # site = self.web.web_scrap(url=qualidades[index-1])
                    status = self.web.download_archive(url=qualidades[index-1].get('href'), path_archive=dest_dir)
                    if status is False:
                        driver = self.web.init_webdriver(default=False)
                        sleep(3)
                        self.web.check_driver(driver)
                        driver.get(ep.get('href'))
                        site = self.web.web_scrap(markup=driver.page_source)
                        iframe = site.find_all('iframe')
                        if iframe:
                            # entra no link do iframe
                            driver.get(iframe[0].get('src'))
                            # obtem o botão do video e clica
                            elements = driver.find_elements(By.CLASS_NAME, 'play-button')
                            if elements:
                                elements[0].click()
                                sleep(3)
                                new_iframe = driver.find_elements(By.ID, 'videocontainer')
                                if new_iframe:
                                    # troca pra o iframe
                                    driver.switch_to.frame(new_iframe[0])
                                    site = self.web.web_scrap(markup=driver.page_source)
                                    video = site.find('video')
                                    driver.get(video.get('src'))
                                    video = driver.find_elements(By.TAG_NAME, 'video')
                                    if video:
                                        video[0].click()
                                        # obtem a localização do video na tela
                                        localizacao = video[0].location
                                        x = localizacao['x']
                                        y = localizacao['y']
                                        # Obter o titulo da janela do WebDriver
                                        window_title = driver.current_url+' - Google Chrome'
                                        window_index = gw.getAllTitles().index(window_title)
                                        # Obter o objeto da janela usando o identificador
                                        window = gw.getWindowsWithTitle(gw.getAllTitles()[window_index])
                                        sleep(3)
                                        # Colocar a janela em foco
                                        try:
                                            window[0].activate()
                                        except Exception as err:
                                            if 'concluída' not in str(err):
                                                print(str(err))
                                                raise
                                        # clica com botão direito onde está localizado o vídeo
                                        pyautogui.click(x=x, y=y, button='right')
                                        # pressio a seta pra baixo 4 vezes, para chegar na opção "Salvar como"
                                        for x in range(0, 3):
                                            pyautogui.press('down')
                                        pyautogui.press('enter')
                                        # espera até a janela de salvar como aparecer
                                        while True:
                                            if 'Salvar como' in gw.getAllTitles():
                                                ep_name = self.common.normalize_name(ep.text)
                                                pyautogui.typewrite(os.path.join(dest_dir, ep_name))
                                                pyautogui.press('enter')
                                                break
                                            else:
                                                sleep(5)
                                                
                                        self.web.check_crdownload(dest_dir)
                    # download normal
                    else:
                        print("Sucesso")
                driver.quit()
                                
                                
                            
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.down_episodes_animefire_net.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    
    def click_ads(self, n_clicks:int, driver:webdriver):
        try:
            for x in range(0, n_clicks):
                driver.find_elements(By.TAG_NAME, 'body')[0].click()
                sleep(1)
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.click_ads.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    
    def select_range_episodes(self, select_eps:str, lista_eps:list):
        try:
            if '-' in select_eps:
                nums = [int(x)-1 for x in select_eps.split('-')]
                lista_eps = lista_eps[nums[0]:nums[1]+1]
            elif ',' in select_eps:
                nums = [int(x)-1 for x in select_eps.split(',')]
                lista_eps = [lista_eps[x] for x in nums]
            else:
                try:
                    int(select_eps)
                    lista_eps = [lista_eps[int(select_eps)-1]]
                except:
                    print("Intervalo não encontrado, será realizado o download de todos os episódios")
            return lista_eps
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.select_range_episodes.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    
    def get_anime_index(self, animes:list):
        try:
            for index, item in enumerate(animes):
                print("{} - {}".format(index+1, item))
            index = self.common.only_read_int("Digite o numero correspondente ao anime >> ")
            return index
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_anime_index.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            
    def get_anime_ep_index(self, episodes:list):
        try:
            while True:
                for index, item in enumerate(episodes):
                    print("{} - {}".format(index+1, item))
                print('Exemplos:\nUm itervalo de episódios 1-10\nDeterminados episódios 1,3,4\nTodos os episódios *')
                print('Digite o intervalo de episódios')
                select_eps = input('>> ')
                search = re.search('[0-9\-\,]+|[aA\*]', select_eps)
                if search != None: 
                    break
                else:
                    print("Opção inválida")
                    continue
            return select_eps
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_anime_ep_index.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
     
if __name__ == "__main__":
    # possiveis sites para baixar animes pelo script
    # https://animefire.to
    # https://animefire.net
    # https://www.hinatasoul.com
    # https://animesaria.com
    # https://animesorionvip.com
    # https://animeq.blog
    # https://www.anitube.vip
    # https://goyabu.org/
    # https://www.animesking.com
    # https://animeszone.net 
    # https://www.superanimes.biz
    # https://animesdigital.org
    # https://animesflix.net
    
    
    downloader = DownloaderAnime()
    common = downloader.common
    
    url, name = downloader.get_anime_animefire_net("Naruto Shippuuden")
    downloader.down_episodes_animefire_net(url, name, r'C:\Users\bros_\Videos')
    
    while True:
        # cria instancia da tela que não tera um pai (janela principal)
        app = wx.App(None)
        # cria um objeto de dialog de diretório sem um pai
        dialog = wx.DirDialog (None, "Escolha um diretório para salvar os animes", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        #verifica se o usuário clicou em ok
        if dialog.ShowModal() == wx.ID_OK: 
            # diretorio selecionado para criar diretório onde salvar imagens
            save_path = dialog.GetPath()
            break
        if dialog.ShowModal() == wx.ID_CLOSE_FRAME:
            print("Escolha o diretorio")
            continue 
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
        
        print("0 - SAIR\n1 - Baixar todos os episódios Saiko Animes")
        option = input("Digite -> ")
        if option == '1':
            t_i = common.initCountTime(True)
            login = input("Deseja realizar o login? (S)sim/(n)não\n-> ")
            out_path = common.create_folder("- Downloaded -", save_path)
            if 's' in login.lower() or 'sim' in login.lower() or 'si' in login.lower() or 'yes' in login.lower() or 'y' in login.lower():
                driver = downloader.login_saiko(save_path)
            else:
                driver = None
            search = input("Digite o nome do anime -> ")
            driver, name = downloader.get_anime_saiko(search=search, web_driver=driver, save_path=out_path)
            if driver and name:
                downloader.down_episodes_saiko(web_driver=driver, save_path=out_path, name=name)
            t_f = common.finishCountTime(t_i, True)
            common.print_time(t_f)
            
                