import streamlit as st
from db import query_df
import altair as alt

st.set_page_config(
    page_title="Kandidatët",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Rezultatet e Zgjedhjeve për Kuvendin e Republikës së Kosovës sipas Kandidatëve Politik")

vitet = query_df("SELECT * FROM lista_zgjedhjeve_parlamentare()")
partite = query_df("SELECT * FROM lista_e_partive()")
komunat = query_df("SELECT * FROM lista_e_komunave()")
kandidatet = query_df("SELECT * FROM lista_e_kandidateve()")

col1, col2, col3, col4 = st.columns(4)
with col1:
    selected_kandidati = st.selectbox(
        "Kandidatët",
        placeholder="Zgjidhe kandidatin",
        options=["All"] + kandidatet["kombinim"].tolist(),
    )

with col2:
    selected_parties = st.multiselect(
        "Partia",
        options=partite["partia"].tolist(),
        default=partite["partia"].tolist()
    )

with col3:
    selected_komuna = st.selectbox(
        "Komuna",
        placeholder="Zgjidhe komunen",
        options=["All"] + komunat["komuna"].tolist(),
    )

with col4:
    selected_vitet = st.multiselect(
        "Viti zgjedhor",
        options=vitet["kombinim"],
        default=vitet["kombinim"]
    )

partia_ids = partite[partite["partia"].isin(selected_parties)]["id"].tolist()
viti_ids = vitet[vitet["kombinim"].isin(selected_vitet)]["id"].tolist()
komunas = komunat[komunat["komuna"] == selected_komuna]["id"].tolist()
kandidatis = kandidatet[kandidatet["kombinim"] == selected_kandidati]["id"].tolist()

params = {
    "vitet_ids": viti_ids if viti_ids else None,
    "partia_ids": partia_ids if partia_ids else None,
    "kandidatis": kandidatis[0] if kandidatis else None
}
sql2 = "SELECT * FROM total_votave_per_kandidat(%(vitet_ids)s, %(partia_ids)s, %(kandidatis)s)"
df_kand_anembane = query_df(sql2, params)

params["komunas"] = komunas[0] if komunas else None
sql1 = "SELECT * FROM total_votave_per_kandidat_komune(%(vitet_ids)s, %(partia_ids)s, %(kandidatis)s, %(komunas)s)"

st.subheader("Kandidatët me më së shumti vota anembanë Kosovës dhe diasporës")
st.dataframe(df_kand_anembane, width='stretch')

df_kand_per_komune = query_df(sql1, params)
st.subheader("Kandidatët me më së shumti vota për komuna")
st.dataframe(df_kand_per_komune, width='stretch')