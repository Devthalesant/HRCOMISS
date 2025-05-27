import pandas as pd
import numpy as np

# Função para tratar a base de VMB

def Treating_VMB(vmb_path):
  # Importando a base
  vmb = pd.read_excel(vmb_path)

  # Colunas úteis
  vmb_columns = ['ID orçamento','Status','Data venda','Mês venda',
                'Unidade', 'Consultor','Valor líquido']

  vmb = vmb[vmb_columns]

  # Filtrando o Status e unidades
  vmb = vmb.loc[vmb["Status"] == "Finalizado"]

  # Tirando Praia Grande
  vmb = vmb.loc[vmb["Unidade"] != "PRAIA GRANDE"]

  # Tirando Linhas duplicadas (O valor do orçamento fica somente na primeira linha do orçamneto)
  vmb = vmb.drop_duplicates(subset='ID orçamento', keep='first')

  # trocando NaN por zero
  vmb = vmb.fillna(0)

  # Tratando as Datas
  vmb["Data venda"] = pd.to_datetime(vmb["Data venda"])

  vmb["Ano Venda"] = vmb["Data venda"].dt.year

  vmb["Data venda formatada"] = vmb["Data venda"].dt.strftime('%d/%m/%Y')

  vmb = vmb.drop(columns=["Data venda"])

  vmb = vmb.rename(columns={"Data venda formatada": "Data venda"})

  # Coluna mês/ano
  vmb["Mês/Ano"] = vmb["Mês venda"].astype(str) + "/" + vmb["Ano Venda"].astype(str)

  # Reorganizando Colunas
  vmb_columns = ['Consultor', 'Mês/Ano','Unidade', 'Valor líquido']

  vmb = vmb[vmb_columns]

  vmb_final = vmb.groupby(["Consultor", "Mês/Ano", "Unidade"]).agg({"Valor líquido": "sum"}).reset_index()

  vmb_final = vmb_final.sort_values(by=["Unidade", "Consultor"])

  return vmb_final

#################################################################################################################################################

# Função para tratar a base de Vendas X forma de Pagamento: 

def Treating_VendaXPgto(venda_x_pgto):
  # Importando a base
  venda_x_pgto = pd.read_excel(venda_x_pgto)

  # Colunas úteis
  venda_x_pgto_columns = ['Status', 'Data venda','Mês venda',
                          'Unidade','Consultor(a)','Valor líquido',
                          'Forma de pagamento', 'Conciliado (sim ou não)']

  venda_x_pgto = venda_x_pgto[venda_x_pgto_columns]

  # Filtrando Unidade, Status e Conciliado:
  venda_x_pgto = venda_x_pgto.loc[venda_x_pgto["Status"] == "Finalizado"]
  venda_x_pgto = venda_x_pgto.loc[venda_x_pgto["Unidade"] != "PRAIA GRANDE"]
  venda_x_pgto = venda_x_pgto.loc[venda_x_pgto["Conciliado (sim ou não)"] == "Sim"]

  venda_x_pgto['Forma de pagamento'].unique()

  formas_de_pgto_validas = ['PIX', 'Cartão de Crédito à Vista','Cartão de Débito',
                            'Dinheiro','Cartão de Crédito à Vista (Link)'
                            'Transferência Bancária', 'Cartão de Crédito Vindi à Vista']

  venda_x_pgto = venda_x_pgto[venda_x_pgto['Forma de pagamento'].isin(formas_de_pgto_validas)]

  # Tratando as Datas
  venda_x_pgto["Data venda"] = pd.to_datetime(venda_x_pgto["Data venda"])

  venda_x_pgto["Ano Venda"] = venda_x_pgto["Data venda"].dt.year

  venda_x_pgto["Data venda formatada"] = venda_x_pgto["Data venda"].dt.strftime('%d/%m/%Y')

  venda_x_pgto = venda_x_pgto.drop(columns=["Data venda"])

  venda_x_pgto = venda_x_pgto.rename(columns={"Data venda formatada": "Data venda"})

  venda_x_pgto = venda_x_pgto.rename(columns={"Valor líquido": "Valor líquido à Vista"})

  venda_x_pgto = venda_x_pgto.rename(columns={"Consultor(a)": "Consultor"})

  # coluna mês/ano
  venda_x_pgto["Mês/Ano"] = venda_x_pgto["Mês venda"].astype(str) + "/" + venda_x_pgto["Ano Venda"].astype(str)

  venda_x_pgto_columns = [ 'Consultor', 'Mês/Ano', 'Unidade','Valor líquido à Vista']

  venda_x_pgto = venda_x_pgto[venda_x_pgto_columns]

  venda_x_pgto = venda_x_pgto.groupby(["Consultor", "Mês/Ano", "Unidade"]).agg({"Valor líquido à Vista": "sum"}).reset_index()

  venda_x_pgto = venda_x_pgto.sort_values(by=["Unidade", "Consultor"])

  return venda_x_pgto

#################################################################################################################################################

def Treating_Garantido_meta_1_mes(arquivo_principal_path):

  # Importando a base
  Garantido_meta_1_mes = pd.read_excel(arquivo_principal_path, sheet_name='Sheet1')

  Garantido_meta_1_mes_columns = ['NOME CRM', 'LOJA', 'META DE VENDAS','Valor do Garantido', 'Primeiro Mês']

  Garantido_meta_1_mes = Garantido_meta_1_mes[Garantido_meta_1_mes_columns]

  Garantido_meta_1_mes.rename(columns={'NOME CRM': 'Consultor', 'LOJA': 'Unidade', 'META DE VENDAS' : 'Meta de Vendas'}, inplace=True)

  Garantido_meta_1_mes = Garantido_meta_1_mes.dropna(subset=['Consultor', 'Unidade'])

  return Garantido_meta_1_mes

#################################################################################################################################################

def treating_vmb_personais(vmb,arquivo_principal_path):
    # Importando a base
  vmb_geral = pd.read_excel(vmb)

  # Importando a base - nome de personais
  listagem_personal = pd.read_excel(arquivo_principal_path, sheet_name='Sheet3')

  lista_nomes_personais = listagem_personal["Personais"].dropna().unique()

  lista_nomes_personais = list(listagem_personal["Personais"])

  # colunas úteis
  vmb_personal_columns = ['ID orçamento','Status', 'Data venda','Mês venda',
                          'Unidade', 'Avaliador','Valor líquido']

  vmb_personal = vmb_geral[vmb_personal_columns]

  # Filtrando o Status e unidades
  vmb_personal = vmb_personal.loc[vmb_personal["Status"] == "Finalizado"]

  # Tirando Linhas duplicadas (O valor do orçamento fica somente na primeira linha do orçamneto)
  vmb_personal = vmb_personal.drop_duplicates(subset='ID orçamento', keep='first')

  # Deixando somente personais
  vmb_personal = vmb_personal.loc[vmb_personal["Avaliador"].isin(lista_nomes_personais)]

  # Tirando linhas que não tenham "Avaliador":
  vmb_personal = vmb_personal.dropna(subset=['Avaliador'])

  # Tirando Praia Grande
  vmb_personal = vmb_personal.loc[vmb_personal["Unidade"] != "PRAIA GRANDE"]

    # Tratando as Datas
  vmb_personal["Data venda"] = pd.to_datetime(vmb_personal["Data venda"])

  vmb_personal["Ano Venda"] = vmb_personal["Data venda"].dt.year

  vmb_personal["Data venda formatada"] = vmb_personal["Data venda"].dt.strftime('%d/%m/%Y')

  vmb_personal = vmb_personal.drop(columns=["Data venda"])

  vmb_personal = vmb_personal.rename(columns={"Data venda formatada": "Data venda"})

    # Coluna mês/ano
  vmb_personal["Mês/Ano"] = vmb_personal["Mês venda"].astype(str) + "/" + vmb_personal["Ano Venda"].astype(str)

  vmb_personal_columns = ['Avaliador', 'Mês/Ano','Unidade', 'Valor líquido']

  vmb_personal = vmb_personal[vmb_personal_columns]

  vmb_personal = vmb_personal.rename(columns={"Avaliador" : "Personais"})

  vmb_personal_gpb = vmb_personal.groupby(["Personais", "Mês/Ano", "Unidade"]).agg({"Valor líquido": "sum"}).reset_index()

  vmb_personal_gpb = vmb_personal_gpb.sort_values(by=["Unidade", "Personais"])

  return vmb_personal_gpb

#################################################################################################################################################

def atingimento_meta(vmb,arquivo_principal_path):
  # Importando base VMB
  vmb_atingimento = pd.read_excel(vmb)

  # Importando base Metas das Unidades
  metas_unidades = pd.read_excel(arquivo_principal_path, sheet_name='Sheet2')

  # Colocando a coluna em maiúscula para o merge
  metas_unidades["Unidade"] = metas_unidades["Unidade"].str.upper()

  #Filtrando a base
  vmb_atingimento = vmb_atingimento.loc[vmb_atingimento["Status"] == "Finalizado"]

  vmb_atingimento = vmb_atingimento.loc[vmb_atingimento["Unidade"] != "PRAIA GRANDE"]

  vmb_atingimento = vmb_atingimento.drop_duplicates(subset='ID orçamento', keep='first')

  vmb_atingimento = vmb_atingimento.fillna(0)

  # Groupby para pegar o Faturmaento da unidade
  vmb_atingimento = vmb_atingimento.groupby(["Unidade"]).agg({"Valor líquido": "sum"}).reset_index()

  # Merge de faturamento com Metas (left)
  validador_de_metas = pd.merge(vmb_atingimento, metas_unidades, on='Unidade', how='left')

  # Criando coluna atingimento de meta
  validador_de_metas["Atigimento Meta"] = (validador_de_metas["Valor líquido"] / validador_de_metas["META"])*100

  return validador_de_metas

#################################################################################################################################################

def treating_conversion(arquivo_principal_path):

  conversao_personais = pd.read_excel(arquivo_principal_path, sheet_name='Sheet3')

  conversao_personais_columns = ['Personais', 'Unidade', 'Conversão']

  conversao_personais = conversao_personais[conversao_personais_columns]

  return conversao_personais

#################################################################################################################################################

def Comission_calculator(vmb,venda_x_pgto,arquivo_principal_path,mes,ano):

  # colocando em maiúscula :
  mes = mes.upper()

  vmb_final = Treating_VMB(vmb)
  venda_x_pgto = Treating_VendaXPgto(venda_x_pgto)
  Garantido_meta_1_mes = Treating_Garantido_meta_1_mes(arquivo_principal_path)

  # Fazendo o merge considerando também a unidade, para garantir que só traga vendas da unidade correta
  merged_df = pd.merge(
      Garantido_meta_1_mes,
      vmb_final[['Consultor', 'Mês/Ano', 'Valor líquido', 'Unidade']],
      on=['Consultor', 'Unidade'],
      how='left'
  )

  final_merged_df = pd.merge(
      merged_df,
      venda_x_pgto[['Consultor', 'Mês/Ano', 'Valor líquido à Vista', 'Unidade']],
      on=['Consultor', 'Unidade'],
      how='left',
      suffixes=('', '_Vista')
  )

  final_merged_df_colums = ['Consultor', 'Mês/Ano', 'Unidade', 'Meta de Vendas',
                            'Valor líquido', 'Valor líquido à Vista', 'Valor do Garantido','Primeiro Mês']


  final_merged_df = final_merged_df[final_merged_df_colums]

  final_merged_df.replace(np.nan, 0, inplace=True)

  final_merged_df

  final_merged_df["Atingimento De Meta Total"] = (final_merged_df["Valor líquido"] / final_merged_df["Meta de Vendas"])*100
  final_merged_df["Atingimento de Meta À Vista"] = (final_merged_df["Valor líquido à Vista"] / (final_merged_df["Meta de Vendas"] * 0.4)) * 100



  def calcular_comissao_total(atingimento):
      if atingimento <= 80:
          return 0.50 / 100
      elif 80 < atingimento <= 90:
          return 0.75 / 100
      elif 90 < atingimento <= 100:
          return 1 / 100
      else:
          return 1.25 / 100

  # Função para calcular comissões do Faturamento à Vista
  def calcular_comissao_vista(atingimento):
      if atingimento <= 50:
          return 0.5 / 100
      elif 50 < atingimento <= 75:
          return 0.75 / 100
      elif 75 < atingimento <= 100:
          return 1 / 100
      else:
          return 1.25 / 100

  #Separando o Final_merged_df em 3 Groupbys para melhorar a análise

  #GARANTIDO

  final_merged_df_garantido = final_merged_df.loc[final_merged_df["Valor do Garantido"] > 0]

  # Aplicando as funções para calcular a comissão nas respectivas colunas
  final_merged_df_garantido['Range de Comissão Total'] = final_merged_df_garantido['Atingimento De Meta Total'].apply(calcular_comissao_total)
  final_merged_df_garantido['Range de Comissão à Vista'] = final_merged_df_garantido['Atingimento de Meta À Vista'].apply(calcular_comissao_vista)

  # Calculando o valor de comissão pelo atingimento de meta e meta à vista
  final_merged_df_garantido["Comissão Total"] = (
      (final_merged_df_garantido["Range de Comissão Total"] * final_merged_df_garantido["Valor líquido"]) +
      (final_merged_df_garantido["Range de Comissão à Vista"] * final_merged_df_garantido["Valor líquido"])
  )

  #Verificando se o valor é maior ou menor que o garantido e substituindo caso seja menor:
  final_merged_df_garantido["Comissão Total"] = np.where(
      final_merged_df_garantido["Comissão Total"] < final_merged_df_garantido["Valor do Garantido"],
      final_merged_df_garantido["Valor do Garantido"],
      final_merged_df_garantido["Comissão Total"]
  )

  garantido_groupby = final_merged_df_garantido.groupby(["Unidade", "Consultor","Mês/Ano"]).agg({"Comissão Total": "sum"}).reset_index()
  garantido_groupby

  #PRIMEIRO MÊS:

  # aletaração: foi de : final_merged_df_primeiro_mes_e_ativo = final_merged_df.loc[final_merged_df["Primeiro Mês"] == "Sim"]
  # Para:

  final_merged_df_primeiro_mes_e_ativo = final_merged_df.loc[(final_merged_df["Primeiro Mês"] == "Sim") & (final_merged_df["Valor do Garantido"] == 0)]
  final_merged_df_primeiro_mes_e_ativo

  # Fixei que é 1 % em cada pois a vendedora primeiro mês e Ativo tem comissão de 2%
  final_merged_df_primeiro_mes_e_ativo['Range de Comissão Total'] = 1/100
  final_merged_df_primeiro_mes_e_ativo['Range de Comissão à Vista'] = 1/100

  # Calculando o valor de comissão pelo atingimento de meta e meta à vista
  final_merged_df_primeiro_mes_e_ativo["Comissão Total"] = (
      (final_merged_df_primeiro_mes_e_ativo["Range de Comissão Total"] * final_merged_df_primeiro_mes_e_ativo["Valor líquido"]) +
      (final_merged_df_primeiro_mes_e_ativo["Range de Comissão à Vista"] * final_merged_df_primeiro_mes_e_ativo["Valor líquido"])
  )

  #Verificando se o valor é maior ou menor que o garantido e substituindo caso seja menor:
  final_merged_df_primeiro_mes_e_ativo["Comissão Total"] = np.where(
      final_merged_df_primeiro_mes_e_ativo["Comissão Total"] < final_merged_df_primeiro_mes_e_ativo["Valor do Garantido"],
      final_merged_df_primeiro_mes_e_ativo["Valor do Garantido"],
      final_merged_df_primeiro_mes_e_ativo["Comissão Total"]
  )

  primeiro_mes_groupby = final_merged_df_primeiro_mes_e_ativo.groupby(["Unidade", "Consultor","Mês/Ano"]).agg({"Comissão Total": "sum"}).reset_index()
  primeiro_mes_groupby


  #Faturamento Normal
  final_merged_df_normal = final_merged_df.loc[(final_merged_df["Primeiro Mês"] == "Não") & (final_merged_df["Valor do Garantido"] == 0)]

  # Aplicando as funções para calcular a comissão nas respectivas colunas
  final_merged_df_normal['Range de Comissão Total'] = final_merged_df_normal['Atingimento De Meta Total'].apply(calcular_comissao_total)

  final_merged_df_normal['Range de Comissão à Vista'] = final_merged_df_normal['Atingimento de Meta À Vista'].apply(calcular_comissao_vista)

  # Calculando o valor de comissão pelo atingimento de meta e meta à vista
  final_merged_df_normal["Comissão Total"] = (
      (final_merged_df_normal["Range de Comissão Total"] * final_merged_df_normal["Valor líquido"]) +
      (final_merged_df_normal["Range de Comissão à Vista"] * final_merged_df_normal["Valor líquido"])
  )

  normal_groupby = final_merged_df_normal.groupby(["Unidade", "Consultor","Mês/Ano"]).agg({"Comissão Total": "sum"}).reset_index()
  normal_groupby

  visualisation_df_groupby = pd.concat([garantido_groupby, primeiro_mes_groupby, normal_groupby])
  visualisation_df_groupby.sort_values(by=["Unidade", "Consultor"])

  visualisation_df = pd.concat([final_merged_df_garantido, final_merged_df_primeiro_mes_e_ativo, final_merged_df_normal])
  visualisation_df.sort_values(by=["Unidade", "Consultor"])

  # Formata as colunas de valor para R$
  valor_cols = ["Meta de Vendas", "Valor líquido", "Valor líquido à Vista", "Valor do Garantido", "Comissão Total"]
  for col in valor_cols:
      if col in visualisation_df.columns:
          visualisation_df[col] = visualisation_df[col].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

  visualisation_df
 ### CALCULANDO COMISSÃO PERSONAIS


  # Bases Para Cálculo de Comissão Personais - ## Quebrando aqui
  vmb_personal_gpb = treating_vmb_personais(vmb,arquivo_principal_path)
  validador_de_metas = atingimento_meta(vmb,arquivo_principal_path)
  conversao_personais = treating_conversion(arquivo_principal_path)

  # Mergind vmb com validador de metas

  merged_vmb_validador = pd.merge(vmb_personal_gpb,validador_de_metas, on=['Unidade'], how='left')

  # Mergind merged_vmb_validador com conversao_personais

  merged_vmb_validador_conversao = pd.merge(merged_vmb_validador, conversao_personais, on=['Personais', 'Unidade'], how='left')

  merged_vmb_validador_conversao.rename(columns={'Valor líquido_x': 'Valor Avaliação','Valor líquido_y': 'Faturmento Unidade',
  'Atigimento Meta': 'Atingimento Meta Unidade','META' : 'Meta','Conversão': 'Conversão Personal'}, inplace=True)

  # Base	0,75%
  # Conversão > 60% 	1,00%
  # Conversão > 60% & Meta Unidade >= 100%	1%

  ## Calculando Comissão

  def calcular_percent_personal(row):
      if row['Conversão Personal'] > 0.6:
          if row['Atingimento Meta Unidade'] >= 100:
              return 1.25/100
          else:
              return 1.0/100
      else:
          return 0.75/100

  merged_vmb_validador_conversao['% Comissão'] = merged_vmb_validador_conversao.apply(calcular_percent_personal, axis=1)

  #axis=1 (ou axis='columns'): Aplica a função ao longo das colunas, ou seja, a função será aplicada a cada linha para todas as colunas. Isso significa que a função receberá como entrada uma linha inteira do DataFrame.


  merged_vmb_validador_conversao["Comissão Total"] = (merged_vmb_validador_conversao["% Comissão"] * merged_vmb_validador_conversao["Valor Avaliação"])

  Personal_comissão_gpb = merged_vmb_validador_conversao.groupby(["Personais", "Mês/Ano", "Unidade"]).agg({"Comissão Total": "sum"}).reset_index()

  # Formata as colunas de valor para R$
  valor_cols = ["Comissão Total"]
  for col in valor_cols:
      if col in Personal_comissão_gpb.columns:
          Personal_comissão_gpb[col] = Personal_comissão_gpb[col].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

  Personal_comissão_gpb

  return visualisation_df, Personal_comissão_gpb