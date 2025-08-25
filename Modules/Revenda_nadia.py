import pandas as pd
import numpy as np
import streamlit as st
from Functions.func_revenda import *
import io
import xlsxwriter
import re

# --- CORES ---
COR_BASE = "#7E57C2"
COR_CLARA = "#ede7f6"
COR_TEXTO = "#fff"
COR_SECUNDARIA = "#5E35B1"

# --- TEMA E ESTILO ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {COR_BASE};
    }}
    .stTextInput > div > div > input {{
        background-color: {COR_CLARA};
        color: {COR_BASE};
        border-radius: 8px;
        border: 1px solid {COR_BASE};
    }}
    .stButton > button {{
        background-color: {COR_SECUNDARIA};
        color: {COR_TEXTO};
        border-radius: 8px;
        border: none;
        font-weight: bold;
        font-size: 18px;
        padding: 10px 24px;
        margin-top: 10px;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: {COR_BASE};
        transform: scale(1.05);
    }}
    .stFileUploader > div {{
        background-color: {COR_CLARA};
        border-radius: 8px;
        border: 1px solid {COR_BASE};
    }}
    .dataframe {{
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {COR_TEXTO};
        font-family: 'Arial', sans-serif;
    }}
    .warning {{
        background-color: #ffecb3;
        color: #7e57c2;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }}
    .success {{
        background-color: #c8e6c9;
        color: #2e7d32;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }}
    .download-btn {{
        background-color: #4caf50 !important;
    }}
    .download-btn:hover {{
        background-color: #388e3c !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- TÍTULO APENAS ---
st.markdown(
    """
    <h1 style="color: #fff; margin: 0; text-align: center; padding: 10px 0 20px 0;">
    Ranking de Revenda - Responsável Técnica 🏆
    </h1>
    """,
    unsafe_allow_html=True
)

# --- INPUTS ---
st.markdown("### 📋 Preencha os dados abaixo:")

col1, col2, col3 = st.columns(3)
with col1:
    vmb = st.file_uploader(
        "Venda Mensal Bruta 💵 (Excel):",
        type=["xlsx"],
        accept_multiple_files=False,
        help="Faça upload do arquivo Excel com os dados de vendas"
    )
with col2:
    mes = st.text_input("Digite o mês (por Extenso):", placeholder="Ex: Janeiro")
with col3:
    ano = st.text_input("Digite o ano:", placeholder="Ex: 2023")

# Adicionar um separador visual
st.markdown("---")

if vmb and mes and ano:
    calcular = st.button("Calcular Ranking 🔝", use_container_width=True)
    
    if calcular:
        with st.spinner('Processando dados... Aguarde!'):
            try:
                ranking = calcular_ranking_revenda(vmb)
                
                # Exibir sucesso
                st.markdown(
                    f'<div class="success"><b>✅ Ranking calculado com sucesso para {mes} de {ano}!</b></div>', 
                    unsafe_allow_html=True
                )
                
                # Exibir dataframe com formatação
                st.markdown("### 📊 Resultado do Ranking")
                st.dataframe(
                    ranking,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Adicionar métricas rápidas no topo
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Avaliadoras", len(ranking))
                with col2:
                    st.metric("Valor Total", f"R$ {ranking['Valor líquido'].sum():,.2f}")
                with col3:
                    top_avaliadora = ranking.iloc[0]['avaliadora_padronizada']
                    st.metric("Top Avaliadora", top_avaliadora.split()[0] + "...")
                
                # Preparar dados para download
                excel_data = to_excel(ranking)
                
                # Botão de download
                st.download_button(
                    label="📥 Baixar Ranking em Excel",
                    data=excel_data,
                    file_name=f"ranking_revenda_{mes}_{ano}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key='download-excel'
                )
                
            except Exception as e:
                st.error(f"Ocorreu um erro ao processar o arquivo: {str(e)}")

else: 
    st.markdown(
        '<div class="warning"><b>⚠️ Por Favor, Preencha todos os Campos!</b></div>', 
        unsafe_allow_html=True
    )

# Adicionar informações de uso (menos proeminente)
with st.expander("ℹ️ Instruções de uso"):
    st.markdown("""
    1. **Faça upload** do arquivo Excel com os dados de vendas
    2. **Informe** o mês e ano de referência
    3. **Clique** em 'Calcular Ranking' para processar os dados
    4. **Visualize** o ranking gerado
    5. **Baixe** o resultado em formato Excel se desejar
    
    **Observação:** O processamento considera apenas orçamentos com status 'Finalizado' e exclui a unidade 'PRAIA GRANDE'.
    """)

# Adicionar rodapé discreto
st.markdown("---")
st.markdown(
    f'<div style="text-align: center; color: {COR_TEXTO}; opacity: 0.7; font-size: 0.8rem;">'
    'Desenvolvido para análise de desempenho de revenda</div>',
    unsafe_allow_html=True
)