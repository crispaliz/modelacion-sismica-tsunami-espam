# Modelación Sísmica y Tsunami (IRD-505) · ESPAM MFL

Cuadernos de Google Colab y datos de la asignatura **Modelación Sísmica y Tsunami** de la carrera de Ingeniería en Riesgos de Desastres, Escuela Superior Politécnica Agropecuaria de Manabí Manuel Félix López (ESPAM MFL).

Docente: Ing. Cristian Paliz Acosta, MSc.

Todo el contenido es público. Los cuadernos corren en Google Colab con una cuenta de Google gratuita, sin instalar nada en el computador.

## Cuadernos

| Cuaderno | Para qué sirve | Abrir |
|---|---|---|
| `Cap1_fuente_sismica.ipynb` | Capítulo 1 del proyecto integrador: datos del USGS y Global CMT, comparación entre agencias, pelotas de playa, réplicas, mapa tectónico, dimensiones de la ruptura, deslizamiento y ficha de la fuente en CSV | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/Cap1_fuente_sismica.ipynb) |
| `Practica_consolidacion_Okada_IRD505.ipynb` | De la ficha de la fuente a la deformación: modelo de Okada (1985), mapa de Uz, perfil por la localidad, validación, sensibilidad y condición inicial del tsunami. Lee la ficha desde el CSV del Capítulo 1 | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/Practica_consolidacion_Okada_IRD505.ipynb) |
| `DOCENTE_preparar_respaldo.ipynb` | Uso docente: descarga y empaqueta la copia de respaldo de los datos de los 11 eventos | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/modelacion-sismica-tsunami-espam/blob/main/cuadernos/DOCENTE_preparar_respaldo.ipynb) |

**Cómo trabajar:** abran el enlace, guarden una copia en su Drive (*Archivo → Guardar una copia en Drive*) y ejecuten las celdas en orden. Solo se editan las celdas marcadas con ✏️.

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

## Referencias

- Bird, P. (2003). An updated digital model of plate boundaries. *Geochemistry, Geophysics, Geosystems, 4*(3), 1027. https://doi.org/10.1029/2001GC000252
- Ekström, G., Nettles, M., y Dziewoński, A. M. (2012). The global CMT project 2004–2010. *Physics of the Earth and Planetary Interiors, 200–201*, 1–9. https://doi.org/10.1016/j.pepi.2012.04.002
- Okada, Y. (1985). Surface deformation due to shear and tensile faults in a half-space. *Bulletin of the Seismological Society of America, 75*(4), 1135–1154.
- Strasser, F. O., Arango, M. C., y Bommer, J. J. (2010). Scaling of the source dimensions of interface and intraslab subduction-zone earthquakes with moment magnitude. *Seismological Research Letters, 81*(6), 941–950.
