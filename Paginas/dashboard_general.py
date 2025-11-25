import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_project_data
from utils.analysis_functions import filter_projects, calculate_kpis

st.title("Dashboard General de Proyectos")

# Cargar datos
df = load_project_data()

# Sidebar con filtros
with st.sidebar:
    st.markdown("### Filtros")
    
    estados = df['State'].dropna().unique().tolist()
    estado_filtro = st.multiselect("Estado", estados, default=estados)
    
    areas = df['Geographical scope'].dropna().unique().tolist()
    area_filtro = st.multiselect("Área Geográfica", areas, default=areas)
    
    managers = df['Project manager'].dropna().unique().tolist()
    manager_filtro = st.multiselect("Project Manager", managers)
    
    avance_min = st.slider("Avance mínimo (%)", 0, 100, 0)

# Filtrar datos
df_filtrado, avg_progress = filter_projects(
    df, estado_filtro, area_filtro if area_filtro else ['Todas'], 
    avance_min, manager_filtro if manager_filtro else None
)

# KPIs Generales
st.markdown("### KPIs Generales")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric('Total de Proyectos', len(df_filtrado), border=True)

with col2:
    st.metric('Avance Promedio', f'{avg_progress:.1f}%', border=True)
    
with col3:
    st.metric('Project Managers', df_filtrado['Project manager'].nunique(), border=True)

with col4:
    st.metric('Ubicaciones', df_filtrado['Geographical scope'].nunique(), border=True)

st.markdown("---")

# Tabla filtrable
st.markdown("### Tabla de Proyectos")
st.dataframe(
    df_filtrado[['Project Name', 'State', 'Geographical scope', 'Project manager', 'Percent complete', 'Project Type']],
    use_container_width=True,
    height=300
)

st.markdown("---")

# Pestañas con gráficos
tab1, tab2, tab3 = st.tabs(["Gráfico de Pastel", "Gráfico de Barras", "Histograma de Avances"])

with tab1:
    st.markdown("#### Distribución por Área Geográfica")
    fig_pie = px.pie(
        df_filtrado, 
        names='Geographical scope',
        title='Proyectos por Área Geográfica',
        hole=0.3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.markdown("#### Proyectos por Estado")
    state_counts = df_filtrado['State'].value_counts().reset_index()
    state_counts.columns = ['Estado', 'Cantidad']
    
    fig_bar = px.bar(
        state_counts,
        x='Estado',
        y='Cantidad',
        title='Cantidad de Proyectos por Estado',
        color='Cantidad',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.markdown("#### Distribución de Avances")
    fig_hist = px.histogram(
        df_filtrado,
        x='Percent complete',
        nbins=20,
        title='Distribución de Porcentaje de Avance',
        labels={'Percent complete': 'Porcentaje de Avance'},
        color_discrete_sequence=['#636EFA']
    )
    fig_hist.update_layout(
        xaxis_title="Porcentaje de Avance (%)",
        yaxis_title="Número de Proyectos"
    )
    st.plotly_chart(fig_hist, use_container_width=True)
