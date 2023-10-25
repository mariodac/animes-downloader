# Projeto em andamento ...

Download de animes & mangás com automação python

Projeto idealizado e desenvolvido por mim, qualquer dúvida fique a vontade para entrar contato comigo você pode me encontrar [aqui](https://linktr.ee/mariodac)



Até o momento o projeto possui três opções:

1. Baixar episódios da Saiko Animes (com ou sem acesso premium) [Tutorial](#item1)
2. Baixar episódio da AnimeFire [Tutorial](#item2)
3. Atualizar listas personalizadas de mangás no anilist [Tutorial](#item3)

## Tecnologias utilizadas

<div style="display: inline_block"><br>
  <img align="center" alt="Python" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">
  <img align="center" alt="Selenium" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/selenium/selenium-original.svg">
</div><br>

<a id="item1"></a>

## Dependências

Caso queira não queira fazer o passos a seguir manualmente. Apenas execute o [Script Windows](start_CLI.bat) ou [Script Linux](start_CLI.sh)


É necessário ter o seguinte item para executar o projeto:
- Python 3.7+ [Linux](https://python.org.br/instalacao-linux/) | [Windows](https://www.python.org/downloads/)

É recomendado a criação de ambiente virtual para execução do projeto, recomendo seguir os passos a seguir:


No linux:
- Para criação do ambiente:
```
python3 -m venv env
```
- Para ativar o ambiente:
```
env/bin/activate
```
No windows:
- Para criação do ambiente:
```
py -3 -m venv env
```
- Para ativar o ambiente:
```
env\Scripts\activate
```

É preciso realizar a instalação das bibliotecas necessárias para executar o projeto.
Todos as bibliotecas e suas versões estão no arquivo [requirements](requirements.txt)

Para instalar as bibliotecas siga os passos:

**ATENÇÃO [Ative](#ancora1) o seu ambiente antes executar esses comandos!**

*Será criado o ambiente python*


No Linux:
```
env/bin/pip install -r requirements.txt
```

No windows:
```
env\Scripts\pip install -r requirements.txt
```



## Páginas suportadas

<table>
    <thead>
      <tr>
        <th>Anime</th>
        <th>Manga</th>
        <th>Track List</th>
      </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="https://saikoanimes.net"><img src="https://www.google.com/s2/favicons?domain=https://saikoanimes.net"> Saikô Animes</a></td>
            <td><a href="https://mangaschan.net"><img src="https://www.google.com/s2/favicons?domain=https://mangaschan.net"> Mangás Chan</a></td>
            <td><a href="https://anilist.co"><img src="https://www.google.com/s2/favicons?domain=https://anilist.co"> Anilist</a></td>
        </tr>
        <tr>
            <td><a href="https://animefire.net"><img src="https://www.google.com/s2/favicons?domain=https://animefire.net"> AnimeFire.net</a></td>
            <td></td>
            <td></td>
        </tr>
    </tbody>
  </table>

<a id="item1"></a>

## Baixar episódios da Saiko Animes
Nesta função é feita uma automação no navegador para baixar os episódios de animes do site Saikô Animes. Pode haver a necessidade de realizar login
**IMPORTANTE**: o Saikô Animes apenas disponibiliza para download de apenas animes que estão em lançamento na temporada, para obter acesso a todos os anime é preciso ter uma conta no site e pagar o Saikô Pass.

### Tutorial

 O caminho padrão onde será salvo os vídeos é `C:/Users/%USERNAME%/Videos`


<a id="item2"></a>

## Baixar episódios do AnimeFire.net
Nesta função é feita uma automação no navegador para baixar os episódios de animes do site AnimeFire.net. Não há necessidade de realizar login.

### Tutorial

Ao executar o arquivo [main_cli](main_cli.py), será exibida o seguinte:

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_1.png?raw=true)

Escolha a opção 2 para selecionar para baixar episódios do AnimeFire.net

Será soliciado para que digite o nome do anime, então digite o nome do anime que deseja baixar

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_2.png?raw=true)


Quando a pesquisa retornar mais de um resultado será solicitado digitar o numero correspondente ao resultado

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_4.png?raw=true)

Depois de selecionar qual resultado corresponde a sua pesquisa ou caso sua pesquisa retorna apenas 1 resultado, será exibido a lista de episódios, e solicitado que digite o intervalo de episódios que deseja baixar:

 ![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_5.png?raw=true)

Foi configurado o seguinte esquema para seleção dos episódios:

 - Caso deseje baixar apenas 1 episódio, digite apenas o número do episódio desejado, por exemplo, para baixar o episódio 1, basta digitar 1
 - Caso deseje baixar um intervalo de episódios, digite o número inicial seguido do - e após o número final, por exemplo, para baixar do episódio 1 até 10, basta digitar 1-10
 - Caso deseja baixar todos os episódios, basta digitar *

 Após selecionar o intervalo de episódios será solicitado a seleção da qualidade do vídeo, digite o numero correspondente a qualidade desejada:

 ![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_6.png?raw=true)

 Após selecionar o intervalo de episódios, iniciará o carregamento do episódio, o que pode demorar um pouco.

  ![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_3.png?raw=true)

 Logo em seguida é iniciado o download do vídeo:

 ![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_7.png?raw=true)

 O caminho padrão onde será salvo os vídeos é `C:/Users/%USERNAME%/Videos`

**OBSERVAÇÃO:** Em certos animes, devido utilizar um player antigo, o script abrirá o navegador e realizara o download pelo navegador, é importantissímo que não meche no PC nesse momento pois pode acabar atrapalhando


<a id="item1"></a>

## Atualizar listas personalizadas de mangás no anilist

Nesta função é feita uma automação no navegador para criar listas personalizadas no anilist para salvar mangás com novo lançamentos de capítulos, mangas sem lançamento de capítulos e mangás que já encerrou o lançamento de capítulos. Inicialmente o script realiza a criação de 4 listas personalizadas com os seguintes nomes:

- New Chaps Releases
- Waiting New Chaps Releases
- Finished Releases
- Adult Label

**OBSERVAÇÃO**: É indispensável criar as listas com outros nomes, recomendo, recomendo a criação manual das listas.

Inicialmente selecione a opção corresponte a está função:

 ![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_8.png?raw=true)

 Após irá iniciar o chrome, e o terminal ficará pausado, vá para o chrome que acabou de abrir e realize o login e aguarde a tela inicial do anilist, após realizado isso volte para o terminal e apenas pressione qualquer tecla para continuar.

Como isso será iniciado a captura da lista dos mangás que estão na sua lista "Reading" e captura dos nomes alternativos, este processo demora um pouco, mas no final é criado um arquivo chamado "alt_names.txt", que será utilizado para pular esta etapa de captura dos nomes dos mangás. 

A próxima parte é onde será realizada busca do mangá no site leitor e comparado o ultimo capítulo do leitor com o ultimo capítulo atualizado no anilist, caso o mangá esteja com o mesmo número de capítulo tanto no anilis quanto no leitor será adicionado na lista "Waiting New Chaps Releases", caso o mangá esteja com o número de capítulo no leitor maior que o do anilist será adicionado na lista "New Chaps Releases", caso o mangá esteja finalizado no anilist e no leitor será adicionado na lista "Finishe Releases".

