import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image
import io
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import uuid

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão de Fotos",
    page_icon="📸",
    layout="wide"
)

# Diretórios
DATA_DIR = "data"
IMAGES_DIR = os.path.join(DATA_DIR, "images")
DB_FILE = os.path.join(DATA_DIR, "database.json")

# Criar diretórios se não existirem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Inicializar banco de dados
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def load_data():
    init_db()
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_image(uploaded_file, item_id):
    """Salva a imagem e retorna o caminho"""
    file_extension = uploaded_file.name.split('.')[-1]
    filename = f"{item_id}.{file_extension}"
    filepath = os.path.join(IMAGES_DIR, filename)
    
    with open(filepath, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return filepath

def generate_pdf(data, output_path):
    """Gera PDF com os dados"""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Título
    story.append(Paragraph("Relatório de Fotos", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Tabela de dados
    for idx, item in enumerate(data, 1):
        # Título do item
        story.append(Paragraph(f"<b>Item {idx}: {item['pavimento']}</b>", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        # Informações do item (sem cabeçalho)
        info_data = [
            ['Pavimento', item['pavimento']],
            ['Empresa', item['empresa']],
            ['Atividade', item['atividade']],
            ['Local', item['local']],
            ['Observações', item['observacoes']],
            ['Data de Criação', item['data_criacao']],
            ['Status', item['status']]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Imagem se existir
        if item.get('imagem_path') and os.path.exists(item['imagem_path']):
            try:
                img = RLImage(item['imagem_path'], width=4*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.3*inch))
            except:
                story.append(Paragraph("<i>Imagem não disponível</i>", styles['Normal']))
        
        # Linha separadora
        if idx < len(data):
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("_" * 80, styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)

# Carregar dados
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Sidebar para navegação
st.sidebar.title("📸 Menu")
page = st.sidebar.radio(
    "Navegação",
    ["➕ Adicionar Item", "📋 Lista de Itens", "🔍 Filtrar e Relatório"]
)

# Página: Adicionar Item
if page == "➕ Adicionar Item":
    st.title("➕ Adicionar Novo Item")
    
    # Inicializar session_state para foto e contador de formulário
    if 'foto_selecionada' not in st.session_state:
        st.session_state.foto_selecionada = None
    if 'form_counter' not in st.session_state:
        st.session_state.form_counter = 0
    
    # Limpar formulário se necessário (incrementar contador para criar novo form)
    if st.session_state.get('limpar_formulario', False):
        st.session_state.foto_selecionada = None
        st.session_state.form_counter += 1
        st.session_state.limpar_formulario = False
    
    with st.form(key=f"form_adicionar_{st.session_state.form_counter}", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            pavimento = st.text_input("Pavimento (Título):", key=f"pavimento_{st.session_state.form_counter}")
            empresa = st.text_input("Empresa:", key=f"empresa_{st.session_state.form_counter}")
            atividade = st.text_input("Atividade:", key=f"atividade_{st.session_state.form_counter}")
            local = st.text_input("Local:", key=f"local_{st.session_state.form_counter}")
        
        with col2:
            observacoes = st.text_area("Observações:", height=100, key=f"observacoes_{st.session_state.form_counter}")
            status = st.selectbox(
                "Status:",
                ["Concluído", "Não Concluído", "Em Andamento"],
                key=f"status_{st.session_state.form_counter}"
            )
        
        st.markdown("---")
        st.subheader("📷 Carregar Foto")
        
        # Tabs para escolher entre galeria ou câmera
        tab1, tab2 = st.tabs(["📁 Galeria", "📷 Tirar Foto"])
        
        uploaded_file = None
        
        with tab1:
            file_upload = st.file_uploader(
                "Selecione uma foto da galeria:",
                type=['png', 'jpg', 'jpeg'],
                key=f"upload_galeria_{st.session_state.form_counter}"
            )
            if file_upload is not None:
                st.session_state.foto_selecionada = file_upload
        
        with tab2:
            camera_input = st.camera_input("Tire uma foto:", key=f"camera_{st.session_state.form_counter}")
            if camera_input is not None:
                st.session_state.foto_selecionada = camera_input
        
        # Usar foto do session_state
        if st.session_state.foto_selecionada is not None:
            uploaded_file = st.session_state.foto_selecionada
        
        # Mostrar preview da imagem
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Preview da foto", width=300)
            except Exception as e:
                st.warning(f"Erro ao carregar preview: {str(e)}")
        
        submitted = st.form_submit_button("💾 Salvar Item", type="primary")
        
        if submitted:
            # Verificar foto no session_state se não estiver no uploaded_file
            if uploaded_file is None and st.session_state.foto_selecionada is not None:
                uploaded_file = st.session_state.foto_selecionada
            
            # Validar campos
            if not pavimento or not pavimento.strip():
                st.error("⚠️ Por favor, preencha o campo Pavimento!")
            elif uploaded_file is None:
                st.error("⚠️ Por favor, adicione uma foto!")
            else:
                try:
                    # Criar novo item
                    item_id = str(uuid.uuid4())
                    imagem_path = save_image(uploaded_file, item_id)
                    
                    novo_item = {
                        "id": item_id,
                        "pavimento": pavimento.strip(),
                        "empresa": empresa.strip() if empresa else "",
                        "atividade": atividade.strip() if atividade else "",
                        "local": local.strip() if local else "",
                        "observacoes": observacoes.strip() if observacoes else "",
                        "status": status,
                        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "imagem_path": imagem_path
                    }
                    
                    st.session_state.data.append(novo_item)
                    save_data(st.session_state.data)
                    
                    st.success(f"✅ Item '{pavimento}' adicionado com sucesso!")
                    st.balloons()
                    
                    # Marcar para limpar formulário (incrementar contador)
                    st.session_state.limpar_formulario = True
                    st.session_state.foto_selecionada = None
                    
                    # Forçar rerun para limpar formulário
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Erro ao salvar item: {str(e)}")

# Página: Lista de Itens
elif page == "📋 Lista de Itens":
    st.title("📋 Lista de Itens")
    
    data = st.session_state.data
    
    if not data:
        st.info("📭 Nenhum item cadastrado ainda. Adicione um novo item!")
    else:
        # Ordenar por Pavimento (alfabético/numérico)
        data_sorted = sorted(data, key=lambda x: (
            # Separar números e letras para ordenação natural
            [int(c) if c.isdigit() else c.lower() for c in x['pavimento']]
        ))
        
        st.info(f"📊 Total de itens: {len(data_sorted)}")
        
        # Mostrar itens
        for idx, item in enumerate(data_sorted):
            with st.expander(f"🏢 {item['pavimento']} - {item['status']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Empresa:** {item['empresa']}")
                    st.write(f"**Atividade:** {item['atividade']}")
                    st.write(f"**Local:** {item['local']}")
                    st.write(f"**Observações:** {item['observacoes']}")
                    st.write(f"**Data de Criação:** {item['data_criacao']}")
                    st.write(f"**Status:** {item['status']}")
                
                with col2:
                    if item.get('imagem_path') and os.path.exists(item['imagem_path']):
                        try:
                            img = Image.open(item['imagem_path'])
                            st.image(img, caption="Foto", width=200)
                        except:
                            st.error("Erro ao carregar imagem")
                    else:
                        st.warning("Imagem não encontrada")
                
                # Botões de ação
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"✏️ Editar", key=f"edit_{item['id']}"):
                        st.session_state.edit_id = item['id']
                        st.session_state.edit_item = item.copy()
                        st.rerun()
                with col_btn2:
                    if st.button(f"🗑️ Excluir", key=f"delete_{item['id']}"):
                        st.session_state.delete_id = item['id']
                        st.session_state.delete_item = item.copy()
                        st.rerun()
        
        # Diálogo de confirmação de exclusão
        if 'delete_id' in st.session_state:
            st.markdown("---")
            st.warning("⚠️ Confirmar Exclusão")
            
            item_delete = st.session_state.delete_item
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**Pavimento:** {item_delete['pavimento']}")
                st.write(f"**Empresa:** {item_delete['empresa']}")
                st.write(f"**Status:** {item_delete['status']}")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("✅ Confirmar Exclusão", type="primary", key="confirm_delete"):
                    # Remover item da lista
                    st.session_state.data = [item for item in st.session_state.data if item['id'] != st.session_state.delete_id]
                    save_data(st.session_state.data)
                    
                    # Deletar imagem se existir
                    if item_delete.get('imagem_path') and os.path.exists(item_delete['imagem_path']):
                        try:
                            os.remove(item_delete['imagem_path'])
                        except:
                            pass
                    
                    st.success(f"✅ Item '{item_delete['pavimento']}' excluído com sucesso!")
                    
                    # Limpar estado de exclusão
                    if 'delete_id' in st.session_state:
                        del st.session_state.delete_id
                    if 'delete_item' in st.session_state:
                        del st.session_state.delete_item
                    
                    st.rerun()
            
            with col_btn2:
                if st.button("❌ Cancelar", key="cancel_delete"):
                    if 'delete_id' in st.session_state:
                        del st.session_state.delete_id
                    if 'delete_item' in st.session_state:
                        del st.session_state.delete_item
                    st.rerun()
        
        # Formulário de edição
        if 'edit_id' in st.session_state:
            st.markdown("---")
            st.subheader("✏️ Editar Item")
            
            item_edit = st.session_state.edit_item
            
            with st.form("form_editar"):
                col1, col2 = st.columns(2)
                
                with col1:
                    pavimento_edit = st.text_input("Pavimento (Título):", value=item_edit['pavimento'], key="pavimento_edit")
                    empresa_edit = st.text_input("Empresa:", value=item_edit['empresa'], key="empresa_edit")
                    atividade_edit = st.text_input("Atividade:", value=item_edit['atividade'], key="atividade_edit")
                    local_edit = st.text_input("Local:", value=item_edit['local'], key="local_edit")
                
                with col2:
                    observacoes_edit = st.text_area("Observações:", value=item_edit['observacoes'], key="observacoes_edit", height=100)
                    status_edit = st.selectbox(
                        "Status:",
                        ["Concluído", "Não Concluído", "Em Andamento"],
                        index=["Concluído", "Não Concluído", "Em Andamento"].index(item_edit['status']),
                        key="status_edit"
                    )
                
                st.markdown("---")
                st.subheader("📷 Foto Atual")
                if item_edit.get('imagem_path') and os.path.exists(item_edit['imagem_path']):
                    try:
                        img_edit = Image.open(item_edit['imagem_path'])
                        st.image(img_edit, caption="Foto atual", width=300)
                    except:
                        st.warning("Imagem não encontrada")
                
                st.subheader("📷 Nova Foto (opcional)")
                
                # Inicializar session_state para foto de edição
                edit_foto_key = f"foto_edit_{item_edit['id']}"
                if edit_foto_key not in st.session_state:
                    st.session_state[edit_foto_key] = None
                
                # Tabs para escolher entre galeria ou câmera
                tab1_edit, tab2_edit = st.tabs(["📁 Galeria", "📷 Tirar Foto"])
                
                uploaded_file_edit = None
                
                with tab1_edit:
                    file_upload_edit = st.file_uploader(
                        "Selecione uma nova foto:",
                        type=['png', 'jpg', 'jpeg'],
                        key="upload_galeria_edit"
                    )
                    if file_upload_edit is not None:
                        st.session_state[edit_foto_key] = file_upload_edit
                
                with tab2_edit:
                    camera_input_edit = st.camera_input("Tire uma nova foto:", key="camera_edit")
                    if camera_input_edit is not None:
                        st.session_state[edit_foto_key] = camera_input_edit
                
                # Usar foto do session_state
                if st.session_state[edit_foto_key] is not None:
                    uploaded_file_edit = st.session_state[edit_foto_key]
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    salvar_edit = st.form_submit_button("💾 Salvar Alterações", type="primary")
                with col_btn2:
                    cancelar_edit = st.form_submit_button("❌ Cancelar")
                
                if salvar_edit:
                    # Verificar foto no session_state se não estiver no uploaded_file_edit
                    if uploaded_file_edit is None and st.session_state.get(edit_foto_key) is not None:
                        uploaded_file_edit = st.session_state[edit_foto_key]
                    
                    if not pavimento_edit or not pavimento_edit.strip():
                        st.error("⚠️ Por favor, preencha o campo Pavimento!")
                    else:
                        # Atualizar item
                        for i, item in enumerate(st.session_state.data):
                            if item['id'] == st.session_state.edit_id:
                                st.session_state.data[i]['pavimento'] = pavimento_edit
                                st.session_state.data[i]['empresa'] = empresa_edit
                                st.session_state.data[i]['atividade'] = atividade_edit
                                st.session_state.data[i]['local'] = local_edit
                                st.session_state.data[i]['observacoes'] = observacoes_edit
                                st.session_state.data[i]['status'] = status_edit
                                
                                # Atualizar foto se fornecida
                                if uploaded_file_edit:
                                    # Deletar foto antiga
                                    if os.path.exists(item['imagem_path']):
                                        try:
                                            os.remove(item['imagem_path'])
                                        except:
                                            pass
                                    
                                    # Salvar nova foto
                                    nova_imagem_path = save_image(uploaded_file_edit, item['id'])
                                    st.session_state.data[i]['imagem_path'] = nova_imagem_path
                                
                                break
                        
                        save_data(st.session_state.data)
                        st.success("✅ Item atualizado com sucesso!")
                        
                        # Limpar estado de edição e foto
                        if 'edit_id' in st.session_state:
                            del st.session_state.edit_id
                        if 'edit_item' in st.session_state:
                            del st.session_state.edit_item
                        if edit_foto_key in st.session_state:
                            del st.session_state[edit_foto_key]
                        
                        st.rerun()
                
                if cancelar_edit:
                    if 'edit_id' in st.session_state:
                        del st.session_state.edit_id
                    if 'edit_item' in st.session_state:
                        del st.session_state.edit_item
                    st.rerun()

# Página: Filtrar e Relatório
elif page == "🔍 Filtrar e Relatório":
    st.title("🔍 Filtrar e Gerar Relatório")
    
    data = st.session_state.data
    
    if not data:
        st.info("📭 Nenhum item cadastrado ainda. Adicione um novo item!")
    else:
        # Filtros
        st.subheader("🔍 Filtros")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Filtro por Empresa
            empresas = sorted(set([item['empresa'] for item in data if item['empresa']]))
            empresa_filtro = st.selectbox(
                "Filtrar por Empresa:",
                ["Todos"] + empresas,
                key="filtro_empresa"
            )
        
        with col2:
            # Filtro por Pavimento
            pavimentos = sorted(set([item['pavimento'] for item in data if item['pavimento']]))
            pavimento_filtro = st.selectbox(
                "Filtrar por Pavimento:",
                ["Todos"] + pavimentos,
                key="filtro_pavimento"
            )
        
        with col3:
            # Filtro por Status
            status_filtro = st.selectbox(
                "Filtrar por Status:",
                ["Todos", "Concluído", "Não Concluído", "Em Andamento"],
                key="filtro_status"
            )
        
        # Aplicar filtros
        data_filtrada = data.copy()
        
        if empresa_filtro != "Todos":
            data_filtrada = [item for item in data_filtrada if item['empresa'] == empresa_filtro]
        
        if pavimento_filtro != "Todos":
            data_filtrada = [item for item in data_filtrada if item['pavimento'] == pavimento_filtro]
        
        if status_filtro != "Todos":
            data_filtrada = [item for item in data_filtrada if item['status'] == status_filtro]
        
        # Ordenar por Pavimento
        data_filtrada = sorted(data_filtrada, key=lambda x: (
            [int(c) if c.isdigit() else c.lower() for c in x['pavimento']]
        ))
        
        st.markdown("---")
        st.subheader(f"📊 Resultados ({len(data_filtrada)} itens)")
        
        if data_filtrada:
            # Mostrar itens filtrados
            for item in data_filtrada:
                with st.expander(f"🏢 {item['pavimento']} - {item['status']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Empresa:** {item['empresa']}")
                        st.write(f"**Atividade:** {item['atividade']}")
                        st.write(f"**Local:** {item['local']}")
                        st.write(f"**Observações:** {item['observacoes']}")
                        st.write(f"**Data de Criação:** {item['data_criacao']}")
                        st.write(f"**Status:** {item['status']}")
                    
                    with col2:
                        if item.get('imagem_path') and os.path.exists(item['imagem_path']):
                            try:
                                img = Image.open(item['imagem_path'])
                                st.image(img, caption="Foto", width=200)
                            except:
                                st.error("Erro ao carregar imagem")
                        else:
                            st.warning("Imagem não encontrada")
            
            st.markdown("---")
            st.subheader("📄 Gerar Relatório PDF")
            
            # Botão para gerar PDF
            if st.button("📥 Gerar PDF com Itens Filtrados", type="primary"):
                try:
                    pdf_filename = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    pdf_path = os.path.join(DATA_DIR, pdf_filename)
                    
                    generate_pdf(data_filtrada, pdf_path)
                    
                    # Ler o arquivo PDF e disponibilizar para download
                    with open(pdf_path, 'rb') as pdf_file:
                        pdf_bytes = pdf_file.read()
                    
                    st.success("✅ PDF gerado com sucesso!")
                    st.download_button(
                        label="⬇️ Baixar PDF",
                        data=pdf_bytes,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"❌ Erro ao gerar PDF: {str(e)}")
        else:
            st.warning("⚠️ Nenhum item encontrado com os filtros selecionados.")


