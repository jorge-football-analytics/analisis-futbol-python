import pandas as pd
import cloudscraper

url = "https://fbref.com/es/equipos/53a2f082/Estadisticas-de-Real-Madrid"

print("Conectando con FBref (saltando protección Cloudflare)...")

# Crear el scraper capaz de superar la pantalla de verificación
scraper = cloudscraper.create_scraper()
response = scraper.get(url)

# Cargar las tablas HTML con Pandas
tablas = pd.read_html(response.text)

# Tomar la primera tabla (resumen de la plantilla)
df_plantilla = tablas[0]

# Limpiar las columnas si vienen en formato multinivel
if isinstance(df_plantilla.columns, pd.MultiIndex):
    df_plantilla.columns = df_plantilla.columns.droplevel(0)

# Mostrar en consola los primeros 5 jugadores
print("\n--- PRIMEROS JUGADORES Y SUS ESTADÍSTICAS ---")
print(df_plantilla[['Jugador', 'Pos.', 'Edad', 'PJ', 'Goles', 'Ast']].head())

# Guardar la tabla limpia en un CSV
df_plantilla.to_csv("estadisticas_real_madrid.csv", index=False)
print("\n¡Archivo 'estadisticas_real_madrid.csv' guardado con éxito en tu carpeta!")