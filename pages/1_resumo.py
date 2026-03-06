# pages/1_resumo.py
import re
import streamlit as st

st.set_page_config(page_title="Seleção de Processos", page_icon="📋", layout="wide")

# ===== ESTILO PROFISSIONAL EATON (AZUL) =====
st.markdown(
    """
    <style>
        :root {
            --eaton-blue: #005EB8;
            --eaton-blue-dark: #00468A;
            --eaton-blue-light: #E6F0FA;
            --eaton-gray-dark: #333333;
            --eaton-gray-medium: #666666;
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
            font-weight: 500 !important;
            margin: 4px 8px !important;
            border-left: 3px solid transparent !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stSidebar"] nav ul li a:hover {
            background: rgba(0, 94, 184, 0.3) !important;
            color: #FFFFFF !important;
            border-left: 3px solid #005EB8 !important;
        }

        [data-testid="stSidebar"] nav ul li a[aria-current="page"] {
            background: rgba(0, 94, 184, 0.4) !important;
            color: #FFFFFF !important;
            border-left: 3px solid #005EB8 !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            color: #FFFFFF !important;
            border: 1px solid #1A5F9E !important;
            border-radius: 8px !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #005EB8 !important;
            border-color: #005EB8 !important;
        }

        .main-header {
            background: linear-gradient(135deg, #003366 0%, #00468A 100%);
            padding: 2rem 3rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,94,184,0.2);
            border-left: 5px solid #005EB8;
            border-top: 3px solid #005EB8;
        }

        .main-header h1 { color: #FFFFFF !important; font-size: 2rem !important; font-weight: 700 !important; }
        .main-header p { color: #CCCCCC !important; font-size: 1rem !important; }

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
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 2px solid #005EB8 !important;
        }

        .process-group {
            background: #F0F5FA !important;
            border: 1px solid #D0E1F5 !important;
            border-radius: 10px !important;
            padding: 1.5rem !important;
            margin-bottom: 1.5rem !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #005EB8 0%, #00468A 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(0,94,184,0.3) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0,94,184,0.4) !important;
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
            border: 1px solid #D0E1F5 !important;
        }

        .eaton-footer {
            text-align: center !important;
            padding: 2rem !important;
            color: #666666 !important;
            font-size: 0.85rem !important;
            border-top: 3px solid #005EB8 !important;
            margin-top: 3rem !important;
            background: #FAFAFA !important;
        }

        .streamlit-expanderHeader {
            background: #F0F5FA !important;
            border: 1px solid #D0E1F5 !important;
            border-radius: 8px !important;
        }

        .streamlit-expanderHeader:hover {
            background: #E6F0FA !important;
            border-color: #005EB8 !important;
        }

        .stCheckbox label {
            font-weight: 500 !important;
            color: #333333 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
    <div class="main-header">
        <h1>📋 Seleção de Processos de Manufatura</h1>
        <p>Marque os processos necessários para esta cotação. Selecione o código e multiplicidade quando aplicável.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Lista de opções
# ---------------------------
BASE_OPCOES = [
    ("23505", "CORTE"), ("23506", "FORJARIA"), ("23507", "FORJARIA PRENSA"),
    ("23508", "RETÍFICA DE DENTES"), ("23509", "ANELARES"), ("23510", "COROA & PINHÃO"),
    ("23516", "TRATAMENTO TÉRMICO"), ("23522", "FORNO CONTÍNUO"), ("23524", "MONTAGEM"),
    ("23526", "BAIXO VOLUME"), ("23527", "RETÍFICAS / NORMALIZAÇÃO FORJA"),
    ("23528", "JATOS FORJA"), ("23529", "INDUÇÃO T. TÉRMICO"), ("23530", "JATOS T. TÉRMICO"),
    ("23531", "FOSFATIZAÇÃO"), ("23532", "OPERAÇÃO MANUAL T. TÉRMICO"),
    ("23533", "TORNEAMENTO DE ENGRENAGENS"), ("23534", "BROCHAMENTO"),
    ("23535", "CORTE/ACABAMENTO DE ENGRENAGENS"), ("23536", "PREPARAÇÃO DE EIXOS"),
    ("23537", "TORNEAMENTO DE EIXOS"), ("23538", "CORTE/ACABAMENTO DE EIXOS CREMALHEIRA"),
    ("23540", "PONTEIRAS E EIXOS CREMALHEIRA"), ("23541", "BIG GEAR"),
    ("23542", "ENGRENAGENS CÔNICAS"), ("23333", "TORNEAMENTO EXTERNO"),
    ("CC 2152", "CENTRO DE CUSTO 2152"),
]
BASE_LABELS = [f"{cod} — {desc}" for cod, desc in BASE_OPCOES]
BASE_LABEL_TO_CODE = {f"{cod} — {desc}": cod for cod, desc in BASE_OPCOES}
BASE_CODE_TO_LABEL = {cod: f"{cod} — {desc}" for cod, desc in BASE_OPCOES}

# ---------------------------
# Grupos
# ---------------------------
GRUPOS = {
    "1) Obtenção do blank": ["Corte/Serra", "Forjamento"],
    "2) Pré-usinagem": ["Facear e Centrar", "Vazão"],
    "3) Usinagens de base": ["Torneamento externo", "Furação", "Fresamento de chaveta", "Furação profunda", "Fresamento", "Chanframento de furo", "Chanframento de arestas"],
    "4) Engrenagens / Perfis gerados": ["Hobber", "Shaper", "Laminação a frio (dentes/estrias)", "Shaver", "Chanfrar dentes", "Ajuste/Amassamento de dentes", "Brochamento", "Rebrochamento", "Skiving", "Recalque", "Power honing"],
    "5) Tratamento térmico": ["Forno contínuo", "Forno câmara", "Carbonitretação", "Revenimento", "Normalização", "Recozimento isotérmico", "Recristalização"],
    "6) Pós-usinagem / Acabamentos dimensionais": ["Retificação externa", "Retificação interna", "Retificação plana", "Torneamento duro (pós-TT)", "Retificação de dentes"],
    "7) Tratamentos de superfície": ["Shot peening", "Shot cleaning", "Fosfato", "Tinta protetiva", "Endireitamento"],
    "8) Lavagem e Montagem": ["Lavagem industrial", "Montagem"],
    "9) Inspeções e ensaios": ["Engrenômetro", "Teste de contato/ruído", "Inspeção dimensional", "Inspeção final"],
    "10) Marcação": ["Gravação/Marcação"],
}

MULTI_PROCS = {"Hobber", "Shaper", "Shaver"}
MULTI_OPCOES = ["x1", "x2", "x3", "x4"]

# ---------------------------
# ✅ INICIALIZAÇÃO CORRETA DO SESSION STATE
# ---------------------------
def slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s

def init_session_state():
    # Inicializa processos_sel COM TODAS AS CHAVES DOS GRUPOS
    if "processos_sel" not in st.session_state:
        st.session_state["processos_sel"] = {}
    
    # Garante que TODOS os grupos existam no session_state
    for grupo in GRUPOS.keys():
        if grupo not in st.session_state["processos_sel"]:
            st.session_state["processos_sel"][grupo] = set()
    
    # Inicializa detalhes_proc
    if "detalhes_proc" not in st.session_state:
        st.session_state["detalhes_proc"] = {}
    
    # Garante que dados_peca exista (vem da Interface.py)
    if "dados_peca" not in st.session_state:
        st.session_state["dados_peca"] = {}
    
    # Garante que calculos exista (para página 3)
    if "calculos" not in st.session_state:
        st.session_state["calculos"] = {}

# Chama a inicialização
init_session_state()

# ---------------------------
# Toggle Item
# ---------------------------
def toggle_item(grupo: str, item: str, marcado: bool):
    sel = st.session_state["processos_sel"][grupo]
    if marcado:
        sel.add(item)
        st.session_state["detalhes_proc"].setdefault(item, {})
    else:
        sel.discard(item)
        st.session_state["detalhes_proc"].pop(item, None)
        st.session_state.pop(f"sb_{slug(item)}", None)
        st.session_state.pop(f"multi_{slug(item)}", None)
    st.session_state["processos_sel"][grupo] = sel

# ---------------------------
# Linha de processo
# ---------------------------
def render_linha_processo(grupo_nome: str, processo: str):
    marcado = processo in st.session_state["processos_sel"][grupo_nome]
    c_chk, c_cod, c_multi = st.columns([0.35, 0.45, 0.20])

    with c_chk:
        st.checkbox(processo, value=marcado, key=f"chk_{slug(grupo_nome)}_{slug(processo)}",
            on_change=lambda g=grupo_nome, p=processo: toggle_item(g, p, st.session_state[f'chk_{slug(g)}_{slug(p)}']))

    with c_cod:
        if st.session_state.get(f"chk_{slug(grupo_nome)}_{slug(processo)}", False):
            cod_prev = st.session_state["detalhes_proc"].get(processo, {}).get("codigo")
            default_label = BASE_CODE_TO_LABEL.get(cod_prev)
            escolhido_label = st.selectbox(f"Código ({processo})", options=BASE_LABELS,
                index=BASE_LABELS.index(default_label) if default_label in BASE_LABELS else 0, key=f"sb_{slug(processo)}")
            st.session_state["detalhes_proc"].setdefault(processo, {})
            st.session_state["detalhes_proc"][processo]["codigo"] = BASE_LABEL_TO_CODE[escolhido_label]

    with c_multi:
        if st.session_state.get(f"chk_{slug(grupo_nome)}_{slug(processo)}", False) and processo in MULTI_PROCS:
            multi_prev = st.session_state["detalhes_proc"].get(processo, {}).get("multi", "x1")
            multi_sel = st.selectbox("Mult.", options=MULTI_OPCOES,
                index=MULTI_OPCOES.index(multi_prev) if multi_prev in MULTI_OPCOES else 0, key=f"multi_{slug(processo)}")
            st.session_state["detalhes_proc"][processo]["multi"] = multi_sel

def render_grupo(container, grupo_nome: str, expanded=True):
    with container:
        with st.expander(grupo_nome, expanded=expanded):
            for proc in GRUPOS[grupo_nome]:
                render_linha_processo(grupo_nome, proc)

# ---------------------------
# Layout
# ---------------------------
col_esq, col_dir = st.columns(2)
grupos = list(GRUPOS.keys())
for i, g in enumerate(grupos, start=1):
    if i % 2 == 1:
        render_grupo(col_esq, g, expanded=True)
    else:
        render_grupo(col_dir, g, expanded=True)

st.markdown("")

# ---------------------------
# Resumo das Seleções
# ---------------------------
st.markdown('<h3 class="eaton-subheader">📊 Resumo das Seleções</h3>', unsafe_allow_html=True)
tem_algo = False
for g in GRUPOS:
    itens = sorted(st.session_state["processos_sel"][g])
    if itens:
        tem_algo = True
        st.markdown(f"**{g}**: " + ", ".join(itens))

for proc, det in st.session_state["detalhes_proc"].items():
    cod = det.get("codigo")
    if cod:
        extra = f" | mult: {det.get('multi')}" if proc in MULTI_PROCS and det.get('multi') else ""
        st.markdown(f"• **{proc}** – Código: `{cod}`{extra}")

if not tem_algo:
    st.info("Nenhum processo marcado ainda.")

# ---------------------------
# Navegação
# ---------------------------
st.markdown('<div class="nav-fixed">', unsafe_allow_html=True)
col_prev, col_next = st.columns([1, 1])
with col_prev:
    st.page_link("Interface.py", label="⬅ Voltar", use_container_width=True)
with col_next:
    st.page_link("pages/2_calculos.py", label="Ir para Cálculos ➡", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown(
    """
    <div class="eaton-footer">
        <p><strong>EATON</strong> | Powering Business Worldwide</p>
        <p>© 2026 Eaton Corporation. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
