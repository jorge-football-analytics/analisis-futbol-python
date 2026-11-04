import pandas as pd
from mplsoccer import Sbopen

print("Conectando con la base de datos abierta de LaLiga...")

# 1. Conectar con el parser oficial de StatsBomb
parser = Sbopen()

# 2. Descargar la lista de partidos disponibles de LaLiga (ID de competición 11)
partidos = parser.match(competition_id=11, season_id=90)
print(f"¡Conectado! Se han encontrado {len(partidos)} partidos completos de LaLiga.")

# 3. Tomar el primer partido de la lista y extraer sus eventos
match_id = partidos['match_id'].iloc[0]
equipo_local = partidos['home_team_name'].iloc[0]
equipo_visitante = partidos['away_team_name'].iloc[0]

print(f"\nAnalizando el partido: {equipo_local} vs {equipo_visitante}...")
events, related, freeze, players = parser.event(match_id)

# 4. Filtrar disparos y agrupar con Pandas para calcular xG por jugador
tiros = events[events['type_name'] == 'Shot'].copy()

resumen_jugadores = (
    tiros.groupby(['player_name', 'team_name'])
    .agg(tiros_totales=('id', 'count'), xG_acumulado=('shot_statsbomb_xg', 'sum'))
    .reset_index()
)

# Redondear y ordenar de mayor a menor xG
resumen_jugadores['xG_acumulado'] = resumen_jugadores['xG_acumulado'].round(2)
resumen_jugadores = resumen_jugadores.sort_values(by='xG_acumulado', ascending=False)

# 5. Mostrar por pantalla
print("\n--- ESTADÍSTICAS DE JUGADORES Y xG ACUMULADO ---")
print(resumen_jugadores.head(10))

# 6. Guardar en archivo CSV
resumen_jugadores.to_csv("estadisticas_partido_laliga.csv", index=False)
print(
    "\n¡ÉXITO! Archivo 'estadisticas_partido_laliga.csv' generado en tu carpeta."
)