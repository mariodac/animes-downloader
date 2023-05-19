import wx
import re
import os
import sys
from time import sleep
from modules.log import Logger
from modules.downloader import DownloaderAnime

if __name__ == "__main__":
    
    downloader = DownloaderAnime()
    common = downloader.common
    
    
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