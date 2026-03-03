# Interface.py
# -------------------------------------------
# Projeto de Cotação de Peças EATON
# -------------------------------------------

import re
from pathlib import Path
from io import BytesIO

import pandas as pd
import streamlit as st

# =========================
# Configuração da página
# =========================
st.set_page_config(
    page_title="Cotação de Peças EATON",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# ESTILO PROFISSIONAL EATON (AZUL)
# =========================
st.markdown(
    """
    <style>
        :root {
            --eaton-blue: #005EB8;
            --eaton-blue-dark: #00468A;
            --eaton-gray-dark: #333333;
            --white: #FFFFFF;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #003366 0%, #00468A 100%) !important;
        }

        [data-testid="stSidebar"] * { color: #FFFFFF !important; }

        [data-testid="stSidebar"] nav ul li a {
            background: transparent !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            color: #CCCCCC !important;
            margin: 4px 8px !important;
            border-left: 3px solid transparent !important;
        }

        [data-testid="stSidebar"] nav ul li a:hover,
        [data-testid="stSidebar"] nav ul li a[aria-current="page"] {
            background: rgba(0, 94, 184, 0.3) !important;
            color: #FFFFFF !important;
            border-left: 3px solid #005EB8 !important;
        }

        .main-header {
            background: linear-gradient(135deg, #003366 0%, #00468A 100%);
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border-left: 5px solid #005EB8;
        }

        .main-header h1 { color: #FFFFFF !important; font-size: 1.8rem !important; margin-bottom: 0.3rem !important; }
        .main-header p { color: #CCCCCC !important; font-size: 0.95rem !important; margin: 0 !important; }

        .eaton-card {
            background: #FFFFFF !important;
            border: 1px solid #D0E1F5 !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 2px 8px rgba(0,94,184,0.08) !important;
        }

        .eaton-subheader {
            color: #003366 !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.8rem !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 2px solid #005EB8 !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #005EB8 0%, #00468A 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
        }

        .nav-fixed {
            position: fixed !important;
            right: 24px !important;
            bottom: 24px !important;
            z-index: 1000 !important;
            background: #FFFFFF !important;
            padding: 12px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0,94,184,0.2) !important;
            display: flex !important;
            gap: 12px !important;
        }

        .eaton-footer {
            text-align: center !important;
            padding: 1.5rem !important;
            color: #666666 !important;
            border-top: 3px solid #005EB8 !important;
            margin-top: 2rem !important;
            background: #FAFAFA !important;
        }

        /* Remove espaços extras */
        .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
        .stForm { margin: 0 !important; }
        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stEmpty"]) { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# LOGO da Eaton
# =========================
LOGO_PATH = Path("imagens/Eaton.png")

st.markdown('<div class="main-header">', unsafe_allow_html=True)
col_logo, col_title = st.columns([0.3, 0.7], vertical_alignment="center")

with col_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=150)
    else:
        st.write("**EATON**")

with col_title:
    st.markdown("<h1>Sistema de Cotação - Engenharia</h1>", unsafe_allow_html=True)
    st.write("Preencha os campos com atenção. Campos com * são obrigatórios.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# EXCEL
# =========================
EXCEL_PATH = Path("entradas_eaton.xlsx")
EXCEL_SHEET = "Entradas"

# =========================
# Funções
# =========================
def validar_ce(ce: str) -> bool:
    return bool(re.fullmatch(r"CE-\d{6}", ce.strip()))

def montar_registro_excel(ce, numero_peca, material, planta, tipo_classificacao, 
                          subtipo_classificacao, diametro_interno, diametro_externo,
                          numero_dentes, modulo, observacoes):
    return {
        "CE": ce.strip(),
        "Peça (nº dentro da CE)": (numero_peca or "").strip(),
        "Material": (material or "").strip(),
        "Planta": planta,
        "Tipo (classificação)": tipo_classificacao,
        "Subtipo (classificação)": subtipo_classificacao,
        "Ø interno (mm)": float(diametro_interno) if diametro_interno else None,
        "Ø externo (mm)": float(diametro_externo) if diametro_externo else None,
        "Nº dentes": int(numero_dentes) if numero_dentes else None,
        "Módulo (mm)": float(modulo) if modulo else None,
        "Observações": (observacoes or "").strip(),
    }

def anexar_e_salvar_excel(nova_linha_df, caminho, aba):
    if caminho.exists():
        try:
            existente_df = pd.read_excel(caminho, sheet_name=aba, engine="openpyxl")
            combinado_df = pd.concat([existente_df, nova_linha_df], ignore_index=True)
        except:
            combinado_df = nova_linha_df.copy()
    else:
        combinado_df = nova_linha_df.copy()
    
    with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
        combinado_df.to_excel(writer, sheet_name=aba, index=False)
    return combinado_df

# =========================
# ✅ MAPEAMENTO DOS SUBTIPOS
# =========================
MAPA_SUBTIPOS = {
    "Engrenagens": ["Helicoidais", "Retas", "Planetárias", "Anelar (interno)", "Big Gear"],
    "Eixos": ["Eixo primário", "Eixo secundário", "Eixo intermediário", "Eixo cremalheira", "Ponteira"],
    "Cônicas": ["Revacycle", "Coniflex", "Hipóides"],
    "Sincronizadores": ["Cubo", "Capa", "Cone", "Anéis"],
}

# =========================
# FORMULÁRIO PRINCIPAL
# =========================
with st.form("form_principal"):
    st.markdown('<div class="eaton-card">', unsafe_allow_html=True)
    
    # ✅ TÍTULO DO PRIMEIRO TÓPICO (ADICIONADO)
    st.markdown('<h3 class="eaton-subheader">📋 Informações da Peça</h3>', unsafe_allow_html=True)
    
    # ===== Linha 1: CE, Peça, Material =====
    col1, col2, col3 = st.columns(3)
    with col1:
        ce = st.text_input("CE (Cost Estimate) *", placeholder="CE-123456")
    with col2:
        num_peca = st.text_input("Peça (nº dentro da CE)", placeholder="ex.: 01")
    with col3:
        material = st.text_input("Material", placeholder="ex.: 16MnCr5")
    
    # ===== Linha 2: Planta =====
    col4, _, _ = st.columns(3)
    with col4:
        planta = st.selectbox(
            "Planta *",
            ["Valinhos (2110)", "Caxias do Sul (2152)", "Mogi Mirim (2136)", "São José dos Campos (1025)"]
        )
    
    # ===== DADOS DO DESENHO =====
    st.markdown('<h3 class="eaton-subheader" style="margin-top:1rem">📐 Dados de Entrada do Desenho</h3>', unsafe_allow_html=True)
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    with col_d1:
        d_interno = st.number_input("Diâmetro interno (mm)", min_value=0.0, step=0.01)
    with col_d2:
        d_externo = st.number_input("Diâmetro externo (mm)", min_value=0.0, step=0.01)
    with col_d3:
        n_dentes = st.number_input("Número de dentes", min_value=0, step=1)
    with col_d4:
        modulo = st.number_input("Módulo (mm)", min_value=0.0, step=0.01)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    botao_salvar = st.form_submit_button("💾 Salvar Dados", use_container_width=True)

# =========================
# ✅ CLASSIFICAÇÃO DA PEÇA (FORA DO FORM)
# =========================
st.markdown('<div class="eaton-card">', unsafe_allow_html=True)
st.markdown('<h3 class="eaton-subheader">🏷️ Classificação da Peça</h3>', unsafe_allow_html=True)

col_tipo, col_subtipo = st.columns(2)

with col_tipo:
    tipo_escolhido = st.selectbox(
        "Tipo *",
        options=["-- selecione --", "Engrenagens", "Eixos", "Cônicas", "Sincronizadores"],
        index=0,
        key="chave_tipo"
    )

with col_subtipo:
    if tipo_escolhido in MAPA_SUBTIPOS:
        lista_subtipos = MAPA_SUBTIPOS[tipo_escolhido]
        subtipo_escolhido = st.selectbox(
            "Subtipo *",
            options=lista_subtipos,
            index=0,
            key="chave_subtipo"
        )
    else:
        st.selectbox(
            "Subtipo",
            options=["(não aplicável)"],
            index=0,
            disabled=True,
            key="chave_subtipo"
        )

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# OBSERVAÇÕES (FORA DO FORM)
# =========================
st.markdown('<div class="eaton-card">', unsafe_allow_html=True)
st.markdown('<h3 class="eaton-subheader">📝 Observações</h3>', unsafe_allow_html=True)
obs = st.text_area("", placeholder="Digite observações relevantes (ex.: revisões, exceções, referências de desenho)", height=80, key="obs_form", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# VALIDAÇÃO E SALVAMENTO
# =========================
if botao_salvar:
    erros = []
    
    if not ce or not validar_ce(ce):
        erros.append("❌ **CE** deve estar no formato **CE-######**")
    
    if tipo_escolhido == "-- selecione --":
        erros.append("❌ **Tipo** é obrigatório")
    
    if tipo_escolhido in MAPA_SUBTIPOS and st.session_state.chave_subtipo == "(não aplicável)":
        erros.append("❌ **Subtipo** é obrigatório")
    
    if d_externo > 0 and d_interno > 0 and d_externo < d_interno:
        erros.append("❌ Ø externo não pode ser menor que Ø interno")
    
    if erros:
        for e in erros:
            st.error(e)
    else:
        registro = montar_registro_excel(
            ce=ce, numero_peca=num_peca, material=material, planta=planta,
            tipo_classificacao=tipo_escolhido,
            subtipo_classificacao=st.session_state.chave_subtipo if tipo_escolhido in MAPA_SUBTIPOS else "",
            diametro_interno=d_interno, diametro_externo=d_externo,
            numero_dentes=n_dentes, modulo=modulo, observacoes=st.session_state.get("obs_form", "")
        )
        
        df = pd.DataFrame([registro])
        anexar_e_salvar_excel(df, EXCEL_PATH, EXCEL_SHEET)
        
        st.success("✔ Dados salvos com sucesso!")
        
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as w:
            df.to_excel(w, sheet_name=EXCEL_SHEET, index=False)
        buffer.seek(0)
        
        st.download_button("⬇️ Baixar Excel", buffer, "entradas_eaton.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# =========================
# NAVEGAÇÃO
# =========================
st.markdown('<div class="nav-fixed">', unsafe_allow_html=True)
c1, c2 = st.columns([1, 1])
with c1:
    st.page_link("Interface.py", label="⬅ Início", use_container_width=True)
with c2:
    st.page_link("pages/1_resumo.py", label="Próxima Etapa ➡", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="eaton-footer">
        <p><strong>EATON</strong> | Powering Business Worldwide</p>
        <p>© 2024 Eaton Corporation. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True,
)