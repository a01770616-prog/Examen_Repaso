import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.data_loader import load_project_data
from utils.analysis_functions import assign_coords_to_projects

st.title("Mapa de Proyectos")

# Cargar datos
df = load_project_data()

# Sidebar con filtros
with st.sidebar:
    st.markdown("### Filtros del Mapa")
    
    # Filtro por área geográfica
    areas = ['Todas'] + df['Geographical scope'].dropna().unique().tolist()
    area_seleccionada = st.selectbox("Filtrar por Área", areas)
    
    # Filtro por planta (usando columna que tenga info de planta)
    if 'Geographical scope' in df.columns:
        plantas = df['Geographical scope'].dropna().unique().tolist()
        plantas_seleccionadas = st.multiselect(
            "Filtrar por Planta/Ubicación", 
            plantas,
            default=plantas
        )
    
    # Filtro por estado del proyecto
    estados = df['State'].dropna().unique().tolist()
    estados_seleccionados = st.multiselect(
        "Filtrar por Estado", 
        estados,
        default=estados
    )

# Aplicar filtros
df_filtrado = df.copy()

if area_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Geographical scope'] == area_seleccionada]

if plantas_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['Geographical scope'].isin(plantas_seleccionadas)]

if estados_seleccionados:
    df_filtrado = df_filtrado[df_filtrado['State'].isin(estados_seleccionados)]

# Asignar coordenadas
df_coords = assign_coords_to_projects(df_filtrado, 'Geographical scope')

# Mostrar KPIs del mapa
col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Proyectos en Mapa', len(df_coords), border=True)

with col2:
    st.metric('Ubicaciones', df_coords['Geographical scope'].nunique(), border=True)

with col3:
    avg_progress = df_coords['Percent complete'].mean()
    st.metric('Avance Promedio', f'{avg_progress:.1f}%', border=True)

st.markdown("---")

# Crear mapa con Folium
if len(df_coords) > 0:
    st.markdown("### Vista de Mapa Interactivo")
    
    # Calcular centro del mapa
    map_center = [df_coords['lat'].mean(), df_coords['lon'].mean()]
    
    # Crear mapa
    m = folium.Map(
        location=map_center, 
        zoom_start=2,
        tiles='OpenStreetMap'
    )
    
    # Definir colores según avance
    def get_color(progress):
        if progress < 25:
            return 'red'
        elif progress < 50:
            return 'orange'
        elif progress < 75:
            return 'lightblue'
        else:
            return 'green'
    
    # Agregar marcadores con popups
    for _, row in df_coords.iterrows():
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="margin-bottom: 10px; color: #1f77b4;">{row['Project Name']}</h4>
            <hr style="margin: 5px 0;">
            <p><b>Ubicación:</b> {row['Geographical scope']}</p>
            <p><b>Estado:</b> {row['State']}</p>
            <p><b>Avance:</b> {row['Percent complete']:.1f}%</p>
            <p><b>Manager:</b> {row['Project manager']}</p>
            <p><b>Tipo:</b> {row['Project Type']}</p>
        </div>
        """
        
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['Project Name'],
            icon=folium.Icon(
                color=get_color(row['Percent complete']),
                icon='info-sign'
            )
        ).add_to(m)
    
    # Mostrar mapa
    st_folium(m, width=1200, height=600)
    
    # Leyenda de colores
    st.markdown("---")
    st.markdown("### Leyenda de Colores")
    
    legend_col1, legend_col2, legend_col3, legend_col4 = st.columns(4)
    
    with legend_col1:
        st.markdown("**Rojo:** < 25% avance")
    
    with legend_col2:
        st.markdown("**Naranja:** 25-50% avance")
    
    with legend_col3:
        st.markdown("**Azul claro:** 50-75% avance")
    
    with legend_col4:
        st.markdown("**Verde:** > 75% avance")
    
    st.markdown("---")
    
    # Tabla de proyectos en el mapa
    st.markdown("### Detalle de Proyectos")
    st.dataframe(
        df_coords[[
            'Project Name', 
            'Geographical scope', 
            'State', 
            'Percent complete',
            'Project manager',
            'Project Type'
        ]].sort_values('Percent complete', ascending=False),
        use_container_width=True,
        height=300
    )
else:
    st.warning("No hay proyectos que mostrar con los filtros seleccionados")
