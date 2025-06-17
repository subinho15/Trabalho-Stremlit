import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from PIL import Image
import base64
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="CEUB CPA - Painel de Avaliação",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para aplicar a identidade visual
st.markdown("""
<style>
    /* Cores principais baseadas na identidade visual */
    :root {
        --primary-purple: #5B2C6F;
        --primary-pink: #E91E63;
        --light-purple: #8E44AD;
        --background-light: #F8F9FA;
        --text-dark: #2C3E50;
    }
    
    /* Estilo do header */
    .main-header {
        background: linear-gradient(90deg, var(--primary-purple) 0%, var(--primary-pink) 100%);
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        border-radius: 0 0 10px 10px;
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .logo-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        gap: 15px;
        color: white;
    }
    
    .nav-buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    
    .nav-button {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.3);
        text-decoration: none;
        color: white;
    }
    
    .nav-button.active {
        background: white;
        color: var(--primary-purple);
    }
    
    /* Estilo da sidebar */
    .css-1d391kg {
        background-color: var(--background-light);
    }
    
    /* Estilo dos filtros */
    .filter-section {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .filter-title {
        color: var(--primary-purple);
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    /* Estilo dos KPIs */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        flex: 1;
        border-left: 4px solid var(--primary-purple);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary-purple);
        margin-bottom: 0.5rem;
    }
    
    .kpi-label {
        color: var(--text-dark);
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Estilo das tabelas */
    .dataframe {
        border: none !important;
    }
    
    .dataframe th {
        background-color: var(--primary-purple) !important;
        color: white !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    .dataframe td {
        text-align: center !important;
        padding: 8px !important;
    }
    
    /* Rodapé */
    .footer {
        margin-top: 3rem;
        padding: 1rem;
        text-align: center;
        color: #666;
        border-top: 1px solid #eee;
        font-size: 0.9rem;
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .header-content {
            flex-direction: column;
            gap: 10px;
        }
        
        .kpi-container {
            flex-direction: column;
        }
        
        .nav-buttons {
            flex-wrap: wrap;
        }
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Carrega os dados do arquivo Excel"""
    try:
        df = pd.read_excel("/home/ubuntu/upload/CEUB_export-data-desafio-pbi.xlsx")
        # Converter \'Faixa MGA\' para numérico, tratando erros
        df[\'Faixa MGA\'] = pd.to_numeric(df[\'Faixa MGA\'], errors=\'coerce\')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

def create_header():
    """Cria o cabeçalho do painel"""
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo-text">CEUB | CPA</div>
            </div>
            <div class="user-info">
                <span>👤 gabriel.teixeira</span>
            </div>
        </div>
        <div class="nav-buttons">
            <a href="#" class="nav-button active">📅 Período Letivo</a>
            <a href="#" class="nav-button">📚 Disciplina</a>
            <a href="#" class="nav-button">👨‍🏫 Docente</a>
            <a href="#" class="nav-button">🎓 Curso</a>
            <a href="#" class="nav-button">📋 Instrumento</a>
            <a href="#" class="nav-button">📊 Gráficos</a>
            <a href="#" class="nav-button">↩️ Voltar</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar_filters(df):
    """Cria os filtros na sidebar"""
    st.sidebar.markdown("<div class=\"filter-section\">", unsafe_allow_html=True)
    st.sidebar.markdown("<div class=\"filter-title\">Modalidade</div>", unsafe_allow_html=True)
    modalidade = st.sidebar.selectbox("", ["Todos"] + list(df["EnsinoModalidade"].unique()), key="modalidade")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class=\"filter-section\">", unsafe_allow_html=True)
    st.sidebar.markdown("<div class=\"filter-title\">Período Letivo</div>", unsafe_allow_html=True)
    periodo_letivo = st.sidebar.selectbox("", ["Todos"] + list(df["Período Letivo"].unique()), key="periodo")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class=\"filter-section\">", unsafe_allow_html=True)
    st.sidebar.markdown("<div class=\"filter-title\">Campus</div>", unsafe_allow_html=True)
    campus = st.sidebar.selectbox("", ["Todos"] + list(df["Nome do Campus"].unique()), key="campus")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class=\"filter-section\">", unsafe_allow_html=True)
    st.sidebar.markdown("<div class=\"filter-title\">Faculdade | Curso</div>", unsafe_allow_html=True)
    curso = st.sidebar.selectbox("", ["Todos"] + list(df["Curso"].unique()), key="curso")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class=\"filter-section\">", unsafe_allow_html=True)
    st.sidebar.markdown("<div class=\"filter-title\">Eixo de Formação (EAD)</div>", unsafe_allow_html=True)
    eixo_formacao = st.sidebar.selectbox("", ["Todos"] + list(df["Eixo de Formação"].dropna().unique()), key="eixo")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class=\"filter-section\">", unsafe_allow_html=True)
    st.sidebar.markdown("<div class=\"filter-title\">Instrumento</div>", unsafe_allow_html=True)
    instrumento = st.sidebar.selectbox("", ["Todos"] + list(df["Nome da Avaliação"].unique()), key="instrumento")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class=\"filter-section\">", unsafe_allow_html=True)
    st.sidebar.markdown("<div class=\"filter-title\">Grupo de Questão</div>", unsafe_allow_html=True)
    grupo_questao = st.sidebar.selectbox("", ["Todos"] + list(df["Grupo da Questão"].unique()), key="grupo")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class=\"filter-section\">", unsafe_allow_html=True)
    st.sidebar.markdown("<div class=\"filter-title\">Disciplina</div>", unsafe_allow_html=True)
    disciplina = st.sidebar.selectbox("", ["Todos"] + list(df["Disciplina_Inv"].unique()), key="disciplina")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class=\"filter-section\">", unsafe_allow_html=True)
    st.sidebar.markdown("<div class=\"filter-title\">Docente</div>", unsafe_allow_html=True)
    docente = st.sidebar.selectbox("", ["Todos"] + list(df["Professor"].unique()), key="docente")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    return {
        "modalidade": modalidade,
        "periodo_letivo": periodo_letivo,
        "campus": campus,
        "curso": curso,
        "eixo_formacao": eixo_formacao,
        "instrumento": instrumento,
        "grupo_questao": grupo_questao,
        "disciplina": disciplina,
        "docente": docente
    }

def apply_filters(df, filters):
    """Aplica os filtros selecionados aos dados"""
    filtered_df = df.copy()
    
    if filters["modalidade"] != "Todos":
        filtered_df = filtered_df[filtered_df["EnsinoModalidade"] == filters["modalidade"]]
    
    if filters["periodo_letivo"] != "Todos":
        filtered_df = filtered_df[filtered_df["Período Letivo"] == filters["periodo_letivo"]]
    
    if filters["campus"] != "Todos":
        filtered_df = filtered_df[filtered_df["Nome do Campus"] == filters["campus"]]
    
    if filters["curso"] != "Todos":
        filtered_df = filtered_df[filtered_df["Curso"] == filters["curso"]]
    
    if filters["eixo_formacao"] != "Todos":
        filtered_df = filtered_df[filtered_df["Eixo de Formação"] == filters["eixo_formacao"]]
    
    if filters["instrumento"] != "Todos":
        filtered_df = filtered_df[filtered_df["Nome da Avaliação"] == filters["instrumento"]]
    
    if filters["grupo_questao"] != "Todos":
        filtered_df = filtered_df[filtered_df["Grupo da Questão"] == filters["grupo_questao"]]
    
    if filters["disciplina"] != "Todos":
        filtered_df = filtered_df[filtered_df["Disciplina_Inv"] == filters["disciplina"]]
    
    if filters["docente"] != "Todos":
        filtered_df = filtered_df[filtered_df["Professor"] == filters["docente"]]
    
    return filtered_df

def create_kpis(df):
    """Cria os KPIs principais"""
    amostra = len(df)
    nota_media = df["Peso da Resposta"].mean()
    
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-value">{amostra:,}</div>
            <div class="kpi-label">Amostra</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{nota_media:.2f}</div>
            <div class="kpi-label">Nota Média</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return amostra, nota_media

def create_mga_distribution_chart(df):
    """Cria o gráfico de distribuição da Nota Média por Faixa de MGA"""
    if not df.empty and \'Faixa MGA\' in df.columns:
        # Agrupar por Faixa MGA e calcular a média da Peso da Resposta
        mga_avg = df.groupby(\'Faixa MGA\')[\'Peso da Resposta\'].mean().reset_index()
        mga_avg = mga_avg.sort_values(by=\'Faixa MGA\')

        fig = px.bar(mga_avg, x=\'Faixa MGA\', y=\'Peso da Resposta\',
                     title=\'Nota Média por Faixa de MGA\',
                     labels={\'Faixa MGA\': \'Faixa MGA\', \'Peso da Resposta\': \'Nota Média\'},
                     color_discrete_sequence=[st.get_option("theme.primaryColor")] * len(mga_avg))
        
        fig.update_layout(xaxis_title="Faixa MGA", yaxis_title="Nota Média",
                          xaxis={\'categoryorder\':\'category ascending\'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Não há dados de \'Faixa MGA\' para exibir o gráfico.")

def create_main_table(df):
    """Cria a tabela principal com drill-down (exemplo por Disciplina) """
    st.subheader("Tabela de Desempenho por Disciplina")
    
    if not df.empty:
        # Agrupar por Disciplina e calcular a média
        discipline_avg = df.groupby(\'Disciplina_Inv\')[\'Peso da Resposta\'].mean().reset_index()
        discipline_avg.columns = [\'Disciplina\', \'Nota Média\']
        discipline_avg = discipline_avg.sort_values(by=\'Nota Média\', ascending=False)
        
        st.dataframe(discipline_avg, use_container_width=True)
        
        # Exemplo de drill-down: ao clicar em uma disciplina, mostra detalhes
        st.markdown("**Clique em uma disciplina na tabela acima para ver detalhes (funcionalidade em desenvolvimento)**")
        
    else:
        st.info("Não há dados para exibir a tabela principal.")

def create_footer():
    """Cria o rodapé"""
    st.markdown("""
    <div class="footer">
        ceub.br | Comissão Própria de Avaliação
    </div>
    """, unsafe_allow_html=True)

def main():
    """Função principal do aplicativo"""
    # Criar cabeçalho
    create_header()
    
    # Carregar dados
    df = load_data()
    if df is None:
        st.stop()
    
    # Criar filtros na sidebar
    filters = create_sidebar_filters(df)
    
    # Aplicar filtros
    filtered_df = apply_filters(df, filters)
    
    # Criar KPIs
    amostra, nota_media = create_kpis(filtered_df)
    
    # Área principal de conteúdo
    st.subheader("📊 Visão Geral")
    
    # Nota Média por Faixa de MGA
    create_mga_distribution_chart(filtered_df)
    
    # Tabela Principal
    create_main_table(filtered_df)
    
    # Mostrar dados filtrados (para teste)
    if st.checkbox("Mostrar dados filtrados (para desenvolvimento)"):
        st.dataframe(filtered_df.head(10))
    
    # Criar rodapé
    create_footer()

if __name__ == "__main__":
    main()

