# pages/2_calculos.py
import pandas as pd
import streamlit as st
from utils import carregar_dados, salvar_dados

st.set_page_config(page_title="Cálculos de Processos", page_icon="🧮", layout="wide")

# ===== ESTILO PROFISSIONAL EATON (AZUL) =====
dados_carregados = carregar_dados()
if "dados_peca" in dados_carregados:
    st.session_state["dados_peca"] = dados_carregados["dados_peca"]
if "processos_sel" in dados_carregados:
    st.session_state["processos_sel"] = dados_carregados["processos_sel"]
if "detalhes_proc" in dados_carregados:
    st.session_state["detalhes_proc"] = dados_carregados["detalhes_proc"]
if "calculos" in dados_carregados:
    st.session_state["calculos"] = dados_carregados["calculos"]
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
            border-right: none !important;
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
            font-weight: 600 !important;
            border-left: 3px solid #005EB8 !important;
        }

        [data-testid="stSidebar"] hr { border-color: #1A5F9E !important; }

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
        .main-header p { color: #CCCCCC !important; }

        .eaton-card {
            background: #FFFFFF !important;
            border: 1px solid #D0E1F5 !important;
            border-radius: 12px !important;
            padding: 2rem !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 2px 8px rgba(0,94,184,0.08) !important;
            transition: all 0.3s ease !important;
        }

        .eaton-card:hover {
            box-shadow: 0 4px 16px rgba(0,94,184,0.15) !important;
            border-color: #005EB8 !important;
        }

        .eaton-subheader {
            color: #003366 !important;
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
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
            box-shadow: 0 2px 8px rgba(0,94,184,0.3) !important;
            transition: all 0.3s ease !important;
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

        .pill {
            display:inline-block;
            padding: 6px 14px;
            background: linear-gradient(135deg, #005EB8 0%, #00468A 100%);
            color: #FFFFFF !important;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
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

        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            border-radius: 8px !important;
            border: 1px solid #CCCCCC !important;
            padding: 10px 14px !important;
            background: #FAFAFA !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #005EB8 !important;
            box-shadow: 0 0 0 3px rgba(0, 94, 184, 0.15) !important;
            background: #FFFFFF !important;
        }

        ::-webkit-scrollbar { width: 8px !important; height: 8px !important; }
        ::-webkit-scrollbar-track { background: #F0F5FA !important; }
        ::-webkit-scrollbar-thumb { background: #005EB8 !important; border-radius: 4px !important; }
        ::-webkit-scrollbar-thumb:hover { background: #00468A !important; }

        .streamlit-expanderHeader {
            background: #F0F5FA !important;
            border: 1px solid #D0E1F5 !important;
            border-radius: 8px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
    <div class="main-header">
        <h1>🧮 Cálculos de Processos</h1>
        <p>Selecione os parâmetros essenciais dos processos escolhidos.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Campos (labels exatas)
# ============================================================
FC_LONG_FIELDS = [
    "Velocidade de corte face (Vc) [m/min]",
    "Diâmetro da face (D) [mm]",
    "Avanço face f [mm/rot]",
    "Percurso radial da face (Le) [mm]",
    "Velocidade de corte centrar (Vc) [m/min]",
    "Diâmetro da broca (D) [mm]",
    "Avanço centrar f [mm/rot]",
    "Profundidade de furo (ld) [mm]",
    "Aproximação/Saída [mm]",
]
FC_SHORT_TO_LONG = {
    "Vc_face [m/min]": "Velocidade de corte face (Vc) [m/min]",
    "D_face [mm]": "Diâmetro da face (D) [mm]",
    "f_face [mm/rot]": "Avanço face f [mm/rot]",
    "Le_face [mm]": "Percurso radial da face (Le) [mm]",
    "Vc_ctr [m/min]": "Velocidade de corte centrar (Vc) [m/min]",
    "D_broca [mm]": "Diâmetro da broca (D) [mm]",
    "f_ctr [mm/rot]": "Avanço centrar f [mm/rot]",
    "ld [mm]": "Profundidade de furo (ld) [mm]",
}

VAZAO_LONG_FIELDS = ["DiametroInicial","DiametroFinal","ComprimentoUsinado","ProfundidadeCorte"]
CORTE_SERRA_LONG_FIELDS = ["Tempo de ciclo (s)"]
FORJAMENTO_LONG_FIELDS = ["MassaEmBranco","ReducaoArea"]
MULTI_OPTIONS = ["x1","x2","x3","x4"]

TORNEAMENTO_EXT_FIELDS = [
    "Velocidade de corte (Vc) [m/min]",
    "Diâmetro (D) [mm]",
    "Avanço por rotação (f) [mm/rot]",
    "Comprimento efetivo (Le) [mm]",
]

FURACAO_FIELDS = [
    "Velocidade de corte (Vc) [m/min]",
    "Diâmetro (D) [mm]",
    "Avanço por rotação (f) [mm/rot]",
    "Profundidade de furo (ld) [mm]",
    "Aproximação/Saída [mm]",
]

FRES_CHAVETA_FIELDS = [
    "Velocidade de corte (Vc) [m/min]",
    "Diâmetro (D) [mm]",
    "Nº de dentes (z)",
    "Avanço por dente (F/Z) [mm/dente]",
    "Comprimento total (L) [mm]",
]

FURACAO_PROFUNDA_FIELDS = [
    "Velocidade de corte (Vc) [m/min]",
    "Diâmetro (D) [mm]",
    "Avanço por rotação (f) [mm/rot]",
    "Comprimento total (L) [mm]",
    "Tempos auxiliares (t_aux) [min]",
]

FRESAMENTO_FIELDS = [
    "Velocidade de corte (Vc) [m/min]",
    "Diâmetro (D) [mm]",
    "Nº de dentes (z)",
    "Avanço por dente (F/Z) [mm/dente]",
    "Comprimento efetivo (Le) [mm]",
]

CHANF_FURO_FIELDS = [
    "Nº de dentes (Z)",
    "Comprimento do chanfro (L_ch) [mm]",
    "Avanço de trabalho (Vf) [mm/min]",
    "Nº de passadas (Np)",
    "Tempo de indexação por dente (t_idx) [min]",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
]

HOBBER_FIELDS = [
    "Largura de face (B) [mm]",
    "Sobrecurso (Bov) [mm]",
    "Avanço de trabalho (v_trab) [mm/min]",
    "Estoque radial (Sr) [mm]",
    "Incremento radial por passada (ae) [mm/min]",
    "Profundidade por camada (ap) [mm]",
    "Nº de passadas (Np)",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Tempo de troca (t_troca) [min]",
    "Peças entre trocas (P_vida)",
]

SHAPER_FIELDS = [
    "Comprimento com corte (L_trab) [mm]",
    "Avanço de trabalho (Vf_trab) [mm/min]",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Paradas/Medições (t_paradas) [min]",
]

SHAVER_FIELDS = [
    "Largura de face (B) [mm]",
    "Sobrecurso (Bov) [mm]",
    "Passadas de desbaste (Nbr)",
    "Passadas de acabamento (Nfin)",
    "Avanço desbaste (v_trab_br) [mm/min]",
    "Avanço acabamento (v_trab_fin) [mm/min]",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Tempos auxiliares (t_aux) [min]",
]

CHANF_ARESTAS_FIELDS = [
    "Comprimento da aresta [mm]",
    "Avanço de trabalho (Vf) [mm/min]",
]

LAMIN_FRIO_FIELDS = [
    "Largura de face (B) [mm]",
    "Sobrecurso (Bov) [mm]",
    "Avanço de trabalho (v_trab) [mm/min]",
    "Nº de passadas (Np)",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Tempo de troca (t_troca) [min]",
    "Peças entre trocas (P_vida)",
]

CHANFRAR_DENTES_FIELDS = [
    "Nº de dentes (Z)",
    "Comprimento do chanfro (L_ch) [mm]",
    "Avanço de trabalho (Vf) [mm/min]",
    "Nº de passadas (Np)",
    "Tempo de indexação por dente (t_idx) [min]",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Tempos auxiliares (t_aux) [min]",
]

AJUSTE_AMASS_FIELDS = [
    "Largura de face (B) [mm]",
    "Sobrecurso (Bov) [mm]",
    "Avanço de trabalho (v_trab) [mm/min]",
    "Nº de passadas (Np)",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Tempos auxiliares (t_aux) [min]",
]

BROCHAMENTO_FIELDS = [
    "Curso de corte (L_fwd) [mm]",
    "Avanço de trabalho (Vf) [mm/min]",
    "Nº de passadas (Np)",
    "Curso de retorno (L_ret) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido pos. (Vr_pos) [mm/min]",
    "Dwell/Paradas (t_dw) [min]",
    "Tempos auxiliares (t_aux) [min]",
]

REBROCHAMENTO_FIELDS = [
    "Curso de corte (L_fwd) [mm]",
    "Avanço de trabalho (Vf) [mm/min]",
    "Curso de retorno (L_ret) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido pos. (Vr_pos) [mm/min]",
    "Tempos auxiliares (t_aux) [min]",
]

SKIVING_FIELDS = [
    "Largura de face (B) [mm]",
    "Sobrecurso (Bov) [mm]",
    "Avanço de trabalho (v_trab) [mm/min]",
    "Nº de passadas (Np)",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Tempos auxiliares (t_aux) [min]",
]

RECALQUE_FIELDS = [
    "Curso de conformação (L_form) [mm]",
    "Avanço de conformação (Vf_form) [mm/min]",
    "Nº de passadas (Np)",
    "Curso de retorno (L_ret) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido pos. (Vr_pos) [mm/min]",
    "Dwell/Paradas (t_dw) [min]",
    "Tempos auxiliares (t_aux) [min]",
]

POWER_HONING_FIELDS = [
    "Nº de dentes (Z)",
    "Largura de face (B) [mm]",
    "Spark-out (t_so) [min]",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
    "Tempos auxiliares (t_aux) [min]",
]

TT_FIELDS = [
    "CICLO por batelada (min)",
    "CARGA/B (peças/batelada)",
]

RETIFICACAO_DENTES_FIELDS = [
    "Nº de dentes (Z)",
    "Comprimento de perfil por dente (L_per) [mm]",
    "Avanço de trabalho (Vf) [mm/min]",
    "Passadas de desbaste (Nbr)",
    "Passadas de acabamento (Nfin)",
    "Spark-out (t_so) [min]",
    "Tempo de indexação por dente (t_idx) [min]",
    "Tempo de dress (t_dress) [min]",
    "Peças entre dressagens (P_dress)",
    "Percurso em rápido (L0) [mm]",
    "Velocidade de rápido (Vr) [mm/min]",
]

RETIFICACAO_PLANA_FIELDS = [
    "Avanço de travessa (V_feed_travessa) [mm/min]",
    "Incremento radial por passada (ae) [mm/min]",
    "Sobremetal total (S) [mm]",
    "Comprimento efetivo (Le) [mm]",
    "Spark-out (t_sp) [s]",
]

TORNEAMENTO_DURO_FIELDS = [
    "Tempo de ciclo",
]

RETIFICACAO_INTERNA_FIELDS = [
    "Velocidade da pedra (Vs) [m/s]",
    "Diâmetro do rebolo (Dr) [mm]",
    "Velocidade da peça (Vw) [m/min]",
    "Rotação da peça (n_w) [rpm]",
    "Diâmetro do furo (D_furo) [mm]",
    "Incremento radial por passada (ae) [mm/min]",
    "Sobremetal no diâmetro (S_diam) [mm]",
    "Sobremetal no raio (S_raio) [mm]",
    "Comprimento efetivo (Le) [mm]",
    "Avanço de passagem (V_feed) [mm/min]",
    "Spark-out (t_sp) [s]",
]

RETIFICACAO_EXTERNA_FIELDS = [
    "Velocidade da pedra (Vs) [m/s]",
    "Diâmetro do rebolo (Dr) [mm]",
    "Velocidade da peça (Vw) [m/min]",
    "Rotação da peça (n_w) [rpm]",
    "Diâmetro da peça (Dw) [mm]",
    "Incremento radial por passada (ae) [mm/min]",
    "Sobremetal no diâmetro (S_diam) [mm]",
    "Sobremetal no raio (S_raio) [mm]",
    "Comprimento efetivo (Le) [mm]",
    "Avanço de passagem (V_feed) [mm/min]",
    "Spark-out (t_sp) [s]",
]

SHOT_PEENING_FIELDS = [
    "Tempo de ciclo (min)",
]

SHOT_CLEANING_FIELDS = [
    "Tempo de ciclo (min)",
]

FOSFATO_FIELDS = [
    "CICLO por batelada (min)",
    "CARGA/B (peças/batelada)",
]

TINTA_PROTETIVA_FIELDS = [
    "Tempo de ciclo (min)",
]

ENDIREITAMENTO_FIELDS = [
    "Peças/hora",
]

ENGRENOMETRO_FIELDS = [
    "Peças/hora",
]

TESTE_CONTATO_RUIDO_FIELDS = [
    "Peças/hora",
]

INSPECAO_DIMENSIONAL_FIELDS = [
    "Peças/hora",
]

INSPECAO_FINAL_FIELDS = [
    "Peças/hora",
]

LAVAGEM_INDUSTRIAL_FIELDS = [
    "CICLO por batelada (min)",
    "CARGA/B (peças/batelada)",
]

MONTAGEM_FIELDS = [
    "Tempo de ciclo (min)",
]

GRAVACAO_MARCACAO_FIELDS = [
    "Peças/hora",
]

# ============================================================
# Utils
# ============================================================
def _num_input(label: str, key: str, default: float | None, step: float, fmt: str):
    if key in st.session_state:
        init = st.session_state[key]
    else:
        init = 0.0 if (default is None) else float(default)
    return st.number_input(label, min_value=0.0, step=step, format=fmt, value=init, key=key)

def _prefill_template(process_name: str, field_names: list[str], short_map: dict | None = None):
    op = process_name
    codigo = ""
    values = {f: None for f in field_names}

    rows = st.session_state.get("tabela_rows_editada") or st.session_state.get("tabela_rows")
    if isinstance(rows, list) and rows:
        row = next((r for r in rows if r.get("Operação") == op), None)
        if row:
            if row.get("Código") is not None:
                codigo = str(row.get("Código"))
            normalized = {}
            for k, v in row.items():
                if short_map and k in short_map:
                    normalized[short_map[k]] = v
                else:
                    normalized[k] = v
            for f in field_names:
                if f in normalized and normalized[f] is not None:
                    values[f] = normalized[f]

    if not codigo:
        det = st.session_state.get("detalhes_proc", {}).get(op, {})
        if det and det.get("codigo") is not None:
            codigo = str(det.get("codigo"))

    return op, codigo, values

def _prefill_facear():     return _prefill_template("Facear e Centrar", FC_LONG_FIELDS, FC_SHORT_TO_LONG)
def _prefill_vazao():      return _prefill_template("Vazão", VAZAO_LONG_FIELDS)
def _prefill_corte():      return _prefill_template("Corte/Serra", CORTE_SERRA_LONG_FIELDS)
def _prefill_forjamento(): return _prefill_template("Forjamento", FORJAMENTO_LONG_FIELDS)
def _prefill_simple(proc_name: str, fields: list[str]):
    return _prefill_template(proc_name, fields)

def _prefill_multi_only(proc_name: str):
    op = proc_name
    codigo = ""
    mult = "x1"
    rows = st.session_state.get("tabela_rows_editada") or st.session_state.get("tabela_rows")
    if isinstance(rows, list) and rows:
        row = next((r for r in rows if r.get("Operação") == op), None)
        if row:
            if row.get("Código") is not None:
                codigo = str(row.get("Código"))
            if row.get("Multiplicidade"):
                mult = str(row.get("Multiplicidade"))
            elif row.get("x"):
                mult = str(row.get("x"))
    if not codigo:
        det = st.session_state.get("detalhes_proc", {}).get(op, {})
        if det and det.get("codigo") is not None:
            codigo = str(det.get("codigo"))
        if det and det.get("multi"):
            mult = det["multi"]
    if mult not in MULTI_OPTIONS:
        mult = "x1"
    return op, codigo, mult

# ============================================================
# Blocos (forms) base
# ============================================================
def block_facear(container):
    op, codigo, prefill = _prefill_facear()
    with container:
        st.subheader(op); st.markdown("**Parâmetros essenciais**")
        res_ph = st.empty()
        with st.form("form_fc"):
            _num_input(FC_LONG_FIELDS[0], "fc_vc_face", prefill[FC_LONG_FIELDS[0]], 1.0, "%.2f")
            _num_input(FC_LONG_FIELDS[1], "fc_d_face", prefill[FC_LONG_FIELDS[1]], 0.1, "%.2f")
            _num_input(FC_LONG_FIELDS[2], "fc_f_face", prefill[FC_LONG_FIELDS[2]], 0.01, "%.3f")
            _num_input(FC_LONG_FIELDS[3], "fc_le_face", prefill[FC_LONG_FIELDS[3]], 0.1, "%.2f")
            _num_input(FC_LONG_FIELDS[4], "fc_vc_ctr", prefill[FC_LONG_FIELDS[4]], 1.0, "%.2f")
            _num_input(FC_LONG_FIELDS[5], "fc_d_broca", prefill[FC_LONG_FIELDS[5]], 0.1, "%.2f")
            _num_input(FC_LONG_FIELDS[6], "fc_f_ctr", prefill[FC_LONG_FIELDS[6]], 0.01, "%.3f")
            _num_input(FC_LONG_FIELDS[7], "fc_ld", prefill[FC_LONG_FIELDS[7]], 0.1, "%.2f")
            _num_input(FC_LONG_FIELDS[8], "fc_aprox_saida", prefill[FC_LONG_FIELDS[8]], 0.1, "%.2f")
            c1, c2 = st.columns(2)
            with c1:  salvar = st.form_submit_button("💾 Salvar parâmetros")
            with c2:  calc   = st.form_submit_button("🧮 Calcular")
        if salvar:
            st.session_state.setdefault("calculos", {})
            st.session_state["calculos"][op] = {
                "codigo": codigo,
                "Velocidade de corte face (Vc) [m/min]": st.session_state["fc_vc_face"],
                "Diâmetro da face (D) [mm]": st.session_state["fc_d_face"],
                "Avanço face f [mm/rot]": st.session_state["fc_f_face"],
                "Percurso radial da face (Le) [mm]": st.session_state["fc_le_face"],
                "Velocidade de corte centrar (Vc) [m/min]": st.session_state["fc_vc_ctr"],
                "Diâmetro da broca (D) [mm]": st.session_state["fc_d_broca"],
                "Avanço centrar f [mm/rot]": st.session_state["fc_f_ctr"],
                "Profundidade de furo (ld) [mm]": st.session_state["fc_ld"],
                "Aproximação/Saída [mm]": st.session_state["fc_aprox_saida"],
            }; res_ph.success("Parâmetros salvos para Facear e Centrar.")
        if 'calc' in locals() and calc:
            soma = (float(st.session_state["fc_vc_face"]) + float(st.session_state["fc_d_face"]) +
                    float(st.session_state["fc_f_face"]) + float(st.session_state["fc_le_face"]) +
                    float(st.session_state["fc_vc_ctr"]) + float(st.session_state["fc_d_broca"]) +
                    float(st.session_state["fc_f_ctr"]) + float(st.session_state["fc_ld"]) +
                    float(st.session_state["fc_aprox_saida"]))
            st.session_state["resultado_fc"] = soma
        if "resultado_fc" in st.session_state:
            st.markdown("**Resultado:**"); st.info(f"{st.session_state['resultado_fc']:,.3f}")

def block_vazao(container):
    op, codigo, prefill = _prefill_vazao()
    with container:
        st.subheader(op); st.markdown("**Parâmetros essenciais**")
        res_ph = st.empty()
        with st.form("form_vz"):
            _num_input("DiametroInicial", "vz_diam_ini", prefill["DiametroInicial"], 0.1, "%.2f")
            _num_input("DiametroFinal", "vz_diam_fin", prefill["DiametroFinal"], 0.1, "%.2f")
            _num_input("ComprimentoUsinado", "vz_comp_usinado", prefill["ComprimentoUsinado"], 0.1, "%.2f")
            _num_input("ProfundidadeCorte", "vz_prof_corte", prefill["ProfundidadeCorte"], 0.1, "%.2f")
            c1, c2 = st.columns(2)
            with c1:  salvar = st.form_submit_button("💾 Salvar parâmetros")
            with c2:  calc   = st.form_submit_button("🧮 Calcular")
        if salvar:
            st.session_state.setdefault("calculos", {})
            st.session_state["calculos"][op] = {
                "codigo": codigo,
                "DiametroInicial": st.session_state["vz_diam_ini"],
                "DiametroFinal": st.session_state["vz_diam_fin"],
                "ComprimentoUsinado": st.session_state["vz_comp_usinado"],
                "ProfundidadeCorte": st.session_state["vz_prof_corte"],
            }; res_ph.success("Parâmetros salvos para Vazão.")
        if 'calc' in locals() and calc:
            soma = (float(st.session_state["vz_diam_ini"]) + float(st.session_state["vz_diam_fin"]) +
                    float(st.session_state["vz_comp_usinado"]) + float(st.session_state["vz_prof_corte"]))
            st.session_state["resultado_vazao"] = soma
        if "resultado_vazao" in st.session_state:
            st.markdown("**Resultado:**"); st.info(f"{st.session_state['resultado_vazao']:,.3f}")

def block_corte_serra(container):
    op, codigo, prefill = _prefill_corte()
    with container:
        st.subheader("Corte/Serra"); st.markdown("**Parâmetros essenciais**")
        res_ph = st.empty()
        with st.form("form_cs"):
            _num_input("Tempo de ciclo (s)", "cs_tempo_ciclo", prefill["Tempo de ciclo (s)"], 0.1, "%.2f")
            c1, c2 = st.columns(2)
            with c1:  salvar = st.form_submit_button("💾 Salvar parâmetros")
            with c2:  calc   = st.form_submit_button("🧮 Calcular")
        if salvar:
            st.session_state.setdefault("calculos", {})
            st.session_state["calculos"]["Corte/Serra"] = {"codigo": codigo, "Tempo de ciclo (s)": st.session_state["cs_tempo_ciclo"]}
            res_ph.success("Parâmetros salvos para Corte/Serra.")
        if 'calc' in locals() and calc:
            st.session_state["resultado_corte_serra"] = float(st.session_state["cs_tempo_ciclo"])
        if "resultado_corte_serra" in st.session_state:
            st.markdown("**Resultado:**"); st.info(f"{st.session_state['resultado_corte_serra']:,.3f}")

def block_forjamento(container):
    op, codigo, prefill = _prefill_forjamento()
    with container:
        st.subheader("Forjamento"); st.markdown("**Parâmetros essenciais**")
        res_ph = st.empty()
        with st.form("form_fj"):
            _num_input("MassaEmBranco", "fj_massa_branco", prefill["MassaEmBranco"], 0.1, "%.2f")
            _num_input("ReducaoArea", "fj_reducao_area", prefill["ReducaoArea"], 0.1, "%.2f")
            c1, c2 = st.columns(2)
            with c1:  salvar = st.form_submit_button("💾 Salvar parâmetros")
            with c2:  calc   = st.form_submit_button("🧮 Calcular")
        if salvar:
            st.session_state.setdefault("calculos", {})
            st.session_state["calculos"]["Forjamento"] = {
                "codigo": codigo,
                "MassaEmBranco": st.session_state["fj_massa_branco"],
                "ReducaoArea": st.session_state["fj_reducao_area"],
            }; res_ph.success("Parâmetros salvos para Forjamento.")
        if 'calc' in locals() and calc:
            st.session_state["resultado_forjamento"] = float(st.session_state["fj_massa_branco"]) + float(st.session_state["fj_reducao_area"])
        if "resultado_forjamento" in st.session_state:
            st.markdown("**Resultado:**"); st.info(f"{st.session_state['resultado_forjamento']:,.3f}")

def _render_hss_form(container, proc_name: str, fields: list[str], state_prefix: str):
    op, codigo, mult = _prefill_multi_only(proc_name)
    _, _, prefill = _prefill_simple(proc_name, fields)

    with container:
        st.subheader(proc_name)
        st.markdown(f"<span class='pill'>Multiplicidade: {mult}</span>", unsafe_allow_html=True)

        st.markdown("**Parâmetros essenciais**")
        res_ph = st.empty()

        with st.form(f"form_{state_prefix}"):
            values_keys = []
            for idx, label in enumerate(fields):
                key = f"{state_prefix}_{idx}"
                values_keys.append((label, key))
                step, fmt = 0.1, "%.2f"
                lb = label.lower()
                if "[mm/rot]" in lb or "[mm/dente]" in lb:
                    step, fmt = 0.01, "%.3f"
                if "[min]" in lb:
                    step, fmt = 0.01, "%.2f"
                if "(np)" in lb or "(nbr)" in lb or "(nfin)" in lb or "(p_vida)" in lb or "(z)" in lb:
                    step, fmt = 1.0, "%.0f"
                _num_input(label, key, prefill[label], step, fmt)

            c1, c2 = st.columns(2)
            with c1:
                salvar = st.form_submit_button("💾 Salvar parâmetros")
            with c2:
                calcular = st.form_submit_button("🧮 Calcular")

        if salvar:
            st.session_state.setdefault("calculos", {})
            payload = {"codigo": codigo, "Multiplicidade": mult}
            for (label, key) in values_keys:
                payload[label] = st.session_state[key]
            st.session_state["calculos"][proc_name] = payload
            res_ph.success(f"Parâmetros salvos para {proc_name}.")

        if 'calcular' in locals() and calcular:
            soma = 0.0
            for (label, key) in values_keys:
                soma += float(st.session_state[key])
            st.session_state[f"resultado_{state_prefix}"] = soma

        if f"resultado_{state_prefix}" in st.session_state:
            st.markdown("**Resultado:**")
            st.info(f"{st.session_state[f'resultado_{state_prefix}']:,.3f}")

def block_hobber(c):  _render_hss_form(c, "Hobber", HOBBER_FIELDS, "hb")
def block_shaper(c):  _render_hss_form(c, "Shaper", SHAPER_FIELDS, "shp")
def block_shaver(c):  _render_hss_form(c, "Shaver", SHAVER_FIELDS, "shv")

def _render_simple_form(container, proc_name: str, fields: list[str], state_prefix: str):
    op, codigo, prefill = _prefill_simple(proc_name, fields)
    with container:
        st.subheader(proc_name)
        st.markdown("**Parâmetros essenciais**")

        res_ph = st.empty()
        with st.form(f"form_{state_prefix}"):
            values_keys = []
            for idx, label in enumerate(fields):
                key = f"{state_prefix}_{idx}"
                values_keys.append((label, key))
                step = 0.1
                fmt  = "%.2f"
                lb = label.lower()
                if "[mm/rot]" in lb or "[mm/dente]" in lb:
                    step, fmt = 0.01, "%.3f"
                if "[min]" in lb:
                    step, fmt = 0.01, "%.2f"
                if "(np)" in lb or "(nbr)" in lb or "(nfin)" in lb or "(p_vida)" in lb or "(z)" in lb:
                    step, fmt = 1.0, "%.0f"
                if "peças" in lb or "pecas" in lb:
                    step, fmt = 1.0, "%.0f"

                _num_input(label, key, prefill[label], step, fmt)

            c1, c2 = st.columns(2)
            with c1:  salvar = st.form_submit_button("💾 Salvar parâmetros")
            with c2:  calc   = st.form_submit_button("🧮 Calcular")

        if salvar:
            st.session_state.setdefault("calculos", {})
            payload = {"codigo": codigo}
            for (label, key) in values_keys:
                payload[label] = st.session_state[key]
            st.session_state["calculos"][proc_name] = payload
            res_ph.success(f"Parâmetros salvos para {proc_name}.")

        if 'calc' in locals() and calc:
            soma = 0.0
            for (label, key) in values_keys:
                soma += float(st.session_state[key])
            st.session_state[f"resultado_{state_prefix}"] = soma

        if f"resultado_{state_prefix}" in st.session_state:
            st.markdown("**Resultado:**")
            st.info(f"{st.session_state[f'resultado_{state_prefix}']:,.3f}")

def block_torneamento_externo(c): _render_simple_form(c, "Torneamento externo", TORNEAMENTO_EXT_FIELDS, "tx")
def block_furacao(c):             _render_simple_form(c, "Furação", FURACAO_FIELDS, "fu")
def block_fres_chaveta(c):        _render_simple_form(c, "Fresamento de chaveta", FRES_CHAVETA_FIELDS, "fcv")
def block_furacao_profunda(c):    _render_simple_form(c, "Furação profunda", FURACAO_PROFUNDA_FIELDS, "fup")
def block_fresamento(c):          _render_simple_form(c, "Fresamento", FRESAMENTO_FIELDS, "frs")
def block_chanf_furo(c):          _render_simple_form(c, "Chanframento de furo", CHANF_FURO_FIELDS, "chf")
def block_chanf_arestas(c):       _render_simple_form(c, "Chanframento de arestas", CHANF_ARESTAS_FIELDS, "car")
def block_lamin_frio(c):          _render_simple_form(c, "Laminação a frio (dentes/estrias)", LAMIN_FRIO_FIELDS, "lam")
def block_chanfrar_dentes(c):     _render_simple_form(c, "Chanfrar dentes", CHANFRAR_DENTES_FIELDS, "chd")
def block_ajuste_amass(c):        _render_simple_form(c, "Ajuste/Amassamento de dentes", AJUSTE_AMASS_FIELDS, "ajd")
def block_brochamento(c):         _render_simple_form(c, "Brochamento", BROCHAMENTO_FIELDS, "brc")
def block_rebrochamento(c):       _render_simple_form(c, "Rebrochamento", REBROCHAMENTO_FIELDS, "rbr")
def block_skiving(c):             _render_simple_form(c, "Skiving", SKIVING_FIELDS, "skv")
def block_recalque(c):            _render_simple_form(c, "Recalque", RECALQUE_FIELDS, "rcl")
def block_power_honing(c):        _render_simple_form(c, "Power honing", POWER_HONING_FIELDS, "pwh")
def block_forno_continuo(c):      _render_simple_form(c, "Forno contínuo", TT_FIELDS, "tt_fc")
def block_forno_camara(c):        _render_simple_form(c, "Forno câmara", TT_FIELDS, "tt_fcam")
def block_carbonitr(c):           _render_simple_form(c, "Carbonitretação", TT_FIELDS, "tt_cbn")
def block_revenimento(c):         _render_simple_form(c, "Revenimento", TT_FIELDS, "tt_rev")
def block_normalizacao(c):        _render_simple_form(c, "Normalização", TT_FIELDS, "tt_norm")
def block_recoz_iso(c):           _render_simple_form(c, "Recozimento isotérmico", TT_FIELDS, "tt_reciso")
def block_recristalizacao(c):     _render_simple_form(c, "Recristalização", TT_FIELDS, "tt_recris")
def block_retificacao_dentes(c):      _render_simple_form(c, "Retificação de dentes", RETIFICACAO_DENTES_FIELDS, "rd")
def block_retificacao_plana(c):       _render_simple_form(c, "Retificação plana", RETIFICACAO_PLANA_FIELDS, "rp")
def block_torneamento_duro(c):        _render_simple_form(c, "Torneamento duro (pós-TT)", TORNEAMENTO_DURO_FIELDS, "td")
def block_retificacao_interna(c):     _render_simple_form(c, "Retificação interna", RETIFICACAO_INTERNA_FIELDS, "ri")
def block_retificacao_externa(c):     _render_simple_form(c, "Retificação externa", RETIFICACAO_EXTERNA_FIELDS, "re")
def block_shot_peening(c):        _render_simple_form(c, "Shot peening", SHOT_PEENING_FIELDS, "sp")
def block_shot_cleaning(c):       _render_simple_form(c, "Shot cleaning", SHOT_CLEANING_FIELDS, "sc")
def block_fosfato(c):             _render_simple_form(c, "Fosfato", FOSFATO_FIELDS, "fos")
def block_tinta_protetiva(c):     _render_simple_form(c, "Tinta protetiva", TINTA_PROTETIVA_FIELDS, "tp")
def block_endireitamento(c):      _render_simple_form(c, "Endireitamento", ENDIREITAMENTO_FIELDS, "end")
def block_engrenometro(c):            _render_simple_form(c, "Engrenômetro", ENGRENOMETRO_FIELDS, "eng")
def block_teste_contato_ruido(c):     _render_simple_form(c, "Teste de contato/ruído", TESTE_CONTATO_RUIDO_FIELDS, "tcr")
def block_inspecao_dimensional(c):    _render_simple_form(c, "Inspeção dimensional", INSPECAO_DIMENSIONAL_FIELDS, "id")
def block_inspecao_final(c):          _render_simple_form(c, "Inspeção final", INSPECAO_FINAL_FIELDS, "if")
def block_lavagem_industrial(c):      _render_simple_form(c, "Lavagem industrial", LAVAGEM_INDUSTRIAL_FIELDS, "lav")
def block_montagem(c):                _render_simple_form(c, "Montagem", MONTAGEM_FIELDS, "mont")
def block_gravacao_marcacao(c):       _render_simple_form(c, "Gravação/Marcação", GRAVACAO_MARCACAO_FIELDS, "gm")

# ============================================================
# Auto‑organização 2×N por ordem de seleção
# ============================================================
SUPPORTED = [
    "Facear e Centrar", "Vazão", "Corte/Serra", "Forjamento",
    "Hobber", "Shaper", "Shaver",
    "Torneamento externo", "Furação", "Fresamento de chaveta",
    "Furação profunda", "Fresamento", "Chanframento de furo",
    "Chanframento de arestas", "Laminação a frio (dentes/estrias)",
    "Chanfrar dentes", "Ajuste/Amassamento de dentes", "Brochamento",
    "Rebrochamento", "Skiving", "Recalque", "Power honing",
    "Retificação de dentes", "Retificação plana", "Torneamento duro (pós-TT)",
    "Retificação interna", "Retificação externa",
    "Shot peening", "Shot cleaning", "Fosfato", "Tinta protetiva", "Endireitamento",
    "Engrenômetro", "Teste de contato/ruído", "Inspeção dimensional", "Inspeção final",
    "Lavagem industrial", "Montagem", "Gravação/Marcação",
    "Forno contínuo", "Forno câmara", "Carbonitretação", "Revenimento",
    "Normalização", "Recozimento isotérmico", "Recristalização",
]

def _get_selected_in_order() -> list[str]:
    detalhes = st.session_state.get("detalhes_proc", {})
    ordered = []
    for k in detalhes.keys():
        if k in SUPPORTED and detalhes[k].get("codigo"):
            ordered.append(k)
    return ordered

def _prepare_rows_for_prefill(selected: list[str]):
    rows = st.session_state.get("tabela_rows", [])
    if not isinstance(rows, list):
        rows = []
    for proc in selected:
        if not any(r.get("Operação") == proc for r in rows):
            codigo = st.session_state["detalhes_proc"][proc]["codigo"]
            row = {"Operação": proc, "Código": codigo}
            if proc in {"Hobber","Shaper","Shaver"}:
                multi = st.session_state["detalhes_proc"][proc].get("multi", "x1")
                row["Multiplicidade"] = multi
            rows.append(row)
    st.session_state["tabela_rows"] = rows

# ---------------- Render principal ----------------
selected = _get_selected_in_order()
_prepare_rows_for_prefill(selected)

if not selected:
    st.warning("Nenhum processo foi selecionado para preenchimento. Volte à página de seleção e escolha um processo.")
    st.page_link("pages/1_resumo.py", label="⬅ Voltar para seleção (Página 2)")
else:
    for i in range(0, len(selected), 2):
        col_esq, col_dir = st.columns([0.5, 0.5])

        left = selected[i]
        if left == "Facear e Centrar":   block_facear(col_esq)
        elif left == "Vazão":            block_vazao(col_esq)
        elif left == "Corte/Serra":      block_corte_serra(col_esq)
        elif left == "Forjamento":       block_forjamento(col_esq)
        elif left == "Hobber":           block_hobber(col_esq)
        elif left == "Shaper":           block_shaper(col_esq)
        elif left == "Shaver":           block_shaver(col_esq)
        elif left == "Torneamento externo":   block_torneamento_externo(col_esq)
        elif left == "Furação":               block_furacao(col_esq)
        elif left == "Fresamento de chaveta": block_fres_chaveta(col_esq)
        elif left == "Furação profunda":      block_furacao_profunda(col_esq)
        elif left == "Fresamento":            block_fresamento(col_esq)
        elif left == "Chanframento de furo":  block_chanf_furo(col_esq)
        elif left == "Chanframento de arestas":  block_chanf_arestas(col_esq)
        elif left == "Laminação a frio (dentes/estrias)":  block_lamin_frio(col_esq)
        elif left == "Chanfrar dentes":       block_chanfrar_dentes(col_esq)
        elif left == "Ajuste/Amassamento de dentes":  block_ajuste_amass(col_esq)
        elif left == "Brochamento":           block_brochamento(col_esq)
        elif left == "Rebrochamento":         block_rebrochamento(col_esq)
        elif left == "Skiving":               block_skiving(col_esq)
        elif left == "Recalque":              block_recalque(col_esq)
        elif left == "Power honing":          block_power_honing(col_esq)
        elif left == "Retificação de dentes": block_retificacao_dentes(col_esq)
        elif left == "Retificação plana":     block_retificacao_plana(col_esq)
        elif left == "Torneamento duro (pós-TT)": block_torneamento_duro(col_esq)
        elif left == "Retificação interna":   block_retificacao_interna(col_esq)
        elif left == "Retificação externa":   block_retificacao_externa(col_esq)
        elif left == "Shot peening":        block_shot_peening(col_esq)
        elif left == "Shot cleaning":       block_shot_cleaning(col_esq)
        elif left == "Fosfato":             block_fosfato(col_esq)
        elif left == "Tinta protetiva":     block_tinta_protetiva(col_esq)
        elif left == "Endireitamento":      block_endireitamento(col_esq)
        elif left == "Engrenômetro":            block_engrenometro(col_esq)
        elif left == "Teste de contato/ruído":  block_teste_contato_ruido(col_esq)
        elif left == "Inspeção dimensional":    block_inspecao_dimensional(col_esq)
        elif left == "Inspeção final":          block_inspecao_final(col_esq)
        elif left == "Lavagem industrial":      block_lavagem_industrial(col_esq)
        elif left == "Montagem":                block_montagem(col_esq)
        elif left == "Gravação/Marcação":       block_gravacao_marcacao(col_esq)
        elif left == "Forno contínuo":        block_forno_continuo(col_esq)
        elif left == "Forno câmara":          block_forno_camara(col_esq)
        elif left == "Carbonitretação":       block_carbonitr(col_esq)
        elif left == "Revenimento":           block_revenimento(col_esq)
        elif left == "Normalização":          block_normalizacao(col_esq)
        elif left == "Recozimento isotérmico": block_recoz_iso(col_esq)
        elif left == "Recristalização":       block_recristalizacao(col_esq)

        if i + 1 < len(selected):
            right = selected[i+1]
            if right == "Facear e Centrar":   block_facear(col_dir)
            elif right == "Vazão":            block_vazao(col_dir)
            elif right == "Corte/Serra":      block_corte_serra(col_dir)
            elif right == "Forjamento":       block_forjamento(col_dir)
            elif right == "Hobber":           block_hobber(col_dir)
            elif right == "Shaper":           block_shaper(col_dir)
            elif right == "Shaver":           block_shaver(col_dir)
            elif right == "Torneamento externo":   block_torneamento_externo(col_dir)
            elif right == "Furação":               block_furacao(col_dir)
            elif right == "Fresamento de chaveta": block_fres_chaveta(col_dir)
            elif right == "Furação profunda":      block_furacao_profunda(col_dir)
            elif right == "Fresamento":            block_fresamento(col_dir)
            elif right == "Chanframento de furo":  block_chanf_furo(col_dir)
            elif right == "Chanframento de arestas":  block_chanf_arestas(col_dir)
            elif right == "Laminação a frio (dentes/estrias)":  block_lamin_frio(col_dir)
            elif right == "Chanfrar dentes":       block_chanfrar_dentes(col_dir)
            elif right == "Ajuste/Amassamento de dentes":  block_ajuste_amass(col_dir)
            elif right == "Brochamento":           block_brochamento(col_dir)
            elif right == "Rebrochamento":         block_rebrochamento(col_dir)
            elif right == "Skiving":               block_skiving(col_dir)
            elif right == "Recalque":              block_recalque(col_dir)
            elif right == "Power honing":          block_power_honing(col_dir)
            elif right == "Retificação de dentes": block_retificacao_dentes(col_dir)
            elif right == "Retificação plana":     block_retificacao_plana(col_dir)
            elif right == "Torneamento duro (pós-TT)": block_torneamento_duro(col_dir)
            elif right == "Retificação interna":   block_retificacao_interna(col_dir)
            elif right == "Retificação externa":   block_retificacao_externa(col_dir)
            elif right == "Shot peening":        block_shot_peening(col_dir)
            elif right == "Shot cleaning":       block_shot_cleaning(col_dir)
            elif right == "Fosfato":             block_fosfato(col_dir)
            elif right == "Tinta protetiva":     block_tinta_protetiva(col_dir)
            elif right == "Endireitamento":      block_endireitamento(col_dir)
            elif right == "Engrenômetro":            block_engrenometro(col_dir)
            elif right == "Teste de contato/ruído":  block_teste_contato_ruido(col_dir)
            elif right == "Inspeção dimensional":    block_inspecao_dimensional(col_dir)
            elif right == "Inspeção final":          block_inspecao_final(col_dir)
            elif right == "Lavagem industrial":      block_lavagem_industrial(col_dir)
            elif right == "Montagem":                block_montagem(col_dir)
            elif right == "Gravação/Marcação":       block_gravacao_marcacao(col_dir)
            elif right == "Forno contínuo":        block_forno_continuo(col_dir)
            elif right == "Forno câmara":          block_forno_camara(col_dir)
            elif right == "Carbonitretação":       block_carbonitr(col_dir)
            elif right == "Revenimento":           block_revenimento(col_dir)
            elif right == "Normalização":          block_normalizacao(col_dir)
            elif right == "Recozimento isotérmico": block_recoz_iso(col_dir)
            elif right == "Recristalização":       block_recristalizacao(col_dir)

# ---------------------------
# Navegação
# ---------------------------
# No final do arquivo 2_calculos.py, altere a navegação para:

st.markdown('<div class="nav-fixed">', unsafe_allow_html=True)
col_prev, col_next = st.columns([1, 1])
with col_prev:
    st.page_link("pages/1_resumo.py", label="⬅ Voltar", use_container_width=True)
with col_next:
    st.page_link("pages/3_relatorio.py", label="Ver Relatório Final ➡", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown(
    """
    <div class="eaton-footer">
        <p><strong>EATON</strong> | Powering Business Worldwide</p>
        <p>© 2024 Eaton Corporation. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True,
)