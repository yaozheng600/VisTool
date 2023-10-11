import streamlit as st

def language():
    return st.radio('Language',['🇬🇧','🇨🇳'],captions=['EN','中文'],horizontal=True,key="language")