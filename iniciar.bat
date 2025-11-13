@echo off
echo ========================================
echo   Sistema de Gestao de Fotos
echo ========================================
echo.
echo Verificando dependencias...
pip install -r requirements.txt
echo.
echo Iniciando aplicativo...
echo.
echo O aplicativo abrira automaticamente no navegador.
echo Para acessar pelo celular, use o IP do computador.
echo.
streamlit run app.py
pause


