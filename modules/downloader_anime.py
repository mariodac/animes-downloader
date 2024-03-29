import sys
import os
import re
import shutil
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
    def __init__(self, save_path:str):
        """
        Classe para funções de baixar animes
        
        Iniciar as variáveis de classe e criar instâncias de classes Web e Common.

        Args:
            save_path (str): caminho para salvar episódios de animes
        """
        self.web = Web()
        self.common = Common()
        self.save_path = save_path
        self.web_driver = self.web.init_webdriver(default=False, output=self.save_path)
        self.web_driver.minimize_window()
        self.web_driver_wait = WebDriverWait(self.web_driver, 60)

    def __del__(self):
        """Função destrutora, fecha o navegador
        """
        self.web.try_quit_webdriver(self.web_driver)

    def download_animes_episodes_fenix(self, url:str):
        """Download de episódios de animes do site fenixfansublix

        Args:
            url (str): url do animes
            save_path (str): local para salvar videos do episódios
        """
        try:
            # obtem dados da url
            site = self.web.webScraping(url=url)
            # Obtem o nome do anime e criar um diretorio com o nome
            episodes = site.find_all('div', class_='ep d-flex')
            series = site.find('span', class_='cat-series')
            if series:
                name = series.next_sibling
                name = name.strip()
                name = re.sub(r'[\\/:"*?!<>|]+', '', name)
                saida = self.common.create_folder(name, self.save_path)
            # Obtem os episódios do anime
            links = []
            for item in episodes:
                if item.find('a', title="mfire"):
                    links.append(item.find('a', title="mfire"))
            if links is None:
                print("Impossível baixar episódios")
                return
            # filtra pelas url dos episódios
            links = [x.get('href') for x in links]
            # monta caminho do arquivo
            file_name = r'{}/{}.txt'.format(saida.replace("\\", r"/"), name)
            if not os.path.isfile(file_name):
                file_get = open(file_name, 'x', encoding='utf-8')
                file_get.close()
            file_get = open(file_name, 'r+', encoding='utf-8')
            texts_file = file_get.readlines()
            texts_file = [x.replace('\n', '') for x in texts_file]
            self.web_driver = self.web.init_webdriver(True, output=saida)
            for index,link in enumerate(links):
                print("Baixando episodio {} de {}".format(index+1, len(links)))
                self.web_driver.get(link)
                # obtem site de download
                site = self.web.webScraping(markup=self.web_driver.page_source)
                # busca elemento
                elements = site.find('font', text="Name:")
                if elements:
                    # busca do elemento com o nome do arquivo
                    elements = [x for x in elements.next_elements if x.name == 'font' if re.search(r"\.[0-9a-z]+$", x.text)]
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
                    new_link = self.web_driver.find_element(By.ID, 'dlbutton')
                except:
                    new_link = None
                if new_link:
                    new_link = new_link.get_attribute('href')
                file_down = self.web.downloadArchive(url=new_link, path_archive=saida)
                if file_down:
                    file_get.write('{} - {}\n'.format(link, file_down))
            file_get.close() 
        except:
            exc_type,exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.download_animes_episodes_fenix.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

    def login_saiko(self,):
        """Realiza o login no site Saiko Animes
        """
        try:
            # acessa url de login da saiko
            self.web_driver.get("{}login".format(cnst.AGREGADOR_ANIME.get('saiko')))
            sleep(3)
            # busca elemento de login
            elements = self.web_driver.find_elements(By.NAME, 'user_login')
            if elements:
                # obtem email digitado pelo usuário e envia para o elemento
                elements[0].send_keys(input('Digite seu email >> '))
                # busca elemento de senha
                elements = self.web_driver.find_elements(By.NAME, 'user_pass')
                if elements:
                    # envia senha digitada pelo usuário e envia para o elemento
                    elements[0].send_keys(getpass.getpass())
                    # busca pelo botão de login
                    elements = self.web_driver.find_elements(By.NAME, 'armFormSubmitBtn')
                    if elements:
                        elements[0].click()
                        # buscar elemento do avatar para verificar se logou com sucesso
                        elements = self.web_driver.find_elements(By.CSS_SELECTOR, '.avatar-content')
                        if elements:
                            print("Login efetuado com sucesso")
                        
            sleep(4)
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.login_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            
    def logout_saiko(self):
        """Realiza logout do site Saiko Animes
        """        
        try:
            # busca elemento do avatar
            elements = self.web_driver.find_elements(By.ID, 'btn2')
            if elements:
                # clica no elemento
                elements[0].click()
                sleep(2)
                # busca o elemento de logout
                elements = self.web_driver.find_elements(By.CLASS_NAME, 'logout-btn')
                if elements:
                    elements[0].click()
                    # buscar elemento do avatar para verificar se deslogou com sucesso
                    elements = self.web_driver.find_elements(By.CSS_SELECTOR, '.avatar-content')
                    if len(elements) == 0:
                        print("Logout efetuado com sucesso")

        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.logout_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

    def get_anime_saiko(self, search:str):
        """
        Obter o anime de uma pesquisa

        Realiza a pesquisa digitada pelo usuário, retorna o nome do anime escolhido

        Args:
            search (str): Anime a ser pesquisado

        Returns:
            str: nome do anime escolhido
        """
        try:
            sleep(4)
            self.web_driver.get("{}multimidia/?fwp_pesquisa={}".format(cnst.AGREGADOR_ANIME.get('saiko'),search))
            site = self.web.web_scrap(markup=self.web_driver.page_source)
            sleep(2)
            # Lista de animes
            animes = site.find_all("div", "anilist")
            animes_names = []
            for item in animes:
                name = item.find("div", class_="title-list")
                if name:
                    name = name.text
                else:
                    name = "None"
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
                index = self.get_option_index(animes_names)
            else:
                print("Não foi encontrado nenhum resultado")
                return None
            # Obter o índice do elemento da lista de anime
            if index in range(1, len(animes_names) + 1):
                self.web_driver.get(animes[index-1].a.get('href'))
                download_area = self.web_driver.find_elements(By.CLASS_NAME, 'column-ani')
                site = self.web.web_scrap(markup=self.web_driver.page_source)
                # Verificar se anime está com acesso bloqueado
                if download_area:
                    sleep(3)
                    if len(download_area) > 1:
                        print('Temporada disponíveis: ')
                        seasons = [x.text.replace('mais informações\nWEB\n', '').replace('\n', ' - ') for x in download_area]
                        season_choice = self.get_option_index(seasons)
                        actions = ActionChains(self.web_driver)
                        actions.move_to_element(download_area[season_choice-1]).perform()
                        download_area[season_choice-1].click()
                    else:
                        actions = ActionChains(self.web_driver)
                        actions.move_to_element(download_area[0]).perform()
                        download_area[0].click()
                        sleep(3)
                    element = self.web_driver.find_elements(By.ID, 'blockModalLabel')
                    # Se estiver com acesso bloqueado exibe mensagem
                    if element:
                        # Retorna o elemento da lista de proibição pelo seguinte motivo
                        if element[0].is_displayed():
                            print("Entrada proibido pelo seguinte motivo:")
                            print(element[0].text) 
                            return None
                else:
                    print("Opção inválida")
                return seasons[season_choice-1]
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_anime_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            return None, None

    def down_episodes_saiko(self, save_path,anime_name:str, limit:int=1):
        """Baixar episódios do site Saiko Animes

        Args:
            save_path (str,): Diretório onde irá baixar os episódios.
            name (str): nome do anime.
            limit (int, optional): limite de downloads. Defaults to 1.
        """
        try:
            # rola pela página de episódios
            try:
                SCROLL_PAUSE_TIME = 2
                # Pega tamanho do scroll
                scroll_height = self.web_driver.execute_script("return document.evaluate('//div[@class=\"list-body\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                # obtem os episódios e rola até o ultimo episódio que está visível
                element = self.web_driver.find_elements(By.CLASS_NAME, 'container-down')
                ActionChains(self.web_driver).move_to_element(element[-1]).perform()
                # Define o tamanho de rolagem
                scroll_old = scroll_height
                while True:
                    # Pega tamanho do scroll
                    scroll_height = self.web_driver.execute_script("return document.evaluate('//div[@class=\"list-body\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                    # armazena tamanho antigo antes da rolagem
                    scroll_old = scroll_height
                    # obtem os episódios e rola até o ultimo episódio que está visível
                    element = self.web_driver.find_elements(By.CLASS_NAME, 'container-down')
                    ActionChains(self.web_driver).move_to_element(element[-1]).perform()
                    # Espera página carregar
                    sleep(SCROLL_PAUSE_TIME)
                    # Verifica se chegou no fim
                    scroll_height = self.web_driver.execute_script("return document.evaluate('//div[@class=\"list-body\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                    if scroll_old >= scroll_height:
                        break
            except Exception as err:
                exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.down_episodes_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            # define a quantidade de downloads a ser realizada
            downloads_count = 1
            # obtem itens da tabela
            lines_table = self.web_driver.find_elements(By.CLASS_NAME, 'container-down')
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
                if not anime_name:
                    anime_name = item.find_element(By.XPATH, '//td[@data-testid="col-name"]')
                    anime_name = anime_name.text
                    search_name = re.search(r'\[Saiko\-Animes\]_([A-Za-z0-9_]+)_|\[Saiko\-Animes\]_([\-A-Za-z0-9]+)_', anime_name)
                    if search_name:
                        name_dir = search_name.group()
                        name_dir = name_dir.replace('[Saiko-Animes]_', '')
                        dir_name = self.common.create_folder(name_dir, save_path)
                else:
                    
                    dest_anime_dir = os.path.join(save_path, anime_name)
                    new_dest_dir = (os.path.join(os.path.split(save_path)[0], os.path.split(dest_anime_dir)[-1]))
                    if os.path.isdir(new_dest_dir) is False:
                        dir_name = self.common.create_folder(anime_name, save_path)
                # clica no episodio
                actions = ActionChains(self.web_driver)
                actions.move_to_element(item).perform()
                item.click()
                sleep(2)
                name_log = item.text.split('\n')[0]
                print('Iniciado download {}'.format(name_log))
                self.web.check_crdownload(save_path)
            downs = os.listdir(save_path)
            # move arquivo baixados para o diretório do anime
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
            self.logout_saiko()
        except Exception as err:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.down_episodes_saiko.__name__,exc_type, fname, exc_tb.tb_lineno, err))
    
    def get_anime_animefire_net(self, search:str):
        """Baixar animes do site animesfire.net

        Args:
            search (str): _description_

        Returns:
            str, str: link do anime e nome do anime
        """
        try:
            print(f'Realizando busca do anime "{search}"')
            # formata busca para forma utilizada na url
            search = search.replace(' ', '-')
            search = search.lower()
            site = self.web.web_scrap(url='{}pesquisar/{}'.format(cnst.AGREGADOR_ANIME.get("animefire.net"), search))
            # obtem resultados da busca
            articles = site.find_all('article')
            # imprime nomes dos animes da busca e solicita a entrada do usuário
            if len(articles) == 1:
                index = 1
            elif len(articles) > 0:
                print("A pesquisa obteu os seguintes animes:")
                animes = [x.h3.text for x in articles if x.h3]
                index = self.get_option_index(animes)
            else:
                print("Nenhum anime encontrado")
                return None, None
            # obtem o link do anime e o seu nome
            if index in range(1, len(articles) + 1):
                link = articles[index-1].a.get('href')
                anime_name = articles[index-1].h3.text      
            return link, anime_name
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_anime_animefire_net.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
     
    def down_episodes_animefire_net(self, url:str, anime_name:str, save_path:str):
        """Baixar episódios de anime do site AnimeFire.net

        Args:
            url (str): URL do anime 
            anime_name (str): Nome do anime
            save_path (str): Diretório onde irá baixar os episódios
        """
        try:
            # cria diretorio com o nome do anime
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
            selected_resolution = False
            for ep in eps:
                # abre o link do episodio
                site = self.web.web_scrap(url=ep.get('href'))
                # obtem o botão de download
                link = site.find('a', id='dw')
                site = self.web.web_scrap(url=link.get('href'))
                resolutions = site.find_all('a', class_='mb-1')
                resolutions_name = []
                for item_resolution in resolutions:
                    if item_resolution.text == 'SD':
                        resolution_name = f'{item_resolution.text} (640 x 480)'
                    elif item_resolution.text == 'HD':
                        resolution_name = f'{item_resolution.text} (1280 x 720)'
                    elif item_resolution.text == 'F-HD':
                        resolution_name = f'{item_resolution.text} (1920 x 1080)'
                    resolutions_name.append(resolution_name)
                if selected_resolution is False:
                    index = self.get_option_index(resolutions_name)
                    selected_resolution = True
                try:
                    resolutions[index-1]
                except IndexError:
                    index = 1
                if index-1 in range(0, len(resolutions)):
                    # site = self.web.web_scrap(url=qualidades[index-1])
                    status = self.web.download_archive(url=resolutions[index-1].get('href'), path_archive=dest_dir)
                    if status is False:
                        self.web_driver = self.web.init_webdriver(default=False)
                        sleep(3)
                        self.web.check_driver(self.web_driver)
                        self.web_driver.get(ep.get('href'))
                        site = self.web.web_scrap(markup=self.web_driver.page_source)
                        iframe = site.find_all('iframe')
                        if iframe:
                            # entra no link do iframe
                            self.web_driver.get(iframe[0].get('src'))
                            # obtem o botão do video e clica
                            elements = self.web_driver.find_elements(By.CLASS_NAME, 'play-button')
                            if elements:
                                elements[0].click()
                                sleep(3)
                                new_iframe = self.web_driver.find_elements(By.ID, 'videocontainer')
                                if new_iframe:
                                    # troca pra o iframe
                                    self.web_driver.switch_to.frame(new_iframe[0])
                                    site = self.web.web_scrap(markup=self.web_driver.page_source)
                                    video = site.find('video')
                                    self.web_driver.get(video.get('src'))
                                    video = self.web_driver.find_elements(By.TAG_NAME, 'video')
                                    if video:
                                        video[0].click()
                                        # obtem a localização do video na tela
                                        screen_location = video[0].location
                                        x = screen_location['x']
                                        y = screen_location['y']
                                        # Obter o titulo da janela do WebDriver
                                        window_title = self.web_driver.current_url+' - Google Chrome'
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
                                        # pressiona a seta pra baixo 4 vezes, para chegar na opção "Salvar como"
                                        for x in range(0, 3):
                                            pyautogui.press('down')
                                        pyautogui.press('enter')
                                        # espera até a janela de salvar como aparecer
                                        while True:
                                            # verifica se janela de salvar como aparece e aperta para iniciar o download
                                            if 'Salvar como' in gw.getAllTitles():
                                                ep_name = self.common.normalize_name(ep.text)
                                                pyautogui.typewrite(os.path.join(dest_dir, ep_name))
                                                pyautogui.press('enter')
                                                break
                                            else:
                                                sleep(5)
                                        # verifica se download encerrou
                                        self.web.check_crdownload(dest_dir)
                    else:
                        print("Sucesso")
            
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.down_episodes_animefire_net.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    
    def click_ads(self, n_clicks:int):
        """Clica nos ads para liberar conteudo

        Args:
            n_clicks (int): quantidades de cliques
        """
        try:
            for x in range(0, n_clicks):
                self.web_driver.find_elements(By.TAG_NAME, 'body')[0].click()
                sleep(1)
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.click_ads.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    
    def select_range_episodes(self, select_eps:str, lista_eps:list):
        """obtem o quais episódios serão baixados

        Args:
            select_eps (str): intervalo de episódios
            lista_eps (list): Lista de episódeios

        Returns:
            list: lista de episódios a ser baixados
        """
        try:
            if '-' in select_eps:
                nums = [int(x)-1 for x in select_eps.split('-')]
                lista_eps = lista_eps[nums[0]:nums[1]+1]
            elif ',' in select_eps:
                nums = [int(x)-1 for x in select_eps.split(',')]
                lista_eps = [lista_eps[x] for x in nums]
            elif '*' in select_eps:
                lista_eps = lista_eps
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
    
    def get_option_index(self, items:list):
        """Exibe itens da lista e solicita a escolha para o usuário

        Args:
            items (list): Items a ser exibidos

        Returns:
            int: escolha do usuário
        """
        try:
            for index, item in enumerate(items):
                print("{} - {}".format(index+1, item))
            index = self.common.only_read_int("Digite o numero correspondente a uma opção>> ")
            return index
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_option_index.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            
    def get_anime_ep_index(self, episodes:list):
        """Exibe lista de episódios do anime e solicita o intervalo de episódios a ser baixar

        Args:
            episodes (list): Lista de episódios

        Returns:
            int: Intervalo de episódios escolhidos
        """
        try:
            while True:
                for index, item in enumerate(episodes):
                    print("{} - {}".format(index+1, item))
                print('Exemplos:\nUm itervalo de episódios 1-10\nDeterminados episódios 1,3,4\nTodos os episódios *')
                print('Digite o intervalo de episódios')
                select_eps = input('>> ')
                search = re.search(r'[0-9\-\,]+|[aA\*]', select_eps)
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
    
    def login_anitsu(self):
        try:
            regex = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
            self.web_driver.get('https://anitsu.online/login')
            email = input('Digite o e-mail -> ')
            while regex.match(email) is None:
                print('Digite um e-mail válido')
                email = input('Digite o e-mail -> ')
            passwd = getpass.getpass('Digite a senha -> ')
            email_element = self.web_driver.find_elements(By.CSS_SELECTOR, '.mantine-Input-input.mantine-TextInput-input')
            if email_element is not None:
                email_element[0].send_keys(email)
            else:
                return False
            password_element = self.web_driver.find_elements(By.CSS_SELECTOR, '.mantine-PasswordInput-innerInput')
            if password_element is not None:
                password_element[0].send_keys(passwd)
            else:
                return False
            login = self.web_driver.find_elements(By.CSS_SELECTOR, '.mantine-focus-auto.mantine-active.mantine-Button-root.mantine-UnstyledButton-root')
            self.web_driver.maximize_window()
            if login is not None:
                login[0].click()
                print('Realizando login ...')
            else:
                return False
            sleep(3)
            return True
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.login_anitsu.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

    def scroll_bottom_anitsu(self, url=None):
        if url is not None:
            self.web_driver.get(url)
        SCROLL_PAUSE_TIME = 2
        # elementos da lista
        items_td = self.web_driver.find_elements(By.XPATH, '//td[@class="filename"]')
        # Pega tamanho do scroll
        scroll_height = self.web_driver.execute_script("return document.getElementById('files-public-content').scrollHeight")
        # rola até o ultimo episódio que está visível
        self.web_driver.execute_script("arguments[0].scrollIntoView();", items_td[-1])
        # Define o tamanho de rolagem
        scroll_old = scroll_height
        while True:
            # Pega tamanho do scroll
            items_td = self.web_driver.find_elements(By.XPATH, '//td[@class="filename"]')
            scroll_height = self.web_driver.execute_script("return document.getElementById('files-public-content').scrollHeight")
            # armazena tamanho antigo antes da rolagem
            scroll_old = scroll_height
            # rola até o ultimo episódio que está visível
            self.web_driver.execute_script("arguments[0].scrollIntoView();", items_td[-1])
            # Espera página carregar
            sleep(SCROLL_PAUSE_TIME)
            # Verifica se chegou no fim
            scroll_height = self.web_driver.execute_script("return document.getElementById('files-public-content').scrollHeight")
            if scroll_old >= scroll_height:
                break
    
    def search_anitsu(self):
        try:
            is_not_files = True
            while is_not_files:
                self.scroll_bottom_anitsu()
                items_td = self.web_driver.find_elements(By.XPATH, '//td[@class="filename"]')
                # items_td = self.web_driver_wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//td[@class="filename"]')))
                items = [x.text for x in items_td  if x.text != 'Readme\n.md']
                if items[0].endswith('.mkv') or items[0].endswith('.mp4') or items[0].endswith('.cbz') or items[0].endswith('.rar') or items[0].endswith('.zip'):
                    is_not_files = False
                options = dict(zip(range(1, len(items)+1), items))
                if is_not_files:
                    for key, item in options.items(): print(f'{key} - {item}')
                    self.web_driver.minimize_window()
                    op = self.common.only_read_int('Selecione uma opção -> ')
                    self.web_driver.maximize_window()
                    ActionChains(self.web_driver).move_to_element(items_td[op-1]).perform()
                    app_interable = self.web_driver.find_elements(By.ID, 'app-content')
                    app_interable[0].send_keys(Keys.DOWN)
                    app_interable[0].send_keys(Keys.DOWN)
                    sleep(3)
                    items_td[op-1].click()
                    sleep(10)
            while True:
                for key, item in options.items(): print(f'{key} - {item}')
                print('Exemplos:\nUm itervalo de episódios 1-10\nDeterminados episódios 1,3,4\nTodos os episódios *')
                print('Digite o intervalo de episódios')
                self.web_driver.maximize_window()
                select_eps = input('>> ')
                search = re.search(r'[0-9\-\,]+|[aA\*]', select_eps)
                if search != None: 
                    break
                else:
                    print("Opção inválida")
                    continue
            selected_items = self.select_range_episodes(select_eps, items_td)
            return selected_items
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.search_anitsu.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            
    def downdload_anitsu(self, search:bool, url:str=None):
        try:
            if search is True:
                is_logged = self.login_anitsu()
                if is_logged is False or is_logged is None:
                    raise Exception('Erro ao realizar login')
                acervo_link = self.web_driver.find_elements(By.CSS_SELECTOR, '.mantine-focus-auto.mantine-Text-root.mantine-Anchor-root')
                if acervo_link is not None:
                    acervo_link = [x for x in acervo_link if 'anitsu' in x.get_attribute('href')]
                    link = acervo_link[0].get_attribute('href')
                    self.web_driver.get(link)
                    sleep(2)
                    self.scroll_bottom_anitsu()
                    selected_items = self.search_anitsu()
                else:
                    print('Erro ao obter link do acervo')
                    return 
            elif url is not None and search is False:
                self.web_driver.get(url)
            sleep(2)
            element = self.web_driver.find_elements(By.XPATH,'//div[@class="breadcrumb"]//div/following-sibling::div[4]')
            sleep(2)
            name = "000"
            if element:
                name_dir = element[0].text
                dir_name = self.common.create_folder(name_dir, self.save_path)
            else:
                element = self.web_driver.find_elements(By.XPATH, '//div[@class="crumb svg"]')
                if element:
                    name_dir = element[0].text
                    dir_name = self.common.create_folder(name_dir, self.save_path)
                else:
                    dest_anime_dir = os.path.join(self.save_path, name)
                    new_dest_dir = (os.path.join(os.path.split(self.save_path)[0], os.path.split(dest_anime_dir)[-1]))
                    if os.path.isdir(new_dest_dir) is False:
                        dir_name = self.common.create_folder(name, self.save_path)
            self.scroll_bottom_anitsu()
            """ SCROLL_PAUSE_TIME = 2
            # Pega tamanho do scroll
            scroll_height = self.web_driver.execute_script("return document.getElementById(\"files-public-content\").scrollHeight")
            # rola até o ultimo episódio que está visível
            self.web_driver.execute_script("document.getElementById(\"files-public-content\").scrollIntoView(false)")
            # Define o tamanho de rolagem
            scroll_old = scroll_height
            while True:
                # Pega tamanho do scroll
                scroll_height = self.web_driver.execute_script("return document.getElementById(\"files-public-content\").scrollHeight")
                # armazena tamanho antigo antes da rolagem
                scroll_old = scroll_height
                # rola até o ultimo episódio que está visível
                self.web_driver.execute_script("document.getElementById(\"files-public-content\").scrollIntoView(false)")
                # Espera página carregar
                sleep(SCROLL_PAUSE_TIME)
                # Verifica se chegou no fim
                scroll_height = self.web_driver.execute_script("return document.getElementById(\"files-public-content\").scrollHeight")
                if scroll_old >= scroll_height:
                    break """
            if not search:
                elements = self.web_driver.find_elements(By.XPATH, '//a[@class="name"]')
            else:
                elements = selected_items
            if elements:
                # entrar em cada vídeo
                """ for index in range(len(elements)):
                    elements = self.web_driver.find_elements(By.XPATH, '//a[@class="name"]')
                    ActionChains(self.web_driver).move_to_element(elements[index]).perform()
                    sleep(2)
                    elements[index].click()
                    sleep(2)
                    element = self.web_driver.find_elements(By.XPATH, '//div[@class="plyr__poster"]')
                    sleep(2)
                    if element: element[0].click()
                    sleep(2)
                    element = self.web_driver.find_elements(By.XPATH,'//div[@class="icons-menu"]//a')
                    if element:
                        link = element[0].get_attribute('href')
                        print(link)
                        element = self.web_driver.find_elements(By.XPATH,'//button[@class="button-vue header-close button-vue--icon-only button-vue--vue-tertiary"]')
                        if element: 
                            element[0].click() """
                for item in elements:
                    # busca o elemento com o nome do arquivo
                    element = item.find_elements(By.CLASS_NAME, 'nametext')
                    index = elements.index(item)
                    name_file = element[0].text.replace("\n","")
                    # move para o elemento atual
                    ActionChains(self.web_driver).move_to_element(item).perform()
                    # caminho onde é baixado o video
                    out_dir_name = os.path.join(self.save_path, name_file)
                    # caminho com o nome do anime
                    new_dir_name = os.path.join(out_dir_name, name_file)
                    if (os.path.isfile(out_dir_name)): continue
                    elif (os.path.isfile(new_dir_name)): continue
                    else:
                        # busca o elemento de fechar player do video
                        element = self.web_driver.find_elements(By.XPATH,'//button[@class="button-vue header-close button-vue--icon-only button-vue--vue-tertiary"]')
                        if element: 
                            element[0].click()
                        # busca o elemento de acoes do arwuivo
                        element = item.find_elements(By.CLASS_NAME, 'fileactions')
                        if element:
                            # tenta mover para o elemento
                            try:
                                self.web_driver.execute_script("arguments[0].scrollIntoView({block:'center'});",element[0])
                                element[0].click()
                            except:
                                print(f"{name_file} Falhou")
                                continue
                            sleep(2)
                            element = self.web_driver.find_elements(By.XPATH, '//div[@class="fileActionsMenu popovermenu bubble open menu"]')
                            if element:
                                self.web_driver.execute_script("arguments[0].scrollIntoView({block:'center'});",element[0])
                                sleep(2)
                                element[0].click()
                                sleep(2)
                                element =item.find_elements(By.CLASS_NAME, 'nametext')
                                if element:
                                    #element[0].click()
                                    sleep(2)
                                    self.web.check_crdownload(self.save_path)
                downs = os.listdir(self.save_path)
                # move arquivo baixados para o diretório do anime
                if dir_name:
                    for item in downs:
                        if os.path.isfile(os.path.join(self.save_path, item)):
                            print(os.path.join(self.save_path, item), "->", os.path.join(dir_name, item))
                            shutil.move(os.path.join(self.save_path, item), dir_name)
                else:
                    for item in downs:
                        if os.path.isfile(os.path.join(self.save_path, item)):
                            print(os.path.join(self.save_path, item), "->", os.path.join(new_dest_dir, item))
                            shutil.move(os.path.join(save_path, item), new_dest_dir)
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.downdload_anitsu.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))


if __name__ == "__main__":
    common = Common()
    save_path = common.wx_dirdialog()
    if save_path == None:
        save_path = os.path.join(os.environ['USERPROFILE'], 'Videos')
    downloader = DownloaderAnime(save_path)
    downloader.downdload_anitsu(True)
    
    
            
                