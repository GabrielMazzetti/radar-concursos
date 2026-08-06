import streamlit as st
import pandas as pd
import sqlite3
import os
import sys
import re

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

st.set_page_config(page_title="Concurso Radar Dashboard", page_icon="📊", layout="wide")

def load_data():
    db_path = config.DB_PATH
    if not os.path.exists(db_path):
        return pd.DataFrame()
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM concursos", conn)
    conn.close()
    return df

def clean_salary(salary_str):
    if not salary_str: return 0.0
    try:
        # Extract numeric value like "R$ 10.685,44" -> 10685.44
        numeric = re.sub(r'[^\d,]', '', salary_str).replace(',', '.')
        return float(numeric) if numeric else 0.0
    except:
        return 0.0

st.title("🎯 Concurso Radar - Dashboard")
st.markdown("Monitoramento de concursos para **Estatísticos**")

df = load_data()

if df.empty:
    st.warning("Nenhum dado encontrado no banco de dados. Execute o `main.py` primeiro.")
else:
    # Pre-processing
    df['valor_salario'] = df['salario'].apply(clean_salary)
    df['data'] = pd.to_datetime(df['data'])
    
    # Sidebar Filters
    st.sidebar.header("Filtros")
    search = st.sidebar.text_input("Buscar por órgão ou cargo")
    min_salary = st.sidebar.slider("Salário Mínimo", 0, 30000, 0, step=1000)
    min_score = st.sidebar.slider("Score Mínimo", 0, 150, 0)
    
    # Apply Filters
    filtered_df = df[df['valor_salario'] >= min_salary]
    filtered_df = filtered_df[filtered_df['score'] >= min_score]
    if search:
        filtered_df = filtered_df[
            filtered_df['orgao'].str.contains(search, case=False) | 
            filtered_df['cargo'].str.contains(search, case=False)
        ]

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Concursos", len(df))
    with col2:
        last_7_days = len(df[df['data'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))])
        st.metric("Novos (7 dias)", last_7_days)
    with col3:
        avg_salary = df[df['valor_salario'] > 0]['valor_salario'].mean()
        st.metric("Média Salarial", f"R$ {avg_salary:,.2f}")
    with col4:
        top_org = df['orgao'].mode()[0] if not df['orgao'].empty else "N/A"
        st.metric("Órgão + Frequente", top_org[:15])

    # Charts
    st.subheader("Visualizações")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("### Distribuição de Scores")
        st.bar_chart(df['score'].value_counts())
        
    with c2:
        st.write("### Top 10 Órgãos por Vagas/Menções")
        st.bar_chart(df['orgao'].value_counts().head(10))

    # Data Table
    st.subheader("Lista de Concursos Encontrados")
    
    # Format table for display
    display_df = filtered_df[['score', 'orgao', 'cargo', 'salario', 'cidade', 'inscricao', 'link']].copy()
    display_df = display_df.sort_values(by='score', ascending=False)
    
    st.dataframe(
        display_df,
        column_config={
            "link": st.column_config.LinkColumn("Link do Edital"),
            "score": st.column_config.NumberColumn("Score ⭐", format="%d")
        },
        hide_index=True,
        use_container_width=True
    )

st.sidebar.markdown("---")
st.sidebar.info("Projeto Concurso Radar MVP - Desenvolvido para Estatísticos.")
