import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

print("Iniciando modelo de Clustering K-Means para Scouting...")

# 1. Dataset simulación de métricas por 90 min (10 jugadores de ejemplo)
data = {
    'jugador': [
        'Pedri',
        'Fede Valverde',
        'Rodri',
        'Vinicius Jr',
        'Tchouaméni',
        'Bellingham',
        'Gavi',
        'Kroos',
        'Camavinga',
        'Lamine Yamal',
    ],
    'equipo': [
        'Barcelona',
        'Real Madrid',
        'Man City',
        'Real Madrid',
        'Real Madrid',
        'Real Madrid',
        'Barcelona',
        'Real Madrid',
        'Real Madrid',
        'Barcelona',
    ],
    'pases_progresivos': [8.5, 6.2, 9.8, 3.1, 5.4, 6.8, 5.1, 10.2, 6.0, 4.5],
    'regates_completados': [2.8, 1.9, 0.5, 4.8, 0.6, 2.3, 2.1, 0.4, 2.0, 5.2],
    'recuperaciones': [5.1, 6.8, 8.9, 1.8, 9.2, 5.5, 7.4, 4.2, 8.1, 2.1],
    'xg_creado': [0.45, 0.38, 0.15, 0.68, 0.08, 0.55, 0.32, 0.25, 0.18, 0.61],
    'acciones_area': [4.2, 3.8, 1.2, 8.9, 0.9, 6.5, 3.9, 1.1, 2.1, 7.8],
}

df = pd.DataFrame(data)

# 2. Selección de métricas numéricas para el modelo
features = [
    'pases_progresivos',
    'regates_completados',
    'recuperaciones',
    'xg_creado',
    'acciones_area',
]
X = df[features]

# 3. Normalizar los datos (StandardScaler para media=0 y varianza=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Entrenar el algoritmo K-Means con 3 Clusters (Perfiles de Juego)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_scaled)

# 5. Reducción de dimensionalidad con PCA (2D) para visualizar en una gráfica
pca = PCA(n_components=2)
coords = pca.fit_transform(X_scaled)
df['pca1'] = coords[:, 0]
df['pca2'] = coords[:, 1]

# 6. Graficar los grupos / perfiles de scouting
plt.figure(figsize=(10, 7), facecolor='#f4f4f4')
colores = {0: '#e63946', 1: '#1d3557', 2: '#2a9d8f'}
etiquetas_cluster = {
    0: 'Regateadores / Creadores',
    1: 'Mediocentros / Destructores',
    2: 'Organizadores / Interiores',
}

for cluster_id, color in colores.items():
    sub_df = df[df['cluster'] == cluster_id]
    plt.scatter(
        sub_df['pca1'],
        sub_df['pca2'],
        c=color,
        label=etiquetas_cluster[cluster_id],
        s=180,
        alpha=0.8,
        edgecolors='black',
        zorder=3,
    )

    # Etiquetar los nombres de cada jugador sobre el gráfico
    for _, row in sub_df.iterrows():
        plt.annotate(
            row['jugador'],
            (row['pca1'], row['pca2']),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=11,
            fontweight='bold',
        )

plt.title(
    'Modelo de Scouting No Supervisado (Clustering K-Means + PCA)\nAgrupación de Jugadores por Perfil Técnico-Táctico',
    fontsize=13,
    pad=15,
)
plt.xlabel('Componente Principal 1 (Ataque y Regate)', fontsize=10)
plt.ylabel('Componente Principal 2 (Defensa y Distribución)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5, zorder=1)
plt.legend(title='Perfil Identificado', loc='upper left')

# Guardar la imagen para el portfolio
plt.savefig('clustering_scouting.png', dpi=300, bbox_inches='tight')
print("¡ÉXITO! Gráfico guardado como 'clustering_scouting.png'.")
plt.show()