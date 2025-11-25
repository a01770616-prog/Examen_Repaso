import pandas as pd
import streamlit as st


def filter_percentage(df, regiones, grupo):
    """Filtra datos de porcentaje por región y grupo"""
    df_filtered = df.copy()
    if regiones:
        df_filtered = df_filtered[df_filtered['Region'].isin(regiones)]
    if grupo and grupo != 'Todos':
        df_filtered = df_filtered[df_filtered['Group'] == grupo]
    return df_filtered


def filter_projects(df, estados, areas, avance_min, project_managers=None):
    """Filtra proyectos por estado, área geográfica, avance mínimo y project manager"""
    df_filtered = df.copy()
    if estados:
        df_filtered = df_filtered[df_filtered['State'].isin(estados)]
    if areas and 'Todas' not in areas:
        df_filtered = df_filtered[df_filtered['Geographical scope'].isin(areas)]
    if project_managers:
        df_filtered = df_filtered[df_filtered['Project manager'].isin(project_managers)]
    df_filtered = df_filtered[df_filtered['Percent complete'] >= avance_min]
    avg_progress = df_filtered['Percent complete'].mean() if len(df_filtered) > 0 else 0
    
    return df_filtered, avg_progress


def assign_coords_to_projects(df, region_col='Geographical scope'):
    """Asigna coordenadas geográficas a proyectos según su región"""
    region_coords = {
        'EMEA': {'lat': 50.1109, 'lon': 8.6820},
        'ASIA': {'lat': 35.6895, 'lon': 139.6917},
        'NAO': {'lat': 42.3314, 'lon': -83.0458},
        'BRAZIL': {'lat': -23.5505, 'lon': -46.6333},
    }
    
    df = df.copy()
    df['lat'] = df[region_col].map(lambda x: region_coords.get(x, {}).get('lat', None))
    df['lon'] = df[region_col].map(lambda x: region_coords.get(x, {}).get('lon', None))
    return df.dropna(subset=['lat', 'lon'])


def calculate_kpis(df):
    """Calcula KPIs generales de proyectos"""
    total_projects = len(df)
    avg_progress = df['Percent complete'].mean() if total_projects > 0 else 0
    total_managers = df['Project manager'].nunique()
    total_locations = df['Geographical scope'].nunique()
    
    return {
        'total_projects': total_projects,
        'avg_progress': avg_progress,
        'total_managers': total_managers,
        'total_locations': total_locations
    }


def get_percentage_data_by_week(df, selected_week):
    """Obtiene datos de porcentaje para una semana específica"""
    return df[df['CW'] == selected_week]


def calculate_delta_by_week(df, current_week, previous_week):
    """Calcula el delta entre dos semanas"""
    current_data = df[df['CW'] == current_week]
    previous_data = df[df['CW'] == previous_week]
    
    if len(current_data) == 0 or len(previous_data) == 0:
        return 0
    
    current_avg = current_data['valor'].mean()
    previous_avg = previous_data['valor'].mean()
    
    delta = current_avg - previous_avg
    return delta
