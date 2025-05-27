import pandas as pd
import numpy as np
import streamlit as st
from func import *

# --- CORES ---
COR_BASE = "#7E57C2"  # Lilás escuro
COR_CLARA = "#ede7f6" # Lilás claro
COR_TEXTO = "#fff"    # Branco

# --- LOGO ---

st.image("C:/Users/novo1/OneDrive/Desktop/Dev/hrcomiss/logo.png")

st.markdown(
    """
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <h1 style="color: #fff; margin: 0;">Cálculo de Comissão - Recursos Humanos 💰</h1>
    </div>
    """,
    unsafe_allow_html=True
)

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
        background-color: {COR_BASE};
        color: {COR_TEXTO};
        border-radius: 8px;
        border: none;
        font-weight: bold;
        font-size: 18px;
        padding: 10px 24px;
        margin-top: 10px;
    }}
    .stFileUploader > div {{
        background-color: {COR_CLARA};
        border-radius: 8px;
        border: 1px solid {COR_BASE};
    }}
    .stDataFrame {{
        background-color: {COR_CLARA};
        border-radius: 8px;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {COR_TEXTO};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- INPUTS ---
mes = st.text_input("Digite o mês (por Extenso):")
ano = st.text_input("Digite o ano:")

col1, col2, col3 = st.columns(3)
with col1:
    vmb = st.file_uploader(
        "Vendas Mensais Brutas 💵 (Excel):",
        type=["xlsx"],
        accept_multiple_files=False
    )
with col2:
    venda_x_pgto = st.file_uploader(
        "Venda X Forma de PGTO 💳 (Excel):",
        type=["xlsx"],
        accept_multiple_files=False
    )
with col3:
    arquivo_principal_path = st.file_uploader(
        "Demais Informações⚡(Excel):",
        type=["xlsx"],
        accept_multiple_files=False
    )

if vmb and venda_x_pgto and arquivo_principal_path:
    vmb_path_exib = pd.read_excel(vmb)
    venda_x_pgto_exib = pd.read_excel(venda_x_pgto)
    arquivo_principal_path_exib = pd.read_excel(arquivo_principal_path)

    st.subheader("Vendas Mensais Brutas - 💵")
    st.dataframe(vmb_path_exib)
    st.subheader("Venda X Forma de PGTO - 💳")
    st.dataframe(venda_x_pgto_exib)
    st.subheader("Arquivo Principal - ⚡⬆️ Metas")
    st.dataframe(arquivo_principal_path_exib)

    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 20px;">
            <span style="color: {COR_TEXTO}; font-size: 18px;">
                Verifique os arquivos e clique em <b>Calcular Comissão</b> se estiver tudo certo! ✅
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Calcular Comissão", key="calcular_comissao", help="Clique para calcular a comissão", use_container_width=True):
        with st.spinner("Calculando comissão, por favor aguarde..."):
            resultado_vendedoras, resultado_personais = Comission_calculator(
                vmb, venda_x_pgto, arquivo_principal_path, mes, ano
            )
        st.subheader("Comissão das Vendedoras")
        st.dataframe(resultado_vendedoras)
        st.subheader("Comissão das Personais")
        st.dataframe(resultado_personais)
