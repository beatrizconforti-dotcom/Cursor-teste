#!/bin/bash

echo "========================================"
echo "  Sistema de Gestão de Fotos"
echo "========================================"
echo ""
echo "Verificando dependências..."
pip install -r requirements.txt
echo ""
echo "Iniciando aplicativo..."
echo ""
echo "O aplicativo abrirá automaticamente no navegador."
echo "Para acessar pelo celular, use o IP do computador."
echo ""
streamlit run app.py


