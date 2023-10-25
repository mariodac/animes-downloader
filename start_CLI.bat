: Desenvolvido: Mario Cabral
: Executa script para instalação de ambiente e suas dependencias
@echo off
: obtem versão do python
set cmd=python -V
FOR /F "tokens=*" %%i IN (' %cmd% ') DO SET P=%%i

: Verifica se ambiente existe e executa script, senão existir cria ambiente e executa script
IF EXIST "%CD%\env" (
	echo executando script
	"%CD%\env\Scripts\python" main_cli.py
    
) ELSE (
	echo criando ambiente
    set c="python -V"
	py -3 -m venv ./env
	echo instalando requisitos
	"%CD%\env\Scripts\pip" install -r ./requirements.txt
    : Verifa versão do python e instalado wxpython
    echo %P% | findstr /r "3.7" >null 2>&1
    if errorlevel 1 (echo ) else ("%CD%\env\Scripts\pip" install "%CD%\utils\wxPython-4.2.1a1-cp37-cp37m-win_amd64.whl")
    echo %P% | findstr /r "3.8" >null 2>&1
    if errorlevel 1 (echo ) else ("%CD%\env\Scripts\pip" install "%CD%\utils\wxPython-4.2.1a1-cp38-cp38-win_amd64.whl")
    echo %P% | findstr /r "3.9" >null 2>&1
    if errorlevel 1 (echo ) else ("%CD%\env\Scripts\pip" install "%CD%\utils\wxPython-4.2.1a1-cp39-cp39-win_amd64.whl")
    echo %P% | findstr /r "3.10" >null 2>&1
    if errorlevel 1 (echo ) else ("%CD%\env\Scripts\pip" install "%CD%\utils\wxPython-4.2.1a1-cp310-cp310-win_amd64.whl")
    echo %P% | findstr /r "3.11" >null 2>&1
    if errorlevel 1 (echo ) else ("%CD%\env\Scripts\pip" install "%CD%\utils\wxPython-4.2.1a1-cp311-cp311-win_amd64.whl")
	"%CD%\env\Scripts\python" main_cli.py
)