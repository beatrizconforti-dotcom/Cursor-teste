# 🚀 Guia Rápido de Uso

## ⚡ Início Rápido

### Windows:
1. Clique duas vezes em `iniciar.bat`
2. Aguarde o navegador abrir automaticamente

### Mac/Linux:
1. Abra o terminal na pasta do projeto
2. Execute: `chmod +x iniciar.sh && ./iniciar.sh`

### Manual:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📱 Acessar pelo Celular

### Passo a Passo:

1. **Encontrar o IP do computador:**
   - Windows: Abra o Prompt de Comando → digite `ipconfig` → procure "IPv4"
   - Mac: Terminal → digite `ifconfig | grep "inet "`
   - Linux: Terminal → digite `hostname -I`

2. **Executar com acesso externo:**
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

3. **No celular:**
   - Conecte na mesma rede Wi-Fi
   - Abra o navegador
   - Digite: `http://SEU_IP:8501`
   - Exemplo: `http://192.168.1.100:8501`

## 📸 Como Usar

### 1. Adicionar Item
- Clique em "➕ Adicionar Item"
- Preencha todos os campos
- Escolha: Upload da galeria OU Tirar foto
- Clique em "Salvar Item"

### 2. Ver Lista
- Clique em "📋 Lista de Itens"
- Veja todos os itens ordenados por Pavimento
- Clique em um item para expandir e ver detalhes

### 3. Editar Item
- Na lista, clique em "✏️ Editar" no item desejado
- Modifique os campos
- Opcionalmente, troque a foto
- Clique em "Salvar Alterações"

### 4. Filtrar e Gerar PDF
- Clique em "🔍 Filtrar e Relatório"
- Selecione os filtros desejados
- Clique em "Gerar PDF com Itens Filtrados"
- Baixe o PDF gerado

## 💡 Dicas

- ✅ Os dados são salvos automaticamente
- ✅ Faça backup da pasta `data/` regularmente
- ✅ Use filtros para encontrar itens rapidamente
- ✅ O PDF inclui todas as informações e fotos

## 🔧 Solução de Problemas

**App não abre:**
- Verifique se Python está instalado
- Execute: `pip install -r requirements.txt`

**Não consigo acessar pelo celular:**
- Verifique se está na mesma rede Wi-Fi
- Desative o firewall temporariamente
- Use o IP correto do computador

**Fotos não aparecem:**
- Verifique se a pasta `data/images/` existe
- Certifique-se de ter permissões de escrita

## 📞 Precisa de Ajuda?

Consulte o `README.md` para informações detalhadas!


