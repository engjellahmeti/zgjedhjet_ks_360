import streamlit as st
from db import query_df
import altair as alt

st.set_page_config(
    page_title="Partitë",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Rezultatet e Zgjedhjeve për Kuvendin e Republikës së Kosovës sipas Partive Politike")
# st.title("")

vitet = query_df("SELECT * FROM lista_zgjedhjeve_parlamentare()")
partite = query_df("SELECT * FROM lista_e_partive()")
komunat = query_df("SELECT * FROM lista_e_komunave()")

col1, col2, col3 = st.columns(3)

with col1:
    selected_vitet = st.multiselect(
        "Viti zgjedhor",
        options=vitet["kombinim"],
        default=vitet["kombinim"]
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

partia_ids = partite[partite["partia"].isin(selected_parties)]["id"].tolist()
viti_ids = vitet[vitet["kombinim"].isin(selected_vitet)]["id"].tolist()
komunas = komunat[komunat["komuna"] == selected_komuna]["id"].tolist()

params = {
    "vitet_ids": viti_ids if viti_ids else None,
    "partia_ids": partia_ids if partia_ids else None,
    "komunas": komunas if komunas else None
}

if selected_komuna == 'All':
    cols = ['viti', 'partia', 'votat']
    sql = "SELECT * FROM total_votave_per_partite(%(vitet_ids)s, %(partia_ids)s)"
else:
    cols = ['viti', 'partia', 'komuna', 'votat']
    sql = "SELECT * FROM total_votave_per_partite_komune(%(vitet_ids)s, %(partia_ids)s, %(komunas)s)"

df = query_df(sql, params)

st.subheader("Totali i votave për partitë politike në vite të ndryshme zgjedhore dhe komuna të caktuara")
st.subheader("")

if df.empty:
    st.warning("Nuk ka të dhëna për filtrat e përzgjedhur.")
else:
    if selected_komuna == 'Diaspora':
        df = df[df["regjioni"] == selected_komuna]
        df['komuna'] = df['regjioni']
        df = df.groupby(by=['viti', 'partia', 'komuna'])['votat'].sum().reset_index()

    elif selected_komuna != 'All':
        df = df[df["komuna"] == selected_komuna]
    
    party_colors = {
        "AAK": "#F2C300",
        "PDK": "#0054A6",
        "LVV": "#E31E24",
        "LDK": "#7A7A7A"
    }
    
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("viti:O", title="Viti zgjedhor"),
            xOffset=alt.XOffset("partia:N"),
            y=alt.Y("votat:Q", title="Numri i votave"),
            color=alt.Color("partia:N",
                            title="Partia",
                            scale=alt.Scale(
                                domain=list(party_colors.keys()),
                                range=list(party_colors.values())
                            ),
                            ),
            tooltip=["viti", "partia", "votat"]
        )
    )

    st.altair_chart(chart, width='stretch')

with st.expander("Shfaq të dhënat"):
    st.dataframe(df[cols], width='stretch')