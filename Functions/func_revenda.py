import pandas as pd
import numpy as np
import streamlit as st
import io
import xlsxwriter
import re


def calcular_ranking_revenda(base):
    base = pd.read_excel(base)

    base_columns = ['ID orçamento', 'Data orçamento', 'Status', 'Revenda', 'Data venda','Mês venda', 'Unidade','Avaliador', 'Valor líquido','ID cliente']

    base = base[base_columns]

    base = base.loc[base['Status'] == "Finalizado"]

    base = base.loc[~base['Avaliador'].isna()]

    base['Valor líquido'] = base['Valor líquido'].fillna(0)

    base = base.loc[base['Unidade'] != 'PRAIA GRANDE']

    personais = [
    "Natali de Souza Oliveira",
    "Julia Macena Dantas",
    "Paloma Santos Linhares",
    "Amanda Santos Amorim",
    "Tamires Regina De A. Dos Santos",
    "Nathalia Ranciaro Calabrez",
    "Karine Oliveira Santos",
    "Gabriela Gomes Magalhaes dos Anjos",
    "Eloiza Karyna Zonho"
    ]

    mask = ~base['Avaliador'].str.contains('|'.join(personais), case=False, na=False)
    base = base.loc[mask]

    base = base.loc[~base['Avaliador'].str.contains("AVAL",case=False)]

    def remover_parenteses(nome):
        return re.sub(r'\s*\(.*\)', '', nome).strip()

    base['avaliadora_padronizada'] = base['Avaliador'].apply(remover_parenteses)

    base['avaliadora_padronizada'] = base['avaliadora_padronizada'].replace("AMANDA SOUZA FAIOLI GRU","AMANDA SOUZA FAIOLI")

    base['avaliadora_padronizada'] = base['avaliadora_padronizada'].str.upper()

    groupby_revenda = base.groupby(['avaliadora_padronizada']).agg({"Unidade" : 'unique','Valor líquido' : 'sum'}).reset_index()

    groupby_revenda = groupby_revenda.sort_values(by=['Valor líquido'],ascending=False).reset_index(drop=True)

    return groupby_revenda

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Ranking_Revenda')
        workbook = writer.book
        worksheet = writer.sheets['Ranking_Revenda']
        
        format_header = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#7E57C2',
            'font_color': 'white',
            'border': 1
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, format_header)
            
        for idx, col in enumerate(df.columns):
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),
                len(str(series.name))
            )) + 2
            worksheet.set_column(idx, idx, max_len)
            
    processed_data = output.getvalue()
    return processed_data