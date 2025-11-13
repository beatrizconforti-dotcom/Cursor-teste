# 📸 Sistema de Gestão de Fotos

Aplicativo web para gerenciar fotos com informações detalhadas, filtros e geração de relatórios em PDF.

## 🚀 Funcionalidades

- ✅ Adicionar fotos da galeria ou tirar fotos em tempo real
- ✅ Formulário completo com todos os campos solicitados
- ✅ Lista de itens ordenada alfabeticamente por Pavimento
- ✅ Edição de itens existentes
- ✅ Filtros por Empresa, Pavimento e Status
- ✅ Geração de relatórios PDF (com dados filtrados ou todos)
- ✅ Interface responsiva para celular e desktop

## 📋 Campos do Formulário

- **Pavimento** (Título) - Texto
- **Foto** - Upload ou captura em tempo real
- **Empresa** - Texto
- **Atividade** - Texto
- **Local** - Texto
- **Observações** - Texto
- **Data de Criação** - Automática
- **Status** - Concluído, Não Concluído ou Em Andamento

## 🛠️ Instalação

### 1. Instalar Python

Certifique-se de ter Python 3.8 ou superior instalado:
- Windows: [Download Python](https://www.python.org/downloads/)
- Mac: `brew install python3`
- Linux: `sudo apt-get install python3`

### 2. Instalar Dependências

Abra o terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

### 3. Executar o Aplicativo

```bash
streamlit run app.py
```

O aplicativo abrirá automaticamente no navegador em `http://localhost:8501`

## 📱 Como Usar no Celular

### Opção 1: Acessar pelo Navegador do Celular (Mais Simples)

1. **Encontrar o IP do seu computador:**
   - Windows: Abra o Prompt de Comando e digite `ipconfig`
   - Procure por "Endereço IPv4" (exemplo: 192.168.1.100)
   - Mac/Linux: Digite `ifconfig` ou `ip addr`

2. **Executar o Streamlit com acesso externo:**
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

3. **Acessar pelo celular:**
   - Certifique-se de que o celular está na mesma rede Wi-Fi
   - Abra o navegador do celular
   - Digite: `http://SEU_IP:8501` (exemplo: `http://192.168.1.100:8501`)

### Opção 2: Deploy em Serviço Cloud (Recomendado para Uso Contínuo)

#### Streamlit Cloud (Grátis)
1. Crie uma conta em [streamlit.io](https://streamlit.io)
2. Conecte seu repositório GitHub
3. Deploy automático!

#### Outras Opções:
- **Heroku** - Deploy simples
- **Railway** - Deploy rápido
- **Render** - Grátis para começar
- **PythonAnywhere** - Fácil de usar

### Opção 3: Criar App Nativo (Avançado)

Para criar um app nativo que instala no celular, você pode usar:
- **Kivy** - Framework Python para apps mobile
- **BeeWare** - Cria apps nativos
- **Buildozer** - Compila para Android

## 📁 Estrutura de Arquivos

```
projeto/
├── app.py              # Aplicativo principal
├── requirements.txt    # Dependências
├── README.md          # Este arquivo
└── data/              # Criado automaticamente
    ├── database.json  # Banco de dados (JSON)
    ├── images/        # Fotos salvas
    └── relatorio_*.pdf # PDFs gerados
```

## 💾 Armazenamento de Dados

Os dados são salvos localmente em:
- `data/database.json` - Informações dos itens
- `data/images/` - Fotos salvas

**⚠️ Importante:** Faça backup regular da pasta `data/` para não perder informações!

## 🔧 Personalização

O aplicativo pode ser facilmente personalizado editando `app.py`:
- Cores e estilos
- Campos adicionais
- Layout
- Funcionalidades extras

## 📝 Notas

- As fotos são salvas localmente na pasta `data/images/`
- Os PDFs são gerados na pasta `data/`
- A ordenação é alfabética/numérica natural por Pavimento
- Todos os filtros podem ser combinados

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique se todas as dependências estão instaladas
2. Certifique-se de ter Python 3.8+
3. Verifique se a porta 8501 não está em uso

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente.


