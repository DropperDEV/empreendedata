import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
import io
import os
import tempfile

# ============================================================
# CONFIGURAÇÃO DA PÁGINA (deve ser o PRIMEIRO comando Streamlit)
# ============================================================
st.set_page_config(
    page_title="EmpreendeData — Dashboard Inteligente",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """
        # EmpreendeData v1.0
        Dashboard inteligente para empreendedores revendedores.
        
        Desenvolvido por **James Soares Costa**  
        Estácio (UNESA) — Análise e Desenvolvimento de Sistemas  
        Projeto de Extensão — Sistemas de Informação e Sociedade
        """
    }
)

# ============================================================
# CSS CUSTOMIZADO — Visual Premium
# ============================================================
def inject_custom_css():
    st.markdown("""
    <style>
    /* ===== Google Font Import ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ===== Base Typography ===== */
    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Inter', sans-serif !important;
    }

    /* ===== Animated Gradient Background ===== */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #0c4a6e, #0f172a);
        background-size: 400% 400%;
        animation: gradientShift 25s ease infinite;
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ===== Smooth Fade-in for Main Content ===== */
    .stMainBlockContainer {
        animation: fadeIn 0.6s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ===== Sidebar Styling ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #c7d2fe !important;
    }

    /* ===== Premium Metric Cards ===== */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 20px 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.25);
        border-color: rgba(99, 102, 241, 0.5);
        background: rgba(255, 255, 255, 0.07);
    }

    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        background: linear-gradient(135deg, #c7d2fe, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ===== Glassmorphism Container (border=True) ===== */
    [data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 8px 40px rgba(99, 102, 241, 0.1) !important;
    }

    /* ===== Styled Buttons ===== */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.3px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.5) !important;
        background: linear-gradient(135deg, #818cf8, #a78bfa) !important;
    }

    /* ===== Download Button ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.5) !important;
    }

    /* ===== File Uploader ===== */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(99, 102, 241, 0.3) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        background: rgba(99, 102, 241, 0.05) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: rgba(99, 102, 241, 0.6) !important;
        background: rgba(99, 102, 241, 0.08) !important;
    }

    /* ===== Tabs ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(139, 92, 246, 0.3)) !important;
        border-radius: 10px !important;
    }

    /* ===== DataFrames ===== */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden;
    }

    /* ===== Expander ===== */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* ===== Custom Scrollbar ===== */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.4);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.7);
    }

    /* ===== Hide Streamlit Default Elements ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ===== Divider ===== */
    hr {
        border-color: rgba(99, 102, 241, 0.15) !important;
    }

    /* ===== Success/Warning/Error Alerts ===== */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }

    /* ===== Hero Title Gradient ===== */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #c7d2fe, #6366f1, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin-top: 4px;
        font-weight: 400;
    }

    /* ===== Glass Card Custom HTML ===== */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.35);
        box-shadow: 0 8px 40px rgba(99, 102, 241, 0.1);
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #c7d2fe, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* ===== Pulse Animation for Upload Hint ===== */
    .pulse-hint {
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }

    /* ===== Info Card ===== */
    .info-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.05));
        border-left: 4px solid #6366f1;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
    }

    .info-card h4 {
        color: #c7d2fe;
        margin: 0 0 8px 0;
    }

    .info-card p {
        color: #94a3b8;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()


# ============================================================
# CONFIGURAÇÃO DO PLOTLY — Tema escuro consistente
# ============================================================
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#e2e8f0"),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(99,102,241,0.2)',
        borderwidth=1,
        font=dict(color='#94a3b8')
    ),
    hoverlabel=dict(
        bgcolor='#1e293b',
        bordercolor='#6366f1',
        font=dict(color='#f1f5f9', family='Inter')
    )
)

CHART_COLORS = [
    '#6366f1', '#8b5cf6', '#a78bfa', '#c084fc',
    '#818cf8', '#6d28d9', '#4f46e5', '#7c3aed',
    '#60a5fa', '#38bdf8', '#2dd4bf', '#34d399'
]

CHART_COLORS_GRADIENT = [
    ['#6366f1', '#818cf8'],
    ['#8b5cf6', '#a78bfa'],
    ['#06b6d4', '#22d3ee'],
    ['#10b981', '#34d399'],
    ['#f59e0b', '#fbbf24'],
    ['#ef4444', '#f87171'],
]


# ============================================================
# SIDEBAR — Branding e Upload
# ============================================================
with st.sidebar:
    # Logo / Branding
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div style="font-size: 3rem; margin-bottom: 8px;">📊</div>
        <div style="font-size: 1.5rem; font-weight: 800; 
                    background: linear-gradient(135deg, #c7d2fe, #6366f1, #a78bfa);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text;">
            EmpreendeData
        </div>
        <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px; letter-spacing: 1.5px; text-transform: uppercase;">
            Dashboard Inteligente
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Upload
    st.markdown("### 📁 Enviar Planilha")
    uploaded_file = st.file_uploader(
        "Arraste ou selecione seu arquivo CSV ou Excel",
        type=["csv", "xlsx"],
        help="Formatos aceitos: .csv e .xlsx"
    )

    # Carregar exemplo
    st.markdown("---")
    st.markdown("##### 💡 Sem planilha?")
    usar_exemplo = st.button("📋 Usar Dados de Exemplo", use_container_width=True)

    st.markdown("---")

    # Info do projeto
    st.markdown("""
    <div style="padding: 12px; background: rgba(99,102,241,0.08); border-radius: 12px; border: 1px solid rgba(99,102,241,0.15);">
        <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">
            Projeto de Extensão
        </div>
        <div style="font-size: 0.8rem; color: #c7d2fe; font-weight: 600;">
            Sistemas de Informação e Sociedade
        </div>
        <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">
            Estácio (UNESA) — ADS
        </div>
        <div style="font-size: 0.75rem; color: #64748b;">
            James Soares Costa
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown(
        "<div style='text-align:center; color:#475569; font-size:0.7rem;'>"
        "EmpreendeData v1.0 © 2025"
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def detectar_colunas(df):
    """Detecta colunas numéricas, categóricas e de data."""
    numericas = df.select_dtypes(include=['float64', 'int64', 'float32', 'int32']).columns.tolist()
    categoricas = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    # Tenta detectar colunas de data
    datas = []
    for col in categoricas[:]:
        try:
            pd.to_datetime(df[col], format='mixed', dayfirst=True)
            datas.append(col)
            categoricas.remove(col)
        except (ValueError, TypeError):
            pass

    return numericas, categoricas, datas


def formatar_valor(valor):
    """Formata número como moeda brasileira."""
    if abs(valor) >= 1_000_000:
        return f"R$ {valor/1_000_000:,.1f}M"
    elif abs(valor) >= 1_000:
        return f"R$ {valor/1_000:,.1f}K"
    else:
        return f"R$ {valor:,.2f}"


def formatar_numero(valor):
    """Formata número inteiro com separador de milhares."""
    if abs(valor) >= 1_000_000:
        return f"{valor/1_000_000:,.1f}M"
    elif abs(valor) >= 1_000:
        return f"{valor/1_000:,.1f}K"
    else:
        return f"{valor:,.0f}"


def gerar_pdf(df, kpis, fig_barras=None, fig_pizza=None, fig_treemap=None):
    """Gera relatório PDF completo."""
    pdf = FPDF()
    pdf.add_page()

    # === CABEÇALHO ===
    pdf.set_font("Helvetica", "B", size=28)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 18, txt="EmpreendeData", ln=True, align="C")

    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 8, txt="Relatorio de Analise de Dados", ln=True, align="C")
    pdf.cell(0, 6, txt=f"Gerado em: {datetime.now().strftime('%d/%m/%Y as %H:%M')}", ln=True, align="C")
    pdf.ln(5)

    # Linha divisória
    pdf.set_draw_color(99, 102, 241)
    pdf.set_line_width(0.8)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(10)

    # === SEÇÃO: KPIs ===
    pdf.set_font("Helvetica", "B", size=16)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, txt="Indicadores Principais (KPIs)", ln=True)
    pdf.ln(5)

    # KPI Cards no PDF
    pdf.set_font("Helvetica", size=11)
    for label, value in kpis.items():
        pdf.set_fill_color(243, 244, 246)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(80, 10, txt=f"  {label}:", border=0)
        pdf.set_text_color(99, 102, 241)
        pdf.set_font("Helvetica", "B", size=12)
        pdf.cell(0, 10, txt=str(value), border=0, ln=True)
        pdf.set_font("Helvetica", size=11)
    pdf.ln(8)

    # === SEÇÃO: Gráficos como imagens ===
    charts_added = False
    temp_files = []
    try:
        if fig_barras is not None:
            try:
                tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                fig_barras.write_image(tmp.name, width=800, height=400, scale=2)
                tmp.close()
                temp_files.append(tmp.name)

                pdf.set_font("Helvetica", "B", size=14)
                pdf.set_text_color(30, 41, 59)
                pdf.cell(0, 10, txt="Grafico de Barras", ln=True)
                pdf.ln(3)
                pdf.image(tmp.name, x=15, w=180)
                pdf.ln(10)
                charts_added = True
            except Exception:
                pass

        if fig_pizza is not None:
            try:
                tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                fig_pizza.write_image(tmp.name, width=800, height=400, scale=2)
                tmp.close()
                temp_files.append(tmp.name)

                if pdf.get_y() > 200:
                    pdf.add_page()

                pdf.set_font("Helvetica", "B", size=14)
                pdf.set_text_color(30, 41, 59)
                pdf.cell(0, 10, txt="Grafico de Distribuicao", ln=True)
                pdf.ln(3)
                pdf.image(tmp.name, x=15, w=180)
                pdf.ln(10)
                charts_added = True
            except Exception:
                pass

        if fig_treemap is not None:
            try:
                tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                fig_treemap.write_image(tmp.name, width=800, height=400, scale=2)
                tmp.close()
                temp_files.append(tmp.name)

                if pdf.get_y() > 200:
                    pdf.add_page()

                pdf.set_font("Helvetica", "B", size=14)
                pdf.set_text_color(30, 41, 59)
                pdf.cell(0, 10, txt="Mapa de Categorias (Treemap)", ln=True)
                pdf.ln(3)
                pdf.image(tmp.name, x=15, w=180)
                pdf.ln(10)
                charts_added = True
            except Exception:
                pass
    finally:
        for f in temp_files:
            try:
                os.unlink(f)
            except OSError:
                pass

    if not charts_added:
        pdf.set_font("Helvetica", "I", size=10)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, txt="(Graficos nao puderam ser incluidos - instale 'kaleido' para exportar graficos)", ln=True)
        pdf.ln(5)

    # === SEÇÃO: Tabela de Dados ===
    pdf.add_page()
    pdf.set_font("Helvetica", "B", size=16)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, txt="Tabela de Dados", ln=True)
    pdf.ln(5)

    # Cabeçalho da tabela
    cols = df.columns.tolist()
    max_cols = min(len(cols), 6)  # Limitar colunas para caber no PDF
    cols = cols[:max_cols]

    col_width = (190 - 10) / max_cols

    pdf.set_fill_color(99, 102, 241)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", size=8)
    for col in cols:
        col_name = str(col)[:15]  # Truncar nomes longos
        pdf.cell(col_width, 8, txt=col_name, border=1, fill=True, align="C")
    pdf.ln()

    # Linhas da tabela
    pdf.set_font("Helvetica", size=7)
    max_rows = min(len(df), 30)  # Limitar linhas
    for i in range(max_rows):
        if i % 2 == 0:
            pdf.set_fill_color(248, 250, 252)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(51, 65, 85)

        for col in cols:
            valor = str(df.iloc[i][col])[:18]  # Truncar valores longos
            pdf.cell(col_width, 7, txt=valor, border=1, fill=True, align="C")
        pdf.ln()

    if len(df) > max_rows:
        pdf.set_font("Helvetica", "I", size=8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 8, txt=f"... e mais {len(df) - max_rows} registros", ln=True, align="C")

    # === RODAPÉ ===
    pdf.ln(15)
    pdf.set_draw_color(99, 102, 241)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(8)

    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, txt="EmpreendeData - Dashboard Inteligente para Empreendedores", ln=True, align="C")
    pdf.cell(0, 6, txt="Projeto de Extensao - Sistemas de Informacao e Sociedade", ln=True, align="C")
    pdf.cell(0, 6, txt="Estacio (UNESA) - Analise e Desenvolvimento de Sistemas", ln=True, align="C")
    pdf.cell(0, 6, txt="Desenvolvido por James Soares Costa", ln=True, align="C")

    return pdf.output()


# ============================================================
# CARREGAR DADOS
# ============================================================
df = None

# Verificar se há dados de exemplo ou upload
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.toast("✅ Arquivo carregado com sucesso!", icon="🎉")
    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")

elif usar_exemplo or st.session_state.get('usar_exemplo', False):
    st.session_state['usar_exemplo'] = True
    exemplo_path = os.path.join(os.path.dirname(__file__), "dados_exemplo_revendedores.csv")
    if os.path.exists(exemplo_path):
        df = pd.read_csv(exemplo_path)
        st.toast("📋 Dados de exemplo carregados!", icon="💡")
    else:
        st.error("Arquivo de exemplo não encontrado.")


# ============================================================
# TELA PRINCIPAL
# ============================================================

if df is None:
    # ===== TELA DE BOAS-VINDAS =====
    st.markdown("")
    st.markdown("")

    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <div style="font-size: 4.5rem; margin-bottom: 20px; animation: pulse 2s ease-in-out infinite;">📊</div>
        <div class="hero-title">EmpreendeData</div>
        <div class="hero-subtitle">Dashboard Inteligente para Empreendedores Revendedores</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    col_welcome1, col_welcome2, col_welcome3 = st.columns(3)

    with col_welcome1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 180px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">📥</div>
            <h4 style="color: #c7d2fe; margin: 0 0 8px 0;">1. Envie sua Planilha</h4>
            <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5;">
                Faça o upload de um arquivo CSV ou Excel com seus dados de vendas, clientes ou produtos.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_welcome2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 180px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">📈</div>
            <h4 style="color: #c7d2fe; margin: 0 0 8px 0;">2. Visualize os Dados</h4>
            <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5;">
                Gráficos interativos são gerados automaticamente para você entender seus números.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_welcome3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; min-height: 180px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">📄</div>
            <h4 style="color: #c7d2fe; margin: 0 0 8px 0;">3. Baixe o Relatório</h4>
            <p style="color: #94a3b8; font-size: 0.85rem; line-height: 1.5;">
                Exporte um relatório PDF profissional com todos os dados e gráficos analisados.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("""
    <div class="info-card">
        <h4>🎯 Para quem é o EmpreendeData?</h4>
        <p>
            Criado especialmente para <strong style="color: #c7d2fe;">empreendedores revendedores</strong> — 
            vendedores de perfumaria, cosméticos, chocolates e outros produtos. 
            Uma ferramenta simples e poderosa para transformar suas planilhas de vendas em informações visuais 
            que ajudam a tomar decisões melhores para o seu negócio.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <p class="pulse-hint" style="color: #6366f1; font-weight: 600; font-size: 1rem;">
            👈 Use a barra lateral para enviar sua planilha ou carregar dados de exemplo
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    # ===== DASHBOARD COM DADOS =====
    numericas, categoricas, datas = detectar_colunas(df)

    # Header
    st.markdown("""
    <div class="hero-title" style="font-size: 1.8rem;">📊 EmpreendeData</div>
    <div class="hero-subtitle">Análise dos seus dados • {n} registros • {c} colunas</div>
    """.format(n=len(df), c=len(df.columns)), unsafe_allow_html=True)

    st.markdown("")

    # ===== TABS =====
    tab_dashboard, tab_tabela, tab_relatorio, tab_sobre = st.tabs([
        "📊 Dashboard", "📋 Tabela de Dados", "📄 Relatório PDF", "ℹ️ Sobre o Projeto"
    ])

    # Armazenar figuras para o PDF
    fig_barras_pdf = None
    fig_pizza_pdf = None
    fig_treemap_pdf = None

    # =====================================================
    # TAB 1: DASHBOARD
    # =====================================================
    with tab_dashboard:
        st.markdown("")

        # --- KPIs ---
        if numericas:
            st.markdown("#### 🎯 Indicadores Principais")
            num_kpis = min(len(numericas), 4)
            kpi_cols = st.columns(num_kpis + 1)

            # Total de registros
            kpi_cols[0].metric(
                label="📋 Registros",
                value=formatar_numero(len(df)),
                help="Total de linhas na planilha"
            )

            for i, col_num in enumerate(numericas[:4]):
                total = df[col_num].sum()
                media = df[col_num].mean()

                kpi_cols[i + 1].metric(
                    label=f"💰 {col_num}",
                    value=formatar_valor(total) if total > 100 else formatar_numero(total),
                    delta=f"Média: {media:,.2f}",
                    help=f"Soma total e média de {col_num}"
                )

            st.markdown("")
            st.divider()

        # --- GRÁFICOS ---
        st.markdown("#### 📈 Visualizações")
        st.markdown("")

        # Gráfico 1 e 2 lado a lado
        chart_col1, chart_col2 = st.columns(2)

        # GRÁFICO DE BARRAS
        if categoricas and numericas:
            with chart_col1:
                with st.container(border=True):
                    cat_col = categoricas[0]
                    num_col = numericas[0]

                    df_agrupado = df.groupby(cat_col)[num_col].sum().reset_index()
                    df_agrupado = df_agrupado.sort_values(num_col, ascending=True)

                    fig_barras = px.bar(
                        df_agrupado, x=num_col, y=cat_col,
                        orientation='h',
                        title=f"Soma de {num_col} por {cat_col}",
                        color=num_col,
                        color_continuous_scale=['#312e81', '#6366f1', '#818cf8', '#c7d2fe'],
                        text_auto='.2s'
                    )
                    fig_barras.update_layout(**PLOTLY_LAYOUT)
                    fig_barras.update_layout(
                        height=400,
                        showlegend=False,
                        coloraxis_showscale=False,
                        title_font=dict(size=16, color='#c7d2fe'),
                        xaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.1)'),
                        yaxis=dict(showgrid=False),
                    )
                    fig_barras.update_traces(
                        textposition='outside',
                        textfont=dict(color='#c7d2fe', size=11),
                        marker_line_width=0,
                    )
                    st.plotly_chart(fig_barras, use_container_width=True, key="chart_barras")
                    fig_barras_pdf = fig_barras

        # GRÁFICO DE ROSCA/DONUT
        if categoricas:
            with chart_col2:
                with st.container(border=True):
                    cat_col_pizza = categoricas[0]

                    df_contagem = df[cat_col_pizza].value_counts().reset_index()
                    df_contagem.columns = [cat_col_pizza, 'Contagem']

                    fig_pizza = px.pie(
                        df_contagem,
                        names=cat_col_pizza,
                        values='Contagem',
                        title=f"Distribuição por {cat_col_pizza}",
                        hole=0.45,
                        color_discrete_sequence=CHART_COLORS
                    )
                    fig_pizza.update_layout(**PLOTLY_LAYOUT)
                    fig_pizza.update_layout(
                        height=400,
                        title_font=dict(size=16, color='#c7d2fe'),
                    )
                    fig_pizza.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        textfont=dict(size=11, color='white'),
                        marker=dict(line=dict(color='#0f172a', width=2)),
                    )
                    st.plotly_chart(fig_pizza, use_container_width=True, key="chart_pizza")
                    fig_pizza_pdf = fig_pizza

        st.markdown("")

        # Gráfico 3 e 4 lado a lado
        chart_col3, chart_col4 = st.columns(2)

        # GRÁFICO TREEMAP
        if categoricas and numericas:
            with chart_col3:
                with st.container(border=True):
                    cat_col = categoricas[0]
                    num_col = numericas[0]

                    df_tree = df.groupby(cat_col)[num_col].sum().reset_index()

                    fig_treemap = px.treemap(
                        df_tree,
                        path=[cat_col],
                        values=num_col,
                        title=f"Mapa de Categorias — {num_col} por {cat_col}",
                        color=num_col,
                        color_continuous_scale=['#1e1b4b', '#4338ca', '#6366f1', '#818cf8', '#c7d2fe'],
                    )
                    fig_treemap.update_layout(**PLOTLY_LAYOUT)
                    fig_treemap.update_layout(
                        height=400,
                        title_font=dict(size=16, color='#c7d2fe'),
                        coloraxis_showscale=False,
                    )
                    fig_treemap.update_traces(
                        textinfo="label+value+percent root",
                        textfont=dict(size=13, color='white'),
                        marker_line_width=2,
                        marker_line_color='#0f172a',
                    )
                    st.plotly_chart(fig_treemap, use_container_width=True, key="chart_treemap")
                    fig_treemap_pdf = fig_treemap

        # GRÁFICO EXTRA: Se houver mais de uma coluna numérica e uma categórica
        if categoricas and len(numericas) >= 2:
            with chart_col4:
                with st.container(border=True):
                    cat_col = categoricas[0]
                    num_col2 = numericas[1]

                    df_scatter = df.copy()

                    fig_scatter = px.scatter(
                        df_scatter,
                        x=numericas[0],
                        y=num_col2,
                        color=cat_col if categoricas else None,
                        title=f"Relação: {numericas[0]} vs {num_col2}",
                        color_discrete_sequence=CHART_COLORS,
                        size=numericas[0],
                        size_max=20,
                    )
                    fig_scatter.update_layout(**PLOTLY_LAYOUT)
                    fig_scatter.update_layout(
                        height=400,
                        title_font=dict(size=16, color='#c7d2fe'),
                        xaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.1)'),
                        yaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.1)'),
                    )
                    fig_scatter.update_traces(
                        marker=dict(line=dict(color='#0f172a', width=1)),
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True, key="chart_scatter")

        elif len(numericas) >= 1:
            with chart_col4:
                with st.container(border=True):
                    num_col = numericas[0]

                    fig_hist = px.histogram(
                        df, x=num_col,
                        title=f"Distribuição de {num_col}",
                        color_discrete_sequence=['#6366f1'],
                        nbins=15,
                    )
                    fig_hist.update_layout(**PLOTLY_LAYOUT)
                    fig_hist.update_layout(
                        height=400,
                        title_font=dict(size=16, color='#c7d2fe'),
                        xaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.1)'),
                        yaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.1)'),
                        bargap=0.05,
                    )
                    fig_hist.update_traces(
                        marker_line_width=1,
                        marker_line_color='#0f172a',
                    )
                    st.plotly_chart(fig_hist, use_container_width=True, key="chart_hist")

        # --- Gráfico temporal se houver coluna de data ---
        if datas and numericas:
            st.markdown("")
            with st.container(border=True):
                data_col = datas[0]
                num_col = numericas[0]

                df_temporal = df.copy()
                df_temporal[data_col] = pd.to_datetime(df_temporal[data_col], format='mixed', dayfirst=True)
                df_temporal = df_temporal.sort_values(data_col)

                fig_linha = px.area(
                    df_temporal, x=data_col, y=num_col,
                    title=f"📅 Evolução Temporal — {num_col} ao longo do tempo",
                    color_discrete_sequence=['#6366f1'],
                )
                fig_linha.update_layout(**PLOTLY_LAYOUT)
                fig_linha.update_layout(
                    height=350,
                    title_font=dict(size=16, color='#c7d2fe'),
                    xaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.07)'),
                    yaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.07)'),
                )
                fig_linha.update_traces(
                    fill='tozeroy',
                    fillcolor='rgba(99,102,241,0.15)',
                    line=dict(width=3, color='#6366f1'),
                )
                st.plotly_chart(fig_linha, use_container_width=True, key="chart_temporal")

        if not categoricas and not numericas:
            st.warning("⚠️ A planilha não possui colunas numéricas ou categóricas suficientes para gerar gráficos.")


    # =====================================================
    # TAB 2: TABELA DE DADOS
    # =====================================================
    with tab_tabela:
        st.markdown("")
        st.markdown("#### 📋 Visualização Completa dos Dados")
        st.markdown("")

        # Filtros
        if categoricas:
            with st.expander("🔍 Filtros", expanded=False):
                filtro_cols = st.columns(min(len(categoricas), 3))
                filtros_ativos = {}
                for i, cat in enumerate(categoricas[:3]):
                    with filtro_cols[i]:
                        opcoes = ['Todos'] + df[cat].unique().tolist()
                        selecionado = st.selectbox(f"Filtrar por {cat}", opcoes, key=f"filtro_{cat}")
                        if selecionado != 'Todos':
                            filtros_ativos[cat] = selecionado

                df_filtrado = df.copy()
                for col_filtro, valor in filtros_ativos.items():
                    df_filtrado = df_filtrado[df_filtrado[col_filtro] == valor]
        else:
            df_filtrado = df.copy()

        # Tabela de dados
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            height=450,
        )

        st.markdown("")

        # Estatísticas descritivas
        if numericas:
            st.markdown("#### 📊 Estatísticas Descritivas")
            st.markdown("")

            stats_cols = st.columns(min(len(numericas), 4))
            for i, col_num in enumerate(numericas[:4]):
                with stats_cols[i]:
                    with st.container(border=True):
                        st.markdown(f"**{col_num}**")
                        st.markdown(f"""
                        | Métrica | Valor |
                        |---------|-------|
                        | **Soma** | {df_filtrado[col_num].sum():,.2f} |
                        | **Média** | {df_filtrado[col_num].mean():,.2f} |
                        | **Mediana** | {df_filtrado[col_num].median():,.2f} |
                        | **Mín** | {df_filtrado[col_num].min():,.2f} |
                        | **Máx** | {df_filtrado[col_num].max():,.2f} |
                        | **Desvio** | {df_filtrado[col_num].std():,.2f} |
                        """)

        # Download CSV
        st.markdown("")
        csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados Filtrados (CSV)",
            data=csv_data,
            file_name=f"dados_filtrados_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )


    # =====================================================
    # TAB 3: RELATÓRIO PDF
    # =====================================================
    with tab_relatorio:
        st.markdown("")
        st.markdown("#### 📄 Geração de Relatório PDF")
        st.markdown("")

        st.markdown("""
        <div class="info-card">
            <h4>📑 O que está incluído no relatório?</h4>
            <p>
                O PDF gerado contém: indicadores principais (KPIs), gráficos de barras, 
                distribuição e treemap renderizados como imagens, além de uma tabela completa 
                dos dados. Tudo formatado com a identidade visual do EmpreendeData.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Preview dos KPIs que irão no PDF
        kpis_pdf = {"Total de Registros": str(len(df))}
        if numericas:
            for col_num in numericas[:3]:
                kpis_pdf[f"Soma de {col_num}"] = f"{df[col_num].sum():,.2f}"
                kpis_pdf[f"Média de {col_num}"] = f"{df[col_num].mean():,.2f}"

        if categoricas:
            kpis_pdf["Categorias Encontradas"] = ", ".join(categoricas[:3])

        with st.container(border=True):
            st.markdown("##### 👁️ Pré-visualização do Conteúdo")
            st.markdown("")
            for label, value in kpis_pdf.items():
                st.markdown(f"- **{label}**: `{value}`")

        st.markdown("")

        # Botão de gerar e baixar
        col_pdf1, col_pdf2, col_pdf3 = st.columns([1, 2, 1])
        with col_pdf2:
            try:
                pdf_bytes = gerar_pdf(df, kpis_pdf, fig_barras_pdf, fig_pizza_pdf, fig_treemap_pdf)

                st.download_button(
                    label="📄 Gerar e Baixar Relatório PDF",
                    data=pdf_bytes,
                    file_name=f"EmpreendeData_Relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

                st.markdown("""
                <div style="text-align: center; margin-top: 12px;">
                    <span style="color: #10b981; font-size: 0.85rem;">
                        ✅ Relatório pronto para download!
                    </span>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
                st.info("💡 Certifique-se de que as bibliotecas `fpdf2` e `kaleido` estão instaladas.")


    # =====================================================
    # TAB 4: SOBRE O PROJETO
    # =====================================================
    with tab_sobre:
        st.markdown("")

        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 3.5rem; margin-bottom: 12px;">🎓</div>
            <div class="hero-title" style="font-size: 1.6rem;">Projeto de Extensão</div>
            <div class="hero-subtitle">Sistemas de Informação e Sociedade</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        col_sobre1, col_sobre2 = st.columns(2)

        with col_sobre1:
            with st.container(border=True):
                st.markdown("##### 🎯 Objetivo do Projeto")
                st.markdown("""
                O **EmpreendeData** é uma aplicação web desenvolvida como atividade de extensão 
                universitária com o objetivo de **democratizar o acesso à análise de dados** 
                para empreendedores revendedores da comunidade local.

                A ferramenta permite que pessoas sem conhecimento técnico em programação ou 
                estatística possam visualizar e compreender seus dados de vendas, identificar 
                padrões e tomar decisões mais informadas para seus negócios.
                """)

            with st.container(border=True):
                st.markdown("##### 👥 Público-Alvo")
                st.markdown("""
                - **Revendedores autônomos** de produtos (perfumaria, cosméticos, chocolates)
                - **Microempreendedores individuais (MEIs)** que controlam vendas por planilhas
                - **Pequenos comerciantes** que precisam visualizar dados financeiros de forma simples
                - **Membros da comunidade local** interessados em tecnologia aplicada a negócios
                """)

        with col_sobre2:
            with st.container(border=True):
                st.markdown("##### 💡 Funcionalidades")
                st.markdown("""
                - 📥 **Upload inteligente** de planilhas CSV e Excel
                - 📊 **Dashboard interativo** com gráficos automáticos
                - 🎯 **KPIs calculados** automaticamente dos seus dados
                - 📈 **4+ tipos de gráficos**: barras, rosca, treemap, dispersão, histograma, temporal
                - 🔍 **Filtros dinâmicos** para explorar os dados
                - 📋 **Estatísticas descritivas** completas
                - 📄 **Relatório PDF** exportável com gráficos e dados
                """)

            with st.container(border=True):
                st.markdown("##### 🏫 Informações Acadêmicas")
                st.markdown("""
                | | |
                |---|---|
                | **Instituição** | Estácio (UNESA) |
                | **Curso** | Análise e Desenvolvimento de Sistemas (ADS) |
                | **Disciplina** | Sistemas de Informação e Sociedade |
                | **Atividade** | Extensão Universitária |
                | **Desenvolvedor** | James Soares Costa |
                | **Tecnologias** | Python, Streamlit, Plotly, Pandas, FPDF2 |
                """)

        st.markdown("")

        st.markdown("""
        <div class="info-card">
            <h4>🌍 Impacto Social</h4>
            <p>
                Este projeto busca reduzir a distância entre a tecnologia de análise de dados e os 
                pequenos empreendedores revendedores da comunidade. Muitos desses profissionais utilizam 
                planilhas simples para controlar suas vendas, mas não possuem acesso a ferramentas que 
                transformem esses dados em informações visuais e acionáveis. O EmpreendeData preenche 
                essa lacuna de forma gratuita, intuitiva e acessível.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="color: #64748b; font-size: 0.8rem;">
                Desenvolvido com ❤️ por <strong style="color: #c7d2fe;">James Soares Costa</strong>
                <br>
                Estácio (UNESA) — Análise e Desenvolvimento de Sistemas — 2025
            </div>
        </div>
        """, unsafe_allow_html=True)