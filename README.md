# Modelación Sísmica y Tsunami (IRD-505) · ESPAM MFL

Cuadernos de Google Colab y datos de la asignatura **Modelación Sísmica y Tsunami** de la carrera de Ingeniería en Riesgos de Desastres, Escuela Superior Politécnica Agropecuaria de Manabí Manuel Félix López (ESPAM MFL).

Docente: Ing. Cristian Paliz Acosta, MSc.

Todo el contenido es público. Los cuadernos corren en Google Colab con una cuenta de Google gratuita, sin instalar nada en el computador.

## Cuadernos

| Cuaderno | Para qué sirve | Abrir |
|---|---|---|
| `Cap1_fuente_sismica.ipynb` | Capítulo 1 del proyecto integrador: datos del USGS y Global CMT, comparación entre agencias, pelotas de playa, réplicas, mapa tectónico, dimensiones de la ruptura, deslizamiento y ficha de la fuente en CSV | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/Cap1_fuente_sismica.ipynb) |
| `Practica_consolidacion_Okada_IRD505.ipynb` | De la ficha de la fuente a la deformación: modelo de Okada (1985), mapa de Uz, perfil por la localidad, validación, sensibilidad y condición inicial del tsunami. Lee la ficha desde el CSV del Capítulo 1 | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/Practica_consolidacion_Okada_IRD505.ipynb) |
| `Cap2_deformacion_cosismica.ipynb` | Capítulo 2 (Unidad 2): de la falla finita del USGS a la condición inicial del tsunami. Geometría en profundidad, rectángulo uniforme frente a falla finita, rigidez variable, cinemática animada de la ruptura, aporte horizontal (Tanioka y Satake) y filtro de Kajiura, validación con observaciones, sensibilidad y exportación para GeoClaw | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/Cap2_deformacion_cosismica.ipynb) |
| `DOCENTE_preparar_datos_U2.ipynb` | Uso docente: descarga para los 11 eventos la falla finita y el tensor del USGS, la batimetría ETOPO 2022 (regional y costera) y Slab2, y los deja en `datos/eventos/` | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/DOCENTE_preparar_datos_U2.ipynb) |
| `DOCENTE_preparar_respaldo.ipynb` | Uso docente: descarga y empaqueta la copia de respaldo de los datos de los 11 eventos | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/DOCENTE_preparar_respaldo.ipynb) |

**Cómo trabajar:** abran el enlace, guarden una copia en su Drive (*Archivo → Guardar una copia en Drive*) y ejecuten las celdas en orden. Solo se editan las celdas marcadas con ✏️.

En el cuaderno del Capítulo 1, el evento y la localidad se eligen en **menús desplegables**: la fecha, la zona de búsqueda en los catálogos y las coordenadas de la localidad se completan solas. La ficha exportada lleva también la localidad, y el cuaderno de Okada la toma del CSV sin escribir coordenadas. Las coordenadas de las localidades son las aproximadas del centro poblado.

## Datos

Los cuadernos descargan los datos en el momento desde fuentes públicas y gratuitas:

- **USGS**, catálogo de sismos (servicio FDSN): localización, magnitud, tensor de momento W-phase, réplicas. https://earthquake.usgs.gov/fdsnws/event/1/
- **Global CMT**, catálogo completo en formato NDK: centroide, momento sísmico y planos nodales. https://www.globalcmt.org/
- **Límites de placa PB2002** (Bird, 2003), en GeoJSON de [fraxen/tectonicplates](https://github.com/fraxen/tectonicplates) (licencia ODC-By).
- **Línea de costa, límites internacionales y provinciales y poblados** de Natural Earth 1:10 m (dominio público).

La carpeta `datos/` guarda copias de los límites de placa y de la costa, y en `datos/respaldo/` una copia de los datos de cada evento de la guía. Si el USGS o Global CMT no responden, los cuadernos usan esa copia y lo indican.

| Archivo | Contenido |
|---|---|
| `datos/pb2002_limites.geojson` | Límites de placa PB2002 |
| `datos/pb2002_pasos.csv` | Tramos de límite PB2002 con su clase (`SUB` = subducción) y velocidad relativa (mm/a) |
| `datos/ne_50m_coastline.geojson` | Línea de costa Natural Earth 1:50 m |
| `datos/ne_10m_costa.geojson` | Línea de costa Natural Earth 1:10 m (coordenadas a 3 decimales) |
| `datos/ne_10m_limites_paises.geojson` | Límites internacionales Natural Earth 1:10 m |
| `datos/ne_10m_limites_provincias.geojson` | Límites de primer nivel administrativo (provincias, estados) Natural Earth 1:10 m |
| `datos/ne_10m_poblados.csv` | Poblados Natural Earth 1:10 m: nombre, país, provincia, coordenadas y población |
| `datos/respaldo/<evento>/` | `usgs_detalle.json`, `replicas.csv` y `gcmt.ndk` de cada evento |

### Datos de la Unidad 2 (`datos/eventos/<evento>/`)

| Archivo | Contenido | Fuente |
|---|---|---|
| `evento.json` | Origen, tensor de momento, planos nodales y enlaces | USGS ComCat |
| `falla_finita.param` (o `.fsp`) | Modelo de falla finita: deslizamiento, rake y tiempos de ruptura por subfalla | USGS, producto *finite-fault* |
| `batimetria_regional.nc` | Elevación y batimetría a 1′ de arco en la región del evento | NOAA ETOPO 2022 (ERDDAP) |
| `batimetria_costa_<localidad>.nc` | Elevación y batimetría a 15″ de arco, ±0,3° alrededor de cada localidad | NOAA ETOPO 2022 |
| `slab2_profundidad.grd` | Profundidad de la placa subducida (si se pudo descargar) | USGS Slab2 |
| `observaciones.csv` | Desplazamientos medidos (GPS, InSAR, costa): los completan los grupos con su fuente | Literatura |
| `modelo_U2/` | Resultados del Capítulo 2: dtopo de GeoClaw, η0, campos en NetCDF y resumen | Cuaderno del Capítulo 2 |

## Código (`src/deformacion/`)

Paquete de Python del curso, sin dependencias fuera de las de Colab:

| Módulo | Contenido |
|---|---|
| `okada.py` | Okada (1985), verificado contra la Tabla 2 del artículo |
| `fuentes.py` | Subfallas, rectángulo uniforme, lector de falla finita del USGS, leyes de escala, rigidez variable |
| `superficie.py` | Aporte horizontal (Tanioka y Satake, 1996), filtro de Kajiura (1963), volumen y energía |
| `cinematica.py` | Deformación en el tiempo según la propagación de la ruptura |
| `analisis.py` | Mallas, planos nodales, perfiles, métricas y validación |
| `datos.py` | Descarga y lectura de los datos de cada evento |
| `exportar.py` | dtopo y topo de GeoClaw (tipo 3), NetCDF y NPZ |

Pruebas: `python -m pytest tests/`.

## Referencias

- Bird, P. (2003). An updated digital model of plate boundaries. *Geochemistry, Geophysics, Geosystems, 4*(3), 1027. https://doi.org/10.1029/2001GC000252
- Ekström, G., Nettles, M., y Dziewoński, A. M. (2012). The global CMT project 2004–2010. *Physics of the Earth and Planetary Interiors, 200–201*, 1–9. https://doi.org/10.1016/j.pepi.2012.04.002
- Okada, Y. (1985). Surface deformation due to shear and tensile faults in a half-space. *Bulletin of the Seismological Society of America, 75*(4), 1135–1154.
- Strasser, F. O., Arango, M. C., y Bommer, J. J. (2010). Scaling of the source dimensions of interface and intraslab subduction-zone earthquakes with moment magnitude. *Seismological Research Letters, 81*(6), 941–950.
- Hayes, G. P., Moore, G. L., Portner, D. E., Hearne, M., Flamme, H., Furtney, M., y Smoczyk, G. M. (2018). Slab2, a comprehensive subduction zone geometry model. *Science, 362*(6410), 58–61. https://doi.org/10.1126/science.aat4723
- Kajiura, K. (1963). The leading wave of a tsunami. *Bulletin of the Earthquake Research Institute, 41*, 535–571.
- NOAA National Centers for Environmental Information (2022). ETOPO 2022 15 Arc-Second Global Relief Model. https://doi.org/10.25921/fd45-gt74
- Tanioka, Y., y Satake, K. (1996). Tsunami generation by horizontal displacement of ocean bottom. *Geophysical Research Letters, 23*(8), 861–864. https://doi.org/10.1029/96GL00736
- Wells, D. L., y Coppersmith, K. J. (1994). New empirical relationships among magnitude, rupture length, rupture width, rupture area, and surface displacement. *Bulletin of the Seismological Society of America, 84*(4), 974–1002.
