import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_percentage_data
from utils.analysis_functions import filter_percentage, calculate_delta_by_week

st.title("Análisis Temporal y Comparativo")

# Cargar datos
df = load_percentage_data()

# Sidebar con widgets
with st.sidebar:
    st.markdown("### Controles de Análisis")
    
    # Widget para elegir grupo
    grupos = ['Todos'] + df['Group'].unique().tolist()
    grupo_seleccionado = st.selectbox("Seleccionar Grupo", grupos)
    
    # Widget para elegir semana
    semanas = sorted(df['CW'].unique().tolist())
    semana_seleccionada = st.selectbox("Seleccionar Semana (CW)", semanas, index=len(semanas)-1)
    
    # Widget para elegir región
    regiones = df['Region'].unique().tolist()
    regiones_seleccionadas = st.multiselect("Seleccionar Región", regiones, default=regiones)

# Filtrar datos
df_filtrado = filter_percentage(df, regiones_seleccionadas, grupo_seleccionado)

# Calcular datos para la semana seleccionada
df_semana_actual = df_filtrado[df_filtrado['CW'] == semana_seleccionada]

# Calcular delta con semana anterior
semana_index = semanas.index(semana_seleccionada)
semana_anterior = semanas[semana_index - 1] if semana_index > 0 else semana_seleccionada
delta = calculate_delta_by_week(df_filtrado, semana_seleccionada, semana_anterior)

# KPIs dinámicos con delta
st.markdown("### KPIs Dinámicos")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        'Registros Semana', 
        len(df_semana_actual),
        border=True
    )

with col2:
    promedio_actual = df_semana_actual['valor'].mean() if len(df_semana_actual) > 0 else 0
    st.metric(
        'Promedio Valor', 
        f'{promedio_actual:.2%}',
        delta=f'{delta:.2%}',
        border=True
    )
    
with col3:
    st.metric(
        'Regiones Activas', 
        df_semana_actual['Region'].nunique(),
        border=True
    )

with col4:
    st.metric(
        'Grupos Activos', 
        df_semana_actual['Group'].nunique(),
        border=True
    )

st.markdown("---")

# Gráficas
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### Evolución Temporal")
    # Gráfica de línea de evolución
    df_evolucion = df_filtrado.groupby('CW')['valor'].mean().reset_index()
    
    fig_line = px.line(
        df_evolucion,
        x='CW',
        y='valor',
        title='Evolución del Valor Promedio por Semana',
        markers=True
    )
    fig_line.update_layout(
        xaxis_title="Semana (CW)",
        yaxis_title="Valor Promedio",
        yaxis_tickformat='.1%'
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    st.markdown("#### Promedio por Región")
    # Gráfica de barras promedio por región
    df_region = df_semana_actual.groupby('Region')['valor'].mean().reset_index()
    df_region = df_region.sort_values('valor', ascending=False)
    
    fig_bar = px.bar(
        df_region,
        x='Region',
        y='valor',
        title=f'Valor Promedio por Región (Semana {semana_seleccionada})',
        color='valor',
        color_continuous_scale='RdYlGn_r'
    )
    fig_bar.update_layout(
        xaxis_title="Región",
        yaxis_title="Valor Promedio",
        yaxis_tickformat='.1%'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Tabla comparativa
st.markdown("### Tabla Comparativa")

# Crear tabla comparativa entre semanas
if semana_index > 0:
    df_comparativa = df_filtrado[df_filtrado['CW'].isin([semana_anterior, semana_seleccionada])]
    
    # Pivot para mostrar comparación
    tabla_pivot = df_comparativa.pivot_table(
        values='valor',
        index=['Region', 'Group'],
        columns='CW',
        aggfunc='mean'
    ).reset_index()
    
    # Calcular diferencia
    if semana_anterior in tabla_pivot.columns and semana_seleccionada in tabla_pivot.columns:
        tabla_pivot['Diferencia'] = tabla_pivot[semana_seleccionada] - tabla_pivot[semana_anterior]
        tabla_pivot['% Cambio'] = (tabla_pivot['Diferencia'] / tabla_pivot[semana_anterior] * 100).fillna(0)
    
    st.dataframe(
        tabla_pivot.style.format({
            semana_anterior: '{:.2%}',
            semana_seleccionada: '{:.2%}',
            'Diferencia': '{:.2%}',
            '% Cambio': '{:.1f}%'
        }),
        use_container_width=True,
        height=400
    )
else:
    st.info("Seleccione una semana posterior a la primera para ver comparaciones")
