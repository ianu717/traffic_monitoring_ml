# 🚦 Traffic Monitoring ML

![Badge Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Badge Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter&logoColor=white)
![Badge License](https://img.shields.io/badge/license-MIT-green)
![Badge Status](https://img.shields.io/badge/status-Active-brightgreen)
![Badge Poetry](https://img.shields.io/badge/Poetry-1.4+-blue?logo=poetry&logoColor=white)

Un proyecto de **Machine Learning** para monitoreo, análisis y predicción de patrones de tráfico vehicular utilizando técnicas avanzadas de ciencia de datos.

---

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
- [Metodología](#metodología)
- [Resultados](#resultados)
- [Tecnologías](#tecnologías)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## 📊 Descripción General

Este proyecto implementa un **sistema de análisis y predicción de tráfico vehicular** utilizando algoritmos de Machine Learning. El objetivo es identificar patrones, predecir congestiones futuras y proporcionar insights accionables para la optimización de sistemas de transporte urbano.

**Aplicaciones:**
- 🚗 Predicción de congestiones
- 📈 Análisis de patrones temporales
- 🎯 Optimización de rutas
- ⚠️ Detección de anomalías
- 📊 Reportes y dashboards

---

## ✨ Características

- ✅ **Análisis Exploratorio de Datos (EDA)**: Visualización completa de patrones de tráfico
- ✅ **Preprocesamiento Avanzado**: Limpieza, normalización e ingeniería de features
- ✅ **Modelos Predictivos**: Implementación de múltiples algoritmos ML
- ✅ **Validación Rigurosa**: Cross-validation y evaluación de rendimiento
- ✅ **Visualizaciones Profesionales**: Gráficos interactivos y análisis visual
- ✅ **Documentación Completa**: Notebooks bien comentados y estructurados
- ✅ **Reproducibilidad**: Pipeline reproducible y parametrizable
- ✅ **Gestión de Dependencias con Poetry**: Entorno aislado y reproducible

---

## 🔧 Requisitos Previos

Asegúrate de tener instalado:
- **Python 3.8+**
- **Poetry 1.4+** - [Instalar Poetry](https://python-poetry.org/docs/#installation)
- **Git** (para clonar el repositorio)

### Instalar Poetry

```bash
# En macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# En Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# O usar pip
pip install poetry
```

---

## 📦 Instalación

### Con Poetry (Recomendado) ⭐

```bash
# Clonar el repositorio
git clone https://github.com/ianu717/traffic_monitoring_ml.git
cd traffic_monitoring_ml

# Instalar dependencias y crear entorno virtual
poetry install

# Activar el entorno virtual
poetry shell
```

### Ejecutar comandos sin activar el entorno

```bash
# Ejecutar Jupyter dentro del entorno de Poetry
poetry run jupyter notebook

# Ejecutar un script Python
poetry run python script.py
```

### Agregar nuevas dependencias

```bash
# Añadir una librería de producción
poetry add numpy pandas

# Añadir una librería de desarrollo
poetry add --group dev pytest black flake8
```

### Actualizar dependencias

```bash
# Actualizar todas las dependencias
poetry update

# Actualizar una dependencia específica
poetry update numpy
```

---

## 📁 Estructura del Proyecto

```
traffic_monitoring_ml/
│
├── 📓 01_exploratory_data_analysis.ipynb
│   └── Análisis inicial, visualización y estadísticas descriptivas
│
├── 📓 02_data_preprocessing.ipynb
│   └── Limpieza, normalización e ingeniería de features
│
├── 📓 03_model_development.ipynb
│   └── Entrenamiento y evaluación de modelos
│
├── 📓 04_predictions_and_insights.ipynb
│   └── Predicciones finales y análisis de resultados
│
├── 📊 data/
│   ├── raw/                    # Datos originales sin procesar
│   └── processed/              # Datos preprocessados
│
├── 🎨 visualizations/          # Gráficos y outputs visuales
│
├── 💾 models/                  # Modelos entrenados (.pkl, .h5)
│
├── 📄 README.md               # Este archivo
│
├── 📋 pyproject.toml          # Configuración de Poetry y dependencias
│
├── 📝 poetry.lock             # Lock file con versiones exactas
│
└── 📝 NOTES.md               # Notas técnicas adicionales (opcional)
```

---

## 🚀 Uso

### Ejecución Rápida

1. **Descarga el repositorio:**
   ```bash
   git clone https://github.com/ianu717/traffic_monitoring_ml.git
   cd traffic_monitoring_ml
   ```

2. **Instala las dependencias con Poetry:**
   ```bash
   poetry install
   ```

3. **Activa el entorno y abre Jupyter:**
   ```bash
   poetry shell
   jupyter notebook
   ```

4. **Ejecuta los notebooks secuencialmente:**
   - `01_exploratory_data_analysis.ipynb`
   - `02_data_preprocessing.ipynb`
   - `03_model_development.ipynb`
   - `04_predictions_and_insights.ipynb`

### Ejecución en Script Python

```bash
# Dentro del entorno de Poetry
poetry run python script.py

# O después de activar el entorno
poetry shell
python script.py
```

Ejemplo de script:

```python
# Ejemplo básico de uso
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Cargar datos
df = pd.read_csv('data/raw/traffic_data.csv')

# Procesar datos
# ... (ver notebooks para detalles)

# Entrenar modelo
# ... (implementación en notebooks)
```

---

## 🔬 Metodología

### Pipeline de ML

```
┌─────────────────┐
│  Datos Crudos   │
└────────┬────────┘
         │
┌────────▼────────┐
│    EDA          │  📊 Análisis y Visualización
└────────┬────────┘
         │
┌────────▼────────┐
│  Preprocesado   │  🧹 Limpieza y Feature Engineering
└────────┬────────┘
         │
┌────────▼────────┐
│  Modelamiento   │  🤖 Entrenamiento y Evaluación
└────────┬────────┘
         │
┌────────▼────────┐
│  Predicciones   │  🎯 Resultados e Insights
└─────────────────┘
```

### Técnicas Utilizadas

- **Análisis Exploratorio**: Estadísticas descriptivas, correlaciones, distribuciones
- **Feature Engineering**: Creación de features temporales, estacionales y derivadas
- **Modelos Implementados**:
  - Regresión Lineal
  - Random Forest
  - Gradient Boosting (XGBoost/LightGBM)
  - Redes Neuronales (si aplica)
- **Validación**: K-Fold Cross-Validation, Train/Test Split
- **Métricas**: MAE, RMSE, R², precisión, recall, F1-Score

---

## 📈 Resultados

*(Actualiza esta sección con tus resultados específicos)*

| Modelo | MAE | RMSE | R² Score | Notas |
|--------|-----|------|----------|-------|
| Baseline (Media) | X.XX | X.XX | X.XX | Predicción simple |
| Regresión Lineal | X.XX | X.XX | X.XX | Modelo base |
| Random Forest | X.XX | X.XX | X.XX | Buen balance |
| XGBoost | X.XX | X.XX | X.XX | 🏆 Mejor rendimiento |

### Insights Principales

- 🔍 **Hallazgo 1**: [Describe un patrón o insight importante]
- 🔍 **Hallazgo 2**: [Describe otro insight]
- 🔍 **Hallazgo 3**: [Describe conclusiones relevantes]

---

## 🛠️ Tecnologías

### Librerías Principales (ver `pyproject.toml` para versiones)

```
pandas            # Manipulación de datos
numpy             # Computación numérica
scikit-learn      # Machine Learning
matplotlib        # Visualización estática
seaborn           # Visualización estadística
jupyter           # Notebooks interactivos
```

### Librerías Adicionales (según necesidad)

```
xgboost           # Gradient Boosting avanzado
lightgbm          # Light Gradient Boosting
tensorflow        # Deep Learning
plotly            # Visualización interactiva
statsmodels       # Análisis estadístico
```

Ver `pyproject.toml` para la lista completa de dependencias con sus versiones exactas.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios significativos:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Instala las dependencias: `poetry install`
4. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
5. Push a la rama (`git push origin feature/AmazingFeature`)
6. Abre un Pull Request

---

## 📚 Referencias y Recursos

- [Documentación Poetry](https://python-poetry.org/docs/)
- [Documentación Scikit-learn](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Machine Learning Best Practices](https://developers.google.com/machine-learning/guides)
- [Time Series Forecasting](https://otexts.com/fpp2/)

---

## 📝 Autor

**Ian U.** - [@ianu717](https://github.com/ianu717)

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Ver el archivo `LICENSE` para más detalles.

---

## 📞 Contacto

Para preguntas o sugerencias sobre el proyecto:
- 📧 Email: [Tu email]
- 💼 LinkedIn: [Tu LinkedIn]
- 🐙 GitHub: [@ianu717](https://github.com/ianu717)

---

## ⭐ Soporte

Si este proyecto te fue útil, ¡considera darle una estrella! ⭐

```
  ⭐ Si te resulta útil este proyecto, apreciaré tu apoyo
```

---

**Última actualización**: Mayo 2026
