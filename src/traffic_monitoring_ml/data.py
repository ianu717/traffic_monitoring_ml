import pandas as pd
from .config import BASE_DIR

PATH_DATA_VALUES = f'{BASE_DIR}/data/raw/uk-road-safety-dataset-guide-2024.xlsx'

def create_data_map(table: str, field_names: list) -> dict[int, str]:
    data_values = pd.read_excel(PATH_DATA_VALUES)
    table_values = data_values.loc[data_values['table'] == table].dropna(subset='code/format')
    values_map = {}
    for field_name in field_names:
        codes = table_values.loc[table_values['field name'] == field_name, 'code/format']
        values = table_values.loc[table_values['field name'] == field_name, 'label']
        mapped_codes = dict(zip(codes, values))
        if len(mapped_codes) > 0:
            values_map[field_name] = mapped_codes
    return values_map
