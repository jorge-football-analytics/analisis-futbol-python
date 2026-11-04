import codecs
import json
import re
import cloudscraper
import pandas as pd

print("Conectando con Understat...")

url = "https://understat.com/league/La_liga"

# Usar cloudscraper para pasar los filtros de navegación
scraper = cloudscraper.create_scraper()
response = scraper.get(url)

# Regex ajustada para capturar el bloque entero de datos
match = re.search(r"var playersData\s*=\s*JSON\.parse\('(.+?)'\);", response.text)

if match:
  raw_string = match.group(1)
  # Decodificar secuencias de escape (\x20, \u00, etc.)
  json_string = codecs.decode(raw_string, 'unicode_escape')
  data = json.loads(json_string)

  # Crear el DataFrame
  df = pd.DataFrame(data)

  # Convertir a valores numéricos
  cols = [
      'goals',
      'shots',
      'xG',
      'time',
      'assists',
      'xA',
      'key_passes',
      'games',
  ]
  for col in cols:
    df[col] = pd.to_numeric(df[col])

  # Filtrar Real Madrid y ordenar por xG (Goles Esperados)
  df_madrid = df[df['team_title'] == 'Real Madrid'].sort_values(
      by='xG', ascending=False
  )
  df_madrid['xG'] = df_madrid['xG'].round(2)
  df_madrid['xA'] = df_madrid['xA'].round(2)

  # Mostrar por consola
  print('\n--- PLANTILLA DEL REAL MADRID (Estadísticas xG / xA) ---')
  print(
      df_madrid[['player_name', 'games', 'goals', 'xG', 'assists', 'xA']].head(
          10
      )
  )

  # Guardar en CSV
  df_madrid.to_csv('estadisticas_real_madrid.csv', index=False)
  print(
      "\n¡ÉXITO! Archivo 'estadisticas_real_madrid.csv' generado correctamente en tu carpeta."
  )

else:
  print('No se encontró el patrón de datos en el HTML recibido.')