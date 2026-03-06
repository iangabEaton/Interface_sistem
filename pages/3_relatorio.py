# pages/3_relatorio.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils import carregar_dados, salvar_dados

# Configuração da página
st.set_page_config(page_title="Relatório de Cotação", page_icon="📑", layout="wide")

# =========================
# ESTILO PROFISSIONAL EATON (AZUL)
# =========================
st.markdown(
    """
    <style>
        :root { --eaton-blue: #005EB8; --eaton-blue-dark: #00468A; }
        
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #003366 0%, #00468A 100%) !important; }
        [data-testid="stSidebar"] * { color: #FFFFFF !important; }

        .main-header {
            background: linear-gradient(135deg, #003366 0%, #00468A 100%);
            padding: 2rem 3rem; border-radius: 12px; margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,94,184,0.2);
            border-left: 5px solid #005EB8; border-top: 3px solid #005EB8;
        }
        .main-header h1 { color: #FFFFFF !important; font-size: 2rem !important; font-weight: 700 !important; }
        .main-header p { color: #CCCCCC !important; font-size: 1rem !important; }

        /* ===== VISÃO EXECUTIVA ===== */
        .executive-dashboard {
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            border: 2px solid #005EB8; border-radius: 16px;
            padding: 2rem !important; margin-bottom: 2rem !important;
            box-shadow: 0 4px 20px rgba(0,94,184,0.15) !important;
        }
        
        .executive-title {
            color: #003366 !important; font-size: 1.5rem !important; font-weight: 700 !important;
            margin-bottom: 1.5rem !important; display: flex; align-items: center; gap: 12px;
            padding-bottom: 0.8rem !important; border-bottom: 3px solid #005EB8 !important;
        }

        .info-item {
            background: #F8F9FA; padding: 1rem; border-radius: 8px;
            border-left: 4px solid #005EB8;
        }

        .report-section {
            background: #FFFFFF !important; border: 1px solid #D0E1F5 !important;
            border-radius: 12px !important; padding: 2rem !important;
            margin-bottom: 2rem !important; box-shadow: 0 2px 8px rgba(0,94,184,0.08) !important;
        }

        .eaton-subheader {
            color: #003366 !important; font-size: 1.4rem !important; font-weight: 700 !important;
            margin-bottom: 1.5rem !important; padding-bottom: 0.5rem !important;
            border-bottom: 2px solid #005EB8 !important; display: flex; align-items: center; gap: 10px;
        }

        .process-list-item {
            background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 8px;
            padding: 1rem 1.5rem; margin-bottom: 0.8rem;
            display: flex; justify-content: space-between; align-items: center;
            transition: all 0.2s;
        }
        .process-list-item:hover { border-color: #005EB8; background: #F0F5FA; }
        .process-name { font-weight: 600; color: #003366; font-size: 1.1rem; }
        .process-code { background: #E6F0FA; color: #005EB8; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; }

        .calc-panel {
            background: #F8F9FA; border: 1px solid #D0E1F5; border-radius: 12px;
            padding: 1.5rem; position: sticky; top: 20px;
        }
        .calc-card {
            background: #FFFFFF; border-left: 4px solid #005EB8;
            padding: 1rem; margin-bottom: 1rem; border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .calc-title { font-size: 0.9rem; font-weight: 700; color: #00468A; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid #E0E0E0; }
        .calc-row { display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.3rem; }
        .calc-val { font-weight: 600; color: #333; }

        .nav-fixed {
            position: fixed !important; right: 24px !important; bottom: 24px !important;
            z-index: 1000 !important; background: #FFFFFF !important; padding: 12px !important;
            border-radius: 12px !important; box-shadow: 0 4px 20px rgba(0,94,184,0.2) !important;
            display: flex !important; gap: 12px !important; border: 1px solid #D0E1F5 !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #005EB8 0%, #00468A 100%) !important;
            color: #FFFFFF !important; border: none !important; border-radius: 8px !important;
            padding: 12px 24px !important; font-weight: 600 !important;
        }
        .eaton-footer {
            text-align: center !important; padding: 2rem !important; color: #666666 !important;
            font-size: 0.85rem !important; border-top: 3px solid #005EB8 !important;
            margin-top: 3rem !important; background: #FAFAFA !important;
        }

        /* KPI Cards na Visão Executiva */
        .kpi-card {
            background: linear-gradient(135deg, #005EB8 0%, #00468A 100%);
            color: #FFFFFF !important; padding: 1.5rem; border-radius: 12px;
            text-align: center; box-shadow: 0 4px 15px rgba(0,94,184,0.3);
        }
        .kpi-value { font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }
        .kpi-label { font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }
        
        /* Estilo da Tabela */
        div[data-testid="stDataFrame"] {
            border: 1px solid #D0E1F5 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }
        
        /* Info Grid */
        .info-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem; margin-bottom: 1.5rem;
        }
        
        /* Parâmetro Item - Apenas Nome */
        .param-item {
            background: #F8F9FA; padding: 0.6rem 0.8rem; border-radius: 6px;
            margin-bottom: 0.4rem; color: #003366; font-size: 0.85rem;
            border-left: 3px solid #005EB8;
        }
        
        /* Card de Status */
        .status-card {
            background: #F8F9FA; border: 2px solid #005EB8; 
            border-radius: 12px; padding: 1.5rem; text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# HEADER
# =========================
st.markdown(
    """
    <div class="main-header">
        <h1>📑 Relatório Técnico de Cotação</h1>
        <p>Consolidação final de dados e parâmetros.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# RECUPERAÇÃO DE DADOS
# =========================

# 1. Dados da Peça
dados_peca = st.session_state.get("dados_peca", {})

if not dados_peca:
    dados_salvos = carregar_dados()
    if dados_salvos and "dados_peca" in dados_salvos:
        dados_peca = dados_salvos["dados_peca"]
        st.session_state["dados_peca"] = dados_peca

if not dados_peca:
    st.warning("⚠️ Nenhum dado de peça encontrado. Por favor, preencha a página inicial primeiro.")
    st.page_link("Interface.py", label="⬅ Ir para Entrada de Dados")
    st.stop()

def get_val(key, default="-"):
    val = dados_peca.get(key)
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return default
    return val

# 2. Processos Selecionados
processos_selecionados = []
detalhes_proc = st.session_state.get("detalhes_proc", {})
if not detalhes_proc:
    dados_salvos = carregar_dados()
    if dados_salvos and "detalhes_proc" in dados_salvos:
        detalhes_proc = dados_salvos["detalhes_proc"]

for proc_nome, detalhes in detalhes_proc.items():
    if detalhes.get("codigo"):
        processos_selecionados.append({
            "nome": proc_nome,
            "codigo": detalhes.get("codigo"),
            "multiplicidade": detalhes.get("multi", "-")
        })

# 3. Resultados dos Cálculos
resultados_calculos = st.session_state.get("calculos", {})
if not resultados_calculos:
    dados_salvos = carregar_dados()
    if dados_salvos and "calculos" in dados_salvos:
        resultados_calculos = dados_salvos["calculos"]

# =========================
# 🎯 VISÃO EXECUTIVA
# =========================
st.markdown('<div class="executive-dashboard">', unsafe_allow_html=True)
st.markdown('<h2 class="executive-title">🎯 Visão Executiva da Cotação</h2>', unsafe_allow_html=True)

# KPIs Principais
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    ce_val = get_val('CE', 'N/A')
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{ce_val if ce_val != '-' else 'N/A'}</div>
        <div class="kpi-label">Cost Estimate</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{len(processos_selecionados)}</div>
        <div class="kpi-label">Processos Selecionados</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{len(resultados_calculos)}</div>
        <div class="kpi-label">Cálculos Realizados</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    status_text = "Completo" if len(resultados_calculos) == len(processos_selecionados) and processos_selecionados else "Em Andamento"
    bg_gradient = "linear-gradient(135deg, #28a745 0%, #1e7e34 100%)" if status_text == "Completo" else "linear-gradient(135deg, #ffc107 0%, #ff9800 100%)"
    st.markdown(f"""
    <div class="kpi-card" style="background: {bg_gradient};">
        <div class="kpi-value" style="font-size: 1.5rem;">{status_text}</div>
        <div class="kpi-label">Status</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# 3 COLUNAS: Info Peça | Classificação | Dimensões
# ============================================
col_info, col_class, col_dims = st.columns([0.4, 0.35, 0.25])

# COLUNA 1: Informações da Peça
with col_info:
    st.markdown('<div class="info-item" style="height:100%;">', unsafe_allow_html=True)
    st.markdown('<h3 class="eaton-subheader" style="font-size:1rem; border:none;">🔷 Dados da Peça</h3>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; gap:0.8rem;">
        <div><span style="color:#666; font-size:0.8rem; text-transform:uppercase; font-weight:600;">CE</span><br><strong style="color:#003366;">{get_val('CE')}</strong></div>
        <div><span style="color:#666; font-size:0.8rem; text-transform:uppercase; font-weight:600;">Número da Peça</span><br><strong style="color:#003366;">{get_val('Peça (nº dentro da CE)')}</strong></div>
        <div><span style="color:#666; font-size:0.8rem; text-transform:uppercase; font-weight:600;">Material</span><br><strong style="color:#003366;">{get_val('Material')}</strong></div>
        <div><span style="color:#666; font-size:0.8rem; text-transform:uppercase; font-weight:600;">Planta</span><br><strong style="color:#003366;">{get_val('Planta')}</strong></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# COLUNA 2: Classificação da Peça
with col_class:
    st.markdown('<div class="info-item" style="height:100%; border-left-color: #28a745;">', unsafe_allow_html=True)
    st.markdown('<h3 class="eaton-subheader" style="font-size:1rem; border:none; border-bottom-color: #28a745 !important;">🏷️ Classificação</h3>', unsafe_allow_html=True)
    
    tipo_val = get_val('Tipo (classificação)')
    subtipo_val = get_val('Subtipo (classificação)')
    
    if tipo_val and tipo_val != "-":
        st.markdown(f"""
        <div style="background: #D4EDDA; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.8rem; border-left: 3px solid #28a745;">
            <span style="color:#155724; font-size:0.75rem; text-transform:uppercase; font-weight:600;">Tipo</span><br>
            <strong style="color:#155724; font-size:1.1rem;">{tipo_val}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    if subtipo_val and subtipo_val != "-":
        st.markdown(f"""
        <div style="background: #D4EDDA; padding: 0.8rem; border-radius: 8px; border-left: 3px solid #28a745;">
            <span style="color:#155724; font-size:0.75rem; text-transform:uppercase; font-weight:600;">Subtipo</span><br>
            <strong style="color:#155724; font-size:1.1rem;">{subtipo_val}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    if not tipo_val or tipo_val == "-":
        st.caption("⚠️ Classificação não informada")
    
    st.markdown('</div>', unsafe_allow_html=True)

# COLUNA 3: Dimensões Críticas
with col_dims:
    st.markdown('<div class="info-item" style="height:100%; border-left-color: #17a2b8;">', unsafe_allow_html=True)
    st.markdown('<h3 class="eaton-subheader" style="font-size:1rem; border:none; border-bottom-color: #17a2b8 !important;">📐 Dimensões</h3>', unsafe_allow_html=True)
    
    dims = [
        ("Ø Int.", get_val('Ø interno (mm)')),
        ("Ø Ext.", get_val('Ø externo (mm)')),
        ("Dentes", get_val('Nº dentes')),
        ("Módulo", get_val('Módulo (mm)'))
    ]
    
    for lbl, val in dims:
        if val != "-":
            unidade = " mm" if "Ø" in lbl or "Módulo" in lbl else ""
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #E0E0E0;">
                <span style="color:#666; font-size:0.8rem;">{lbl}</span>
                <strong style="color:#003366;">{val}{unidade}</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #E0E0E0;">
                <span style="color:#999; font-size:0.8rem;">{lbl}</span>
                <span style="color:#CCC;">-</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# OBSERVAÇÕES EM DESTAQUE
# ============================================
obs = get_val('Observações')
if obs and obs != "-":
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #FFF8E1 0%, #FFFFFF 100%); border: 2px solid #FFC107; border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0;">
        <h3 style="color: #856404; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 8px;">
            📝 Observações Importantes
        </h3>
        <p style="color: #666666; line-height: 1.6; margin: 0; white-space: pre-wrap;">{obs}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="background: #F8F9FA; border: 1px dashed #CCCCCC; border-radius: 12px; padding: 1rem; margin: 1.5rem 0; text-align: center;">
        <span style="color: #999999;">📝 Nenhuma observação registrada</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TIMELINE DO PROCESSO (COM NOVA COLUNA)
# ============================================
st.markdown('<h3 class="eaton-subheader" style="font-size:1.1rem; border:none; margin-top:1.5rem">📊 Fluxo do Processo</h3>', unsafe_allow_html=True)

if processos_selecionados:
    ce_valor = get_val('CE', 'N/A')
    
    # Inicializa ou carrega revisões do session_state
    if "revisoes_cotacao" not in st.session_state:
        st.session_state["revisoes_cotacao"] = {}
    
    # Carregar revisões salvas no JSON se existir
    dados_salvos = carregar_dados()
    if dados_salvos and "revisoes_cotacao" in dados_salvos and not st.session_state["revisoes_cotacao"]:
        st.session_state["revisoes_cotacao"] = dados_salvos["revisoes_cotacao"]
    
    proc_data = []
    
    for idx, proc in enumerate(processos_selecionados, 1):
        tem_calculo = proc['nome'] in resultados_calculos
        
        tempo_operacao = "-"
        
        if tem_calculo and resultados_calculos.get(proc['nome']):
            calc_dados = resultados_calculos[proc['nome']]
            
            for chave in ['Tempo de ciclo (s)', 'Tempo de ciclo (min)', 'CICLO por batelada (min)', 
                          'Peças/hora', 't_aux', 't_so', 't_dress', 't_sp']:
                if chave in calc_dados and calc_dados[chave]:
                    valor = calc_dados[chave]
                    unidade = " min" if "min" in chave else " s" if "s" in chave else ""
                    if "peças" in chave.lower():
                        tempo_operacao = f"{valor} pçs/h"
                    else:
                        tempo_operacao = f"{valor}{unidade}"
                    break
        
        # Get revisão existente (1, 2 ou 3)
        revisao = st.session_state["revisoes_cotacao"].get(proc['nome'], 1)
        
        proc_data.append({
            "OP": idx * 10,
            "CE": ce_valor,
            "Processo": proc['nome'],
            "Centro de Custo": proc['codigo'],
            "Multiplicidade": proc['multiplicidade'],
            "Tempo de Operação": tempo_operacao,
            "Operation Multiple Resource Name": "",  # ✅ NOVA COLUNA (EM BRANCO)
            "Revisão de Cotação": int(revisao) if revisao else 1,
            "tem_calculo": tem_calculo
        })
    
    df_proc = pd.DataFrame(proc_data)
    
    # Exibir tabela com editor para colunas editáveis
    edited_df = st.data_editor(
        df_proc[['OP', 'CE', 'Processo', 'Centro de Custo', 'Multiplicidade', 'Tempo de Operação', 'Operation Multiple Resource Name', 'Revisão de Cotação']],
        use_container_width=True, 
        hide_index=True,
        column_config={
            "OP": st.column_config.NumberColumn("OP", format="%d", disabled=True),
            "CE": st.column_config.TextColumn("CE", disabled=True),
            "Processo": st.column_config.TextColumn("Processo", disabled=True),
            "Centro de Custo": st.column_config.TextColumn("Centro de Custo", disabled=True),
            "Multiplicidade": st.column_config.TextColumn("Multiplicidade", disabled=True),
            "Tempo de Operação": st.column_config.TextColumn("Tempo de Operação", disabled=True),
            "Operation Multiple Resource Name": st.column_config.TextColumn("Operation Multiple Resource Name"),
            "Revisão de Cotação": st.column_config.NumberColumn(
                "Revisão de Cotação",
                min_value=1,
                max_value=3,
                step=1,
                format="%d"
            )
        },
        key="editor_revisoes",
        disabled=["OP", "CE", "Processo", "Centro de Custo", "Multiplicidade", "Tempo de Operação"]
    )
    
    # Salvar revisões alteradas automaticamente (sem botão)
    for index, row in edited_df.iterrows():
        proc_nome = row['Processo']
        revisao_valor = row['Revisão de Cotação']
        if pd.notna(revisao_valor):
            st.session_state["revisoes_cotacao"][proc_nome] = int(revisao_valor)
    
    # Salvar automaticamente no JSON
    salvar_dados({"revisoes_cotacao": st.session_state["revisoes_cotacao"]})

else:
    st.info("Nenhum processo selecionado.")

st.markdown(f'<div style="text-align: right; color: #666666; font-size: 0.85rem; margin-top: 1rem;">🕐 Gerado em: {datetime.now().strftime("%d/%m/%Y às %H:%M")}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RESULTADOS DOS CÁLCULOS POR PROCESSO (EXPANDERS COM VALORES)
# =========================
st.markdown('<h3 class="eaton-subheader" style="font-size:1.1rem; border:none; margin-top:2rem">🧮 Resultados dos Cálculos por Processo</h3>', unsafe_allow_html=True)

if processos_selecionados:
    for idx, proc in enumerate(processos_selecionados, 1):
        proc_nome = proc['nome']
        tem_calculo = proc_nome in resultados_calculos
        
        with st.expander(f"**OP {idx*10}** | {proc_nome}", expanded=False):
            col_res1, col_res2 = st.columns([0.7, 0.3])
            
            with col_res1:
                if tem_calculo:
                    calc_dados = resultados_calculos[proc_nome]
                    
                    st.markdown("**⚙️ Parâmetros do Processo:**")
                    
                    # Exibir parâmetros COM VALORES em 2 colunas
                    param_items = [(k, v) for k, v in calc_dados.items() 
                                   if k not in ['codigo', 'Código', 'Multiplicidade'] and isinstance(v, (int, float))]
                    
                    if param_items:
                        col_p1, col_p2 = st.columns(2)
                        for i, (chave, valor) in enumerate(param_items):
                            with col_p1 if i % 2 == 0 else col_p2:
                                st.metric(label=chave, value=f"{valor:.2f}")
                    
                    # Revisão do Processo (se houver)
                    revisao = st.session_state["revisoes_cotacao"].get(proc_nome, 1)
                    if revisao:
                        st.info(f"📝 **Revisão:** {revisao}")
                else:
                    st.warning("⚠️ Cálculos não realizados para este processo.")
            
            with col_res2:
                # Card de Status
                st.markdown(f"""
                <div class="status-card">
                    <div style="color: #666; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 0.5rem; font-weight:700;">
                        Status
                    </div>
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">
                        {"✅" if tem_calculo else "⏳"}
                    </div>
                    <div style="color: {"#28a745" if tem_calculo else "#ffc107"}; font-weight: 700; font-size:1rem;">
                        {"Completo" if tem_calculo else "Pendente"}
                    </div>
                    <hr style="border-color: #D0E1F5; margin: 1rem 0;">
                    <div style="color: #666; font-size: 0.75rem; text-transform:uppercase; font-weight:600;">
                        Centro de Custo
                    </div>
                    <div style="color: #003366; font-size: 1.8rem; font-weight: 700;">
                        {proc['codigo']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if not tem_calculo:
                    st.page_link("pages/2_calculos.py", label="✏️ Realizar Cálculos", use_container_width=True)

# =========================
# LAYOUT PRINCIPAL (DETALHES) - SEM DIMENSÕES PRINCIPAIS
# =========================

col_esq, col_dir = st.columns([0.7, 0.3])

# ---------------------------------------------------------
# COLUNA ESQUERDA (70%)
# ---------------------------------------------------------
with col_esq:
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="eaton-subheader">🔷 1. Informações Detalhadas da Peça</h2>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label">CE (Cost Estimate)</div>
            <div class="info-value">{get_val('CE')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Número da Peça</div>
            <div class="info-value">{get_val('Peça (nº dentro da CE)')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Material</div>
            <div class="info-value">{get_val('Material')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Planta</div>
            <div class="info-value">{get_val('Planta')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Classificação</div>
            <div class="info-value">{get_val('Tipo (classificação)')} - {get_val('Subtipo (classificação)')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Data de Criação</div>
            <div class="info-value">{datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="eaton-subheader">⚙️ 2. Processos Selecionados</h2>', unsafe_allow_html=True)
    
    if not processos_selecionados:
        st.info("Nenhum processo selecionado.")
    else:
        for idx, proc in enumerate(processos_selecionados):
            multi_tag = f" ({proc['multiplicidade']})" if proc['multiplicidade'] != "-" else ""
            st.markdown(f"""
            <div class="process-list-item">
                <span class="process-name">{idx+1}. {proc['nome']}{multi_tag}</span>
                <span class="process-code">{proc['codigo']}</span>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# COLUNA DIREITA (30%) - PARÂMETROS UTILIZADOS (APENAS NOMES)
# ---------------------------------------------------------
with col_dir:
    st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
    st.markdown('<h2 class="eaton-subheader" style="font-size:1.2rem">📋 Parâmetros Utilizados</h2>', unsafe_allow_html=True)
    
    if not resultados_calculos:
        st.warning("Sem cálculos realizados.")
    else:
        for proc_nome, params in resultados_calculos.items():
            st.markdown(f'<div class="calc-card"><div class="calc-title">{proc_nome}</div>', unsafe_allow_html=True)
            
            # Listar APENAS os nomes dos parâmetros (sem valores)
            for chave in params.keys():
                if chave not in ['codigo', 'Código', 'Multiplicidade']:
                    st.markdown(f'<div class="param-item">• {chave}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.metric(label="Total Processos", value=len(processos_selecionados))
    st.metric(label="Cálculos Realizados", value=len(resultados_calculos))
    
    if processos_selecionados:
        progresso = (len(resultados_calculos) / len(processos_selecionados)) * 100
        st.progress(progresso / 100)
        st.caption(f"{progresso:.0f}% dos processos com cálculos completos")
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# NAVEGAÇÃO
# =========================
st.markdown('<div class="nav-fixed">', unsafe_allow_html=True)
col_prev, col_next = st.columns([1, 1])
with col_prev:
    st.page_link("pages/2_calculos.py", label="⬅ Voltar para Cálculos", use_container_width=True)
with col_next:
    st.button("🖨️ Imprimir Relatório", use_container_width=True, type="primary", key="btn_print")
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
