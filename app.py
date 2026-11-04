import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mplsoccer import Pitch, Sbopen
import streamlit as st

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS CUSTOM
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Football Analytics Pro Platform",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    h1, h2, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    .player-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #00e5ff;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
    }
    div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 800 !important; color: #00e5ff !important; }
    div[data-testid="stMetricLabel"] { font-size: 13px !important; color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #111827; padding: 8px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; color: #94a3b8; padding: 10px 20px; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #1e293b !important; color: #00e5ff !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. MOTOR DE DATOS Y FUNCIONES DE CÁLCULO
# -----------------------------------------------------------------------------
parser = Sbopen()


@st.cache_data
def load_all_competitions():
  return parser.competition()


@st.cache_data
def load_matches_by_comp(comp_id, season_id):
  return parser.match(competition_id=comp_id, season_id=season_id)


@st.cache_data
def load_match_events(match_id):
  events, related, freeze, players = parser.event(match_id)
  return events, players


XT_GRID = np.array([
    [
        0.003,
        0.003,
        0.004,
        0.005,
        0.006,
        0.007,
        0.008,
        0.009,
        0.012,
        0.014,
        0.019,
        0.024,
    ],
    [
        0.003,
        0.003,
        0.004,
        0.005,
        0.006,
        0.008,
        0.009,
        0.011,
        0.014,
        0.018,
        0.025,
        0.038,
    ],
    [
        0.003,
        0.004,
        0.005,
        0.006,
        0.008,
        0.010,
        0.012,
        0.015,
        0.021,
        0.030,
        0.052,
        0.084,
    ],
    [
        0.004,
        0.005,
        0.006,
        0.008,
        0.010,
        0.013,
        0.016,
        0.022,
        0.034,
        0.056,
        0.108,
        0.257,
    ],
    [
        0.004,
        0.005,
        0.006,
        0.008,
        0.010,
        0.013,
        0.016,
        0.022,
        0.034,
        0.056,
        0.108,
        0.257,
    ],
    [
        0.003,
        0.004,
        0.005,
        0.006,
        0.008,
        0.010,
        0.012,
        0.015,
        0.021,
        0.030,
        0.052,
        0.084,
    ],
    [
        0.003,
        0.003,
        0.004,
        0.005,
        0.006,
        0.008,
        0.009,
        0.011,
        0.014,
        0.018,
        0.025,
        0.038,
    ],
    [
        0.003,
        0.003,
        0.004,
        0.005,
        0.006,
        0.007,
        0.008,
        0.009,
        0.012,
        0.014,
        0.019,
        0.024,
    ],
])


def get_grid_cell(x, y):
  x_bin = min(int(x / 10), 11)
  y_bin = min(int((80 - y) / 10), 7)
  return y_bin, x_bin


def calculate_xt(events_df):
  passes = events_df[
      (events_df['type_name'] == 'Pass') & (events_df['outcome_name'].isnull())
  ].copy()
  if passes.empty:
    passes['xT'] = 0.0
    return passes
  xt_vals = []
  for _, row in passes.iterrows():
    try:
      y_s, x_s = get_grid_cell(row['x'], row['y'])
      end_x = row.get('end_x', row.get('pass_end_x', row['x']))
      end_y = row.get('end_y', row.get('pass_end_y', row['y']))
      y_e, x_e = get_grid_cell(end_x, end_y)
      xt_vals.append(XT_GRID[y_e, x_e] - XT_GRID[y_s, x_s])
    except:
      xt_vals.append(0.0)
  passes['xT'] = xt_vals
  return passes


# -----------------------------------------------------------------------------
# 3. SELECCIÓN DE PARTIDO
# -----------------------------------------------------------------------------
if 'selected_match_id' not in st.session_state:
  st.session_state['selected_match_id'] = None

st.markdown(
    """
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 38px;'>⚽ PLATAFORMA PROFESIONAL DE SPORTS ANALYTICS</h1>
        <p style='color: #94a3b8; font-size: 16px;'>Ingesta Dinámica de Datos, Modelado Avanzado (xG, xT) y Scouting de Rendimiento</p>
        <p style='color: #00e5ff; font-weight: 600;'>Desarrollado por Jorge Fernández Villar | UPM</p>
    </div>
""",
    unsafe_allow_html=True,
)

with st.expander('⚙️ PANEL DE CONTROL Y SELECCIÓN DE PARTIDO', expanded=True):
  df_comps = load_all_competitions()
  col_s1, col_s2, col_s3, col_s4 = st.columns(4)

  comp_names = sorted(list(df_comps['competition_name'].unique()))
  selected_comp = col_s1.selectbox('1. Competición', comp_names)

  df_sub_comp = df_comps[df_comps['competition_name'] == selected_comp]
  season_names = sorted(list(df_sub_comp['season_name'].unique()), reverse=True)
  selected_season = col_s2.selectbox('2. Temporada', season_names)

  comp_row = df_sub_comp[df_sub_comp['season_name'] == selected_season].iloc[0]
  comp_id, season_id = comp_row['competition_id'], comp_row['season_id']

  df_matches = load_matches_by_comp(comp_id, season_id)

  if (
      'match_week' in df_matches.columns
      and df_matches['match_week'].notnull().any()
  ):
    weeks = sorted([int(w) for w in df_matches['match_week'].dropna().unique()])
    week_labels = [f'Jornada {w}' for w in weeks]
    selected_week_label = col_s3.selectbox('3. Jornada / Fase', week_labels)
    selected_week = int(selected_week_label.replace('Jornada ', ''))
    df_filtered_matches = df_matches[df_matches['match_week'] == selected_week]
  else:
    stages = sorted(list(df_matches['stage_name'].unique()))
    selected_stage = col_s3.selectbox('3. Fase del Torneo', stages)
    df_filtered_matches = df_matches[df_matches['stage_name'] == selected_stage]

  df_filtered_matches = df_filtered_matches.copy()
  df_filtered_matches['match_label'] = (
      df_filtered_matches['home_team_name']
      + ' '
      + df_filtered_matches['home_score'].astype(str)
      + ' - '
      + df_filtered_matches['away_score'].astype(str)
      + ' '
      + df_filtered_matches['away_team_name']
  )

  selected_match_label = col_s4.selectbox(
      '4. Partido', df_filtered_matches['match_label'].unique()
  )
  match_row = df_filtered_matches[
      df_filtered_matches['match_label'] == selected_match_label
  ].iloc[0]

  btn_analyze = st.button('🚀 CARGAR Y ANALIZAR PARTIDO', use_container_width=True)

# -----------------------------------------------------------------------------
# 4. DASHBOARD DE ANÁLISIS
# -----------------------------------------------------------------------------
if btn_analyze or st.session_state['selected_match_id'] is not None:
  st.session_state['selected_match_id'] = match_row['match_id']
  match_id = match_row['match_id']

  events, players = load_match_events(match_id)
  home_team = match_row['home_team_name']
  away_team = match_row['away_team_name']

  st.markdown(
      f"""
        <div style='background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 15px; margin: 15px 0; text-align: center;'>
            <h2 style='margin:0; font-size: 28px; color: #ffffff;'>{home_team} <span style='color:#00e5ff;'>{match_row["home_score"]}</span> - <span style='color:#00e5ff;'>{match_row["away_score"]}</span> {away_team}</h2>
            <p style='margin:5px 0 0 0; color:#94a3b8; font-size:14px;'>{selected_comp} ({selected_season})</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  tab1, tab2, tab3, tab4 = st.tabs([
      '📊 Resumen & xG Flow',
      '🛡️ Análisis de Equipos',
      '👤 Scouting Individual',
      '⚡ Peligro Esperado (xT)',
  ])

  # TAB 1: FLUJO xG
  with tab1:
    shots_all = events[events['type_name'] == 'Shot'].copy()
    home_shots = shots_all[shots_all['team_name'] == home_team]
    away_shots = shots_all[shots_all['team_name'] == away_team]

    home_xg = (
        home_shots['shot_statsbomb_xg'].sum()
        if 'shot_statsbomb_xg' in home_shots.columns
        else 0.0
    )
    away_xg = (
        away_shots['shot_statsbomb_xg'].sum()
        if 'shot_statsbomb_xg' in away_shots.columns
        else 0.0
    )

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric(f'Goles {home_team}', match_row['home_score'])
    kpi2.metric(f'xG {home_team}', f'{home_xg:.2f}')
    kpi3.metric('Tiros Totales', f'{len(home_shots)} - {len(away_shots)}')
    kpi4.metric(f'xG {away_team}', f'{away_xg:.2f}')
    kpi5.metric(f'Goles {away_team}', match_row['away_score'])

    st.markdown('### 📈 Flujo de Peligro Acumulado (xG Timeline)')

    if not shots_all.empty and 'shot_statsbomb_xg' in shots_all.columns:
      shots_df = shots_all.sort_values(by=['minute', 'second']).copy()
      shots_df['home_xg'] = np.where(
          shots_df['team_name'] == home_team, shots_df['shot_statsbomb_xg'], 0
      )
      shots_df['away_xg'] = np.where(
          shots_df['team_name'] == away_team, shots_df['shot_statsbomb_xg'], 0
      )

      shots_df['home_cum'] = shots_df['home_xg'].cumsum()
      shots_df['away_cum'] = shots_df['away_xg'].cumsum()

      fig_f, ax_f = plt.subplots(figsize=(12, 4), facecolor='#0b0f19')
      ax_f.set_facecolor('#111827')

      ax_f.step(
          shots_df['minute'],
          shots_df['home_cum'],
          where='post',
          color='#00e5ff',
          label=home_team,
          linewidth=2.5,
      )
      ax_f.step(
          shots_df['minute'],
          shots_df['away_cum'],
          where='post',
          color='#ff0055',
          label=away_team,
          linewidth=2.5,
      )

      # Búsqueda segura del nombre del resultado de tiro (Goal)
      outcome_col = None
      if 'outcome_name' in shots_all.columns:
        outcome_col = 'outcome_name'
      elif 'shot_outcome_name' in shots_all.columns:
        outcome_col = 'shot_outcome_name'

      if outcome_col:
        goals = shots_all[shots_all[outcome_col] == 'Goal']
        for _, g in goals.iterrows():
          color = '#00e5ff' if g['team_name'] == home_team else '#ff0055'
          cum_val = (
              shots_df[shots_df['minute'] <= g['minute']]['home_cum'].max()
              if g['team_name'] == home_team
              else shots_df[shots_df['minute'] <= g['minute']]['away_cum'].max()
          )
          ax_f.scatter(
              g['minute'],
              cum_val,
              color=color,
              s=120,
              zorder=5,
              edgecolors='white',
          )
          p_name = g.get('player_name', 'Gol')
          ax_f.annotate(
              f'⚽ {p_name}',
              (g['minute'], cum_val + 0.08),
              color='white',
              fontsize=9,
              fontweight='bold',
          )

      ax_f.set_xlabel('Minuto de Juego', color='#94a3b8')
      ax_f.set_ylabel('xG Acumulado', color='#94a3b8')
      ax_f.tick_params(colors='white')
      ax_f.grid(True, linestyle='--', alpha=0.2)
      ax_f.legend(facecolor='#111827', labelcolor='white', edgecolor='none')
      st.pyplot(fig_f)
    else:
      st.info(
          'No se registraron remates con métrica xG en este partido en'
          ' particular.'
      )

  # TAB 2: ANÁLISIS DE EQUIPOS
  with tab2:
    selected_eq = st.radio(
        'Selecciona Equipo para Inspección Táctica:',
        [home_team, away_team],
        horizontal=True,
    )
    eq_events = events[events['team_name'] == selected_eq]

    c_map1, c_map2 = st.columns(2)

    with c_map1:
      st.markdown(f'**🎯 Mapa de Tiros ({selected_eq})**')
      eq_shots = eq_events[eq_events['type_name'] == 'Shot']
      pitch = Pitch(
          pitch_type='statsbomb', pitch_color='#111827', line_color='#374151'
      )
      fig_s, ax_s = pitch.draw(figsize=(7, 4.5))

      if not eq_shots.empty and 'shot_statsbomb_xg' in eq_shots.columns:
        pitch.scatter(
            eq_shots.x,
            eq_shots.y,
            s=eq_shots.shot_statsbomb_xg * 900 + 40,
            c='#00e5ff',
            alpha=0.75,
            edgecolors='white',
            ax=ax_s,
        )
      st.pyplot(fig_s)

    with c_map2:
      st.markdown(f'**🔥 Mapa de Calor / Densidad Ocupacional ({selected_eq})**')
      pitch = Pitch(
          pitch_type='statsbomb', pitch_color='#111827', line_color='#374151'
      )
      fig_k, ax_k = pitch.draw(figsize=(7, 4.5))

      try:
        pitch.kdeplot(
            eq_events.x,
            eq_events.y,
            ax=ax_k,
            cmap='inferno',
            fill=True,
            thresh=0.05,
            levels=100,
            alpha=0.7,
        )
      except:
        st.warning('Sin datos suficientes para estimación KDE.')
      st.pyplot(fig_k)

  # TAB 3: SCOUTING INDIVIDUAL
  with tab3:
    st.markdown('### 🔎 Scouting & Análisis de Perfil Individual')

    col_sel_eq, col_sel_pl = st.columns(2)
    scout_team = col_sel_eq.selectbox(
        '1. Equipo:', [home_team, away_team], key='scout_team_key'
    )

    players_list = sorted(
        list(
            events[events['team_name'] == scout_team]['player_name']
            .dropna()
            .unique()
        )
    )
    scout_player = col_sel_pl.selectbox(
        '2. Selecciona Jugador:', players_list, key='scout_player_key'
    )

    if scout_player:
      p_events = events[events['player_name'] == scout_player].copy()

      passes_p = p_events[p_events['type_name'] == 'Pass']
      passes_comp = passes_p[passes_p['outcome_name'].isnull()]
      shots_p = p_events[p_events['type_name'] == 'Shot']
      xg_p = (
          shots_p['shot_statsbomb_xg'].sum()
          if 'shot_statsbomb_xg' in shots_p.columns
          else 0.0
      )
      recovers_p = p_events[
          p_events['type_name'].isin(
              ['Ball Recovery', 'Interception', 'Tackle']
          )
      ]

      st.markdown(
          f"""
            <div class='player-card'>
                <h3 style='margin:0; color:#00e5ff;'>👤 {scout_player}</h3>
                <p style='margin:3px 0 0 0; color:#94a3b8; font-size:14px;'>{scout_team} | Eventos Registrados: <b>{len(p_events)}</b></p>
            </div>
        """,
          unsafe_allow_html=True,
      )

      pkpi1, pkpi2, pkpi3, pkpi4 = st.columns(4)
      pkpi1.metric(
          'Efectividad Pase',
          f'{(len(passes_comp)/max(len(passes_p),1))*100:.1f}%',
          f'{len(passes_comp)}/{len(passes_p)}',
      )
      pkpi2.metric('Disparos (xG)', len(shots_p), f'{xg_p:.2f} xG')
      pkpi3.metric('Recuperaciones', len(recovers_p))

      p_xt = calculate_xt(p_events)
      total_xt_p = p_xt['xT'].sum() if 'xT' in p_xt.columns else 0.0
      pkpi4.metric('xT Generado', f'{total_xt_p:.3f}')

      row1_c1, row1_c2 = st.columns(2)

      with row1_c1:
        st.markdown('**🎯 Mapa de Pases (Completados vs Incompletos)**')
        pitch = Pitch(
            pitch_type='statsbomb', pitch_color='#111827', line_color='#374151'
        )
        fig_pp, ax_pp = pitch.draw(figsize=(6, 4))

        if not passes_comp.empty:
          end_x_c = passes_comp.get(
              'end_x', passes_comp.get('pass_end_x', passes_comp['x'])
          )
          end_y_c = passes_comp.get(
              'end_y', passes_comp.get('pass_end_y', passes_comp['y'])
          )
          pitch.arrows(
              passes_comp.x,
              passes_comp.y,
              end_x_c,
              end_y_c,
              color='#00e5ff',
              ax=ax_pp,
              width=1.5,
              headwidth=3,
              label='Completados',
          )

        passes_inc = passes_p[passes_p['outcome_name'].notnull()]
        if not passes_inc.empty:
          end_x_i = passes_inc.get(
              'end_x', passes_inc.get('pass_end_x', passes_inc['x'])
          )
          end_y_i = passes_inc.get(
              'end_y', passes_inc.get('pass_end_y', passes_inc['y'])
          )
          pitch.arrows(
              passes_inc.x,
              passes_inc.y,
              end_x_i,
              end_y_i,
              color='#ff0055',
              ax=ax_pp,
              width=1.5,
              headwidth=3,
              label='Incompletos',
          )

        ax_pp.legend(
            facecolor='#111827', labelcolor='white', loc='lower left'
        )
        st.pyplot(fig_pp)

      with row1_c2:
        st.markdown('**🔥 Mapa de Calor e Intervención Espacial**')
        pitch = Pitch(
            pitch_type='statsbomb', pitch_color='#111827', line_color='#374151'
        )
        fig_pk, ax_pk = pitch.draw(figsize=(6, 4))
        try:
          pitch.kdeplot(
              p_events.x,
              p_events.y,
              ax=ax_pk,
              cmap='plasma',
              fill=True,
              thresh=0.05,
              levels=100,
              alpha=0.7,
          )
        except:
          st.info('Sin suficientes eventos para densidad KDE.')
        st.pyplot(fig_pk)

  # TAB 4: MODELO xT
  with tab4:
    st.markdown('### ⚡ Modelo de Peligro Esperado (xT)')

    passes_all_xt = calculate_xt(events)

    xt_c1, xt_c2 = st.columns([1, 2])

    with xt_c1:
      st.markdown('**Ranking Top Generadores de xT (Partido)**')
      ranking_xt = (
          passes_all_xt.groupby(['player_name', 'team_name'])['xT']
          .sum()
          .reset_index()
          .sort_values(by='xT', ascending=False)
      )
      ranking_xt.columns = ['Jugador', 'Equipo', 'xT Total']
      st.dataframe(
          ranking_xt.head(10), hide_index=True, use_container_width=True
      )

    with xt_c2:
      st.markdown('**Matriz Espacial xT y Pases de Mayor Impacto**')
      pitch = Pitch(
          pitch_type='statsbomb', pitch_color='#111827', line_color='#374151'
      )
      fig_xt, ax_xt = pitch.draw(figsize=(7, 4.5))

      ax_xt.imshow(
          XT_GRID,
          extent=[0, 120, 0, 80],
          origin='upper',
          cmap='OrRd',
          alpha=0.45,
          aspect='auto',
      )

      top_p_xt = passes_all_xt[passes_all_xt['xT'] > 0.015]
      if not top_p_xt.empty:
        end_x_xt = top_p_xt.get(
            'end_x', top_p_xt.get('pass_end_x', top_p_xt['x'])
        )
        end_y_xt = top_p_xt.get(
            'end_y', top_p_xt.get('pass_end_y', top_p_xt['y'])
        )
        pitch.arrows(
            top_p_xt.x,
            top_p_xt.y,
            end_x_xt,
            end_y_xt,
            color='#00e5ff',
            ax=ax_xt,
            width=1.8,
            headwidth=3.5,
        )
      st.pyplot(fig_xt)