import streamlit as st
import pandas as pd


@st.cache_data
def load_percentage_data():
    """Carga datos de porcentajes de proyectos no completados"""
    return pd.read_csv("data/percentage_not_completed.csv")


@st.cache_data
def load_project_data():
    """Carga datos de proyectos con limpieza básica"""
    df = pd.read_csv('data/proyectos.csv', encoding='latin1')
    df = df.iloc[:-2].copy()
    df['Percent complete'] = pd.to_numeric(df['Percent complete'], errors='coerce')
    return df


@st.cache_data
def load_region_domain_data():
    """Carga datos de región y dominio"""
    try:
        return pd.read_csv('data/region_domain_data.csv')
    except FileNotFoundError:
        return pd.DataFrame()
