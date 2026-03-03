# Interface.py
# -------------------------------------------
# Projeto de Verão Eaton
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
    page_icon="🧩",
    layout="wide",
)

# =========================
# Estilos
# =========================
# 1) Remove a caixa .card
st.markdown(
    """
    <style>
      .card { display:none!important; padding:0!important; border:none!important; background:transparent!important; box-shadow:none!important; margin:0!important; }
      .muted { color:#6b7280; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2) >>> Azul clarinho na SIDEBAR e nos "pills" do menu <<<
st.markdown(
    """
    <style>
      /* ===== Sidebar: fundo azul clarinho ===== */
      [data-testid="stSidebar"] {
        background: #EAF2FE !important;            /* azul bem clarinho */
        border-right: 1px solid #DFE7FB !important;
      }

      /* Texto na sidebar (melhor contraste) */
      [data-testid="stSidebar"] * {
        color: #123B7A !important;                 /* azul escuro */
      }

      /* ===== Links do menu de páginas (pills) ===== */
      /* Padrão */
      [data-testid="stSidebar"] nav ul li a {
        background: #E3EFFF !important;
        border-radius: 10px !important;
        padding: 6px 10px !important;
        color: #123B7A !important;
      }
      /* Hover */
      [data-testid="stSidebar"] nav ul li a:hover {
        background: #D6E8FF !important;
        text-decoration: none !important;
      }
      /* Ativo (página atual) */
      [data-testid="stSidebar"] nav ul li a[aria-current="page"] {
        background: #CFE3FF !important;
        color: #0F3D91 !important;
        font-weight: 600 !important;
      }

      /* Linha separadora mais suave */
      [data-testid="stSidebar"] hr {
        border-color: #D1DCF5 !important;
      }

      /* ===== Botões na sidebar (se usados) ===== */
      [data-testid="stSidebar"] .stButton > button {
        background: #D6E8FF !important;
        color: #0F3D91 !important;
        border: 1px solid #B7D0FF !important;
        border-radius: 10px !important;
      }
      [data-testid="stSidebar"] .stButton > button:hover {
        background: #C6DDFF !important;
        border-color: #9CC0FF !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# LOGO da Eaton
# =========================
LOGO_PATH = Path("imagens/Eaton.png")
LOGO_WIDTH = 180

col_logo, col_title = st.columns([1, 6], vertical_alignment="center")
with col_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=LOGO_WIDTH)
    else:
        st.write("📁")

with col_title:
    st.title("Sistema de Cotação - Engenharia")
    st.caption("Preencha os campos com atenção. Os campos marcados com * são obrigatórios.")

# =========================
# EXCEL (configurações)
# =========================
EXCEL_PATH = Path("entradas_eaton.xlsx")
EXCEL_SHEET = "Entradas"

# =========================
# Funções auxiliares
# =========================
def validar_ce(ce: str) -> bool:
    """Valida o padrão CE-###### (ex.: CE-123456)."""
    return bool(re.fullmatch(r"CE-\d{6}", ce.strip()))

def montar_registro_excel(
    ce: str,
    numero_peca: str,
    material: str,
    planta: str,
    tipo_classificacao: str,
    subtipo_classificacao: str,
    diametro_interno: float,
    diametro_externo: float,
    numero_dentes: int,
    modulo: float,
    observacoes: str,
) -> dict:
    """Monta um dicionário (linha) para ser gravado no Excel."""
    return {
        "CE": ce.strip(),
        "Peça (nº dentro da CE)": (numero_peca or "").strip(),
        "Material": (material or "").strip(),
        "Planta": planta,
        "Tipo (classificação)": tipo_classificacao,
        "Subtipo (classificação)": subtipo_classificacao,
        "Ø interno (mm)": float(diametro_interno) if diametro_interno is not None else None,
        "Ø externo (mm)": float(diametro_externo) if diametro_externo is not None else None,
        "Nº dentes": int(numero_dentes) if numero_dentes is not None else None,
        "Módulo (mm)": float(modulo) if modulo is not None else None,
        "Observações": (observacoes or "").strip(),
    }

def anexar_e_salvar_excel(nova_linha_df: pd.DataFrame, caminho: Path, aba: str) -> pd.DataFrame:
    """Lê o Excel existente (se houver), anexa a nova linha e salva. Retorna o DataFrame combinado."""
    if caminho.exists():
        try:
            existente_df = pd.read_excel(caminho, sheet_name=aba, engine="openpyxl")
            combinado_df = pd.concat([existente_df, nova_linha_df], ignore_index=True)
        except Exception:
            combinado_df = nova_linha_df.copy()
    else:
        combinado_df = nova_linha_df.copy()

    with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
        combinado_df.to_excel(writer, sheet_name=aba, index=False)
    return combinado_df

# =========================
# Mapeamento de Subtipos por Tipo
# =========================
TIPO_SUBTIPOS = {
    "Engrenagens": ["Helicoidais", "Retas", "Planetárias", "Anelar (interno)", "Big Gear"],
    "Eixos": ["Eixo primário", "Eixo secundário", "Eixo intermediário", "Eixo cremalheira", "Ponteira"],
    "Cônicas": ["Revacycle", "Coniflex", "Hipóides"],
    "Sincronizadores": ["Cubo", "Capa", "Cone", "Anéis"],
}

def _reset_subtipo():
    st.session_state["subtipo"] = "-- selecione --"

# =========================
# Formulário principal
# =========================
with st.form("form_etapa_1"):

    # -------- Linha 1: CE, nº peça, material --------
    col_ce, col_numero_peca, col_material = st.columns([1.1, 1, 1])

    with col_ce:
        ce_input = st.text_input(
            "CE (Cost Estimate) *",
            placeholder="CE-123456",
            help="Formato obrigatório: CE-###### (ex.: CE-123456).",
        )

    with col_numero_peca:
        numero_peca_input = st.text_input(
            "Peça (nº dentro da CE)",
            placeholder="ex.: 01",
            help="Identificador da peça dentro da mesma CE (ex.: 01, 02, A, B…).",
        )

    with col_material:
        material_input = st.text_input(
            "Material",
            placeholder="ex.: 16MnCr5",
            help="Use o vocabulário padrão; se necessário, digite 'Outro'.",
        )

    # -------- Linha 2: Planta --------
    col_planta, _sp1, _sp2 = st.columns([1, 1, 1])
    with col_planta:
        opcoes_planta = ["Valinhos (2110)", "Caxias do Sul (2152)", "Mogi Mirim (2136)", "São José dos Campos (1025)"]
        planta_input = st.selectbox("Planta *", opcoes_planta, index=0)

    # -------- Bloco técnico: dados do desenho --------
    st.subheader("Dados de entrada do desenho")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col_dint, col_dext, col_ndentes, col_modulo = st.columns(4)

    with col_dint:
        diametro_interno_input = st.number_input("Diâmetro interno (mm)", min_value=0.0, step=0.01, format="%.2f", help="Informe o diâmetro interno em milímetros.")
    with col_dext:
        diametro_externo_input = st.number_input("Diâmetro externo (mm)", min_value=0.0, step=0.01, format="%.2f", help="Informe o diâmetro externo em milímetros.")
    with col_ndentes:
        numero_dentes_input = st.number_input("Número de dentes", min_value=0, step=1, help="Quantidade total de dentes da engrenagem.")
    with col_modulo:
        modulo_input = st.number_input("Módulo (mm)", min_value=0.0, step=0.01, format="%.2f", help="Informe o módulo em milímetros (normalizado).")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------- Observações livres --------
    observacoes_input = st.text_area("Observações / Anotações", placeholder="Digite observações relevantes (ex.: revisões, exceções, referências de desenho, etc.)")

    # -------- Botão de envio --------
    submit = st.form_submit_button("Salvar / Gravar em Excel")

# ======= Classificação da Peça (abaixo dos dados, FORA DO FORM para atualizar dinamicamente) =======
st.subheader("Classificação da Peça")
st.markdown('<div class="card">', unsafe_allow_html=True)

opcoes_tipo = ["-- selecione --", "Engrenagens", "Eixos", "Cônicas", "Sincronizadores"]
tipo_input = st.selectbox("Tipo *", opcoes_tipo, index=0, key="tipo", on_change=_reset_subtipo, help="Selecione o tipo da peça.")

if st.session_state.get("tipo") in TIPO_SUBTIPOS:
    subtipo_options = ["-- selecione --"] + TIPO_SUBTIPOS[st.session_state["tipo"]]
    subtipo_disabled = False
else:
    subtipo_options = ["(não aplicável)"]
    subtipo_disabled = True

subtipo_input = st.selectbox(
    "Subtipo" + (" *" if not subtipo_disabled else ""),
    subtipo_options, index=0, key="subtipo", disabled=subtipo_disabled,
    help="Selecione o subtipo correspondente ao tipo escolhido." if not subtipo_disabled else "Não há subtipos para o tipo selecionado.",
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Validação e saída
# =========================
if submit:
    mensagens_erro = []

    if not ce_input or not validar_ce(ce_input):
        mensagens_erro.append("❌ **CE** deve estar no formato **CE-######** (ex.: CE-123456).")
    if not planta_input:
        mensagens_erro.append("❌ **Planta** é obrigatória.")

    tipo_val = st.session_state.get("tipo", "-- selecione --")
    subtipo_val = st.session_state.get("subtipo", "-- selecione --")

    if not tipo_val or tipo_val == "-- selecione --":
        mensagens_erro.append("❌ **Tipo (classificação)** é obrigatório. Selecione uma opção válida.")
    if tipo_val in TIPO_SUBTIPOS:
        if not subtipo_val or subtipo_val == "-- selecione --":
            mensagens_erro.append("❌ **Subtipo** é obrigatório para o tipo selecionado.")
        elif subtipo_val not in TIPO_SUBTIPOS[tipo_val]:
            mensagens_erro.append("❌ **Subtipo** inválido para o tipo selecionado.")

    if (diametro_interno_input is not None) and (diametro_externo_input is not None):
        if diametro_interno_input > 0 and diametro_externo_input > 0 and (diametro_externo_input < diametro_interno_input):
            mensagens_erro.append("❌ **Ø externo** não pode ser menor que o **Ø interno**.")

    if mensagens_erro:
        for msg in mensagens_erro:
            st.error(msg)
    else:
        subtipo_para_salvar = "" if tipo_val not in TIPO_SUBTIPOS else subtipo_val

        registro = montar_registro_excel(
            ce=ce_input, numero_peca=numero_peca_input, material=material_input, planta=planta_input,
            tipo_classificacao=tipo_val, subtipo_classificacao=subtipo_para_salvar,
            diametro_interno=diametro_interno_input, diametro_externo=diametro_externo_input,
            numero_dentes=numero_dentes_input, modulo=modulo_input, observacoes=observacoes_input,
        )
        nova_linha_df = pd.DataFrame([registro])
        combinado_df = anexar_e_salvar_excel(nova_linha_df, EXCEL_PATH, EXCEL_SHEET)

        st.success(f"✔ Dados salvos em **{EXCEL_PATH.name}** (aba **{EXCEL_SHEET}**).")

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            combinado_df.to_excel(writer, sheet_name=EXCEL_SHEET, index=False)
        buffer.seek(0)

        st.download_button(
            label="⬇️ Baixar Excel",
            data=buffer,
            file_name=EXCEL_PATH.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# =========================
# NAV FIXA (se você estiver usando) permanece igual
# =========================
PAGINA_ANTERIOR = "Interface.py"
PROXIMA_PAGINA  = "pages/1_resumo.py"

nav_container = st.container()
c_prev, c_next = nav_container.columns([1, 1])
with c_prev:
    prev_clicked = st.button("⬅ Página anterior", use_container_width=True, key="btn_prev_root")
with c_next:
    next_clicked = st.button("Próxima página ➡", type="primary", use_container_width=True, key="btn_next_root")

try:
    if prev_clicked:
        st.switch_page(PAGINA_ANTERIOR)
    if next_clicked:
        st.switch_page(PROXIMA_PAGINA)
except Exception:
    with nav_container:
        st.info("Use os links abaixo (fallback de navegação):")
        lc1, lc2 = st.columns(2)
        with lc1:
            st.page_link(PAGINA_ANTERIOR, label="⬅ Página anterior")
        with lc2:
            st.page_link(PROXIMA_PAGINA, label="Próxima página ➡")

with st.sidebar:
    st.page_link(PAGINA_ANTERIOR, label="⬅ Página anterior")
    st.page_link(PROXIMA_PAGINA, label="Próxima página ➡")

st.markdown(
    """
    <style>
      section.main > div.block-container > div:last-child {
        position: fixed !important;
        right: 16px; bottom: 16px; z-index: 1000; width: 320px;
        background: rgba(255,255,255,0.92); backdrop-filter: blur(6px);
        padding: 8px; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.15);
      }
      section.main > div.block-container > div:last-child [data-testid="column"] { padding: 0 4px !important; }
      section.main > div.block-container > div:last-child .stButton > button { min-height: 40px; width: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Rodapé
# =========================
st.markdown(
    "<p class='muted'>Os dados preenchidos são salvos em Excel e podem ser exportados a qualquer momento.</p>",
    unsafe_allow_html=True,
)