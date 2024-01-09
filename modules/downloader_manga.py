from common import Common
from web import Web
import constants
import os
import time
import sys
import pyautogui
import pygetwindow as gw
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class DownloaderManga:
    def __init__(self):
        self.web = Web()
        self.common = Common()
        self.save_path = os.path.join(os.environ['USERPROFILE'], 'Pictures')
        self.web_driver = self.web.init_webdriver(default=False, headless=False, saida=self.save_path)
    def __del__(self):
        """Função destrutora, fecha o navegador
        """
        self.web.try_quit_webdriver(self.web_driver)
    
    def search_mangadex(self, manga_name:str):
        self.web_driver.get(f"{constants.AGREGADOR_MANGA.get('MANGADEX')}/titles?&content=suggestive,erotica,safe&translatedLang=pt-br&q={manga_name}")
        links = []
        while True:
            time.sleep(2)
            site = self.web.web_scrap(markup=self.web_driver.page_source)
            links.extend(site.find_all('div', class_="manga-card"))
            pages = self.web_driver.find_elements(By.CSS_SELECTOR, '.router-link-active.router-link-exact-active.rounded')
            if pages:
                try:
                    if 'disabled' in pages[-1].get_attribute('class'):
                        break
                    else:
                        pages[-1].click()
                except:
                    break
            else:
                break
        if len(links) == 1:
            if links[0].a:
                return links[0].a.get('href')
        elif len(links) > 1:
            manga_names = [x.find('a', class_='font-bold title').text for x in links if x.find('a', class_='font-bold title')]
            index_eq = -1
            for index,name in enumerate(manga_names):
                if name == manga_name:
                    index_eq = index
                    manga_path = self.common.create_folder(name, self.save_path)
                    break
            if index_eq > -1:
                manga_path = self.common.create_folder(manga_name, self.save_path)
                return links[index_eq].a.get('href'), manga_path
            else:
                index_eq = 0
                for index, item in enumerate(links):
                    self.web_driver.get(item.a.get('href'))
                    site = self.web.web_scrap(markup=self.web_driver.page_source)
                    alt_title = site.find('div', class_='alt-title')
                    alt_names = [x.text for x in alt_title if manga_name in x.text]
                    filter_alt_names = [x for x in alt_names if manga_name == x]
                    if len(filter_alt_names) == 1:
                        index_eq = index
                        manga_path = self.common.create_folder(manga_name, self.save_path)
                        break
                return links[index_eq].a.get('href') , manga_path

    def get_chaps_mangas(self, url_chap):
        self.web_driver.get(f"{constants.AGREGADOR_MANGA.get('MANGADEX')}{url_chap}")
        chapters_br = []
        while True:
            time.sleep(2)
            site = self.web.web_scrap(markup=self.web_driver.page_source)
            chapters = site.find_all('div', class_='chapter-grid flex-grow')
            chapters_br.extend([x for x in chapters if x.find('img', title="Portuguese (Br)")])
            pages = self.web_driver.find_elements(By.XPATH, '//div[@class="flex justify-center flex-wrap gap-2 mt-6"]//button[contains(@class,"rounded custom-opacity relative md-btn ")]')
            Keys.ARROW_RIGHT
            if pages:
                try:
                    if 'disabled' in pages[-1].get_attribute('class'):
                        break
                    else:
                        pages[-1].click()
                except:
                    break
            else:
                break
        chapters_br.reverse()
        return chapters_br

    def download_chaps(self, chaps, manga_path):
        for index,chap in enumerate(chaps):
            if chap.a:
                self.web_driver.get(f"{constants.AGREGADOR_MANGA.get('MANGADEX')}{chap.a.get('href')}")
                time.sleep(2)
                site = self.web.web_scrap(markup=self.web_driver.page_source)
                pages = site.find_all('div',class_="prog-divider")
                reader = self.web_driver.find_elements(By.CLASS_NAME, 'reader--header-title')
                if reader:
                    chap_path = self.common.create_folder(reader[0].text, manga_path)
                else:
                    chap_path = self.common.create_folder(f"Chapter {index}", manga_path)
                imgs = []
                filter_imgs = {}
                actions = ActionChains(self.web_driver)
                print(f"Total de páginas {len(pages)}")
                for i in range(len(pages)-1):
                    self.web_driver.get(f"{constants.AGREGADOR_MANGA.get('MANGADEX')}{chap.a.get('href')}/{i+1}")
                    time.sleep(2)
                    WebDriverWait(self.web_driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="md--reader-chapter"]')))
                    page =  WebDriverWait(self.web_driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="mx-auto h-full md--page  flex"]')))
                    localizacao = page[0].location
                    x = localizacao['x']
                    y = localizacao['y']
                    # Obter o titulo da janela do WebDriver
                    window_title = self.web_driver.title+' - Google Chrome'
                    window_index = gw.getAllTitles().index(window_title)
                    # Obter o objeto da janela usando o identificador
                    window = gw.getWindowsWithTitle(gw.getAllTitles()[window_index])
                    # Colocar a janela em foco
                    try:
                        window[0].activate()
                    except Exception as err:
                        if 'concluída' not in str(err):
                            print(str(err))
                            raise
                    # clica com botão direito onde está localizado a imagem
                    pyautogui.click(x=x, y=y, button='right')
                    # pressiona a seta pra baixo 2 vezes, para chegar na opção "Salvar como"
                    pyautogui.press('down')
                    time.sleep(1)
                    pyautogui.press('down')
                    time.sleep(1)
                    pyautogui.press('enter')
                    time.sleep(3)
                     # espera até a janela de salvar como aparecer
                    # verifica se janela de salvar como aparece e aperta para iniciar o download
                    if 'Salvar como' in gw.getAllTitles():
                        pyautogui.typewrite(chap_path)
                        pyautogui.press('enter')
                        time.sleep(1)
                        pyautogui.press('enter')
                        time.sleep(2)
                        print(f"Salvar como{i}")
                        break
                    else:
                        print('else')
                        pyautogui.click(x=x, y=y, button='right')
                        pyautogui.press('down')
                        time.sleep(1)
                        pyautogui.press('down')
                        time.sleep(1)
                        pyautogui.press('enter')
                        time.sleep(2)
                    # verifica se download encerrou
                    self.web.check_crdownload(chap_path)
                    time.sleep(3)
                    print(f"Capitulo {i}Próxima página")
                    # site = self.web.web_scrap(markup=self.web_driver.page_source)
                    # imgs.extend(site.find_all('img', class_="img"))
                # for img in imgs:
                #     key = img.get('alt').split('-')[0]
                #     if key in filter_imgs.keys():
                #         continue
                #     else:
                #         filter_imgs.update({key: img})
                # img_url = [filter_imgs.get(x).get('src').replace('blob:', '') for x in filter_imgs]
                # for index,url in enumerate(img_url):
                #     self.web.download_archive(url, self.save_path)
    
    def download_image(self, url_img:str, path_archive:str, pre_name:str=""):
        try:
            fake_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0"
            # freespace = self.common.get_free_space_mb(path_archive)
            # path_archiveName = os.path.join(path_archive, f"{pre_name}.png")
            # # Verifique espaço livre.
            # if not freespace < 1024:
            #     response = request.Request(url_img, headers={'User-Agent': fake_useragent})
            #     f = request.urlopen(response)
            #     with open(path_archiveName, "wb") as file_out:
            #         file_out.write(f.read())
        except Exception as err:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if exc_type.__doc__:
                print('ERRO DURANTE EXECUÇÃO na FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.download_image.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace("\n", " ")))
            # O erro é 520 Erro de servidor 522 Erro de servidor 522 Erro de servidor 520 Erro de servidor
            if('520 Server Error' in str(err) or '522 Server Error' in str(err) or '404 Client Error' in str(err) or '403 Client Error' in str(err)):
                print('INTERN ERROR: {0}'.format(err))
            else:
                print('ERROR na linha {}: {}'.format(exc_tb.tb_lineno, err))
            return False




if __name__ == '__main__':
    downloader_manga = DownloaderManga()
    url, manga_path = downloader_manga.search_mangadex('Isekai Ojisan')
    chaps = downloader_manga.get_chaps_mangas(url)
    downloader_manga.download_chaps(chaps, manga_path)