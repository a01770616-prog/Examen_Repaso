import streamlit as st

st.set_page_config(
    page_title='Dashboard Forvia - Análisis de Proyectos',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Definir las páginas
dashboard_page = st.Page(
    'Paginas/dashboard_general.py',
    title='Dashboard General',
    icon=':material/dashboard:',
    default=True
)

analisis_page = st.Page(
    'Paginas/analisis_temporal.py',
    title='Análisis Temporal',
    icon=':material/analytics:'
)

mapa_page = st.Page(
    'Paginas/mapa_proyectos.py',
    title='Mapa de Proyectos',
    icon=':material/map:'
)

# Crear navegación estructurada
pg = st.navigation({
    'Principal': [dashboard_page],
    'Análisis': [analisis_page],
    'Visualización': [mapa_page]
})

# Ejecutar página seleccionada
pg.run()
