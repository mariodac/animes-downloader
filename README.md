# Projeto em andamento ...

Download de animes & mangás com automação python

Projeto idealizado e desenvolvido por mim, qualquer dúvida fique a vontade para entrar contato comigo você pode me encontrar [aqui](https://linktr.ee/mariodac)



Até o momento o projeto possui três opções:

1. Baixar episódios da Saiko Animes (com ou sem acesso premium) [Tutorial](#item1)
2. Baixar episódio da AnimeFire [Tutorial](#item2)
3. Atualizar listas personalizadas de mangás no anilist [Tutorial](#item3)
4. Adicionar mangás/animes no anilist [Tutorial](#item4)
5. Baixar episódios Anitsu 

## Tecnologias utilizadas

<div style="display: inline_block"><br>
  <img align="center" alt="Python" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">
  <img align="center" alt="Selenium" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/selenium/selenium-original.svg">
</div><br>

### Baixe seu executável [aqui](https://github.com/mariodac/animes-downloader/releases/download/beta/beta_teste_CLI.exe)

## Dependências

Caso não queira fazer o passos a seguir manualmente. Apenas execute o [Script Windows](start_CLI.bat)

É necessário ter o seguinte item para executar o projeto:
- Python 3.7+ [Windows](https://www.python.org/downloads/)

É recomendado a criação de ambiente virtual para execução do projeto, recomendo seguir os passos a seguir:

<a id="ancora1"></a>


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

Após executar o projeto, escolha o numero correspondente a esta função

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_13.png?raw=true)

Em seguida será solicitado se deseja realizar o login. Sendo S ou s para sim e N ou n para não

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_14.png?raw=true)

Lembrando que é apenas necessário login caso tenha pago o Saikô pass na sua conta.

Caso escolha para realizar o login, o navegador será aberto, mas preencha suas credencias diretamente no terminal.

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_15.png?raw=true)

Após realizar o login, ou caso tenha escolhido não realizar login, será solicitado o nome do anime a ser pesquisado no site.

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_16.png?raw=true)

Quando a pesquisa retornar mais de um resultado será solicitado digitar o numero correspondente ao resultado.

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_17.png?raw=true)

Depois de selecionar qual resultado corresponde a sua pesquisa ou caso sua pesquisa retorna apenas 1 resultado, será exibido a lista de episódios, e solicitado que digite o intervalo de episódios que deseja baixar:

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_18.png?raw=true)

Foi configurado o seguinte esquema para seleção dos episódios:

 - Caso deseje baixar apenas 1 episódio, digite apenas o número do episódio desejado, por exemplo, para baixar o episódio 1, basta digitar 1
 - Caso deseje baixar um intervalo de episódios, digite o número inicial seguido do - e após o número final, por exemplo, para baixar do episódio 1 até 10, basta digitar 1-10
 - Caso deseja baixar todos os episódios, basta digitar *

Após selecionar o intervalo de episódios desejado, o download será iniciado no navegador

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_19.png?raw=true)

Após encerrado o download será exibido o tempo de execução para realizar os downloads

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_20.png?raw=true)

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


<a id="item3"></a>

## Atualizar listas personalizadas de mangás no anilist

Nesta função é feita uma automação no navegador para criar listas personalizadas no anilist para salvar mangás com novo lançamentos de capítulos, mangas sem lançamento de capítulos e mangás que já encerrou o lançamento de capítulos. Inicialmente o script realiza a criação de 4 listas personalizadas com os seguintes nomes:

- New Chaps Releases
- Waiting New Chaps Releases
- Finished Releases
- Adult Label

**OBSERVAÇÃO**: É indispensável criar as listas com outros nomes, recomendo, recomendo a criação manual das listas.

Para o tutorial em vídeo acesse [aqui](https://www.youtube.com/watch?v=o7lu4Tc5kCM)

Inicialmente selecione a opção corresponte a está função:

 ![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_8.png?raw=true)

 Após irá iniciar o chrome, e o terminal ficará pausado, vá para o chrome que acabou de abrir e realize o login e aguarde a tela inicial do anilist, após realizado isso volte para o terminal e apenas pressione qualquer tecla para continuar.

Como isso será iniciado a captura da lista dos mangás que estão na sua lista "Reading" e captura dos nomes alternativos, este processo demora um pouco, mas no final é criado um arquivo chamado "alt_names.txt", que será utilizado para pular esta etapa de captura dos nomes dos mangás. O arquivo será salvo no caminho padrão `C:/Users/%USERNAME%/Documents`

A próxima parte é onde será realizada busca do mangá no site leitor e comparado o ultimo capítulo do leitor com o ultimo capítulo atualizado no anilist, caso o mangá esteja com o mesmo número de capítulo tanto no anilis quanto no leitor será adicionado na lista "Waiting New Chaps Releases", caso o mangá esteja com o número de capítulo no leitor maior que o do anilist será adicionado na lista "New Chaps Releases", caso o mangá esteja finalizado no anilist e no leitor será adicionado na lista "Finished Releases".

Após finalizado basta fechar o terminal, mas antes de fechar verificar as mensagens do terminal

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_11.png?raw=true)

Como podemos ver no print, teve mangá com erro, onde seria que ocorreu algum erro durante a execução, teve mangá não encontrado, onde mesmo com os nomes alternativos não foi possível encontrar no mangas chan. Para melhorar as chances de encotrar deve editar o arquivo alt_names.txt e adicionar mais nomes alternativos.

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_10.png?raw=true)

Nesse arquivo cada linha, representa um mangá, onde primeiro vem o nome principal após o "--" vem o link dele no anilist após "||" vem o capitulo e após cada "||" vem os nomes alternativos, por exemplo para adicionar mais nomes alternativos, basta no final da linha, adicionar um espaço seguido de || e mais um espaço seguido do nome alternativo ficando assim:

`Jiken-Jaken! -- /manga/101613/JikenJaken/ || 20/92 || Jiken-Jaken! || JikenJaken || Jiken Jaken`

Com isso terá sua biblioteca muita mais organizada de maneira automática!

![Print](https://github.com/mariodac/animes-downloader/blob/main/.imagens/Screenshot_12.png?raw=true)

<a id="item4"></a>

# Adicionar mangás/animes no anilist

Nesta função é realizada a automação para adicionar mangás/animes no anilist, obtendo os nomes e cápitulos/episódios via terminal ou via arquivo, e adiciona na lista "Reading" do anilist

O arquivo deve ser salvo com nome `names.txt` no caminho `C:/Users/%USERNAME%/Documents`

<a id="default1"></a>
Siga o seguinte padrão:
Nome da obra--quantidade de capitulos/episódios
```
Yamada-kun to Lv999 no Koi wo Suru--2
Satanophany--0
```

