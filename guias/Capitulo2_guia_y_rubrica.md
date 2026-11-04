# Capítulo 2 del proyecto integrador · Guía y rúbrica

**Modelación Sísmica y Tsunami (IRD-505) · Unidad 2: Modelación de desplazamientos verticales**
Ingeniería en Riesgos de Desastres · ESPAM MFL · Docente: Ing. Cristian Paliz Acosta, MSc.

Cuaderno: [`cuadernos/Cap2_deformacion_cosismica.ipynb`](../cuadernos/Cap2_deformacion_cosismica.ipynb) · [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/Cap2_deformacion_cosismica.ipynb)

---

## 1. Propósito

En el Capítulo 1 describieron la fuente de su sismo con una ficha (un rectángulo uniforme). En el Capítulo 2 modelan la **deformación cosísmica** de su evento con una fuente realista y entregan la **condición inicial del tsunami** para las Unidades 3 y 4.

**Resultado de aprendizaje B (Aplicar):** modelar los desplazamientos verticales producidos por un sismo mediante el modelo de dislocación elástica de Okada (1985), a partir de modelos de falla finita y de los parámetros de la fuente, y evaluar el resultado frente a observaciones.

**Habilidad transversal: resolución de problemas complejos.** El problema tiene información incompleta, modelos que no son únicos y supuestos que cambian el resultado. Se trabaja con la **bitácora de decisiones**, el **diagnóstico de la anomalía** y el **cierre metacognitivo** del cuaderno (marcados con 🧭), y se evalúa con el criterio 6 de la rúbrica.

Desde este capítulo cada grupo trabaja **solo con su evento y su localidad**. Pedernales 2016 fue el caso comparativo del Capítulo 1.

## 2. Qué hacen

| Paso del cuaderno | Contenido | Producto para el capítulo |
|---|---|---|
| P | Predicción razonada antes de calcular | Tabla de predicción |
| 0 | Datos del evento: tensor de momento y falla finita del USGS | Mapa de deslizamiento |
| 1 | Geometría de la falla en profundidad | Corte por la localidad |
| 2 | Rectángulo uniforme frente a falla finita | Mapas, perfil y tabla de métricas |
| 3 | Rigidez variable con la profundidad · 🧭 Decisión 1 | Perfil con μ(z) y decisión justificada |
| 4 | Cinemática de la ruptura | Figura de 4 instantes y GIF |
| 5 | Aporte horizontal y filtro de Kajiura · 🧭 Decisión 2 | Mapas de uz, uh y η0; fuente elegida |
| 6 | Validación con observaciones · 🧭 Decisión 3 y diagnóstico | RMSE, gráfico 1:1 y prueba de hipótesis |
| 7 | Sensibilidad | Gráfico de tornado |
| 8 | Predicción frente a modelo · 🧭 Cierre metacognitivo | Tabla comparativa y reflexión |
| 9 | Exportación | Paquete `modelo_U2` (.zip) |

## 3. Estructura del Capítulo 2 (informe)

La numeración continúa la del proyecto integrador (figura 2.1, tabla 2.1…).

- **2.1 Introducción.** Evento, localidad y **pregunta guía** del capítulo (aparece al inicio del cuaderno).
- **2.2 Datos y geometría de la fuente.** Tensor de momento y falla finita (origen, identificador del USGS, número de subfallas, deslizamiento máximo y medio, profundidades). Corte en profundidad e interpretación de la interfase.
- **2.3 Modelación de la deformación.** Fundamento (Okada, superposición). Comparación uniforme frente a falla finita: mapas, perfil y tabla de métricas.
- **2.4 Rigidez y cinemática.** Efecto de μ(z) con su justificación. Dirección y duración de la ruptura; validez de la aproximación instantánea.
- **2.5 Del fondo marino a la superficie del mar.** Aporte horizontal, filtro de Kajiura y descripción de η0 frente a su localidad.
- **2.6 Validación y sensibilidad.** Observaciones usadas (con fuente), RMSE, gráfico 1:1, diagnóstico de la anomalía y gráfico de tornado.
- **2.7 Proceso de resolución.** Bitácora de las tres decisiones, diagnóstico (anomalía, hipótesis, prueba, resultado) y cierre metacognitivo. Tabla de predicción frente a modelo.
- **2.8 Conclusiones.** Respuesta a la pregunta guía y fuente que se entrega a la Unidad 3, con sus limitaciones.
- **Anexo 2.A.** Paquete `modelo_U2` (.zip) y `resumen_U2.json`.

**Reglas de datos:** cada cifra externa lleva su fuente (USGS con identificador del evento, artículo con autor y año). Las figuras se generan con el cuaderno; no se aceptan figuras copiadas de artículos como resultado propio. Los valores de observación sin fuente citable no cuentan para la validación.

## 4. Evaluación

La evaluación de la unidad es un **momento de aprendizaje**: la formativa se gana por intentar y por trabajar la retroalimentación; la sumativa incorpora esa retroalimentación.

| Momento | Qué se entrega | Puntos | Fecha (propuesta, por confirmar) |
|---|---|---|---|
| **Formativa** | Avance: Pasos P a 4 del cuaderno, Decisión 1 de la bitácora y borrador de 2.1–2.3 | 2 | Jueves 26 de noviembre (sesión virtual) |
| **Sumativa** | Capítulo 2 completo + paquete `modelo_U2` + tabla de respuesta a la retroalimentación | 8 | Martes 1 de diciembre (sesión presencial) |

**Formativa (2 puntos).** 1 punto por entregar el avance completo en el plazo; 1 punto por responder a la retroalimentación en la sumativa (tabla «observación recibida → qué cambiamos»).

### Rúbrica de la sumativa (8 puntos)

Niveles: **Excelente** (100 % del puntaje del criterio) · **Satisfactorio** (75 %) · **En desarrollo** (50 %) · **Inicial** (25 %) · **No presenta** (0).

| # | Criterio | Pts | Excelente | Satisfactorio | En desarrollo | Inicial |
|---|---|---|---|---|---|---|
| 1 | **Datos y geometría de la fuente** (2.2) | 1,0 | Describe la falla finita con su origen y limitaciones; interpreta el corte (fosa, buzamiento por tramos, relación con su ficha) con cifras | Describe la falla finita y el corte con cifras, con interpretación parcial | Describe datos sin interpretar la geometría o sin cifras | Copia la salida del cuaderno sin descripción |
| 2 | **Modelación uniforme frente a falla finita** (2.3) | 1,5 | Explica las diferencias (máximo, hundimiento, línea de cero, fracción en el mar) con el principio de superposición y la distancia a la falla; discute su localidad | Compara con cifras y explica parcialmente las diferencias | Presenta mapas y tabla con una comparación superficial | Presenta figuras sin comparación |
| 3 | **Rigidez y cinemática** (2.4) | 1,0 | Cuantifica el efecto de μ(z) y lo relaciona con el tipo de evento; calcula y discute la validez de la aproximación instantánea con c = √(g h) | Cuantifica ambos efectos con discusión parcial | Presenta las figuras con una lectura cualitativa | Presenta figuras sin lectura |
| 4 | **Del fondo a la superficie y paquete para la U3** (2.5 y anexo) | 1,0 | Cuantifica aporte horizontal y efecto de Kajiura, describe η0 frente a la localidad (qué llega primero) y entrega el paquete completo | Cuantifica los efectos y entrega el paquete con alguna omisión menor | Describe η0 sin cuantificar; paquete incompleto | Sin análisis o sin paquete |
| 5 | **Validación y sensibilidad** (2.6) | 1,0 | Al menos 3 observaciones citadas; compara RMSE entre modelos y explica dónde falla; identifica el parámetro dominante y qué dato reduciría la incertidumbre | Valida con observaciones citadas y lee el tornado, con explicación parcial | Valida con menos de 3 observaciones o sin citas; tornado sin lectura | Sin validación o sin sensibilidad |
| 6 | **Resolución de problemas complejos** (2.7) | 1,5 | Ver detalle abajo | | | |
| 7 | **Comunicación** | 1,0 | Responde la pregunta guía con evidencia; figuras numeradas y legibles; redacción técnica clara; todas las cifras externas citadas | Responde la pregunta guía; alguna figura o cita deficiente | Respuesta incompleta; varias figuras o citas deficientes | No responde la pregunta guía |
| | **Total** | **8,0** | | | | |

### Criterio 6 · Resolución de problemas complejos (1,5 puntos)

Se evalúa el **proceso**, no que las decisiones sean «las correctas». Tres indicadores de 0,5 puntos cada uno:

| Indicador | Excelente (0,5) | Satisfactorio (0,375) | En desarrollo (0,25) | Inicial (0,125) |
|---|---|---|---|---|
| **6a · Decidir con evidencia** (bitácora, 3 decisiones) | Las tres decisiones comparan al menos dos alternativas, se apoyan en evidencia concreta del cuaderno o la literatura y declaran el riesgo asumido | Tres decisiones con evidencia; alguna sin alternativas o sin riesgo | Decisiones incompletas o justificadas sin evidencia («porque es mejor») | Bitácora vacía o con la plantilla sin completar |
| **6b · Diagnosticar** (anomalía, hipótesis y prueba) | Describe la anomalía con cifras, plantea dos hipótesis distinguibles, las prueba en el cuaderno y concluye reconociendo lo que no puede afirmar | Hipótesis y prueba realizadas; conclusión poco matizada | Hipótesis planteadas sin prueba, o prueba sin relación con las hipótesis | Solo describe la diferencia entre modelo y observación |
| **6c · Reflexionar** (predicción vs. modelo y cierre metacognitivo) | Explica qué razonamiento falló o acertó en la predicción y describe con concreción su estrategia, su atasco y qué transferiría a otro evento | Reflexión concreta en dos de los tres aspectos | Reflexión genérica («aprendimos mucho») | Sin reflexión |

### Presentación oral (opcional, a criterio del docente)

Si el capítulo se presenta en clase (10 minutos por grupo, ambos integrantes con una parte calificada individualmente), puede reemplazar 1 punto del criterio 7 con la misma escala de niveles.

## 5. Errores frecuentes

- Usar la profundidad del centroide como borde superior (o al revés). La ficha guarda `z_sup`; el cuaderno convierte al centroide.
- Elegir la fuente para la U3 sin mirar la validación: la Decisión 2 se puede revisar después del Paso 6.
- Tratar la falla finita del USGS como una observación: es un modelo, con su incertidumbre.
- Validar con observaciones sin fuente o mezclar deformación cosísmica con deformación posterior al sismo.
- Interpretar los pequeños escalones del perfil de la falla finita como un fenómeno físico: son los bordes de subfallas someras.
- Dejar la bitácora con «...»: el cuaderno avisa con ⚠️ los campos vacíos.

## 6. Referencias

- Bilek, S. L., y Lay, T. (1999). Rigidity variations with depth along interplate megathrust faults in subduction zones. *Nature, 400*, 443–446.
- Hayes, G. P., et al. (2018). Slab2, a comprehensive subduction zone geometry model. *Science, 362*(6410), 58–61.
- Kajiura, K. (1963). The leading wave of a tsunami. *Bulletin of the Earthquake Research Institute, 41*, 535–571.
- Okada, Y. (1985). Surface deformation due to shear and tensile faults in a half-space. *Bulletin of the Seismological Society of America, 75*(4), 1135–1154.
- Strasser, F. O., Arango, M. C., y Bommer, J. J. (2010). Scaling of the source dimensions of interface and intraslab subduction-zone earthquakes with moment magnitude. *Seismological Research Letters, 81*(6), 941–950.
- Tanioka, Y., y Satake, K. (1996). Tsunami generation by horizontal displacement of ocean bottom. *Geophysical Research Letters, 23*(8), 861–864.
- Wells, D. L., y Coppersmith, K. J. (1994). New empirical relationships among magnitude, rupture length, rupture width, rupture area, and surface displacement. *Bulletin of the Seismological Society of America, 84*(4), 974–1002.
