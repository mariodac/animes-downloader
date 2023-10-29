import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
from common import Common
import re
import shutil
from time import sleep
from anilist_get_chaps_from_reader import AnilistGetChapsFromReader
from modules.downloader import DownloaderAnime

if __name__ == "__main__":
    common = Common()
    save_path = os.path.join(os.environ['USERPROFILE'], 'Videos')
    
    option = -1
    list_episodes = []
    
    regex = re.compile('((?:https\:\/\/)|(?:http\:\/\/)|(?:www\.))?([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(?:\??)[a-zA-Z0-9\-\._\?\,\'\/\\\+&%\$#\=~]+)')
    while option != 0:
        
        print("0 - SAIR\n1 - Baixar episódios Saiko Animes\n2 - Baixar episódios AnimeFire.net\n3 - Atualizar Anilist")
        option = common.only_read_int("Digite -> ")
        if option == 1:
            out_path = common.create_folder("- Downloaded -", save_path)
            downloader = DownloaderAnime(out_path)
            t_i = common.initCountTime(True)
            print('Iniciado opção Baixar episódios Saiko Animes em {}'.format(common.timestamp()))
            login = input("Deseja realizar o login? (S)sim/(n)não\n-> ")
            if 's' in login.lower() or 'sim' in login.lower() or 'si' in login.lower() or 'yes' in login.lower() or 'y' in login.lower():
                downloader.login_saiko()
            else:
                driver = None
            search = input("Digite o nome do anime -> ")
            name = downloader.get_anime_saiko(search=search)
            if name:
                downloader.down_episodes_saiko(save_path=out_path, name=name)
                shutil.rmtree(out_path)
            print('Finalizado opção Baixar episódios Saiko Animes em {}'.format(common.timestamp()))
            t_f = common.finishCountTime(t_i, True)
            common.print_time(t_f)
            del downloader
        elif option == 2:
            downloader = DownloaderAnime(save_path)
            t_i = common.initCountTime(True)
            print('Iniciado opção Baixar episódios AnimeFire.net em {}'.format(common.timestamp()))
            search = input("Digite o nome do anime -> ")
            url, name = downloader.get_anime_animefire_net(search)
            if url and name:
                downloader.down_episodes_animefire_net(url, name, save_path)
            t_f = common.finishCountTime(t_i, True)
            common.print_time(t_f)
            print('Finalizado opção Baixar episódios AnimeFire.net em {}'.format(common.timestamp()))
            del downloader
            
        elif option == 3:
            anilist_get_chaps_from_reader = AnilistGetChapsFromReader()
            t_i = common.initCountTime(True)
            print('Iniciado opção Atualizar Anilist em {}'.format(common.timestamp()))
            username = anilist_get_chaps_from_reader.login_anilist()
            # anilist_get_chaps_from_reader.set_list_anilist(driver, 'Megami no Sprinter ', '/manga/101617/Megami-no-Sprinter/', True, True, True)
            anilist_get_chaps_from_reader.create_custom_list()
            mangas_list = {}
            file_anime_names = os.path.join(os.environ['USERPROFILE'], 'Documents', 'alt_names.txt')
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
                mangas_list = anilist_get_chaps_from_reader.get_mangas_anilist(username)
            mangas_not_found = anilist_get_chaps_from_reader.set_list_anilist_mangaschan(mangas_list)
            t_f = common.finishCountTime(t_i, True)
            common.normalize_name()
            common.print_time(t_f)
            print('Finalizado opção Baixar episódios AnimeFire.net em {}'.format(common.timestamp()))
            del anilist_get_chaps_from_reader
        else:
            print("Opção inválida")
            continue