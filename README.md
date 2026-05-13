# 🚦 Sistema Predictivo de Severidad de Accidentes de Tráfico

Modelo de clasificación binaria para predecir la **severidad de accidentes de tráfico** a partir de datos contextuales del siniestro. Entrenado con datos históricos del dataset **STATS19** del Departamento de Transporte del Reino Unido (2019–2024) y desplegado como aplicación web interactiva con Streamlit.

---

## 📋 Índice

- [Descripción del proyecto](#descripción-del-proyecto)
- [Dataset](#dataset)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Stack tecnológico](#stack-tecnológico)
- [Instalación](#instalación)
- [Uso](#uso)
- [Notebooks](#notebooks)
- [Resultados del modelo](#resultados-del-modelo)
- [Contribuir](#contribuir)

---

## Descripción del proyecto

El objetivo del sistema es anticipar si las lesiones de un accidente de tráfico serán **leves** (*Slight*) o **graves** (*Serious/Fatal*) en el momento del siniestro, antes de que los servicios de emergencia lleguen al lugar. Esto permite una asignación de recursos más rápida y eficiente, especialmente en accidentes sin testigos presenciales.

El proyecto abarca todo el ciclo de vida del modelo:

- Ingesta y fusión de tres fuentes de datos (colisiones, víctimas y vehículos)
- Limpieza, análisis exploratorio e ingeniería de variables
- Selección de variables con *feature importance* y *permutation importance*
- Optimización de hiperparámetros con búsqueda bayesiana (Optuna)
- Ajuste del umbral de clasificación orientado a maximizar el recall en accidentes graves
- Despliegue del modelo en un dashboard interactivo (Streamlit)

---

## Dataset

Los datos provienen del sistema **STATS19**, la base de datos oficial del Departamento de Transporte del Reino Unido, que registra todos los accidentes de tráfico con víctimas notificados a la policía. Se utilizan registros del periodo **2019–2024**, estructurados en tres tablas relacionadas:

| Tabla | Descripción |
|---|---|
| `collision` | Datos del accidente: localización, condiciones de la vía, climatología, velocidad permitida |
| `casualty` | Datos de cada víctima: edad, sexo, clase, gravedad de las lesiones |
| `vehicle` | Características de los vehículos implicados: tipo, antigüedad, marca, cilindrada |

**Variable objetivo:** `casualty_severity` — recodificada como clasificación binaria: `Slight` (0) vs `Serious + Fatal` (1).

---

## Estructura del repositorio

```
traffic_monitoring_ml/
├── app/                        # Aplicación web Streamlit
├── data/
│   └── raw/                    # Datos en bruto (no versionados)
├── notebook/                   # Notebooks de análisis y modelado
│   ├── 01_eda_preprocessing.ipynb
│   ├── 02_feature_selection.ipynb
│   └── 03_modeling.ipynb
├── report/                     # Figuras e informes generados
├── src/
│   └── traffic_monitoring_ml/  # Paquete Python del proyecto
├── .gitignore
├── pyproject.toml              # Metadatos y dependencias del proyecto
├── poetry.lock
└── README.md
```

---

## Stack tecnológico

| Categoría | Librerías |
|---|---|
| Procesamiento de datos | `pandas`, `numpy`, `pyarrow` |
| Machine Learning | `scikit-learn`, `catboost` |
| Optimización de hiperparámetros | `optuna` |
| Codificación geoespacial | `geohash2` |
| Aplicación web | `streamlit` |
| Visualización | `matplotlib`, `seaborn`|

**Python:** `>=3.11, <=3.13` · **Gestor de paquetes:** [Poetry](https://python-poetry.org/)

---

## Instalación

### Requisitos previos

- Python 3.11–3.13
- [Poetry](https://python-poetry.org/docs/#installation)

### Pasos

1. **Clonar el repositorio**

```bash
git clone https://github.com/ianu717/traffic_monitoring_ml.git
cd traffic_monitoring_ml
```

2. **Instalar dependencias**

```bash
poetry install
```

3. **Activar el entorno virtual**

```bash
poetry shell
```

---

## Uso

### Aplicación web (Streamlit)

```bash
streamlit run app/main.py
```

El dashboard se abrirá en el navegador en `http://localhost:8501`.

### Notebooks

```bash
jupyter notebook notebook/
```

Los notebooks deben ejecutarse en orden (`01` → `02` → `03`), ya que cada uno genera artefactos que el siguiente consume.

---

## Notebooks

| Notebook | Contenido |
|---|---|
| `01_eda_preprocessing` | Carga y fusión de las tres tablas STATS19, análisis exploratorio, limpieza, ingeniería de variables (`geo_hash`, `day_period`) y división train/test por grupos |
| `02_feature_selection` | Selección iterativa de variables con *model importance* y *permutation importance* de CatBoost |
| `03_modeling` | Baseline con validación cruzada grupal, optimización de hiperparámetros con Optuna, entrenamiento del modelo final y ajuste del umbral de clasificación |

---

## Resultados del modelo

El modelo final es un **CatBoostClassifier** optimizado con Optuna y evaluado con `GroupKFold` (5 folds) para evitar la filtración de datos entre víctimas del mismo accidente.

| Métrica | Train | Test |
|---|---|---|
| AUC-ROC | 0.776 | **0.755** |
| Recall (Serious/Fatal) | — | 0.717 |
| Precision (Serious/Fatal) | — | 0.343 |

Dado que el coste de no detectar un accidente grave es mucho mayor que el de enviar recursos de forma preventiva, el umbral de clasificación se ajusta de **0.5 → 0.268** para alcanzar un recall del **95%** en la clase grave, asumiendo un mayor número de falsas alarmas.

---

**Autor:** Unai Riaño
