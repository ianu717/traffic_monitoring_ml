import geohash2
import pandas as pd

from pathlib import Path
from traffic_monitoring_ml.config import SELECTED_FEATURES_PATH
from traffic_monitoring_ml.utils import get_day_period_from_time, load_json

MODEL_FEATURES = load_json(Path(SELECTED_FEATURES_PATH))

def build_accident_context(casualty, vehicle, collision):
    casualty = casualty.drop(columns=['collision_ref_no'])
    vehicle = vehicle.drop(columns=['collision_ref_no', 'collision_year'])
    collision = collision.drop(columns=['collision_ref_no', 'collision_year'])

    cas_veh = pd.merge(casualty, vehicle, on=['collision_index', 'vehicle_reference'], how='inner')
    accident = pd.merge(cas_veh, collision, on=['collision_index'], how='inner')

    return accident

def generate_day_period(accident):
    accident['day_period'] = accident['time'].apply(
        lambda x: get_day_period_from_time(x)
    )
    return accident

def generate_geo_hash(accident):
    accident["geo_hash"] = accident.apply(
        lambda x: geohash2.encode(x['latitude'], x['longitude'], precision=4), axis=1
    )
    return accident

def enrich_accident_context(accident):
    enriched = accident.copy()
    enriched = generate_day_period(enriched)
    enriched = generate_geo_hash(enriched)
    return enriched

def build_model_input(accident):
    return accident[MODEL_FEATURES]

def preprocess(casualty, vehicle, collision):
    #Se crea el contexto del accidente
    accident_context = build_accident_context(casualty, vehicle, collision)

    #Enriquecemos el contexto con nuevas features
    accident_context_enriched = enrich_accident_context(accident_context)

    #Construimos el input que recibirá el modelo
    model_input = build_model_input(accident_context_enriched)
    
    return model_input

