import streamlit as st
import sqlalchemy as sa
import pandas as pd

@st.cache_resource
def get_engine():
    return sa.create_engine(st.secrets["SUPABASE_DB_URL"])

@st.cache_data(ttl=600)
def query_df(sql: str, params: dict | None = None) -> pd.DataFrame:
    engine = get_engine()

    return pd.read_sql(sql, engine, params=params)
