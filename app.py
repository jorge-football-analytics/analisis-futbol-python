import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mplsoccer import Pitch, Sbopen
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title='Football Data Analytics Dashboard',
    layout='wide',
    initial_sidebar_state='expanded',
)

# Estilo y título
st.title('⚽ Dashboard Interactivo de Sports Analytics')
st.markdown(
    '**Desarrollado por Jorge Fernández Villar** | *Ingeniería y Sistemas de'
    ' Datos (UPM)*'
)
st.markdown('---')


# Carga de datos con cache de Streamlit para optimizar velocidad
@st.cache_data
def get_match_data(match_id):
  parser = Sbopen()
  events, _, _, _ = parser.event(match_id)
  return events


# Menú lateral para seleccionar partido
st.sidebar.header('⚙️ Configuración del Partido')
match_options = {
    'Final Mundial 2022 (Argentina vs Francia)': 3869685,
    'Semifinal Mundial 2022 (Argentina vs Croacia)': 3869519,
    'Cuartos Mundial 2022 (Países Bajos vs Argentina)': 3869321,
}

selected_match_label = st.sidebar.selectbox(
    'Selecciona un partido de StatsBomb Open Data:', list(match_options.keys())
)
match_id = match_options[selected_match_label]

# Cargar eventos del partido seleccionado
events = get_match_data(match_id)
equipos = events['team_name'].dropna().unique()

# Selector de equipo dentro del partido
selected_team = st.sidebar.selectbox('Selecciona Equipo a Analizar:', equipos)

# Filtrar eventos del equipo
team_events = events[events['team_name'] == selected_team]

# Métricas clave en tarjetas superiores
col1, col2, col3, col4 = st.columns(4)

tiros = team_events[team_events['type_name'] == 'Shot']
xg_total = tiros['shot_statsbomb_xg'].sum()
pases = team_events[team_events['type_name'] == 'Pass']
pases_completados = pases[pases['outcome_name'].isnull()]

col1.metric('Disparos Totales', len(tiros))
col2.metric('xG Acumulado', f'{xg_total:.2f}')
col3.metric('Pases Intentados', len(pases))
col4.metric(
    'Efectividad de Pase',
    f'{(len(pases_completados)/max(len(pases), 1))*100:.1f}%',
)

st.markdown('---')

# Pestañas de Análisis Visual
tab1, tab2 = st.tabs(
    ['🎯 Mapa de Disparos (xG)', '🔥 Mapa de Densidad y Calor (KDE)']
)

with tab1:
  st.subheader(f'Mapa de Tiros y Goles Esperados (xG) - {selected_team}')
  pitch = Pitch(
      pitch_type='statsbomb', pitch_color='#101010', line_color='#555555'
  )
  fig, ax = pitch.draw(figsize=(10, 6))

  # Graficar tiros
  pitch.scatter(
      tiros.x,
      tiros.y,
      s=tiros.shot_statsbomb_xg * 900 + 40,
      c='#00e5ff',
      alpha=0.7,
      edgecolors='white',
      ax=ax,
  )

  st.pyplot(fig)

with tab2:
  st.subheader(f'Mapa de Ocupación de Campo (KDE) - {selected_team}')
  pitch = Pitch(
      pitch_type='statsbomb', pitch_color='#101010', line_color='#555555'
  )
  fig, ax = pitch.draw(figsize=(10, 6))

  # Dibujar densidad Kernel
  pitch.kdeplot(
      team_events.x,
      team_events.y,
      ax=ax,
      cmap='hot',
      fill=True,
      thresh=0.05,
      levels=100,
      alpha=0.6,
  )

  st.pyplot(fig)