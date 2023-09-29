import pandas as pd
import numpy as np
import altair as alt
import streamlit as st


def df_describe(data):
    df = pd.DataFrame()
    df = data
    df.rename(index={"top":"most common","freq":"%"},inplace=True)
    df.loc["%",:]=(df.loc["%",:]/df.loc["count",:]).apply(lambda x: "%.1f%%" %(x*100))
    return df

def barchart_describe(data):
    alt.data_transformers.disable_max_rows()
    df = data.to_frame()
    if df[df.columns[0]].dtype is np.dtype("object"):
        fig = alt.Chart(df).mark_bar().encode(
        y= alt.Y(df.columns[0], type="ordinal"),
        x="count()"
        )
    else:
        fig = alt.Chart(df).mark_bar().encode(
            y=alt.Y(df.columns[0],bin=True, type="ordinal"),
            x="count()"
        )
    return fig

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)