"""
deformacion — Modelación de desplazamientos verticales (IRD-505, Unidad 2).

Módulos
-------
okada       Okada (1985), verificado contra la Tabla 2 del artículo.
fuentes     Subfallas, fallas uniformes, falla finita del USGS, rigidez variable.
superficie  Aporte horizontal (Tanioka y Satake, 1996) y filtro de Kajiura (1963).
cinematica  Deformación en el tiempo según la propagación de la ruptura.
analisis    Mallas, planos nodales, perfiles, métricas y validación.
datos       Descarga y lectura de datos por evento (USGS, ETOPO 2022, Slab2).
exportar    dtopo/topo de GeoClaw, NetCDF y NPZ para las Unidades 3 y 4.
eventos     Catálogo de eventos y localidades del curso.
"""
from .okada import okada85
from .fuentes import (Subfalla, Falla, falla_uniforme, subdividir, leer_param_usgs, leer_fsp,
                      mu_rampa, reescalar_por_rigidez, momento_a_mw, mw_a_momento,
                      geo_a_km, km_a_geo, escalamiento)
from .superficie import aporte_horizontal, filtro_kajiura, volumen_desplazado, energia_potencial
from .cinematica import campo_en_el_tiempo, tiempos_sugeridos, fraccion_subida, frente_de_ruptura
from .analisis import (malla, interpolar_malla, elegir_plano, falla_desde_tensor, rumbo_medio,
                       perfil, metricas, cruces_de_cero, validar)
from .eventos import EVENTOS, LOCALIDADES, PREGUNTA_U2, slug, region_sugerida

__version__ = "0.2.0"
