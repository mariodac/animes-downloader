import os
import sys
import time
import re
import logging
import utils.constants as cnst
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
from web import Web
from common import Common
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
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
else:
    path_log = os.environ['HOME']
    # formato do log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
path_log = os.path.join(path_log, '.{}'.format(name_log))
# especificando nome do arquivo de log 
file_handler = logging.FileHandler("{}.log".format(path_log))
file_handler.setFormatter(formatter)
# adiciona arquivo ao manipulador de arquivo de log
logger.addHandler(file_handler)
# FIM configura nivel de log
class AnilistGetChaps():
    def __init__(self):
        self.common = Common()
        self.web = Web()
        self.driver = self.web.init_webdriver()

    def scroll_to_bottom_page(self,driver):
        """Rola até o final da lista de chat
        """
        try:
            SCROLL_PAUSE_TIME = 2
            # Pega tamanho do scroll
            scroll_height = driver.execute_script("return document.getElementsByClassName('list-entries')[0].scrollHeight")
            # pressiona END
            element = driver.find_elements(By.TAG_NAME, 'body')
            element[-1].send_keys(Keys.END)
            # Define o tamanho de rolagem
            scroll_old = scroll_height
            while True:
                # Pega tamanho do scroll
                scroll_height = driver.execute_script("return document.getElementsByClassName('list-entries')[0].scrollHeight")
                # armazena tamanho antigo antes da rolagem
                scroll_old = scroll_height
                # pressiona pgup
                element = driver.find_elements(By.TAG_NAME, 'body')
                element[-1].send_keys(Keys.END)
                # Espera página carregar
                time.sleep(SCROLL_PAUSE_TIME)
                # Verifica se chegou no fim
                scroll_height = driver.execute_script("return document.getElementsByClassName('list-entries')[0].scrollHeight")
                if scroll_old >= scroll_height:
                    break
        except Exception as err:
            driver.quit()
            _, _, tb = sys.exc_info()
            if tb is not None:
                # logger.error('Na linha {} -{}'.format(tb.tb_lineno,err), exc_info=True)
                print('Na linha {} -{}'.format(tb.tb_lineno,err))
            else:
                # logger.error(f"log_exception() called without an active exception.")
                print('log_exception() called without an active exception.')

    def login_anilist(self):
        self.driver.get('https://anilist.co/login')
        inputs = self.driver.find_elements(By.CLASS_NAME, 'al-input')
        # insere informações de login
        # if inputs:
        #     inputs[0].send_keys('')
        #     inputs[1].send_keys('')
        print('Vá no navegador realizei o login e resolva o captcha e clique no Login\nAguarde carregar a página inicial para continuar')
        print('\a')
        if os.name == 'nt':
            time.sleep(1)
            print('\a')
            os.system('pause')
        else:
            time.sleep(1)
            print('\a')
            input('Press enter to continue')
        profile = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@class="link"]')))
        profile_name = profile.get_attribute('href').split('/')[-2]
        return profile_name

    def create_custom_list(self):
        try:
            custom_lists = ['Waiting new chaps releases', 'New chaps releases', 'Finished releases', 'Adult Label']
            for custom in custom_lists:
                self.driver.get('https://anilist.co/settings/lists')
                custom_list = self.driver.find_elements(By.CLASS_NAME, 'el-input__inner')
                if custom in [x.get_attribute('value') for x in custom_list]:
                    continue
                custom_list[-1].send_keys(custom)
                add = self.driver.find_elements(By.CLASS_NAME, 'cancel')
                add[-1].click()
                saves = [x for x in self.driver.find_elements(By.CLASS_NAME, 'button') if x.text == 'Save']
                saves[1].click()
                time.sleep(5)
            print()

        except Exception as err:
            self.driver.quit()
            nline = sys.exc_info()[2]
            if nline:
                print('Na linha {} -{}'.format(nline.tb_lineno,err))

    def search_golden(self, anime_name, url_search_golden):
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

    def search_mangaschan(self, manga_name, url_search):
        site = self.web.web_scrap(url=url_search+manga_name)
        mangas = site.find_all('div', class_='bsx')
        mangas 
        if len(mangas) > 1:
            print(f'Foram encontrados mais de 1 resultado correspondente ao "{manga_name}"')
            choice = 1
            for manga in mangas:
                name_manga = manga.find('div',  class_='tt')
                if name_manga:
                    name_manga = name_manga.text
                manga_search = re.search(f'{manga_name}', name_manga,re.IGNORECASE)
                if manga_search:
                    mangas = [manga]
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

    def get_mangas_anilist(self, username):
        # INICIA buscar lista de mangas em leitura no anilist
        self.driver.get('https://anilist.co/user/{}/mangalist/Reading'.format(username))
        time.sleep(2)
        self.scroll_to_bottom_page(self.driver)
        site = web.web_scrap(markup=self.driver.page_source)
        # titles = site.find_all('div', class_='title')
        # titles_links = [x.a.get('href') for x in titles if x.a]
        entrys = site.find_all('div', class_='entry-card')
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
        t_0 = self.common.initCountTime(True)
        for anime_name in titles_links:
            item = titles_links.get(anime_name)
            alt_names = []
            if item:
                self.driver.get('https://anilist.co'+item[0])
                time.sleep(2)
                data_set = [x for x in self.driver.find_elements(By.CLASS_NAME, 'data-set') if 'Romaji' in x.text or 'Synonyms' in x.text or 'English' in x.text]
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
        t_f = self.common.finishCountTime(t_0,True)
        self.common.print_time(t_f)
        # Salvar o arquivo 
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'alt_names.txt'), 'w', encoding='utf-8') as file_txt:
            for item in titles_links:
                file_txt.write(f"{item} -- {' || '.join(titles_links[item][:-1])} || {' || '.join(titles_links[item][-1])}\n")
        print(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'alt_names.txt'))
        # print(titles_links)
        # FIM obter animes do anilist
        return titles_links

    def set_list_anilist(self, manga_name, manga_url, no_releases, new_release, finish):
        """
         Sets anilist in web. com and returns True if successful. Otherwise returns False
         
         @param driver - Webdriver (navegador)
         @param manga_name - Nome do manga que será configurar
         @param values - Lista de valores 
         @param no_releases - If true don't set release
         @param new_release - If true set release to new one
         @param finish - If true finish the anilist with new
        """
        try:
            # abre página do anime no anilist para realizar edições
            self.driver.get('https://anilist.co'+manga_url)
            time.sleep(2)
            site = web.web_scrap(markup=self.driver.page_source)
            adult = site.find('div', class_='adult-label')
            # If adult is true then adult is true.
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
            nline = sys.exc_info()[2]
            # Imprime em qual mangá teve erro e imprime a linha com erro
            if nline:
                print('Manga com erro {}'.format(manga_name))
                print('Na linha {} -{}'.format(nline.tb_lineno,err))

    def set_list_anilist_mangaschan(self, driver, mangas_list):
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
                    manga = self.search_mangaschan(manga_name, url_search_agregador)
                    if manga:
                        checked = True
                        break
                    else:
                        for value in values[-1]:
                            manga = self.search_mangaschan(value, url_search_agregador)
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
                                    driver.get(f'{manga.a.get("href")}')
                                    break
                                except:
                                    time.sleep(5)
                                    driver.get(f'{manga.a.get("href")}')
                            
                            time.sleep(2)
                            elements = driver.find_elements(By.XPATH, "//ul[@class='clstyle']/li")
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
        except Exception as err:
            driver.quit()
            nline = sys.exc_info()[2]
            if nline:
                print('Manga com erro {}'.format(manga_name))
                print('Na linha {} -{}'.format(nline.tb_lineno,err))

    def search_mangalivre(self, manga_name):
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
            nline = sys.exc_info()[2]
            if nline:
                print('Manga com erro {}'.format(manga_name))
                print('Na linha {} -{}'.format(nline.tb_lineno,err))

    def set_list_anilist_mangalivre(self, mangas_list):
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
            nline = sys.exc_info()[2]
            if nline:
                print('Manga com erro {}'.format(manga_name))
                print('Na linha {} -{}'.format(nline.tb_lineno,err))

if __name__ == "__main__":
    agc = AnilistGetChaps()
    common = Common()
    s=Service(ChromeDriverManager().install())
    web = Web()
    os.path.join(os.path.dirname(__file__))
    driver = webdriver.Chrome(service=s, options=web.optionsChrome(crx_extension=[os.path.join(os.path.dirname(__file__), 'extensions', 'popup_blocker.crx')]))
    url_agregador = cnst.AGREGADOR_MANGA.get('MANGASCHAN')
    username = agc.login_anilist(driver)
    # agc.set_list_anilist(driver, 'Megami no Sprinter ', '/manga/101617/Megami-no-Sprinter/', True, True, True)
    agc.create_custom_list(driver)
    mangas_list = {}
    url_search_agregador = f'{url_agregador[0]}{url_agregador[1]}'
    file_anime_names = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'alt_names.txt')
    if os.path.isfile(file_anime_names):
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

        mangas_list = dict(sorted(mangas_list.items()))
    else:
        mangas_list = agc.get_mangas_anilist(driver, username)
    agc.set_list_anilist_mangalivre(driver, mangas_list)
    mangas_not_found = agc.set_list_anilist_mangaschan(driver, mangas_list)
    