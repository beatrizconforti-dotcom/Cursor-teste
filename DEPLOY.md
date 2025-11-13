# 🚀 Guia de Deploy - Publicar seu App na Nuvem

Este guia vai te ajudar a publicar seu aplicativo na nuvem para que ele funcione **sem precisar do seu computador ligado**, acessível de qualquer lugar (WiFi, 5G, 3G) em qualquer dispositivo!

## 📋 Opções de Deploy (Recomendadas)

### ⭐ Opção 1: Streamlit Cloud (MAIS FÁCIL E GRÁTIS) - RECOMENDADO

**Vantagens:**
- ✅ Totalmente grátis
- ✅ Deploy em minutos
- ✅ Atualizações automáticas
- ✅ HTTPS seguro
- ✅ Sem configuração complexa

**Passo a Passo:**

1. **Criar conta no GitHub:**
   - Acesse: https://github.com
   - Crie uma conta gratuita (se não tiver)

2. **Criar repositório no GitHub:**
   - Clique em "New repository"
   - Nome: `sistema-gestao-fotos` (ou qualquer nome)
   - Marque como **Público** (Public)
   - Clique em "Create repository"

3. **Enviar código para o GitHub:**
   
   **Opção A - Usando GitHub Desktop (Mais Fácil):**
   - Baixe: https://desktop.github.com
   - Instale e faça login
   - Clique em "File" → "Add Local Repository"
   - Selecione a pasta do seu projeto
   - Clique em "Publish repository"
   - Escolha o repositório que criou

   **Opção B - Usando Git no Terminal:**
   ```bash
   cd "C:\Users\beatrizconforti\OneDrive - OR\Aplicativos\Área de Trabalho\Cursor teste"
   git init
   git add .
   git commit -m "Primeiro commit"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/sistema-gestao-fotos.git
   git push -u origin main
   ```
   (Substitua SEU_USUARIO pelo seu usuário do GitHub)

4. **Fazer Deploy no Streamlit Cloud:**
   - Acesse: https://share.streamlit.io
   - Faça login com sua conta GitHub
   - Clique em "New app"
   - Selecione seu repositório
   - Selecione o branch: `main`
   - Main file path: `app.py`
   - Clique em "Deploy"
   - Aguarde alguns minutos...

5. **Pronto!** 🎉
   - Você receberá um link tipo: `https://seuapp.streamlit.app`
   - Compartilhe esse link com quem quiser
   - Acesse de qualquer lugar, qualquer dispositivo!

---

### 🌐 Opção 2: Railway (Gratuito com Limites)

**Vantagens:**
- ✅ Grátis para começar
- ✅ Fácil de usar
- ✅ Deploy rápido

**Passo a Passo:**

1. Acesse: https://railway.app
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha seu repositório
6. Railway detecta automaticamente e faz o deploy
7. Pronto! Você terá um link tipo: `https://seuapp.railway.app`

**Configuração necessária:**
- Railway usa o `Procfile` que já está no projeto
- Pode precisar ajustar o `runtime.txt` se necessário

---

### 🎯 Opção 3: Render (Gratuito)

**Vantagens:**
- ✅ Grátis
- ✅ HTTPS automático
- ✅ Deploy automático do GitHub

**Passo a Passo:**

1. Acesse: https://render.com
2. Faça login com GitHub
3. Clique em "New +" → "Web Service"
4. Conecte seu repositório GitHub
5. Configure:
   - **Name:** sistema-gestao-fotos
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Clique em "Create Web Service"
7. Aguarde o deploy (pode levar alguns minutos)
8. Pronto! Link tipo: `https://seuapp.onrender.com`

---

### 🔧 Opção 4: Heroku (Requer Cartão de Crédito)

**Nota:** Heroku agora requer verificação de cartão de crédito (mesmo no plano gratuito).

**Passo a Passo:**

1. Acesse: https://heroku.com
2. Crie uma conta
3. Instale Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
4. No terminal:
   ```bash
   heroku login
   heroku create seuapp-nome
   git push heroku main
   ```
5. Pronto! Link tipo: `https://seuapp-nome.herokuapp.com`

---

## 📝 Arquivos Necessários para Deploy

Todos os arquivos necessários já estão criados:
- ✅ `requirements.txt` - Dependências
- ✅ `Procfile` - Para Heroku/Railway
- ✅ `runtime.txt` - Versão do Python
- ✅ `.gitignore` - Arquivos a ignorar no Git

---

## 🔒 Importante: Segurança dos Dados

**⚠️ ATENÇÃO:** Com deploy na nuvem, seus dados ficam no servidor da plataforma.

**Recomendações:**
1. **Backup regular:** Faça download da pasta `data/` periodicamente
2. **Acesso privado:** Configure senha no Streamlit (veja abaixo)
3. **Dados sensíveis:** Não coloque informações muito confidenciais

---

## 🔐 Adicionar Senha ao App (Opcional)

Para proteger seu app, crie o arquivo `.streamlit/secrets.toml`:

```toml
[server]
enableCORS = false
enableXsrfProtection = true

[password]
password = "sua_senha_aqui"
```

Ou configure no Streamlit Cloud:
1. Vá em "Settings" do seu app
2. Configure "Password protection"

---

## 🆘 Solução de Problemas

### App não abre após deploy:
- Verifique se todos os arquivos foram enviados para o GitHub
- Confira se o `requirements.txt` está correto
- Veja os logs de erro na plataforma

### Erro de dependências:
- Certifique-se que o `requirements.txt` tem todas as bibliotecas
- Versões específicas podem ajudar: `streamlit==1.28.0`

### Dados não salvam:
- Algumas plataformas resetam dados periodicamente
- Considere usar banco de dados externo (SQLite na nuvem, PostgreSQL, etc.)

---

## 📱 Acessar no Celular

Depois do deploy, é simples:
1. Abra o navegador do celular
2. Digite o link do seu app (ex: `https://seuapp.streamlit.app`)
3. Pronto! Funciona em qualquer lugar!

---

## 💡 Dica Final

**Recomendação:** Use **Streamlit Cloud** - é a opção mais fácil, rápida e gratuita para começar!

Qualquer dúvida, consulte a documentação:
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Railway: https://docs.railway.app
- Render: https://render.com/docs

