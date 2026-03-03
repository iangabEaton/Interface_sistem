# pages/1_resumo.py
import re
import streamlit as st

st.set_page_config(page_title="Resumo", page_icon="🧾", layout="wide")

# ===== CSS azul clarinho na sidebar =====
st.markdown(
    """
    <style>
      [data-testid="stSidebar"] { background: #EAF2FE !important; border-right: 1px solid #DFE7FB !important; }
      [data-testid="stSidebar"] * { color: #123B7A !important; }
      [data-testid="stSidebar"] nav ul li a { background: #E3EFFF !important; border-radius: 10px !important; padding: 6px 10px !important; color: #123B7A !important; }
      [data-testid="stSidebar"] nav ul li a:hover { background: #D6E8FF !important; text-decoration: none !important; }
      [data-testid="stSidebar"] nav ul li a[aria-current="page"] { background: #CFE3FF !important; color: #0F3D91 !important; font-weight: 600 !important; }
      [data-testid="stSidebar"] hr { border-color: #D1DCF5 !important; }
      [data-testid="stSidebar"] .stButton > button { background: #D6E8FF !important; color: #0F3D91 !important; border: 1px solid #B7D0FF !important; border-radius: 10px !important; }
      [data-testid="stSidebar"] .stButton > button:hover { background: #C6DDFF !important; border-color: #9CC0FF !important; }
      .pill { display:inline-block; padding:4px 10px; background:#E3EFFF; color:#123B7A; border-radius:999px; margin-right:8px; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Processos de Manufatura")
st.caption(
    "Marque os processos necessários. Ao marcar um processo, escolha um **código (código — descrição)** ao lado "
    "e, quando aplicável, selecione a **multiplicidade**. A **Próxima página** abrirá os parâmetros essenciais."
)

# ---------------------------
# Lista única de opções (código — descrição)
# ---------------------------
BASE_OPCOES = [
    ("23505", "CORTE"),
    ("23506", "FORJARIA"),
    ("23507", "FORJARIA PRENSA"),
    ("23508", "RETÍFICA DE DENTES"),
    ("23509", "ANELARES"),
    ("23510", "COROA & PINHÃO"),
    ("23516", "TRATAMENTO TÉRMICO"),
    ("23522", "FORNO CONTÍNUO"),
    ("23524", "MONTAGEM"),
    ("23526", "BAIXO VOLUME"),
    ("23527", "RETÍFICAS / NORMALIZAÇÃO FORJA"),
    ("23528", "JATOS FORJA"),
    ("23529", "INDUÇÃO T. TÉRMICO"),
    ("23530", "JATOS T. TÉRMICO"),
    ("23531", "FOSFATIZAÇÃO"),
    ("23532", "OPERAÇÃO MANUAL T. TÉRMICO"),
    ("23533", "TORNEAMENTO DE ENGRENAGENS"),
    ("23534", "BROCHAMENTO"),
    ("23535", "CORTE/ACABAMENTO DE ENGRENAGENS"),
    ("23536", "PREPARAÇÃO DE EIXOS"),
    ("23537", "TORNEAMENTO DE EIXOS"),
    ("23538", "CORTE/ACABAMENTO DE EIXOS CREMALHEIRA"),
    ("23540", "PONTEIRAS E EIXOS CREMALHEIRA"),
    ("23541", "BIG GEAR"),
    ("23542", "ENGRENAGENS CÔNICAS"),
    # genéricos úteis para prototipagem
    ("23333", "TORNEAMENTO EXTERNO"),
    ("CC 2152", "CENTRO DE CUSTO 2152"),
]
BASE_LABELS = [f"{cod} — {desc}" for cod, desc in BASE_OPCOES]
BASE_LABEL_TO_CODE = {f"{cod} — {desc}": cod for cod, desc in BASE_OPCOES}
BASE_CODE_TO_LABEL = {cod: f"{cod} — {desc}" for cod, desc in BASE_OPCOES}

# ---------------------------
# Grupos (AGORA com 10 tópicos, todos como processos)
# ---------------------------
GRUPOS = {
    "1) Obtenção do blank": [
        "Corte/Serra",
        "Forjamento",
    ],
    "2) Pré-usinagem": [
        "Facear e Centrar",
        "Vazão",
    ],
    "3) Usinagens de base": [
        "Torneamento externo",
        "Furação",
        "Fresamento de chaveta",
        "Furação profunda",
        "Fresamento",
        "Chanframento de furo",
        "Chanframento de arestas",
    ],
    "4) Engrenagens / Perfis gerados": [
        "Hobber",
        "Shaper",
        "Laminação a frio (dentes/estrias)",
        "Shaver",
        "Chanfrar dentes",
        "Ajuste/Amassamento de dentes",
        "Brochamento",
        "Rebrochamento",
        "Skiving",
        "Recalque",
        "Power honing",
    ],
    # 5 → 10 também como processos
    "5) Tratamento térmico": [
        "Forno contínuo", "Forno câmara", "Carbonitretação", "Revenimento",
        "Normalização", "Recozimento isotérmico", "Recristalização"
    ],
    "6) Pós-usinagem / Acabamentos dimensionais": [
        "Retificação externa", "Retificação interna", "Retificação plana",
        "Torneamento duro (pós-TT)", "Retificação de dentes"
    ],
    "7) Tratamentos de superfície": [
        "Shot peening", "Shot cleaning", "Fosfato", "Tinta protetiva", "Endireitamento"
    ],
    "8) Lavagem e Montagem": [
        "Lavagem industrial", "Montagem"
    ],
    "9) Inspeções e ensaios": [
        "Engrenômetro", "Teste de contato/ruído", "Inspeção dimensional", "Inspeção final"
    ],
    "10) Marcação": [
        "Gravação/Marcação"
    ],
}

# Multiplicidade x1~x4 apenas para Hobber / Shaper / Shaver
MULTI_PROCS = {"Hobber", "Shaper", "Shaver"}
MULTI_OPCOES = ["x1", "x2", "x3", "x4"]

# ---------------------------
# Estado
# ---------------------------
def slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s

def _init_state():
    if "processos_sel" not in st.session_state:
        st.session_state["processos_sel"] = {g: set() for g in GRUPOS}
    if "detalhes_proc" not in st.session_state:
        st.session_state["detalhes_proc"] = {}

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

_init_state()

# ---------------------------
# Linha de processo: checkbox | código | multiplicidade (quando aplica)
# ---------------------------
def render_linha_processo(grupo_nome: str, processo: str):
    marcado = processo in st.session_state["processos_sel"][grupo_nome]
    c_chk, c_cod, c_multi = st.columns([0.35, 0.45, 0.20])

    with c_chk:
        st.checkbox(
            processo,
            value=marcado,
            key=f"chk_{slug(grupo_nome)}_{slug(processo)}",
            on_change=lambda g=grupo_nome, p=processo: toggle_item(
                g, p, st.session_state[f'chk_{slug(g)}_{slug(p)}']
            ),
        )

    with c_cod:
        if st.session_state.get(f"chk_{slug(grupo_nome)}_{slug(processo)}", False):
            cod_prev = st.session_state["detalhes_proc"].get(processo, {}).get("codigo")
            default_label = BASE_CODE_TO_LABEL.get(cod_prev)
            escolhido_label = st.selectbox(
                f"Código ({processo})",
                options=BASE_LABELS,
                index=BASE_LABELS.index(default_label) if default_label in BASE_LABELS else 0,
                key=f"sb_{slug(processo)}",
            )
            st.session_state["detalhes_proc"].setdefault(processo, {})
            st.session_state["detalhes_proc"][processo]["codigo"] = BASE_LABEL_TO_CODE[escolhido_label]

    with c_multi:
        if st.session_state.get(f"chk_{slug(grupo_nome)}_{slug(processo)}", False) and processo in MULTI_PROCS:
            multi_prev = st.session_state["detalhes_proc"].get(processo, {}).get("multi", "x1")
            multi_sel = st.selectbox(
                "Multiplicidade",
                options=MULTI_OPCOES,
                index=MULTI_OPCOES.index(multi_prev) if multi_prev in MULTI_OPCOES else 0,
                key=f"multi_{slug(processo)}",
            )
            st.session_state["detalhes_proc"][processo]["multi"] = multi_sel

def render_grupo(container, grupo_nome: str, expanded=True):
    with container:
        with st.expander(grupo_nome, expanded=expanded):
            for proc in GRUPOS[grupo_nome]:
                render_linha_processo(grupo_nome, proc)

# ---------------------------
# Layout: 2 colunas com os 10 grupos (acima do Resumo)
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
# Resumo das Seleções (vem DEPOIS dos 10 grupos)
# ---------------------------
st.subheader("Resumo das Seleções")
tem_algo = False
for g in GRUPOS:
    itens = sorted(st.session_state["processos_sel"][g])
    if itens:
        tem_algo = True
        st.markdown(f"**{g}**: " + ", ".join(itens))
    else:
        st.markdown(f"**{g}**: _nenhum_")

for proc, det in st.session_state["detalhes_proc"].items():
    cod = det.get("codigo")
    if cod:
        extra = f" | multiplicidade: {det.get('multi')}" if proc in MULTI_PROCS and det.get("multi") else ""
        st.markdown(f"• **{proc} – código selecionado**: `{cod}`{extra}")
    else:
        # Aviso para processos marcados sem código
        for g in GRUPOS:
            if proc in st.session_state["processos_sel"].get(g, set()):
                st.warning(f"{proc} marcado, mas nenhuma opção foi escolhida.")

if not tem_algo:
    st.info("Nenhum processo marcado ainda.")

# ---------------------------
# Navegação
# ---------------------------
PAGINA_ANTERIOR = "Interface.py"
PROXIMA_PAGINA  = "pages/2_calculos.py"

nav_container = st.container()
c_prev, c_next = nav_container.columns([1, 1])

with c_prev:
    prev_clicked = st.button("⬅ Página anterior", use_container_width=True, key="btn_prev_pg1")
with c_next:
    next_clicked = st.button("Próxima página ➡", type="primary", use_container_width=True, key="btn_next_pg1")

def _build_tabela_rows_from_selection():
    """Monta tabela_rows para prefill da página 2, respeitando a ordem de inserção de detalhes_proc."""
    rows = []
    for proc, det in st.session_state.get("detalhes_proc", {}).items():
        codigo = det.get("codigo")
        if not codigo:
            continue
        row = {"Operação": proc, "Código": codigo}
        if proc in MULTI_PROCS and det.get("multi"):
            row["Multiplicidade"] = det["multi"]
        rows.append(row)
    return rows

try:
    if prev_clicked:
        st.switch_page(PAGINA_ANTERIOR)
    if next_clicked:
        st.session_state["tabela_rows"] = _build_tabela_rows_from_selection()
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
    st.page_link(PROXIMA_PAGINA, label="➜ Ir para Página 3 – Cálculos")