# Memoria del Proyecto — Sistema Predictivo de Severidad de Accidentes de Tráfico

---

## I. Introducción

### Contexto del problema y justificación

Los servicios de emergencia se enfrentan a un reto logístico crítico: cuando se produce un accidente de tráfico, la asignación de recursos (ambulancias, equipos médicos especializados) debe realizarse en cuestión de segundos, muchas veces sin información suficiente sobre la gravedad real del siniestro. En accidentes sin testigos presenciales o con comunicaciones incompletas, el tiempo perdido en esta valoración inicial puede tener consecuencias fatales.

El sistema actual depende en gran medida del criterio humano y de la información que facilitan los propios implicados, lo que introduce una variabilidad considerable. La disponibilidad de datos históricos estructurados de accidentes de tráfico abre la posibilidad de automatizar esta valoración inicial mediante modelos de aprendizaje automático, anticipando la severidad del accidente a partir del contexto registrado en el momento del suceso.

Este proyecto nace con la vocación de construir un sistema predictivo que pueda actuar como primer filtro de triaje, cubriendo automáticamente los accidentes sin testigos presenciales y reduciendo los tiempos de respuesta en los casos más críticos.

### Objetivos y alcance

El objetivo principal del proyecto es desarrollar un modelo de clasificación binaria que, dado el contexto de un accidente de tráfico (condiciones de la vía, características del vehículo, perfil de la víctima, etc.), sea capaz de predecir si la severidad de las lesiones es **leve** (*Slight*) o **grave** (*Serious/Fatal*).

El alcance del proyecto incluye:

- Ingesta, limpieza y preprocesamiento de datos históricos de accidentes de tráfico del Reino Unido (2019–2024).
- Análisis exploratorio de los datos y selección de variables predictoras.
- Entrenamiento, evaluación y optimización de modelos de clasificación.
- Ajuste del umbral de decisión orientado a maximizar el recall en accidentes graves.
- Despliegue de un dashboard interactivo (Streamlit) para visualizar predicciones en tiempo real.

---

## II. Dataset

### Descripción del dataset

Los datos utilizados proceden del sistema **STATS19**, la base de datos oficial del Departamento de Transporte del Reino Unido, que registra todos los accidentes de tráfico con víctimas notificados a la policía. Se han utilizado los registros correspondientes al periodo **2019–2024**.

El dataset está estructurado en tres tablas relacionadas que se combinan para obtener una visión completa de cada accidente:

- **Colisiones** (`collision`): contiene los datos del accidente en sí — localización geográfica (latitud, longitud), condiciones de la vía, climatología, velocidad permitida, tipo de cruce, etc.
- **Víctimas** (`casualty`): recoge información sobre cada persona involucrada — edad, sexo, clase de víctima (conductor, pasajero, peatón), gravedad de las lesiones.
- **Vehículos** (`vehicle`): describe las características de los vehículos implicados — tipo, antigüedad, marca, cilindrada.

Las tres tablas se relacionan a través de `collision_index` y `vehicle_reference`. El merge resultante genera una fila por víctima por accidente, lo que significa que **un mismo accidente puede dar lugar a varias filas** (tantas como víctimas haya tenido). Esta estructura jerárquica es uno de los retos metodológicos principales del proyecto y condiciona toda la estrategia de validación.

### Análisis exploratorio de los datos (EDA)

El primer análisis pone de manifiesto un **desbalanceo de clases significativo** en la variable objetivo `casualty_severity`:

| Clase | Proporción |
|---|---|
| Slight (leve) | 79.8% |
| Serious (grave) | 18.3% |
| Fatal | 1.9% |

Dado el desequilibrio entre clases y la escasa representación de la clase *Fatal*, se toma la decisión de **reformular el problema como clasificación binaria**, agrupando *Serious* y *Fatal* en una única clase positiva. La distribución resultante es:

| Clase | Proporción |
|---|---|
| Slight | 79.8% |
| Serious + Fatal | 20.2% |

Este desbalanceo se tiene en cuenta durante el modelado, configurando `auto_class_weights='Balanced'` en CatBoost para penalizar más los errores sobre la clase minoritaria.

---

## III. Preprocesamiento de los datos

### Verificación de la calidad de los datos

Tras el merge de las tres tablas, se realiza un análisis de valores nulos. Las filas con valores ausentes representan una proporción manejable y se opta por eliminarlas directamente (`dropna()`), dado que su volumen no compromete la representatividad del dataset.

Se identifica también la presencia del valor `-1` como codificación de "desconocido" o "sin datos" en muchas columnas categóricas. Se revisa la proporción de estos valores variable a variable y se descartan aquellas con una concentración excesiva de `-1` que las haría prácticamente inservibles como predictores.

### Decisiones, imputaciones y transformación de variables

**Eliminación de columnas no informativas o problemáticas** — Se identifican y descartan seis grupos de variables:

- **Históricas**: derivadas de agregaciones pasadas que podrían producir *data leakage*.
- **Directamente relacionadas con el target**: columnas que contienen información derivada de la severidad del accidente (e.g., `collision_severity`, `enhanced_casualty_severity`).
- **Identificadores y referencias**: códigos únicos sin valor predictivo (`casualty_reference`, `vehicle_reference`, `collision_year`).
- **Alta cardinalidad**: variables geográficas o de texto libre con demasiados valores únicos (`lsoa_of_casualty`, `generic_make_model`, `local_authority_district`...).
- **Alto porcentaje de desconocidos**: columnas donde el valor `-1` representa una proporción significativa (`junction_control`, `age_of_vehicle`, `propulsion_code`...).
- **No disponibles en inferencia**: variables que, aunque tienen capacidad predictiva, no estarían disponibles en el momento de predecir en producción (datos administrativos post-accidente, índices de deprivación del conductor/víctima, etc.). Incluirlas introduciría *data leakage* y haría el modelo no desplegable.

**Ingeniería de variables** — Se crean dos nuevas variables a partir de los datos existentes:

- `geo_hash`: codificación geoespacial basada en [GeoHash2](https://github.com/vinsci/geohash/) aplicada sobre latitud y longitud con precisión 4. Agrupa zonas geográficas con patrones de accidentalidad similares capturando el contexto espacial sin incurrir en alta cardinalidad.
- `day_period`: discretización de la hora exacta del accidente en cuatro franjas horarias (noche 21–06h, mañana 06–12h, mediodia 12–17h, tarde 17–21h). Reduce el ruido de la hora exacta manteniendo el patrón temporal.

**Agrupación de edades** — Se eliminan las edades exactas (`age_of_casualty`, `age_of_driver`) y se conservan únicamente sus versiones agrupadas por bandas, reduciendo el riesgo de sobreajuste a edades con poca representación.

**División train/test respetando grupos** — Este es el punto metodológico más delicado del proyecto. Dado que cada accidente puede tener múltiples víctimas (filas), una división aleatoria estándar puede dejar víctimas del mismo accidente en train y en test simultáneamente, inflando artificialmente las métricas al filtrar contexto del accidente.

Para evitarlo, se usa `GroupShuffleSplit` con `collision_index` como grupo, garantizando que **todas las víctimas de un mismo accidente queden íntegramente en el mismo conjunto**. La división resultante es 80% train / 20% test.

---

## IV. Modelado

### Selección del algoritmo

Se elige **CatBoostClassifier** como algoritmo principal por las siguientes razones:

- Manejo nativo de variables categóricas sin necesidad de *encoding* manual, lo que encaja perfectamente con la naturaleza del dataset (numerosas variables categóricas codificadas).
- Robustez frente a valores desconocidos y datos ruidosos.
- Menor tendencia al sobreajuste respecto a otras implementaciones de *gradient boosting* gracias a su técnica de *ordered boosting*.
- Alto rendimiento en conjuntos de datos tabulares heterogéneos.

### Selección de variables (Feature Selection)

Antes de optimizar hiperparámetros, se realiza una selección iterativa de variables utilizando dos métricas complementarias sobre un modelo preliminar de CatBoost:

- **Model Importance (importancia intrínseca)**: mide la contribución de cada variable a las divisiones del árbol durante el entrenamiento.
- **Permutation Importance (`LossFunctionChange`)**: permuta aleatoriamente cada variable sobre el conjunto de validación y mide la caída en AUC. Es más robusta frente a correlaciones entre *features* y se considera la métrica principal para la selección.

Se eliminan iterativamente las variables menos relevantes según ambas métricas, reentrenando el modelo en cada iteración hasta llegar a un conjunto estable de predictores. En todos los splits de validación durante esta fase se respeta la estructura de grupos (`GroupShuffleSplit`) para evitar filtración.

Las variables con mayor importancia de permutación son principalmente características del tipo de víctima, condiciones de la vía y características del vehículo.

### Evaluación de modelos e iteraciones

**Baseline con validación cruzada** — Se establece un modelo base con los hiperparámetros por defecto usando `GroupKFold` con 5 folds, respetando la estructura de grupos por `collision_index`. Este modelo base proporciona el punto de referencia para comparar mejoras.

**Optimización de hiperparámetros con Optuna** — Se utiliza Optuna con el sampler TPE (*Tree-structured Parzen Estimator*) para búsqueda bayesiana eficiente. Para acelerar la búsqueda, se trabaja sobre una muestra representativa del 50% del train manteniendo la estructura de grupos. Se ejecutan **20 trials** optimizando el AUC en validación cruzada grupal (GroupKFold con 2 folds).

Los parámetros explorados y sus rangos son:

| Parámetro | Rango | Descripción |
|---|---|---|
| `learning_rate` | 0.05 – 0.3 (log) | Tasa de aprendizaje del boosting |
| `depth` | 4 – 10 | Profundidad máxima de los árboles |
| `l2_leaf_reg` | 1 – 10 | Regularización L2 en las hojas |
| `bagging_temperature` | 0 – 1 | Aleatoriedad en el muestreo de filas |
| `random_strength` | 0 – 1 | Fuerza de perturbación en los splits |

Los mejores hiperparámetros encontrados son:

```
learning_rate:        0.0511
depth:                7
l2_leaf_reg:          3.654
bagging_temperature:  0.292
random_strength:      0.343
```

Estos parámetros se validan con `GroupKFold` de 5 folds sobre el conjunto de entrenamiento completo antes de entrenar el modelo final.

### Selección e interpretación del modelo final

El modelo final se entrena con los hiperparámetros optimizados por Optuna, usando `early_stopping_rounds=10` sobre un set de validación interno (20% del train, dividido por grupos). Se usa `auto_class_weights='Balanced'` para compensar el desbalanceo de clases.

---

## V. Predicción y resultados finales

### Evaluación del modelo

El modelo final alcanza los siguientes resultados sobre el conjunto de test (no visto durante el entrenamiento ni la optimización):

| Métrica | Train | Test |
|---|---|---|
| AUC-ROC | 0.776 | **0.755** |
| Recall (Serious/Fatal) | — | 0.717 |
| Precision (Serious/Fatal) | — | 0.343 |

La diferencia de AUC entre train y test es de **0.021**, lo que indica una generalización correcta sin sobreajuste significativo. Este resultado se obtiene respetando íntegramente la estructura de grupos, evitando que víctimas del mismo accidente aparezcan simultáneamente en train y test.

Con el umbral por defecto (0.5):
- El modelo detecta el **71.7% de los accidentes graves** (recall de la clase positiva).
- De cada 3 alertas de severidad alta, aproximadamente **2 son falsas alarmas** (precision del 34.3%).
- De 25.775 accidentes graves en el conjunto de test, el modelo falla en detectar 7.540.

### Ajuste del umbral de decisión

En un sistema de emergencias médicas, **no detectar un accidente grave es mucho más costoso que enviar recursos de forma preventiva**. Bajo esta premisa, se ajusta el umbral de clasificación desde el valor por defecto (0.5) hasta **0.268**, con el objetivo de alcanzar un recall del 95% en la clase grave.

| Umbral | Recall (grave) | Precision (grave) |
|---|---|---|
| 0.50 (defecto) | 0.717 | 0.343 |
| **0.268 (ajustado)** | **0.950** | **~0.20** |

Con el umbral ajustado, el sistema envía recursos preventivos con mayor frecuencia cuando no es estrictamente necesario, pero reduce considerablemente el riesgo de dejar sin atención inmediata a una víctima grave. Esta decisión está alineada con la lógica de un sistema de triaje donde el coste del falso negativo supera con creces al del falso positivo.

### Impacto en el negocio

El sistema permite cubrir automáticamente la valoración inicial de gravedad en accidentes sin testigos presenciales, reduciendo los tiempos de asignación de recursos en los casos más críticos. El dashboard interactivo desplegado con Streamlit permite a los operadores consultar las predicciones del modelo en tiempo real, facilitando la toma de decisiones bajo presión.

---

## VI. Conclusiones y futuros pasos

### Análisis de los resultados

El proyecto demuestra que es posible predecir la severidad de accidentes de tráfico con una capacidad discriminante razonable (AUC 0.755) a partir de datos disponibles en el momento del suceso, sin acceso a información post-accidente ni variables con data leakage.

**Fortalezas del proyecto:**

- Tratamiento riguroso del data leakage en todas las fases, especialmente en la división de datos y la validación cruzada mediante `GroupShuffleSplit` y `GroupKFold`.
- Pipeline reproducible y modular, con separación clara entre preprocesamiento, selección de variables y modelado.
- Ajuste del umbral orientado al caso de uso real, priorizando el recall sobre la precisión en un contexto de emergencias.
- Selección de variables con doble métrica de importancia (model importance + permutation importance), lo que aporta robustez frente a correlaciones espurias.

**Debilidades y limitaciones:**

- El dataset tiene un componente inherente de aleatoriedad: muchos accidentes graves ocurren en circunstancias aparentemente normales, lo que limita el techo del modelo.
- Algunos datos de alta relevancia no están disponibles públicamente por razones de privacidad (datos del Departamento de Tráfico no publicados), lo que restringe la capacidad predictiva.
- El precision con el umbral ajustado es bajo (~0.20), lo que implica un volumen elevado de falsas alarmas que los servicios de emergencia deben gestionar.
- El modelo está entrenado con datos del Reino Unido (STATS19) y su transferibilidad a otros países o sistemas de registro no está garantizada.

### Propuesta de futuras mejoras

- **Datos en tiempo real**: integrar señales de sensores de tráfico, datos meteorológicos en tiempo real o cámaras de circuito cerrado para enriquecer el contexto del accidente con información más precisa y actualizada.
- **Modelos multimodales**: explorar arquitecturas que combinen datos tabulares con datos de imagen (fotografías del accidente, imágenes satelitales de la vía) o señales de tiempo real para mejorar la capacidad predictiva.
- **Calibración de probabilidades**: aplicar calibración (Platt Scaling, Isotonic Regression) para que las probabilidades de salida del modelo sean más interpretables y fiables como puntuaciones de riesgo continuas.
- **Actualización continua del modelo**: implementar un pipeline de reentrenamiento periódico con nuevos datos de STATS19, dado que los patrones de tráfico y accidentalidad evolucionan con el tiempo.
- **Análisis de subgrupos**: estudiar el rendimiento del modelo por tipo de vía, zona geográfica o franja horaria para identificar segmentos donde el modelo es menos fiable y mejorar su equidad predictiva.
