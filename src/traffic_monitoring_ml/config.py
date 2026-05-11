from pathlib import Path

# PROJECT ROOT (3 levels from this file)
BASE_DIR = Path(__file__).resolve().parents[2]

# DIRS
DATA_DIR = BASE_DIR / 'data'
DATA_PROCESSED_DIR = DATA_DIR / 'processed'
DATA_MAP_DIR = DATA_DIR / 'map'
NOTEBOOKS_DIR = BASE_DIR / 'notebooks'
MODELS_DIR = BASE_DIR / 'model'
MODEL_METRICS_DIR = MODELS_DIR / 'metrics'

#DATA SOURCE URLS
COLLISION_CSV_URL = 'https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-last-5-years.csv'
VEHICLE_CSV_URL = 'https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-vehicle-last-5-years.csv'
CASUALTY_CSV_URL = 'https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-casualty-last-5-years.csv'

# MAP FILES PATHS
COLLISION_VALUE_MAP_PATH = DATA_MAP_DIR / "collision_value_map.pkl"
VEHICLE_VALUE_MAP_PATH = DATA_MAP_DIR / "vehicle_value_map.pkl"
CASUALTY_VALUE_MAP_PATH = DATA_MAP_DIR / "casualty_value_map.pkl"

# DATA SPLIT FILES PATHS
X_TRAIN_PATH = DATA_PROCESSED_DIR / 'X_train.parquet'
X_TEST_PATH = DATA_PROCESSED_DIR / 'X_test.parquet'
Y_TRAIN_PATH = DATA_PROCESSED_DIR / 'Y_train.parquet'
Y_TEST_PATH = DATA_PROCESSED_DIR / 'Y_test.parquet'
GROUPS_TRAIN_PATH = DATA_PROCESSED_DIR / "groups_train.parquet"

#FEATURE FILES PATHS
SELECTED_FEATURES_PATH = DATA_PROCESSED_DIR / 'selected_features.json'

#MODEL PATHS
CATBOOST_MODEL_PATH = MODELS_DIR / 'severity_classifier.cbm'

#METRICS FILE PATHS
BEST_PARAMETERS_PATH = MODEL_METRICS_DIR / 'best_parameters.pkl'