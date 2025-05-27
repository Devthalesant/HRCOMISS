import pandas as pd
import numpy as np
import streamlit as st
from func import *

# Set page configuration
st.set_page_config(
    page_title="Cálculo de Comissão - Recurosos Humanos",
    page_icon="💰",
    layout="wide"
)
# Definição do tema
st.markdown(
    """
    <style>
    .stApp {
        background-color: #b39ddb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Cálculo de Comissão - Recursos Humanos 💰")

# pedir ao usuário para inputar o mês por escrito e ano:

mes = st.text_input("Digite o mês (por Extenso):")
ano = st.text_input("Digite o ano:")


col1, col2, col3 = st.columns(3)
with col1:
    # Upload dos Xlsx Bases
    vmb = st.file_uploader(
        "Carregue o arquivo de Vendas Mensais Brutas -💵 em excel:",
        type=["xlsx"],
        accept_multiple_files=False
    )
with col2:
    # Upload dos Xlsx Bases
    venda_x_pgto = st.file_uploader(
        "Carregue o arquivo de Venda X Forma de PGTO -💳 em excel:",
        type=["xlsx"],
        accept_multiple_files=False
    )
with col3:
    # Upload dos Xlsx Bases
    arquivo_principal_path = st.file_uploader(
        "Carregue o arquivo com as demais informações -⚡⬆️ Metas em excel:",
        type=["xlsx"],
        accept_multiple_files=False
    )

# Verifica se os arquivos foram carregados
if vmb and venda_x_pgto and arquivo_principal_path and arquivo_principal_path is not None:
    # Lê os arquivos Excel
    vmb_path_exib = pd.read_excel(vmb)
    venda_x_pgto_exib = pd.read_excel(venda_x_pgto)
    arquivo_principal_path_exib = pd.read_excel(arquivo_principal_path)

    # Exibe os DataFrames carregados
    st.subheader("Vendas Mensais Brutas - 💵")
    st.dataframe(vmb_path_exib)
    st.subheader("Venda X Forma de PGTO - 💳")
    st.dataframe(venda_x_pgto_exib)
    st.subheader("Arquivo Principal - ⚡⬆️ Metas")
    st.dataframe(arquivo_principal_path_exib)

    #fala pra o usuário verificar os arquivos e aprtar o botão se estiver tudo ok:

    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <button style="padding: 10px 20px; font-size: 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;">
                Verifique os arquivos e clique em Calcular Comissão se estiver tudo certo! ✅
            </button>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Botão para calcular a comissão
    if st.button("Calcular Comissão"):
        with st.spinner("Calculando comissão, por favor aguarde..."):
            # Chama a função para calcular a comissão
            resultado_vendedoras, resultado_personais = Comission_calculator(vmb, venda_x_pgto, arquivo_principal_path,mes,ano)
        st.subheader("Comissão das Vendedoras")
        st.dataframe(resultado_vendedoras)
        st.subheader("Comissão das Personais")
        st.dataframe(resultado_personais)
