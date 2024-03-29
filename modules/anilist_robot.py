import os
import sys
import time
import re
import logging
import requests
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
import constants as cnst
from web import Web
from common import Common
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONFIGURAR LOGGER
name_log = 'anilist_get_chaps_from_reader'
logger = logging.getLogger(name_log)
# INICIO configura nivel de log
logger.setLevel('DEBUG')
if os.name == 'nt':
    path_log = os.environ['TEMP']
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # aplica formato 
    formatter = logging.Formatter(log_format)
path_log = os.path.join(path_log, '.{}'.format(name_log))
# especificando nome do arquivo de log 
file_handler = logging.FileHandler("{}.log".format(path_log))
file_handler.setFormatter(formatter)
# adiciona arquivo ao manipulador de arquivo de log
logger.addHandler(file_handler)
# FIM configura nivel de log
class AnilistRobot():
    def __init__(self):
        """Inicia classe e os objetos necessários para classe e inicia navegador
        """
        self.common = Common()
        self.web = Web()
        self.driver = self.web.init_webdriver()
        # self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'})

    def __del__(self):
        """Função destrutora, fecha o navegador
        """
        self.web.try_quit_webdriver(self.driver)

    def scroll_to_bottom_page(self):
        """Rola até o final da página de mangás em leitura
        """
        try:
            SCROLL_PAUSE_TIME = 2
            # Pega tamanho do scroll
            scroll_height = self.driver.execute_script("return document.getElementsByClassName('list-entries')[0].scrollHeight")
            # pressiona END
            element = self.driver.find_elements(By.TAG_NAME, 'body')
            element[-1].send_keys(Keys.END)
            # Define o tamanho de rolagem
            scroll_old = scroll_height
            while True:
                # Pega tamanho do scroll
                scroll_height = self.driver.execute_script("return document.getElementsByClassName('list-entries')[0].scrollHeight")
                # armazena tamanho antigo antes da rolagem
                scroll_old = scroll_height
                # pressiona pgup
                element = self.driver.find_elements(By.TAG_NAME, 'body')
                element[-1].send_keys(Keys.END)
                # Espera página carregar
                time.sleep(SCROLL_PAUSE_TIME)
                # Verifica se chegou no fim
                scroll_height = self.driver.execute_script("return document.getElementsByClassName('list-entries')[0].scrollHeight")
                if scroll_old >= scroll_height:
                    break
        except Exception as err:
            self.driver.quit()
            _, _, tb = sys.exc_info()
            if tb is not None:
                # logger.error('Na linha {} -{}'.format(tb.tb_lineno,err), exc_info=True)
                print('Na linha {} -{}'.format(tb.tb_lineno,err))
            else:
                # logger.error(f"log_exception() called without an active exception.")
                print('log_exception() called without an active exception.')

    def login_anilist(self):
        """Realiza login no anilist

        Returns:
            str: nome do usuario
        """
        try:
            self.driver.get(f'{cnst.ANILIST}/login')
            inputs = self.driver.find_elements(By.CLASS_NAME, 'al-input')
            # insere informações de login
            # if inputs:
            #     inputs[0].send_keys('')
            #     inputs[1].send_keys('')
            print('Vá no navegador realize o login e resolva o captcha e clique no Login\nAguarde carregar a página inicial para continuar')
            print('\a')
            if os.name == 'nt':
                time.sleep(1)
                print('\a')
                os.system('pause')
            profile = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@class="link"]')))
            profile_name = profile.get_attribute('href').split('/')[-2]
            return profile_name
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def create_custom_list(self):
        """Cria as listas personalizadas no anilist
        """
        try:
            custom_lists = ['Waiting new chaps releases', 'New chaps releases', 'Finished releases', 'Adult Label']
            for custom in custom_lists:
                self.driver.get(f'{cnst.ANILIST}/settings/lists')
                # verifica se listas já existem
                custom_list = self.driver.find_elements(By.CLASS_NAME, 'el-input__inner')
                custom_list_text = [x.get_attribute('value') for x in custom_list]
                if custom in custom_list_text:
                    print(f'Lista {custom} já existe')
                    continue
                else:
                    # Obtem o botão de Add+ e realiza o clique
                    custom_list[-1].send_keys(custom)
                    add = self.driver.find_elements(By.CLASS_NAME, 'cancel')
                    add[-1].click()
                    saves = [x for x in self.driver.find_elements(By.CLASS_NAME, 'button') if x.text == 'Save']
                    saves[1].click()
                    print(f'Lista {custom} criada')
                    time.sleep(5)

        except Exception as err:
            self.web.try_quit_webdriver(self.driver)
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def search_golden(self, anime_name:str, url_search_golden:str):
        """Busca manga no golden mangas

        Args:
            anime_name (str): Nome do anime
            url_search_golden (str): URL de busca da goldenz

        Returns:
            _type_: _description_
        """
        try:
            self.driver.get(url_search_golden+anime_name)
            site = self.web.web_scrap(markup=self.driver.page_source)
            mangas = site.find_all('div', class_='mangas')
            if len(mangas) > 1:
                print(f'Foram encontrados mais de 1 resultado correspondente ao "{anime_name}"')
                print('\a')
                for index, manga in enumerate(mangas):
                    print(f'{index+1} - {manga.text.strip()}')
                time.sleep(1)
                print('\a')
                choice = self.common.only_read_int(len(mangas), 'Sua escolha => ')
                if choice == -1:
                    return None
                site = None
                return mangas[choice-1]
            elif len(mangas) == 0:
                site = None
                return None
            else:
                site = None
                return mangas[0]
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def search_mangaschan(self, manga_name:str, alt_names:list):
        """Busca mangas no site mangaschan

        Args:
            manga_name (str): Nome do manga

        Returns:
            BeautifulSoup: elemento que contem o mangá
        """
        try:
            self.driver.get(url=f'{cnst.AGREGADOR_MANGA.get("MANGASCHAN")}/?s='+manga_name)
            print('Vá no navegador e resolva o captcha e aguarde a página carregar para continuar')
            os.system('pause')
            site = self.web.web_scrap(markup=self.driver.page_source)
            mangas = site.find_all('div', class_='bsx')
            if len(mangas) > 1:
                print(f'Foram encontrados mais de 1 resultado correspondente ao "{manga_name}"')
                for manga in mangas:
                    name_manga = manga.find('div',  class_='tt')
                    if name_manga:
                        name_manga = name_manga.text
                        name_manga = self.common.normalize_name(name_manga)
                    if name_manga in alt_names:
                        mangas = [manga]
                        break
                    # if name_manga:
                    #     name_manga = name_manga.text.replace('\n', '').replace('\t', '')
                    # else:
                    #     name_manga = 'undefined'
                site = None
                return mangas
            elif len(mangas) == 0:
                site = None
                return None
            else:
                site = None
                return mangas[0]
        except Exception as err:
            self.web.try_quit_webdriver(self.driver)
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def set_list_anilist_mangaschan(self, mangas_list:dict):
        """Configura lista do anilist com base nos resultados do mangalivre

        Args:
            mangas_list (dict): Dicionario com informações do mangá
        """
        try:
            mangas_not_found = {}
            needs_check = False
            no_releases = None
            new_release = None
            finish = None
            # compara o progresso do anilist com o do agregador manga
            print("Iniciando pesquisa no MANGAS CHAN mangas")
            t_0 = self.common.initCountTime(True)
            for manga_name, values in mangas_list.items():
                last_chap_anilist = values[1].split('/')[0]
                if len(values[1].split('/')) > 1:
                    finish_chap_anilist = values[1].split('/')[1]
                else:
                    finish_chap_anilist = None

                checked = False
                # pesquisa anime atual no mangas chan
                while True:
                    manga = self.search_mangaschan(manga_name, mangas_list.get(manga_name)[-1])
                    if manga:
                        checked = True
                        break
                    else:
                        for value in values[-1]:
                            manga = self.search_mangaschan(value, mangas_list.get(manga_name)[-1])
                            if manga:
                                checked = True
                                break
                        if not checked:
                            logger.warning(f'Manga {manga_name} não encontrado')
                            print(f'Manga {manga_name} não encontrado')
                            print('\a')
                            time.sleep(1)
                            # print('\a')
                            # os.system('pause')
                            # new_name = input('Digite outro nome >> ')
                            # manga = self.search_mangaschan(new_name, url_search_agregador)
                            if manga:
                                checked = True
                            else:
                                logger.warning(f'Manga {manga_name} não encontrado')
                                checked = False
                            break
                        else:
                            break
                
                if checked:
                    if manga:
                        if manga.a:
                            while True:
                                try:
                                    self.driver.get(f'{manga.a.get("href")}')
                                    break
                                except:
                                    time.sleep(5)
                                    self.driver.get(f'{manga.a.get("href")}')
                            
                            time.sleep(2)
                            elements = self.driver.find_elements(By.XPATH, "//ul[@class='clstyle']/li")
                            if elements:    
                                search = re.search('[0-9]+', elements[0].text)
                                if search:
                                    last_chap = search.group(0)
                                    new_release = int(last_chap) > int(last_chap_anilist)
                                    if int(last_chap) < int(last_chap_anilist):
                                        print("Checar manga {}".format(manga_name))
                                        needs_check = True
                                        logger.warning("Checar manga {}, ultimo capitulo do Mangas Chan maior que o do Anilist".format(manga_name))
                                        # os.system('pause')
                                    if finish_chap_anilist:
                                        finish = last_chap == finish_chap_anilist
                                    else:
                                        finish = False
                                    no_releases = int(last_chap_anilist) == int(last_chap)
                
                else:
                    mangas_not_found.update({manga_name: values})
                    continue
                
                if needs_check:
                    continue
                else:
                    self.set_list_anilist( manga_name, values[0], no_releases, new_release, finish)
            t_f = self.common.finishCountTime(t_0,True)
            self.common.print_time(t_f)
            return mangas_not_found
        except Exception as err:
            self.driver.quit()
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def search_brmangas(self, manga_name:str, alt_names:list):
        try:
            # realiza pesquisa
            site = self.web.web_scrap(url=f'{cnst.AGREGADOR_MANGA['BRMANGA']}/?s={manga_name}')
            # obtem o elementos que contem os resultados
            search_results = site.find('div', class_='listagem row')
            # obtem todos os resultados
            items_search_results = search_results.find_all('div', class_='item')
            # verifica a quantidade de resultados
            if len(items_search_results) > 1:
                # itera todos os resultados encontrados e verifica se algum bate com o que é buscado
                for item in items_search_results:
                    if (item.text.strip() in alt_names) or (item.text.strip() == manga_name):
                        # obtem a url do resultado encotnrado
                        return item.a.get('href')
            elif len(items_search_results) == 1:
                # obtem a url do resultado encotnrado
                return items_search_results[0].a.get('href')
            else: return None
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def set_list_anilist_brmangas(self, mangas_list:dict):
        """Buscar mangás no brmangas e adicionar em lista personalizada no anilist 

        Args:
            mangas_list (dict): dicionario de mangás
        """
        try:
            print("Iniciando pesquisa no BR MANGAS")
            t_0 = self.common.initCountTime(True)
            found = False
            mangas_not_found = {}
            needs_check = False
            no_releases = None
            new_release = None
            finish = None
            mangas_found = 0
            for manga_name, values in mangas_list.items():
                last_chap_anilist = values[1].split('/')[0]
                if len(values[1].split('/')) > 1:
                    finish_chap_anilist = values[1].split('/')[1]
                else:
                    finish_chap_anilist = None
                found = False
                manga = self.search_brmangas(manga_name, mangas_list.get(manga_name)[-1])
                if manga:
                    found = True
                else:
                    for value in values[-1]:
                        manga = self.search_brmangas(value, mangas_list.get(manga_name)[-1])
                        if manga:
                            found = True
                            break
                # verifica se manga foi encontrado em brmangas
                if found:
                    # acessa a url do manga
                    site = self.web.web_scrap(url=manga)
                    # buscar numero do capitulo do site
                    time.sleep(2)
                    session_chapters = site.find('ul', class_="capitulos")
                    if session_chapters:
                        chapters = session_chapters.find_all('li')
                        if chapters:
                            search = re.search('[0-9]+', chapters[-1].text)
                            if search:
                                # obtem numero do ultimo capitulo de brmangas e compara com o que está no anilist
                                last_chap = search.group(0)
                                new_release = int(last_chap) > int(last_chap_anilist)
                                if int(last_chap) < int(last_chap_anilist):
                                    # print("Checar manga {}".format(manga_name))
                                    needs_check = True
                                    manga_name = self.common.normalize_name(manga_name)
                                    logger.warning("Checar manga {}, ultimo capitulo do BRAMANGAS maior que o do Anilist".format(manga_name))
                                    # os.system('pause')
                                if finish_chap_anilist: 
                                    finish = last_chap == finish_chap_anilist
                                else:
                                    finish = False
                                no_releases = int(last_chap_anilist) == int(last_chap)
                    if needs_check:
                        mangas_not_found.update({manga_name: values})
                        continue
                    else:
                        # print(f'Mangá {manga_name} encontrado')
                        self.set_list_anilist( manga_name, values[0], no_releases, new_release, finish)
                        mangas_found += 1
                        continue
                else:
                    manga_name = self.common.normalize_name(manga_name)
                    logger.warning(f'O item {manga_name} não foi encontrado em BR MANGÁS')
                    mangas_not_found.update({manga_name: values})
                    
            t_f = self.common.finishCountTime(t_0,True)
            self.common.print_time(t_f)
            print(f'Foram atualizados {mangas_found} mangas no ANILIST ')
            print(f'{len(mangas_not_found)} mangas não foram atualizados')
            return mangas_not_found
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err)) 

    def search_mangadex(self, manga_name:str, alt_names:list=None):
        try:
            r = requests.get(f"{cnst.AGREGADOR_MANGA['API-MANGADEDX']}/manga", params={"title": manga_name})
            search_results = [manga for manga in r.json()["data"]]
            ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err)) 

    def set_list_anilist_mangadex(self, manga_list:dict):
        try:
            ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err)) 

    def search_lermanga(self, manga_name:str, alt_names:list):
        try:
            ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err)) 

    def set_list_anilist_lermanga(self, manga_list:dict):
        try:
          ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def search_manhastro(self, manga_name:str, alt_names:list):
        try:
          ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def set_list_anilist_manhastro(self, manga_list:dict):
        try:
            ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))
    
    def search_slimeread(self, manga_name:str, alt_names:list):
        try:
            ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def set_list_anilist_slimeread(self, manga_list:dict):
        try:
            ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def search_tsukimangas(self, manga_name:str, alt_names:list):
        try:
            ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def set_list_anilist_tsukimangas(self, manga_list:dict):
        try:
            ...
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def get_alt_names_anilist(self, entrys):
        """_summary_
        """
        try:
            titles_links = {}
            # monta dicionario no seguinte esquema {nome_anime:[link, progresso]}
            print("Obtendo lista de animes")
            for entry in entrys:
                title = entry.find('div', class_='title')
                if title:
                    anime_name = title.text
                    anime_name = anime_name.strip()
                    titles_links.update({anime_name:[]})
                    if title.a:
                        titles_links[anime_name].append(title.a.get('href'))
                    progress = entry.find('div', class_='progress')
                    if progress:
                        progress_text = progress.text
                        progress_text = progress_text.strip()
                        progress_text = progress_text.replace('+', '')
                        titles_links[anime_name].append(progress_text)
            # INICIO busca nomes alternativos de cada anime
            print("Buscando nomes alternativos")
            for anime_name in titles_links:
                item = titles_links.get(anime_name)
                alt_names = []
                if item:
                    self.driver.get(f'{cnst.ANILIST}{item[0]}')
                    time.sleep(2)
                    data_set = [x for x in self.driver.find_elements(By.CLASS_NAME, 'data-set') if 'Romaji' in x.text or 'Synonyms' in x.text or 'English' in x.text or 'Native' in x.text]
                    if data_set:
                        for data in data_set:
                            value = data.find_elements(By.CLASS_NAME, 'value')
                            if value:
                                if '\n' in value[0].text:
                                    alt_names.extend(value[0].text.split('\n'))
                                    # item.extend(value[0].text.split('\n'))
                                else:
                                    alt_names.append(value[0].text)
                                    # item.append(value[0].text)
                    item.append(alt_names)
            # FIM busca nomes alternativos de cada anime
            return titles_links
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err)) 

    def get_mangas_anilist(self, username:str):
        """Obter mangas do anilist

        Args:
            username (str): nome do usuário do anilist

        Returns:
            str: dicionario com valores dos mangás
        """
        try:
            # INICIA buscar lista de mangas em leitura no anilist
            choice = 'n'
            self.driver.get(f'{cnst.ANILIST}/user/{username}/mangalist/Reading')
            time.sleep(2)
            self.scroll_to_bottom_page()
            site = self.web.web_scrap(markup=self.driver.page_source)
            # titles = site.find_all('div', class_='title')
            # titles_links = [x.a.get('href') for x in titles if x.a]
            entrys = site.find_all('div', class_='entry-card')
            titles_links = {}
            t_0 = self.common.initCountTime(True)
            file_anime_names = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Documents', 'alt_names.txt'))
            if os.path.isfile(file_anime_names):
                choice = input('Arquivo "alt_names.txt" já existente. Deseja atualizar arquivo? (S)im ')
                mangas_list = {}
                # ler o arquivo existente
                with open(file_anime_names, 'r', encoding='utf-8') as file_txt:
                    content = file_txt.readlines()
                    content = [x.replace('\n', '') for x in content]
                    for line in content:
                        slices = line.split(" -- ")
                        values = slices[-1].split(' || ')
                        alts = values[2:]
                        values = values[:2]
                        # alts = re.sub("(\'|\[|\])+", "", alts)
                        # alts = alts.split(',')
                        values.append(alts)
                        mangas_list.update({slices[0] : values})
                if choice.lower() == 's' or choice.lower() == 'sim':
                    titles_links = self.get_alt_names_anilist(entrys)
                    # mesclar alt_name existente com o obtido
                    for item_list in mangas_list:
                        list_names = []
                        if titles_links.get(item_list):
                            list_names.extend(titles_links.get(item_list)[-1])
                        else:
                            titles_links[item_list] = mangas_list.get(item_list)
                        list_names.extend(mangas_list.get(item_list)[-1])
                        list_names = list(set(list_names))
                        titles_links[item_list][-1] = list_names
                else:
                    return mangas_list
            else:
                titles_links = self.get_alt_names_anilist(entrys)
            # Salvar o arquivo 
            dict(sorted(titles_links.items()))
            out_file = os.path.join(os.environ['USERPROFILE'], 'Documents', 'alt_names.txt')
            with open(out_file, 'w', encoding='utf-8') as file_txt:
                for item in titles_links:
                    file_txt.write(f"{item} -- {' || '.join(titles_links[item][:-1])} || {' || '.join(titles_links[item][-1])}\n")
            print(f"Arquivo salvo em {out_file}")
            # print(titles_links)
            # FIM obter animes do anilist
            t_f = self.common.finishCountTime(t_0,True)
            self.common.print_time(t_f)
            return titles_links
        except Exception as err:
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def set_list_anilist(self, manga_name:str, manga_url:str, no_releases:bool, new_release:bool, finish:bool):
        """Adiciona manga a lista personalizada do anilist

        Args:
            manga_name (str): Nome do manga que será configurar
            manga_url (str): URL do mangá que será configurado
            no_releases (bool): Define se mangá está sem lançamentos
            new_release (bool): Define se mangá está como novos lançamentos
            finish (bool): Define se mangás já está finalizado
        """
        try:
            # abre página do anime no anilist para realizar edições
            self.driver.get(f'{cnst.ANILIST}{manga_url}')
            time.sleep(2)
            site = self.web.web_scrap(markup=self.driver.page_source)
            adult = site.find('div', class_='adult-label')
            # Se o adulto é verdadeiro, então adicionado a lista adulto
            if adult:
                adult = True
            else:
                adult = False
            # busca botão para o dropdown
            dropdown = self.driver.find_elements(By.XPATH, '//div[@class="dropdown el-dropdown"]')
            # verifica se elemento dropdown foi encontrado
            if dropdown:
                dropdown[0].click()
                time.sleep(5)
                # busca o as opções do dropdown
                elements_dropdown = self.driver.find_elements(By.XPATH, '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--medium"]')
                if elements_dropdown:
                    elements_dropdown = [x for x in self.driver.find_elements(By.XPATH, '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--medium"]') if x.is_displayed()]
                    # Caso não encontre nenhum elemento
                    if len(elements_dropdown) == 0:
                        # inicia a busca até que encontre as opções do dropdown
                        while True:
                            elements_dropdown = self.driver.find_elements(By.XPATH, '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--medium"]')
                            time.sleep(5)
                            # filtra apena elemento que estão visiveis
                            elements_dropdown = [x for x in self.driver.find_elements(By.XPATH, '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--medium"]') if x.is_displayed()]
                            # verificar se encontrou as opções do dropdown
                            if len(elements_dropdown) == 0:
                                continue
                            else:
                                break
                    else:
                        # obtem o elemento da lista que pode varia a posição
                        # obtem elemento de index 1 se lista maior que 1 se não obtem elemento de index 0
                        if len(elements_dropdown) > 1:
                            elements_dropdown = elements_dropdown[1]
                        else:
                            elements_dropdown = elements_dropdown[0]
                        # clica na opção "Open List Editor"
                        if elements_dropdown.is_displayed():
                            options = elements_dropdown.find_elements(By.TAG_NAME, 'li')
                            # Clica no checkboxs
                            if options:
                                options[-1].click()
                                time.sleep(5)
                                checkboxs = self.driver.find_elements(By.CLASS_NAME, 'checkbox')
                                # gera lista com apenas textos dos checkboxs
                                texts_checkboxs = [x.text for x in checkboxs]
                                # Verifica se mangá possui adult label e adiciona na lista adult
                                if adult:
                                    adults = ['Adult Label', 'Hide from status lists', 'Private']
                                    # Obtem o index de cada checkbox para clicar corretamente 
                                    for a in adults:
                                        # index do checkbox com valor da variavel a
                                        index = texts_checkboxs.index(a)
                                        check_box = checkboxs[index].find_elements(By.TAG_NAME, 'input')
                                        # Verifica se checkbox com valor da variavel a não está selecionado e clica para marcar o checkbox
                                        if check_box[0].is_selected() == False:
                                            logger.info(f'{manga_name} adicionado na lista {a}')
                                            print(f'{manga_name} adicionado na lista {a}')
                                            checkboxs[index].click()
                                # verifica se mangá está sem lançamentos e adiciona na lista "Waiting new chaps releases"
                                if no_releases:
                                    # index do checkbox "Waiting new chaps releases"
                                    index = texts_checkboxs.index('Waiting new chaps releases')
                                    check_box = checkboxs[index].find_elements(By.TAG_NAME, 'input')
                                    # Verifica se checkbox "Waiting new chaps releases" não está selecionado e clica para marcar o checkbox
                                    if check_box[0].is_selected() == False:
                                        logger.info(f'{manga_name} adicionado na lista Waiting new chaps releases')
                                        print(f'{manga_name} adicionado na lista Waiting new chaps releases')
                                        checkboxs[index].click()
                                    # index do checkbox "New chaps releases"
                                    index = texts_checkboxs.index('New chaps releases')
                                    check_box = checkboxs[index].find_elements(By.TAG_NAME, 'input')
                                    # Verifica se checkbox "New chaps releases" está selecionado e clica para desmarcar o checkbox
                                    if check_box[0].is_selected() == True:
                                        print(f'{manga_name} removido na lista New chaps releases')
                                        logger.info(f'{manga_name} removido na lista New chaps releases')
                                        checkboxs[index].click()
                                # verifica se mangá está com novos capitulos e adiciona na lista "New chaps releases"
                                if new_release:
                                    # index do checkbox "New chaps releases"
                                    index = texts_checkboxs.index('New chaps releases')
                                    check_box = checkboxs[index].find_elements(By.TAG_NAME, 'input')
                                    # verificar se checkbox "New chaps releases" não está selecionado e clica para marcar o checkbox
                                    if check_box[0].is_selected() == False:
                                        logger.info(f'{manga_name} adicionado da lista New chaps releases')
                                        print(f'{manga_name} adicionado da lista New chaps releases')
                                        logger.info(f'{manga_name} adicionado da lista New chaps releases')
                                        checkboxs[index].click()
                                    # index do checkbox "Waiting new chaps releases"
                                    index = texts_checkboxs.index('Waiting new chaps releases')
                                    check_box = checkboxs[index].find_elements(By.TAG_NAME, 'input')
                                    logger.info(f'{manga_name} removido da lista Waiting new chaps releases')
                                    # Verifica se checkbox "Waiting new chaps releases" está selecionado e clica para desmarcar o checkbox
                                    if check_box[0].is_selected() == True:
                                        print(f'{manga_name} removido da lista Waiting new chaps releases')
                                        logger.info(f'{manga_name} removido da lista Waiting new chaps releases')
                                        checkboxs[index].click()
                                # verifica se mangá está finalizado e adicionado na lista "Finished releases"
                                if finish:
                                    # index do checkbox "Finished releases"
                                    index = texts_checkboxs.index('Finished releases')
                                    check_box = checkboxs[index].find_elements(By.TAG_NAME, 'input')
                                    # Verifica se checkbox "Finished releases" não está selecionado e clica para marcar o checkbox
                                    if check_box[0].is_selected() == False:
                                        logger.info(f'{manga_name} adicionado na lista Finished releases')
                                        print(f'{manga_name} adicionado na lista Finished releases')
                                        checkboxs[index].click()
                                save = self.driver.find_elements(By.CLASS_NAME, 'save-btn')
                                # Clica no botão de salvar
                                if save:
                                    save[0].click()
                                time.sleep(2)
        except Exception as err:
            self.driver.quit()
            exc_info = sys.exc_info()
            # Imprime em qual mangá teve erro e imprime a linha com erro
            if exc_info:
                print('Manga com erro {}'.format(manga_name))
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def search_mangalivre(self, manga_name:str):
        """Pesquisa mangás no mangalivre

        Args:
            manga_name (str): Nome do mangá

        Returns:
            BeautifulSoup: elemento contendo informação do mangá
        """
        try:
            self.driver.get('https://mangalivre.net')
            busca_botao = self.driver.find_elements(By.XPATH, "//button[@class='btn-search']")
            # busca_botao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn-search']")))
            if busca_botao:
                ActionChains(self.driver).click(busca_botao[0]).perform()
                busca_botao[0].click()
            busca = self.driver.find_elements(By.ID, 'searchInput')
            if busca:
                time.sleep(1)
                busca[0].send_keys(manga_name)
                time.sleep(1)
            site = self.web.web_scrap(markup=self.driver.page_source)
            time.sleep(1)
            list_search = site.find_all('ul',class_='active')
            if list_search:
                results = [x for x in list_search[0].find_all('li') if x.a]
                names = [x.a.span.text for x in results if x.a]
                index = None
                for name in names:
                    if manga_name == name:
                        index = names.index(name)
                        break
                if index:
                    return None
                else:
                    return results[index]
            else:
                return None
        except Exception as err:
            self.driver.quit()
            exc_info = sys.exc_info()[2]
            if exc_info:
                print('Manga com erro {}'.format(manga_name))
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def set_list_anilist_mangalivre(self, mangas_list:dict):
        """Configura lista do anilist com base nos resultados do mangalivre

        Args:
            mangas_list (dict): Dicionario com informações do mangá
        """
        mangas_not_found = {}
        needs_check = False
        no_releases = None
        new_release = None
        finish = None
        try:
            print("Iniciando pesquisa no MANGA LIVRE mangas")
            t_0 = self.common.initCountTime(True)
            for manga_name, values in mangas_list.items():
                last_chap_anilist = values[1].split('/')[0]
                if len(values[1].split('/')) > 1:
                    finish_chap_anilist = values[1].split('/')[1]
                else:
                    finish_chap_anilist = None

                checked = False
                
                # pesquisa anime atual no mangas chan
                while True:
                    manga = self.search_mangalivre(manga_name)
                    if manga:
                        checked = True
                        break
                    else:
                        for value in values[-1]:
                            manga = self.search_mangalivre(value)
                            if manga:
                                checked = True
                                break
                        if not checked:
                            logger.warning(f'Manga {manga_name} não encontrado')
                            print(f'Manga {manga_name} não encontrado')
                            print('\a')
                            time.sleep(1)
                            # print('\a')
                            # os.system('pause')
                            # new_name = input('Digite outro nome >> ')
                            # manga = self.search_mangaschan(driver, new_name, url_search_agregador)
                            if manga:
                                checked = True
                            else:
                                logger.warning(f'Manga {manga_name} não encontrado')
                                checked = False
                            break
                        else:
                            break
                
                if checked:
                    if manga:
                        if manga.a:
                            while True:
                                try:
                                    self.driver.get(f'https://mangalivre.net{manga.a.get("href")}')
                                    break
                                except:
                                    time.sleep(5)
                                    self.driver.get(f'https://mangalivre.net{manga.a.get("href")}')
                            
                            time.sleep(2)
                            elements = self.driver.find_elements(By.XPATH, "//ul[@class='full-chapters-list list-of-chapters']/li//span[@class='cap-text']")
                            if elements:    
                                search = re.search('[0-9]+', elements[0].text)
                                if search:
                                    last_chap = search.group(0)
                                    new_release = int(last_chap) > int(last_chap_anilist)
                                    if int(last_chap) < int(last_chap_anilist):
                                        print("Checar manga {}".format(manga_name))
                                        needs_check = True
                                        logger.warning("Checar manga {}, ultimo capitulo do Mangas Livre maior que o do Anilist".format(manga_name))
                                        # os.system('pause')
                                    if finish_chap_anilist:
                                        finish = last_chap == finish_chap_anilist
                                    else:
                                        finish = False
                                    no_releases = int(last_chap_anilist) == int(last_chap)
                else:
                    mangas_not_found.update({manga_name: values})
                    continue
                
                if needs_check:
                    continue
                else:
                    self.set_list_anilist(manga_name, values[0], no_releases, new_release, finish)
            t_f = self.common.finishCountTime(t_0,True)
            self.common.print_time(t_f)
            
        except Exception as err:
            self.driver.quit()
            exc_info = sys.exc_info()
            if exc_info:
                print('Manga com erro {}'.format(manga_name))
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def add_on_anilist(self, list_names:list, type_material:int):
        """Adicionar mangá ou anime no anilist

        Args:
            list_names (list): lista de nome das obras
            type (int): tipo de obra. 1 para manga 2 para anime
        """
        try:
            for item in list_names:
                # pesquisa com e sem tag adult
                params = ['', '&adult=true']
                for p in params:
                    if type_material == 1:
                        self.driver.get(f'{cnst.ANILIST}/search/manga?search={item}{p}')
                    elif type_material == 2:
                        self.driver.get(f'{cnst.ANILIST}/search/anime?search={item}{p}')
                    time.sleep(2)
                    # busca elemento indicando que não houve resultados
                    no_results = self.driver.find_elements(By.CLASS_NAME, 'no-results')
                    results = self.driver.find_elements(By.XPATH, '//div[@class="results cover"]')
                    if no_results:
                        print(f"{item} não foi encotrado no anilist")
                    if results:
                        site = self.web.web_scrap(markup=self.driver.page_source)
                        results_cover = site.find('div', class_='results cover')
                        if results_cover:
                            # vai rolando até ter todos os resultados
                            links_results = results_cover.find_all('a', class_='title')
                            scroll_height = self.driver.execute_script("return document.getElementsByClassName('results cover')[0].scrollHeight")
                            while True:
                                SCROLL_PAUSE_TIME = 2
                                ActionChains(self.driver).send_keys(Keys.END).perform()
                                time.sleep(SCROLL_PAUSE_TIME)
                                scroll_old = scroll_height
                                scroll_height = self.driver.execute_script("return document.getElementsByClassName('results cover')[0].scrollHeight")
                                links_results = results_cover.find_all('a', class_='title')
                                if scroll_old >= scroll_height:
                                    break
                            anilist_results = [f'{cnst.ANILIST}{x.get("href")}' for x in links_results if not x.div]
                            if len(anilist_results) == 0:
                                print(f'{item} já adicionado no anilist')
                            # percorre url de cada resultado verificando qual se encaixa na pesquisa        
                            for url in anilist_results:
                                # obtem nomes alternativos
                                alt_names = []
                                self.driver.get(url)
                                time.sleep(5)
                                data_set = [x for x in self.driver.find_elements(By.CLASS_NAME, 'data-set') if 'Romaji' in x.text or 'Synonyms' in x.text or 'English' in x.text or 'Native' in x.text]
                                if data_set:
                                    for data in data_set:
                                        value = data.find_elements(By.CLASS_NAME, 'value')
                                        if value:
                                            if '\n' in value[0].text:
                                                alt_names.extend(value[0].text.split('\n'))
                                            else:
                                                alt_names.append(value[0].text)
                                # verifica se a pesquisa realiza encaixa nesse item desta url
                                if item in alt_names:
                                    dropdown = self.driver.find_elements(By.XPATH, '//div[@class="dropdown el-dropdown"]')
                                    # verifica se elemento dropdown foi encontrado
                                    if dropdown:
                                        dropdown[0].click()
                                        time.sleep(3)
                                        # busca o as opções do dropdown
                                        elements_dropdown = self.driver.find_elements(By.XPATH, '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--medium"]')
                                        if elements_dropdown:
                                            elements_dropdown = [x for x in self.driver.find_elements(By.XPATH, '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--medium"]') if x.is_displayed()]
                                            # Caso não encontre nenhum elemento
                                            if len(elements_dropdown) == 0:
                                                # inicia a busca até que encontre as opções do dropdown
                                                while True:
                                                    elements_dropdown = self.driver.find_elements(By.XPATH, '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--medium"]')
                                                    time.sleep(3)
                                                    # filtra apena elemento que estão visiveis
                                                    elements_dropdown = [x for x in self.driver.find_elements(By.XPATH, '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--medium"]') if x.is_displayed()]
                                                    # verificar se encontrou as opções do dropdown
                                                    if len(elements_dropdown) == 0:
                                                        continue
                                                    else:
                                                        break
                                            else:
                                                # obtem o elemento da lista que pode varia a posição
                                                # obtem elemento de index 1 se lista maior que 1 se não obtem elemento de index 0
                                                if len(elements_dropdown) > 1:
                                                    elements_dropdown = elements_dropdown[1]
                                                else:
                                                    elements_dropdown = elements_dropdown[0]
                                                # clica na opção "Open List Editor"
                                                if elements_dropdown.is_displayed():
                                                    options = elements_dropdown.find_elements(By.TAG_NAME, 'li')
                                                    # Clica no checkboxs
                                                    if options:
                                                        options[-1].click()
                                                        status = self.driver.find_elements(By.XPATH, '//div[@class="form status"]//input')
                                                        if status:
                                                            status[0].click()
                                                            op_status = self.driver.find_elements(By.XPATH, '//ul[@class="el-scrollbar__view el-select-dropdown__list"]//li')
                                                            if op_status:
                                                                if list_names.get(item) == '0':
                                                                    op_status[1].click()
                                                                else:
                                                                    op_status[0].click()
                                                        progress = self.driver.find_elements(By.XPATH, '//div[@class="form progress"]//input')
                                                        if progress:
                                                            progress[0].send_keys(list_names.get(item))
                                                        save = self.driver.find_elements(By.CLASS_NAME, 'save-btn')
                                                        # Clica no botão de salvar
                                                        if save:
                                                            save[0].click()
                                                        time.sleep(2)
                                                        check = True
                                                        break
                                else:
                                    check = False
                                    continue
                    if check:
                        break
            if check == False:
                print(f"{item} não encontrado")
        except Exception as err:
            self.driver.quit()
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

    def get_alt_names(self, username:str):
        try:
            mangas_list = {}
            file_anime_names = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Documents', 'alt_names.txt'))
            if os.path.isfile(file_anime_names):
                choice = input('Arquivo "alt_names.txt" já existente. Deseja atualizar arquivo? (S)im ')
                if (choice.lower() == 's') or (choice.lower() == 'sim'):
                    mangas_list = al_robot.get_mangas_anilist(username)
                else:
                    # ler o arquivo
                    with open(file_anime_names, 'r', encoding='utf-8') as file_txt:
                        content = file_txt.readlines()
                        content = [x.replace('\n', '') for x in content]
                        for line in content:
                            slices = line.split(" -- ")
                            values = slices[-1].split(' || ')
                            alts = values[2:]
                            values = values[:2]
                            # alts = re.sub("(\'|\[|\])+", "", alts)
                            # alts = alts.split(',')
                            values.append(alts)
                            mangas_list.update({slices[0] : values})

            else:
                mangas_list = al_robot.get_mangas_anilist(username)
            mangas_list = dict(sorted(mangas_list.items()))
            return mangas_list
        except Exception as err:
            self.driver.quit()
            exc_info = sys.exc_info()
            if exc_info:
                print('Na linha {} -{}'.format(exc_info[2].tb_lineno,err))

if __name__ == "__main__":
    al_robot = AnilistRobot()
    common = Common()
    web = Web()
    mangas_list = al_robot.get_alt_names('mariodac')
    username = al_robot.login_anilist()
    al_robot.set_list_anilist_brmangas(mangas_list)
    manga_name = 'Yancha Gal no Anjou-san'
    al_robot.search_mangadex(manga_name)
    mangas_not_found = al_robot.set_list_anilist_brmangas(mangas_list)
    al_robot.set_list_anilist_mangalivre(mangas_list)
    