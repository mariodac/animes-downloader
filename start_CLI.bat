: Desenvolvido: Mario Cabral
: Executa script para instalação de ambiente e suas dependencias
@echo off
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
    echo executando script
	"%CD%\env\Scripts\python" main_cli.py
)