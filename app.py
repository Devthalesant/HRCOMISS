import streamlit as st

st.set_page_config(layout="wide")

# --- PAGE SETUP ---
comission = st.Page(
    "Modules/calculo_comissao.py",
    title="Calculadora de Comissão",
    icon=":material/thumb_up:",
    default=True,
)

revenue = st.Page(
    "Modules/Revenda_nadia.py",
    title="Ranking de Revenda",
    icon=":material/thumb_up:",
)



# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Recursos Humanos 👥": [comission],
        "Responsável Técnica 🔍": [revenue],
    }
)

# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")


# --- RUN NAVIGATION ---
pg.run()