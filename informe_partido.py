import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mplsoccer import Pitch, Sbopen

print("Procesando datos y generando Informe Ejecutivo del Partido...")

# 1. Definir ID de partido (3869685 = Final Mundial 2022: Argentina vs Francia)
match_id = 3869685
parser = Sbopen()

# Cargar eventos e información general
events, related, freeze, players = parser.event(match_id)
matches = parser.match(competition_id=43, season_id=106)
match_info = matches[matches['match_id'] == match_id].iloc[0]

home_team = match_info['home_team_name']
away_team = match_info['away_team_name']
home_score = match_info['home_score']
away_score = match_info['away_score']

# 2. Filtrar disparos y calcular xG por equipo
shots = events[events['type_name'] == 'Shot'].copy()
home_shots = shots[shots['team_name'] == home_team]
away_shots = shots[shots['team_name'] == away_team]

home_xg = home_shots['shot_statsbomb_xg'].sum()
away_xg = away_shots['shot_statsbomb_xg'].sum()

# 3. Diseñar lienzo e infografía (Matplotlib GridSpec)
fig = plt.figure(figsize=(14, 9), facecolor='#101010')
gs = fig.add_gridspec(2, 2, height_ratios=[1, 4], hspace=0.2, wspace=0.1)

# --- CABECERA / PANEL SUPERIOR ---
ax_header = fig.add_subplot(gs[0, :])
ax_header.set_facecolor('#101010')
ax_header.axis('off')

# Título de resultado
ax_header.text(
    0.5,
    0.7,
    f'{home_team} {home_score} - {away_score} {away_team}',
    fontsize=26,
    color='white',
    fontweight='bold',
    ha='center',
)

# Subtítulo de xG
ax_header.text(
    0.5,
    0.35,
    f'Goles Esperados (xG Acumulado):  {home_team} {home_xg:.2f}  |  {away_xg:.2f} {away_team}',
    fontsize=13,
    color='#00e5ff',
    fontweight='bold',
    ha='center',
)

ax_header.text(
    0.5,
    0.1,
    f'Match ID: {match_id}  •  Generado Programáticamente con Python & StatsBomb Data',
    fontsize=9,
    color='#777777',
    ha='center',
)

# --- MAPA DE TIROS EQUIPO LOCAL ---
pitch1 = Pitch(
    pitch_type='statsbomb', pitch_color='#1a1a1a', line_color='#444444'
)
ax1 = fig.add_subplot(gs[1, 0])
pitch1.draw(ax=ax1)
ax1.set_title(
    f'{home_team}\n{len(home_shots)} Tiros totales | {home_xg:.2f} xG',
    color='white',
    fontsize=12,
    pad=10,
)

# Graficar disparos escala por xG (Local)
pitch1.scatter(
    home_shots.x,
    home_shots.y,
    s=home_shots.shot_statsbomb_xg * 900 + 40,
    c='#00e5ff',
    alpha=0.7,
    edgecolors='white',
    ax=ax1,
)

# --- MAPA DE TIROS EQUIPO VISITANTE ---
pitch2 = Pitch(
    pitch_type='statsbomb', pitch_color='#1a1a1a', line_color='#444444'
)
ax2 = fig.add_subplot(gs[1, 1])
pitch2.draw(ax=ax2)
ax2.set_title(
    f'{away_team}\n{len(away_shots)} Tiros totales | {away_xg:.2f} xG',
    color='white',
    fontsize=12,
    pad=10,
)

# Graficar disparos escala por xG (Visitante)
pitch2.scatter(
    away_shots.x,
    away_shots.y,
    s=away_shots.shot_statsbomb_xg * 900 + 40,
    c='#ff0055',
    alpha=0.7,
    edgecolors='white',
    ax=ax2,
)

# 4. Exportar imagen en alta calidad
plt.savefig(
    'informe_partido.png', dpi=300, bbox_inches='tight', facecolor='#101010'
)
print("¡ÉXITO! Infografía generada correctamente como 'informe_partido.png'.")
plt.show()