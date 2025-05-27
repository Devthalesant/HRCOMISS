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


col1, col2, col3 = st.columns(3)
with col1:
    # Upload dos Xlsx Bases
    vmb = st.file_uploader(
        "**<span style='font-size:18px;'>Carregue o arquivo de Vendas Mensais Brutas -💵 em excel:</span>**",
        type=["xlsx"],
        accept_multiple_files=False,
        key="vmb",
        label_visibility="visible"
    )
with col2:
    # Upload dos Xlsx Bases
    venda_x_pgto = st.file_uploader(
        "**<span style='font-size:18px;'>Carregue o arquivo de Venda X Forma de PGTO -💳 em excel:</span>**",
        type=["xlsx"],
        accept_multiple_files=False,
        key="venda_x_pgto",
        label_visibility="visible"
    )
with col3:
    # Upload dos Xlsx Bases
    arquivo_principal_path = st.file_uploader(
        "**<span style='font-size:18px;'>Carregue o arquivo com as demais informações -⚡⬆️ Metas em excel:</span>**",
        type=["xlsx"],
        accept_multiple_files=False,
        key="arquivo_principal_path",
        label_visibility="visible"
    )
    # Aplica o markdown para permitir HTML no label
    st.markdown(
        """
        <style>
        .stFileUploader label span {
            font-weight: bold !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )