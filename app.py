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

# Title
st.title("Cálculo de Comissão - Recurosos Humanos")

# Upload dos Xlsx Bases
uploaded_files = st.file_uploader(
    "Carregue os arquivos Excel (.xlsx) com as bases de dados",
    type=["xlsx"],
    accept_multiple_files=True
)