⚽ Sports Analytics & Football Data ScienceRepositorio modular de proyectos de analítica de datos aplicada al fútbol, modelado estadístico avanzado ($xG$, $xT$), Machine Learning no supervisado para scouting y desarrollo de dashboards interactivos.Desarrollado por Jorge Fernández Villar — Estudiante de Ingeniería y Sistemas de Datos en la Universidad Politécnica de Madrid (UPM).🚀 Inicio Rápido & Despliegue Local1. Clonar el repositorio e instalar dependenciasgit clone https://github.com/jorge-football-analytics/analisis-futbol-python.git
cd analisis-futbol-python

# Activar entorno virtual (Windows PowerShell)
.\env\Scripts\activate

# Instalar librerías principales
pip install pandas numpy matplotlib mplsoccer scikit-learn streamlit
2. Lanza la Web App Interactivastreamlit run app.py
📌 Módulos Destacados & Modelos Avanzados1. Web App Interactiva (Dashboard con Streamlit)Archivo: app.pyDescripción: Cuadro de mando interactivo para la ingesta dinámica de encuentros de StatsBomb Open Data, filtrado por equipos, cálculo de KPIs de rendimiento en tiempo real e inspección visual de mapas de $xG$ y densidad espacial (KDE).2. Modelo de Scouting Inteligente (Machine Learning No Supervisado)Archivo: scouting_clustering.pyDescripción: Algoritmo de aglomeración K-Means y reducción de dimensionalidad con PCA (Análisis de Componentes Principales) para la clasificación automática de futbolistas por perfil técnico-táctico a partir de métricas normalizadas por 90 minutos (StandardScaler).3. Modelo de Peligro Esperado ($xT$ - Expected Threat)Archivo: modelo_xt.pyDescripción: Matriz de probabilidad espacial sobre rejilla discreta de $12 \times 8$ para cuantificar el incremento de amenaza de gol tras pases y conducciones proyectados hacia zonas de mayor valor.4. Generador Automático de Informes Post-Partido (Match Reports)Archivo: informe_partido.pyDescripción: Pipeline de procesamiento de eventos en segundo plano y maquetación programática con Matplotlib GridSpec para generar infografías ejecutivas de alta resolución con métricas agregadas de $xG$ y mapa de tiros.5. Colección de Análisis Espacial y Extracción de DatosScriptDescripción Táctica / Técnicapases_messi.pyFiltrado y representación espacial con vectores de pases completados e incompletos.mapa_tiros_xg.pyVisualización de remates con escalado de disparos en función del valor de $xG$.mapa_calor_jugador.pyEstimación de densidad Kernel (KDE) para el análisis de ocupación de zonas.radar_scouting.pyGráfico radial parametrizado para evaluación de perfiles multidimensionales.estadisticas_laliga.pyExtracción, limpieza y agregación de métricas de acumulación con Pandas exportadas a CSV.📁 Estructura del Repositorioanalisis-futbol-python/
│
├── 📊 Dashboards & Apps
│   └── app.py                        # Aplicación interactiva en Streamlit
│
├── 🤖 Modelos & Machine Learning
│   ├── scouting_clustering.py        # Modelo K-Means + PCA para scouting
│   ├── modelo_xt.py                  # Modelo de Peligro Esperado (xT)
│   └── informe_partido.py            # Generador programático de Match Reports
│
├── 📐 Visualización & Eventos
│   ├── mapa_calor_jugador.py         # Mapa de densidad KDE
│   ├── mapa_tiros_xg.py              # Distribución de remates y xG
│   ├── pases_messi.py                # Redes de pases y dirección
│   └── radar_scouting.py             # Gráficas de radar para scouting
│
├── 💾 Procesamiento de Datos
│   ├── estadisticas_laliga.py        # Extracción y limpieza con Pandas
│   └── estadisticas_partido_laliga.csv
│
└── 🖼️ Assets & Configuración
    ├── clustering_scouting.png
    ├── informe_partido.png
    ├── modelo_xt.png
    └── .gitignore
🛠️ Tecnologías UtilizadasLenguaje: Python 3.11+Ciencia de Datos & ML: scikit-learn, pandas, numpyVisualización & Web: streamlit, mplsoccer, matplotlibProveedor de Datos: StatsBomb Open Data📩 ContactoJorge Fernández VillarIngeniería y Sistemas de Datos — Universidad Politécnica de Madrid (UPM)GitHub: jorge-football-analytics