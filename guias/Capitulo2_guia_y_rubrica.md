# Capítulo 2 del proyecto integrador · Guía y rúbrica

**Modelación Sísmica y Tsunami (IRD-505) · Unidad 2: Modelación de desplazamientos verticales**
Ingeniería en Riesgos de Desastres · ESPAM MFL · Docente: Ing. Cristian Paliz Acosta, MSc.

Cuaderno: [`cuadernos/Cap2_deformacion_cosismica.ipynb`](../cuadernos/Cap2_deformacion_cosismica.ipynb) · [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/Cap2_deformacion_cosismica.ipynb)

---

## 1. Propósito

En el Capítulo 1 describieron la fuente de su sismo con una ficha (un rectángulo uniforme). En el Capítulo 2 modelan la **deformación cosísmica** de su evento con una fuente realista y entregan la **condición inicial del tsunami** para las Unidades 3 y 4.

**Resultado de aprendizaje B (Aplicar):** modelar los desplazamientos verticales producidos por un sismo mediante el modelo de dislocación elástica de Okada (1985), a partir de modelos de falla finita y de los parámetros de la fuente, y evaluar el resultado frente a observaciones.

**Habilidad transversal: resolución de problemas complejos.** El problema tiene información incompleta, modelos que no son únicos y supuestos que cambian el resultado. Se trabaja con la **bitácora de decisiones**, el **diagnóstico de la anomalía** y el **cierre metacognitivo** del cuaderno (marcados con 🧭), y se evalúa con el criterio 8 de la rúbrica (1 punto).

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

Las guías oficiales en Word (**actividad formativa** y **trabajo sumativo**) se publican en el aula virtual; este es su resumen.

| Momento | Qué se entrega | Puntos | Fecha (propuesta, por confirmar) |
|---|---|---|---|
| **Formativa** | Avance: Pasos P a 4, Decisión 1 de la bitácora, dudas y borrador de 2.2 a 2.5 | 2 | Miércoles 25 de noviembre, 23:59; retroalimentación el jueves 26 |
| **Sumativa** | Capítulo 2 completo (PDF) + paquete `modelo_U2` + Anexo 2.A de respuesta a la retroalimentación | 8 | Documento: lunes 30 de noviembre, 23:59 |
| **Defensa oral** | 10 minutos de exposición + 5 de preguntas (parte de la sumativa) | — | Martes 1 de diciembre, sesión presencial |

### Rúbrica de la formativa (2 puntos)

Cuatro criterios de 0,5: cuaderno y evidencias propias; predicción razonada (Paso P); avance de la modelación (2.3 a 2.5); proceso (Decisión 1 de la bitácora y dudas concretas). Niveles: Logrado (100 %), En proceso (70 %), Inicial (40 %), No presenta (0).

### Rúbrica de la sumativa (8 puntos)

Niveles: **Excelente** (100 %) · **Satisfactorio** (70 %) · **En desarrollo** (40 %) · **Insuficiente** (0).

| # | Criterio | Pts |
|---|---|---|
| 1 | Respuesta a la retroalimentación (Anexo 2.A) | 0,50 |
| 2 | Datos y geometría de la fuente (2.3) | 0,75 |
| 3 | Rectángulo uniforme frente a falla finita (2.4) | 1,25 |
| 4 | Rigidez y cinemática (2.5) | 0,75 |
| 5 | Del fondo a la superficie y paquete para la U3 (2.6 y anexo) | 0,75 |
| 6 | Validación y sensibilidad (2.7) | 1,00 |
| 7 | Discusión, conclusiones y formato (2.9, 2.10) | 1,00 |
| 8 | **Resolución de problemas complejos** (2.8) · habilidad blanda | **1,00** |
| 9 | **Defensa oral** · calificación individual | **1,00** |
| | **Total** | **8,00** |

**Criterio 8 · Resolución de problemas complejos.** Se evalúa el proceso, no que las decisiones sean «las correctas»:

| Indicador | Pts | Excelente |
|---|---|---|
| 8a · Decidir con evidencia (bitácora, 3 decisiones) | 0,40 | Las tres decisiones comparan dos o más alternativas, se apoyan en evidencia concreta y declaran el riesgo asumido |
| 8b · Diagnosticar (anomalía, hipótesis y prueba) | 0,30 | Anomalía con cifras, dos hipótesis distinguibles, prueba hecha en el cuaderno y conclusión que reconoce lo que no se puede afirmar |
| 8c · Reflexionar (predicción y cierre metacognitivo) | 0,30 | Explica qué razonamiento de la predicción falló o acertó; describe con concreción estrategia, atasco y transferencia |

**Criterio 9 · Defensa oral.** Ambos integrantes exponen y responden; quien no intervenga obtiene 0 en este criterio.

| Aspecto | Pts | Excelente |
|---|---|---|
| 9a · Dominio técnico | 0,40 | Explica con sus figuras y cifras qué cambia de la fuente uniforme a la falla finita y del fondo a la superficie |
| 9b · Decisiones y respuestas | 0,40 | Defiende sus decisiones de la bitácora con evidencia y responde con datos propios, reconociendo límites |
| 9c · Tiempo y comunicación | 0,20 | 10 minutos (± 1), partes equilibradas, diapositivas con figuras propias |

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
