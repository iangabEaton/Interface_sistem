# pages/2_calculos.py
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cálculos de Processos", page_icon="🧮", layout="wide")

# ===== CSS azul clarinho na sidebar =====
st.markdown(
    """
    &lt;style&gt;
      [data-testid="stSidebar"] { background: #EAF2FE !important; border-right: 1px solid #DFE7FB !important; }
      [data-testid="stSidebar"] * { color: #123B7A !important; }
      [data-testid="stSidebar"] nav ul li a { background: #E3EFFF !important; border-radius: 10px !important; padding: 6px 10px !important; color: #123B7A !important; }
      [data-testid="stSidebar"] nav ul li a:hover { background: #D6E8FF !important; text-decoration: none !important; }
      [data-testid="stSidebar"] nav ul li a[aria-current="page"] { background: #CFE3FF !important; color: #0F3D91 !important; font-weight: 600 !important; }
      [data-testid="stSidebar"] hr { border-color: #D1DCF5 !important; }
      .pill { display:inline-block; padding:4px 10px; background:#E3EFFF; color:#123B7A; border-radius:999px; margin-right:8px; font-weight:600; }
      .card { padding: 1rem 1.25rem; border: 1px solid #e5e7eb; border-radius: 8px; background: #fafafa; margin-bottom: 1rem; }
    &lt;/style&gt;
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Campos (labels exatas)
# ============================================================
# Facear e Centrar
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

# Vazão
VAZAO_LONG_FIELDS = ["DiametroInicial","DiametroFinal","ComprimentoUsinado","ProfundidadeCorte"]

# Corte/Serra
CORTE_SERRA_LONG_FIELDS = ["Tempo de ciclo (s)"]

# Forjamento
FORJAMENTO_LONG_FIELDS  = ["MassaEmBranco","ReducaoArea"]

# Hobber / Shaper / Shaver: multiplicidade definida na página 1
MULTI_OPTIONS = ["x1","x2","x3","x4"]

# ===== Usinagens de base – labels como nas imagens =====
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

# ===== Hobber / Shaper / Shaver – bloquinhos (além da multiplicidade) =====
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

# ===== Engrenagens / Perfis gerados adicionais (anteriores) =====
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

# ===== NOVOS (desta mensagem): Rebrochamento, Skiving, Recalque, Power honing =====
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

# ===== Tratamento térmico (7 processos) – campos comuns =====
TT_FIELDS = [
    "CICLO por batelada (min)",
    "CARGA/B (peças/batelada)",
]

# ============================================================
# Utils
# ============================================================
def _num_input(label: str, key: str, default: float | None, step: float, fmt: str):
    """number_input estável: usa o valor do estado se já existir; senão, usa default (None -> 0.0)."""
    if key in st.session_state:
        init = st.session_state[key]
    else:
        init = 0.0 if (default is None) else float(default)
    return st.number_input(label, min_value=0.0, step=step, format=fmt, value=init, key=key)

def _prefill_template(process_name: str, field_names: list[str], short_map: dict | None = None):
    """Gera (op, codigo, values_dict) a partir de tabela_rows(_editada) e detalhes_proc."""
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
    """Prefill genérico (só labels finais)."""
    return _prefill_template(proc_name, fields)

def _prefill_multi_only(proc_name: str):
    """Prefill para Hobber/Shaper/Shaver (só multiplicidade)."""
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

# ========= Hobber / Shaper / Shaver =========
def _render_hss_form(container, proc_name: str, fields: list[str], state_prefix: str):
    """Renderiza pill de multiplicidade (somente leitura) + parâmetros essenciais do processo HSS."""
    op, codigo, mult = _prefill_multi_only(proc_name)
    _, _, prefill = _prefill_simple(proc_name, fields)

    with container:
        st.subheader(proc_name)
        st.markdown(f"&lt;span class='pill'&gt;Multiplicidade: {mult}&lt;/span&gt;", unsafe_allow_html=True)

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

# ============================================================
# Blocos simples (reutilizam _render_simple_form)
# ============================================================
def _render_simple_form(container, proc_name: str, fields: list[str], state_prefix: str):
    """Renderer padrão: inputs numerados com labels 'fields', salvar, calcular (soma) e resultado."""
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
                # Inteiros para peças/batelada
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

# Usinagens de base
def block_torneamento_externo(c): _render_simple_form(c, "Torneamento externo", TORNEAMENTO_EXT_FIELDS, "tx")
def block_furacao(c):             _render_simple_form(c, "Furação", FURACAO_FIELDS, "fu")
def block_fres_chaveta(c):        _render_simple_form(c, "Fresamento de chaveta", FRES_CHAVETA_FIELDS, "fcv")
def block_furacao_profunda(c):    _render_simple_form(c, "Furação profunda", FURACAO_PROFUNDA_FIELDS, "fup")
def block_fresamento(c):          _render_simple_form(c, "Fresamento", FRESAMENTO_FIELDS, "frs")
def block_chanf_furo(c):          _render_simple_form(c, "Chanframento de furo", CHANF_FURO_FIELDS, "chf")

# Engrenagens / Perfis (anteriores)
def block_chanf_arestas(c):       _render_simple_form(c, "Chanframento de arestas", CHANF_ARESTAS_FIELDS, "car")
def block_lamin_frio(c):          _render_simple_form(c, "Laminação a frio (dentes/estrias)", LAMIN_FRIO_FIELDS, "lam")
def block_chanfrar_dentes(c):     _render_simple_form(c, "Chanfrar dentes", CHANFRAR_DENTES_FIELDS, "chd")
def block_ajuste_amass(c):        _render_simple_form(c, "Ajuste/Amassamento de dentes", AJUSTE_AMASS_FIELDS, "ajd")
def block_brochamento(c):         _render_simple_form(c, "Brochamento", BROCHAMENTO_FIELDS, "brc")

# >>> NOVOS NESTA MENSAGEM (já existiam em etapas anteriores)
def block_rebrochamento(c):       _render_simple_form(c, "Rebrochamento", REBROCHAMENTO_FIELDS, "rbr")
def block_skiving(c):             _render_simple_form(c, "Skiving", SKIVING_FIELDS, "skv")
def block_recalque(c):            _render_simple_form(c, "Recalque", RECALQUE_FIELDS, "rcl")
def block_power_honing(c):        _render_simple_form(c, "Power honing", POWER_HONING_FIELDS, "pwh")

# ===== Tratamento térmico – blocos =====
def block_forno_continuo(c):      _render_simple_form(c, "Forno contínuo", TT_FIELDS, "tt_fc")
def block_forno_camara(c):        _render_simple_form(c, "Forno câmara", TT_FIELDS, "tt_fcam")
def block_carbonitr(c):           _render_simple_form(c, "Carbonitretação", TT_FIELDS, "tt_cbn")
def block_revenimento(c):         _render_simple_form(c, "Revenimento", TT_FIELDS, "tt_rev")
def block_normalizacao(c):        _render_simple_form(c, "Normalização", TT_FIELDS, "tt_norm")
def block_recoz_iso(c):           _render_simple_form(c, "Recozimento isotérmico", TT_FIELDS, "tt_reciso")
def block_recristalizacao(c):     _render_simple_form(c, "Recristalização", TT_FIELDS, "tt_recris")

# ============================================================
# Auto‑organização 2×N por ordem de seleção
# ============================================================
SUPPORTED = [
    "Facear e Centrar",
    "Vazão",
    "Corte/Serra",
    "Forjamento",
    "Hobber",
    "Shaper",
    "Shaver",
    # usinagens base
    "Torneamento externo",
    "Furação",
    "Fresamento de chaveta",
    "Furação profunda",
    "Fresamento",
    "Chanframento de furo",
    # engrenagens/perfis anteriores
    "Chanframento de arestas",
    "Laminação a frio (dentes/estrias)",
    "Chanfrar dentes",
    "Ajuste/Amassamento de dentes",
    "Brochamento",
    # novos desta mensagem
    "Rebrochamento",
    "Skiving",
    "Recalque",
    "Power honing",
    # >>> Tratamento térmico
    "Forno contínuo",
    "Forno câmara",
    "Carbonitretação",
    "Revenimento",
    "Normalização",
    "Recozimento isotérmico",
    "Recristalização",
]

def _get_selected_in_order() -> list[str]:
    detalhes = st.session_state.get("detalhes_proc", {})
    ordered = []
    for k in detalhes.keys():  # ordem de inserção preservada
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
st.title("Cálculos de Processos")
st.markdown("Selecione os parâmetros essenciais dos processos escolhidos.")

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
            elif right == "Forno contínuo":        block_forno_continuo(col_dir)
            elif right == "Forno câmara":          block_forno_camara(col_dir)
            elif right == "Carbonitretação":       block_carbonitr(col_dir)
            elif right == "Revenimento":           block_revenimento(col_dir)
            elif right == "Normalização":          block_normalizacao(col_dir)
            elif right == "Recozimento isotérmico": block_recoz_iso(col_dir)
            elif right == "Recristalização":       block_recristalizacao(col_dir)

# ---------------------------
# Navegação fixa (anterior/próxima)
# ---------------------------
PAGINA_ANTERIOR = "pages/1_resumo.py"
PROXIMA_PAGINA  = "pages/2_calculos.py"

nav_container = st.container()
c_prev, c_next = nav_container.columns([1, 1])

with c_prev:
    prev_clicked = st.button("⬅ Voltar para seleção (Página 2)", use_container_width=True, key="btn_prev_calc")
with c_next:
    next_clicked = st.button("Próxima página ➡", type="primary", use_container_width=True, key="btn_next_calc")

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
            st.page_link(PAGINA_ANTERIOR, label="⬅ Voltar para seleção (Página 2)")
        with lc2:
            st.page_link(PROXIMA_PAGINA, label="Próxima página ➡")

st.markdown(
    """
    &lt;style&gt;
      section.main &gt; div.block-container &gt; div:last-child {
        position: fixed !important;
        right: 16px; bottom: 16px; z-index: 1000; width: 360px;
        background: rgba(255,255,255,0.92); backdrop-filter: blur(6px);
        padding: 8px; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.15);
      }
      section.main &gt; div.block-container &gt; div:last-child [data-testid="column"] { padding: 0 4px !important; }
      section.main &gt; div.block-container &gt; div:last-child .stButton &gt; button { min-height: 40px; width: 100%; }
    &lt;/style&gt;
    """,
    unsafe_allow_html=True,
)


