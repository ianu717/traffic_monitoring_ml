import streamlit as st
import pandas as pd

from service import SeverityInferenceService

severity_inference_service = SeverityInferenceService()

casualty = pd.read_parquet('mock_data/casualty_replaced.parquet')
vehicle = pd.read_parquet('mock_data/vehicle_replaced.parquet')
collision = pd.read_parquet('mock_data/collision_replaced.parquet')
collision_indexes = pd.read_parquet('mock_data/collision_indexes.parquet')

scenario_generated = False

#STYLE
st.markdown('''
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

div[data-testid="stMetric"] {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
}

h1, h2, h3 {
    letter-spacing: -0.5px;
}
</style>
''', unsafe_allow_html=True)

#PAGE CONFIG
st.set_page_config(
    page_title='Predicción de Severidad de Accidentes',
    layout='wide',
    initial_sidebar_state='expanded',
    page_icon='🚗',
)

#MAIN CONTENT
st.title('Monitorización de seguridad vial')

st.markdown('''
Este sistema permanece a la escucha de eventos de accidente de tráfico. 
Cuando se detecta una colisión, recopila la información contextual 
disponible (colisión, vehículos implicados y víctimas) a través de un servicio externo y, 
mediante un modelo de Machine Learning, genera una predicción de la severidad estimada del accidente, 
mostrando posteriormente un informe con el resultado.
''')

st.divider()

#SIDEBAR
st.sidebar.markdown('---')
st.sidebar.caption(
    'Configuración del modelo de inferencia'
)
st.sidebar.info(
    'El umbral determina a partir de qué probabilidad'
    'el accidente se clasifica como grave.'
)
threshold = st.sidebar.slider(label='Umbral de probabilidad', min_value=0.0, max_value=1.0, value=0.5, step=0.0001)


if st.sidebar.button('Generar evento', use_container_width=True):
    severity_inference_service.threshold = threshold

    #Generar accidente
    collision_index = collision_indexes.sample(1)[0].iloc[0]
    casualties = casualty[casualty['collision_index'] == collision_index]
    vehicles = vehicle[vehicle['collision_index'] == collision_index]
    collisions = collision[collision['collision_index'] == collision_index]

    #Predicción del modelo
    prediction = severity_inference_service.predict_from_context(
        casualty_df=casualties, vehicle_df=vehicles, collision_df=collisions,
    )

    st.header('Accidente detectado')

    #Métricas principales
    col1, col2, col3 = st.columns(3)

    with col2:
        st.metric(
            'Probabilidad de gravedad',
            f'{prediction["severity_probability"]:.1%}'
        )

    with col3:
        st.metric(
            'Umbral configurado',
            f'{threshold:.0%}'
        )

    with col1:
        severity_prob = prediction['severity_probability']
        if severity_prob < threshold:
            bg_color = '#14532d'
            border_color = '#22c55e'
            text = '🟢 Riesgo Bajo'

        else:
            bg_color = '#7f1d1d'
            border_color = '#ef4444'
            text ='🔴 Riesgo Alto'

        st.markdown(
            f'''
                    <div style="
                        background-color: {bg_color};
                        border-radius: 12px;
                        border-left: 8px solid {border_color};
                        padding: 20px;
                        min-height: 115px;
                    ">
                        <h3 style="color: white; margin: 0;">
                            {text}
                        </h3>
                    </div>
                    ''',
            unsafe_allow_html=True
        )
        st.progress(min(severity_prob, 1.0))

    #Información técnica
    with st.expander('Ver información detallada'):
        st.caption('Colisión')
        st.dataframe(collisions[[
            'date',
            'day_of_week',
            'time',
            'local_authority_district',
            'local_authority_highway',
            'first_road_class',
            'speed_limit',
            'weather_conditions',
            'road_surface_conditions',
            'carriageway_hazards',
            'urban_or_rural_area',
        ]], hide_index=True)

        st.caption('Vehiculo')
        st.dataframe(vehicles[[
            'vehicle_type',
            'vehicle_manoeuvre',
            'skidding_and_overturning',
            'hit_object_in_carriageway',
            'vehicle_leaving_carriageway',
            'hit_object_off_carriageway',
            'first_point_of_impact',
            'propulsion_code',
            'generic_make_model',
        ]], hide_index=True)

        st.caption('Victima')
        st.dataframe(casualties[[
            'age_band_of_casualty',
            'casualty_type',
            'sex_of_casualty'
        ]], hide_index=True)

    #Ubicación en el mapa
    map_df = pd.DataFrame(
        data={
            'lat': collisions['latitude'],
            'lon': collisions['longitude']
        }
    )
    with st.container(border=True):
        st.caption(
            'Ubicación aproximada del accidente'
        )
        st.map(map_df, zoom=13)



    scenario_generated = True

if not scenario_generated:

    st.markdown('''
    <div style="
        padding: 60px;
        border: 1px solid #374151;
        border-radius: 16px;
        text-align: center;
        margin-top: 60px;
        background-color: #111827;
    ">
        <h2 style="margin-bottom: 10px;">
            Esperando evento...
        </h2>
        <p style="color: #9ca3af;font-size: 16px;">
            Ajuste el umbral de probabilidad y genere un escenario
            desde el panel lateral para comenzar el análisis.
        </p>
    </div>
    ''', unsafe_allow_html=True)