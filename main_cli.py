import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
from common import Common
from re import compile
import shutil
from anilist_robot import AnilistRobot
from modules.downloader_anime import DownloaderAnime

if __name__ == "__main__":
    common = Common()
    print('Selecione o diretório que será salvo os arquivos')
    save_path = common.wx_dirdialog()
    if save_path == None:
        save_path = os.path.join(os.environ['USERPROFILE'], 'Videos')
    print(f'Arquivos serão salvos em {save_path}')
    
    option = -1
    list_episodes = []
    
    regex = compile(r'((?:https\:\/\/)|(?:http\:\/\/)|(?:www\.))?([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(?:\??)[a-zA-Z0-9\-\._\?\,\'\/\\\+&%\$#\=~]+)')
    while option != 0:
        print("-"*15)
        print("| MAIN MENU |")
        print("-"*15)
        print("0) SAIR\n1) Baixar episódios Saiko Animes\n2) Baixar episódios AnimeFire.net\n3) Atualizar Anilist\n4) Adicionar ao Anilist\n5) Baixar episódios Anitsu")
        option = common.only_read_int("Digite -> ")
        if option == 1:
            out_path = common.create_folder("- Downloaded -", save_path)
            t_i = common.initCountTime(True)
            print('Iniciado opção Baixar episódios Saiko Animes em {}'.format(common.timestamp()))
            login = input("Deseja realizar o login? (S)sim/(n)não\n-> ")
            downloader = DownloaderAnime(out_path)
            if 's' in login.lower() or 'sim' in login.lower() or 'si' in login.lower() or 'yes' in login.lower() or 'y' in login.lower():
                downloader.login_saiko()
            else:
                driver = None
            search = input("Digite o nome do anime -> ")
            name_anime = downloader.get_anime_saiko(search=search)
            if name_anime:
                downloader.down_episodes_saiko(save_path=out_path, anime_name=name_anime)
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
            url, name_anime = downloader.get_anime_animefire_net(search)
            if url and name_anime:
                downloader.down_episodes_animefire_net(url, name_anime, save_path)
            t_f = common.finishCountTime(t_i, True)
            common.print_time(t_f)
            print('Finalizado opção Baixar episódios AnimeFire.net em {}'.format(common.timestamp()))
            del downloader
            
        elif option == 3:
            anilist_robot = AnilistRobot()
            t_i = common.initCountTime(True)
            print('Iniciado opção Atualizar Anilist em {}'.format(common.timestamp()))
            username = anilist_robot.login_anilist()
            # anilist_get_chaps_from_reader.set_list_anilist(driver, 'Megami no Sprinter ', '/manga/101617/Megami-no-Sprinter/', True, True, True)
            anilist_robot.create_custom_list()
            mangas_list = {}
            mangas_list = anilist_robot.get_mangas_anilist(username)
            mangas_list = dict(sorted(mangas_list.items()))
            mangas_not_found = anilist_robot.set_list_anilist_brmangas(mangas_list)
            while len(mangas_not_found) > 1:
                ...
            t_f = common.finishCountTime(t_i, True)
            common.print_time(t_f)
            print('Finalizado opção Atualizar Anilist em {}'.format(common.timestamp()))
            del anilist_robot
        
        elif option == 4:
            t_i = common.initCountTime(True)
            print('Iniciado opção adicionar ao Anilist em {}'.format(common.timestamp()))
            anilist_robot = AnilistRobot()
            anilist_robot.login_anilist()
            items = {}
            source_list = common.only_read_int("1 - via terminal\n2 - via arquivo\n-> ")
            type_material = common.only_read_int("1 - para mangas\n2 - para animes\n-> ")
            if source_list == 1:
                print('Todos os nomes deve ter o sinal \"--\" seguido da quantidades de episódios/capitulos')
                print('Siga o exemplo a seguir')
                print('#'*50)
                print('Miageru to Kimi wa--1\nYamada-kun to Lv999 no Koi wo Suru--2')
                print('#'*50)
                print('Para iniciar não digite nada e apenas pressione o ENTER 2 vezes')
                while True:
                    item = input()
                    if item:
                        name_anime, chap = item.split('--')
                        items.update({name_anime : chap})
                    else:
                        break
            elif source_list == 2:
                file_anime_names = os.path.join(os.environ['USERPROFILE'], 'Documents', 'names.txt')
                if os.path.isfile(file_anime_names):
                    # ler o arquivo
                    with open(file_anime_names, 'r', encoding='utf-8') as file_txt:
                        content = file_txt.readlines()
                        content = [x.replace('\n', '') for x in content]
                        for line in content:
                            new_content = line.split('--')
                            if len(new_content) == 2:
                                name_anime, chap = line.split('--')
                                items.update({name_anime : chap})
            anilist_robot.add_on_anilist(items, type_material)
            t_f = common.finishCountTime(t_i, True)
            common.print_time(t_f)
            print('Finalizado opção adicionar ao Anilist em {}'.format(common.timestamp()))
            del anilist_robot
        
        elif option == 5:
            downloader = DownloaderAnime(save_path)
            t_i = common.initCountTime(True)
            print('Iniciado opção Baixar episódios Anitsu em {}'.format(common.timestamp()))
            print('Obtenha o link aqui -> https://anitsu.online')
            url = input("Digite a url do anime -> ")
            if regex.match(url):
                downloader.downdload_anitsu(url)
            else:
                print("Não é url")
            t_f = common.finishCountTime(t_i, True)
            common.print_time(t_f)
            print('Finalizado opção Baixar episódios Anitsu em {}'.format(common.timestamp()))
            del downloader
        
        elif  option == 0:
            break
        
        else:
            print("Opção inválida")
            continue