"""
Catálogo de los eventos de la práctica 1 (IRD-505) y sus localidades costeras.

Fecha UTC y coordenadas aproximadas: sirven para BUSCAR el sismo en los
catálogos; los valores con los que se modela vienen del USGS (datos/).
"""

EVENTOS = {
    "Pedernales 2016": dict(fecha="2016-04-16", lat=0.38, lon=-79.92, Mw=7.8,
                            tipo="Inversa de interplaca", escala="interfase",
                            plano="menor_buzamiento", slab="sam"),
    "Maule 2010": dict(fecha="2010-02-27", lat=-36.12, lon=-72.90, Mw=8.8,
                       tipo="Inversa de interplaca", escala="interfase",
                       plano="menor_buzamiento", slab="sam"),
    "Illapel 2015": dict(fecha="2015-09-16", lat=-31.57, lon=-71.67, Mw=8.3,
                         tipo="Inversa de interplaca", escala="interfase",
                         plano="menor_buzamiento", slab="sam"),
    "Iquique 2014": dict(fecha="2014-04-01", lat=-19.61, lon=-70.77, Mw=8.2,
                         tipo="Inversa de interplaca", escala="interfase",
                         plano="menor_buzamiento", slab="sam"),
    "Pisco 2007": dict(fecha="2007-08-15", lat=-13.39, lon=-76.60, Mw=8.0,
                       tipo="Inversa de interplaca", escala="interfase",
                       plano="menor_buzamiento", slab="sam"),
    "Camaná 2001": dict(fecha="2001-06-23", lat=-16.26, lon=-73.64, Mw=8.4,
                        tipo="Inversa de interplaca", escala="interfase",
                        plano="menor_buzamiento", slab="sam"),
    "Tohoku 2011": dict(fecha="2011-03-11", lat=38.30, lon=142.37, Mw=9.1,
                        tipo="Inversa de interplaca", escala="interfase",
                        plano="menor_buzamiento", slab="kur"),
    "Nicaragua 1992": dict(fecha="1992-09-02", lat=11.74, lon=-87.34, Mw=7.7,
                           tipo="Sismo tsunami", escala="interfase",
                           plano="menor_buzamiento", slab="cam"),
    "Mentawai 2010": dict(fecha="2010-10-25", lat=-3.49, lon=100.08, Mw=7.8,
                          tipo="Sismo tsunami", escala="interfase",
                          plano="menor_buzamiento", slab="sum"),
    "Samoa 2009": dict(fecha="2009-09-29", lat=-15.49, lon=-172.10, Mw=8.1,
                       tipo="Normal, fuera de la fosa", escala="otro",
                       plano=1, slab=None),
    "Océano Índico 2012": dict(fecha="2012-04-11", lat=2.33, lon=93.06, Mw=8.6,
                               tipo="Rumbo", escala="otro", plano=1, slab=None),
}

LOCALIDADES = {
    "Pedernales 2016": {"Pedernales": (0.071, -80.053)},
    "Maule 2010": {"Constitución": (-35.333, -72.417), "Dichato": (-36.546, -72.933),
                   "Talcahuano": (-36.724, -73.117)},
    "Illapel 2015": {"Los Vilos": (-31.911, -71.512), "Tongoy": (-30.256, -71.497),
                     "Coquimbo": (-29.953, -71.343)},
    "Iquique 2014": {"Pisagua": (-19.596, -70.212), "Iquique": (-20.214, -70.152)},
    "Pisco 2007": {"Pisco": (-13.710, -76.203), "Tambo de Mora": (-13.460, -76.188),
                   "Paracas": (-13.835, -76.251)},
    "Camaná 2001": {"Camaná": (-16.624, -72.711), "Atico": (-16.210, -73.611),
                    "Mollendo": (-17.023, -72.015)},
    "Tohoku 2011": {"Ishinomaki": (38.434, 141.303), "Onagawa": (38.445, 141.447),
                    "Kesennuma": (38.906, 141.570), "Rikuzentakata": (39.015, 141.630)},
    "Nicaragua 1992": {"Masachapa": (11.786, -86.519), "El Tránsito": (12.047, -86.708),
                       "San Juan del Sur": (11.253, -85.870)},
    "Mentawai 2010": {"Sikakap (islas Pagai)": (-2.780, 100.220),
                      "Pagai Selatan, costa oeste": (-3.050, 100.250)},
    "Samoa 2009": {"Lalomanu": (-14.060, -171.430), "Pago Pago": (-14.279, -170.700),
                   "Apia": (-13.833, -171.767)},
    "Océano Índico 2012": {"Meulaboh": (4.137, 96.128), "Sinabang (Simeulue)": (2.478, 96.379),
                           "Banda Aceh": (5.550, 95.317)},
}

# Qué enseña cada evento en la Unidad 2 (pregunta guía del capítulo 2)
PREGUNTA_U2 = {
    "Pedernales 2016": "¿Por qué una ruptura bajo la costa y a unos 20 km de profundidad generó "
                       "un tsunami pequeño? ¿Qué parte de la deformación cae en el mar y cuál en tierra?",
    "Maule 2010": "¿Reproduce el modelo la costa que subió y la que se hundió? ¿Dónde cae la "
                  "línea de cero respecto al litoral?",
    "Illapel 2015": "¿Cuánto cambia la condición inicial al pasar del rectángulo uniforme a la "
                    "falla finita en una ruptura de tamaño intermedio?",
    "Iquique 2014": "¿Qué parte de la ruptura queda bajo el mar y cuál bajo tierra? ¿Cómo se "
                    "refleja en la deformación costera?",
    "Pisco 2007": "¿Cómo influye la propagación de la ruptura (tiempos) en la forma del "
                  "levantamiento frente a la península de Paracas?",
    "Camaná 2001": "¿Qué efecto tiene una ruptura muy larga (L) y unilateral sobre la "
                   "deformación a lo largo de la costa?",
    "Tohoku 2011": "¿Cuánto aportan el deslizamiento hasta la fosa y el componente horizontal "
                   "a la ola inicial en aguas muy profundas?",
    "Nicaragua 1992": "¿Puede un rectángulo con rigidez estándar explicar un sismo tsunami? "
                      "¿Qué cambia con una rigidez somera reducida?",
    "Mentawai 2010": "¿Por qué un Mw 7,8 generó un tsunami grande? Efecto de la rigidez "
                     "somera sobre el deslizamiento y el levantamiento.",
    "Samoa 2009": "¿Cómo cambia el patrón con una falla normal fuera de la fosa? ¿Qué plano "
                  "nodal es el de falla y cómo lo justifican?",
    "Océano Índico 2012": "¿Por qué un Mw 8,6 de rumbo deforma poco en vertical? ¿Qué papel "
                          "juegan el rake y el componente horizontal?",
}


def slug(nombre):
    t = nombre.lower()
    for a, b in zip("áéíóúñ ", "aeioun_"):
        t = t.replace(a, b)
    return t


def region_sugerida(nombre, margen_min=3.0):
    """Caja (lon_min, lon_max, lat_min, lat_max) para batimetría y mallas."""
    from .fuentes import escalamiento
    ev = EVENTOS[nombre]
    L, _ = escalamiento(ev["Mw"], ev["escala"])
    half = max(margen_min, 0.6 * L / 111.0 + 2.0)
    lats = [ev["lat"]] + [v[0] for v in LOCALIDADES[nombre].values()]
    lons = [ev["lon"]] + [v[1] for v in LOCALIDADES[nombre].values()]
    return (round(min(lons) - half, 2), round(max(lons) + half, 2),
            round(min(lats) - half, 2), round(max(lats) + half, 2))
