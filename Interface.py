# Interface.py
import re
from pathlib import Path
from io import BytesIO
import pandas as pd
import streamlit as st
from utils import salvar_dados, carregar_dados

st.set_page_config(page_title="Cotação de Peças EATON", page_icon="🔷", layout="wide")

st.markdown(
    """
    <style>
        :root { --eaton-blue: #005EB8; --eaton-blue-dark: #00468A; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #003366 0%, #00468A 100%) !important; }
        [data-testid="stSidebar"] * { color: #FFFFFF !important; }
        .main-header { background: linear-gradient(135deg, #003366 0%, #00468A 100%); padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 5px solid #005EB8; }
        .main-header h1 { color: #FFFFFF !important; font-size: 1.8rem !important; margin-bottom: 0.3rem !important; }
        .main-header p { color: #CCCCCC !important; font-size: 0.95rem !important; margin: 0 !important; }
        .eaton-card { background: #FFFFFF !important; border: 1px solid #D0E1F5 !important; border-radius: 12px !important; padding: 1.5rem !important; margin-bottom: 1rem !important; box-shadow: 0 2px 8px rgba(0,94,184,0.08) !important; }
        .eaton-subheader { color: #003366 !important; font-size: 1.2rem !important; font-weight: 600 !important; margin-bottom: 0.8rem !important; padding-bottom: 0.5rem !important; border-bottom: 2px solid #005EB8 !important; }
        .stButton > button { background: linear-gradient(135deg, #005EB8 0%, #00468A 100%) !important; color: #FFFFFF !important; border: none !important; border-radius: 8px !important; padding: 12px 24px !important; font-weight: 600 !important; }
        .nav-fixed { position: fixed !important; right: 24px !important; bottom: 24px !important; z-index: 1000 !important; background: #FFFFFF !important; padding: 12px !important; border-radius: 12px !important; box-shadow: 0 4px 20px rgba(0,94,184,0.2) !important; display: flex !important; gap: 12px !important; }
        .eaton-footer { text-align: center !important; padding: 1.5rem !important; color: #666666 !important; border-top: 3px solid #005EB8 !important; margin-top: 2rem !important; background: #FAFAFA !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    st.write("Preencha os campos com atenção. Campos opcionais podem ser deixados em branco.")
st.markdown('</div>', unsafe_allow_html=True)

EXCEL_PATH = Path("entradas_eaton.xlsx")
EXCEL_SHEET = "Entradas"

MAPA_SUBTIPOS = {
    "Engrenagens": ["Helicoidais", "Retas", "Planetárias", "Anelar (interno)", "Big Gear"],
    "Eixos": ["Eixo primário", "Eixo secundário", "Eixo intermediário", "Eixo cremalheira", "Ponteira"],
    "Cônicas": ["Revacycle", "Coniflex", "Hipóides"],
    "Sincronizadores": ["Cubo", "Capa", "Cone", "Anéis"],
}

# Inicializa session_state se não existir
if "dados_peca" not in st.session_state:
    st.session_state["dados_peca"] = {}

# ============================================
# FORMULÁRIO 1: Informações da Peça + Dados de Entrada
# ============================================
with st.form("form_principal"):
    st.markdown('<div class="eaton-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="eaton-subheader">📋 Informações da Peça</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        ce = st.text_input("CE (Cost Estimate)", placeholder="Ex.: CE-123456")
    with col2:
        num_peca = st.text_input("Peça (nº dentro da CE)", placeholder="ex.: 01")
    with col3:
        material = st.text_input("Material", placeholder="ex.: 16MnCr5")
    
    col4, _, _ = st.columns(3)
    with col4:
        planta = st.selectbox("Planta", ["Valinhos (2110)", "Caxias do Sul (2152)", "Mogi Mirim (2136)", "São José dos Campos (1025)"])
    
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
    botao_salvar_info = st.form_submit_button("💾 Salvar Informações da Peça", use_container_width=True)

# ============================================
# FORMULÁRIO 2: Classificação + Observações
# ============================================
with st.form("form_classificacao"):
    st.markdown('<div class="eaton-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="eaton-subheader">🏷️ Classificação da Peça</h3>', unsafe_allow_html=True)
    col_tipo, col_subtipo = st.columns(2)
    with col_tipo:
        tipo_escolhido = st.selectbox("Tipo", options=["-- selecione --", "Engrenagens", "Eixos", "Cônicas", "Sincronizadores"], index=0, key="chave_tipo_form2")
    with col_subtipo:
        if tipo_escolhido in MAPA_SUBTIPOS:
            subtipo_escolhido = st.selectbox("Subtipo", options=MAPA_SUBTIPOS[tipo_escolhido], index=0, key="chave_subtipo_form2")
        else:
            subtipo_escolhido = st.selectbox("Subtipo", options=["(não aplicável)"], index=0, disabled=True, key="chave_subtipo_form2")
    
    st.markdown('<h3 class="eaton-subheader" style="margin-top:1rem">📝 Observações</h3>', unsafe_allow_html=True)
    obs = st.text_area("", placeholder="Digite observações relevantes", height=80, key="obs_form2", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    botao_salvar_class = st.form_submit_button("💾 Salvar Classificação e Observações", use_container_width=True)

# ============================================
# LÓGICA DE SALVAMENTO
# ============================================

# Salvar Informações da Peça
if botao_salvar_info:
    erros = []
    if d_externo > 0 and d_interno > 0 and d_externo < d_interno:
        erros.append("❌ Ø externo não pode ser menor que Ø interno")
    
    if erros:
        for e in erros:
            st.error(e)
    else:
        st.session_state["dados_peca"].update({
            "CE": (ce or "").strip(),
            "Peça (nº dentro da CE)": (num_peca or "").strip(),
            "Material": (material or "").strip(),
            "Planta": planta,
            "Ø interno (mm)": float(d_interno) if d_interno else None,
            "Ø externo (mm)": float(d_externo) if d_externo else None,
            "Nº dentes": int(n_dentes) if n_dentes else None,
            "Módulo (mm)": float(modulo) if modulo else None,
        })
        
        salvar_dados({"dados_peca": st.session_state["dados_peca"]})
        st.success("✔ Informações da peça salvas com sucesso!")

# Salvar Classificação e Observações
if botao_salvar_class:
    st.session_state["dados_peca"].update({
        "Tipo (classificação)": tipo_escolhido if tipo_escolhido != "-- selecione --" else "",
        "Subtipo (classificação)": subtipo_escolhido if tipo_escolhido in MAPA_SUBTIPOS and subtipo_escolhido != "(não aplicável)" else "",
        "Observações": (obs or "").strip(),
    })
    
    salvar_dados({"dados_peca": st.session_state["dados_peca"]})
    st.success("✔ Classificação e observações salvas com sucesso!")

# ============================================
# RESUMO DOS DADOS SALVOS
# ============================================
if st.session_state.get("dados_peca"):
    st.markdown('<div class="eaton-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="eaton-subheader">✅ Dados Confirmados</h3>', unsafe_allow_html=True)
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.write(f"**CE:** {st.session_state['dados_peca'].get('CE', 'Não informado')}")
        st.write(f"**Peça:** {st.session_state['dados_peca'].get('Peça (nº dentro da CE)', 'Não informado')}")
        st.write(f"**Material:** {st.session_state['dados_peca'].get('Material', 'Não informado')}")
        st.write(f"**Planta:** {st.session_state['dados_peca'].get('Planta', 'Não informado')}")
    with col_res2:
        st.write(f"**Tipo:** {st.session_state['dados_peca'].get('Tipo (classificação)', 'Não informado')}")
        st.write(f"**Subtipo:** {st.session_state['dados_peca'].get('Subtipo (classificação)', 'Não informado')}")
        obs_preview = st.session_state['dados_peca'].get('Observações', '')
        st.write(f"**Obs:** {obs_preview[:50] + '...' if len(obs_preview) > 50 else obs_preview or 'Não informado'}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# NAVEGAÇÃO
# ============================================
st.markdown('<div class="nav-fixed">', unsafe_allow_html=True)
c1, c2 = st.columns([1, 1])
with c1:
    st.page_link("Interface.py", label="⬅ Início", use_container_width=True)
with c2:
    st.page_link("pages/1_resumo.py", label="Próxima Etapa ➡", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="eaton-footer"><p><strong>EATON</strong> | Powering Business Worldwide</p><p>© 2026 Eaton Corporation. All rights reserved.</p></div>', unsafe_allow_html=True)
