"""
Herramientas de análisis para el cuaderno de la Unidad 2: mallas, elección del
plano nodal, perfiles, métricas de la deformación y validación con observaciones.
"""
import numpy as np

from .fuentes import falla_uniforme, geo_a_km, km_a_geo
from .eventos import EVENTOS


def malla(region, paso_grados=1 / 30):
    """Malla regular lon/lat (latitud creciente). paso por defecto: 2 minutos de arco."""
    lo0, lo1, la0, la1 = region
    lon = np.arange(lo0, lo1 + 1e-9, paso_grados)
    lat = np.arange(la0, la1 + 1e-9, paso_grados)
    return np.meshgrid(lon, lat)


def interpolar_malla(lon_o, lat_o, z_o, lon, lat):
    """Interpolación bilineal de una malla regular (lat creciente) a otra."""
    from scipy.interpolate import RegularGridInterpolator
    f = RegularGridInterpolator((lat_o[:, 0], lon_o[0, :]), z_o, bounds_error=False,
                                fill_value=np.nan)
    return f(np.column_stack([lat.ravel(), lon.ravel()])).reshape(lon.shape)


def elegir_plano(tensor, regla):
    """Plano nodal a usar: 1, 2 o 'menor_buzamiento'."""
    p1, p2 = tensor["plano1"], tensor["plano2"]
    if regla == 1:
        return p1, "plano nodal 1 (justificar en el capítulo)"
    if regla == 2:
        return p2, "plano nodal 2 (justificar en el capítulo)"
    p = p1 if p1["buz"] <= p2["buz"] else p2
    return p, "plano de menor buzamiento (interfase de subducción)"


def falla_desde_tensor(nombre, meta, mu=30e9, L=None, W=None, slip=None, plano=None,
                       prof=None):
    """Rectángulo uniforme desde el tensor de momento del USGS + leyes de escala."""
    t = meta["tensor"]
    p, razon = elegir_plano(t, plano or EVENTOS[nombre]["plano"])
    c = t["centroide"]
    lon = c["lon"] if c["lon"] is not None else meta["hipocentro"]["lon"]
    lat = c["lat"] if c["lat"] is not None else meta["hipocentro"]["lat"]
    z = prof or c["prof_km"] or meta["hipocentro"]["prof_km"]
    f = falla_uniforme(lon, lat, z, p["rumbo"], p["buz"], p["rake"], M0=t["M0_Nm"],
                       L=L, W=W, slip=slip, mu=mu, tipo_escala=EVENTOS[nombre]["escala"],
                       nombre=nombre)
    f.origen += f" · {razon}"
    h = meta["hipocentro"]
    f.hipocentro = (h["lon"], h["lat"], h["prof_km"])
    return f


def rumbo_medio(falla):
    """Rumbo medio ponderado por deslizamiento (promedio circular)."""
    sl = np.maximum(falla.slip, 1e-9)
    a = np.radians([s.rumbo for s in falla.subfallas])
    return float(np.degrees(np.arctan2(np.sum(sl * np.sin(a)), np.sum(sl * np.cos(a)))) % 360)


def perfil(lon0, lat0, rumbo, largo_mar=250.0, largo_tierra=150.0, n=601, lado_mar=None):
    """
    Perfil perpendicular al rumbo que pasa por (lon0, lat0).
    s > 0 hacia tierra, s < 0 hacia el mar (el lado del mar es el contrario al
    buzamiento salvo que se indique lado_mar = +1 o -1).
    Devuelve s (km), lon, lat.
    """
    phi = np.radians(rumbo)
    bv = np.array([np.cos(phi), -np.sin(phi)])     # hacia donde buza (tierra en subducción)
    if lado_mar is not None:
        bv = -lado_mar * bv
    s = np.linspace(-largo_mar, largo_tierra, n)
    lon, lat = km_a_geo(s * bv[0], s * bv[1], lon0, lat0)
    return s, lon, lat


def metricas(lon, lat, uz, z_topo=None):
    """Máximo, mínimo y su posición; fracción del levantamiento en el mar."""
    i = np.unravel_index(np.nanargmax(uz), uz.shape)
    j = np.unravel_index(np.nanargmin(uz), uz.shape)
    d = dict(uz_max_m=float(uz[i]), lon_max=float(lon[i]), lat_max=float(lat[i]),
             uz_min_m=float(uz[j]), lon_min=float(lon[j]), lat_min=float(lat[j]))
    if z_topo is not None:
        mar = z_topo < 0
        pos = np.where(uz > 0, uz, 0)
        tot = pos.sum()
        d["fraccion_levantamiento_en_mar"] = float(pos[mar].sum() / tot) if tot > 0 else None
        d["uz_max_mar_m"] = float(np.nanmax(np.where(mar, uz, np.nan)))
        d["uz_min_tierra_m"] = float(np.nanmin(np.where(~mar, uz, np.nan))) if (~mar).any() else None
    return d


def cruces_de_cero(s, u):
    """Posiciones (km) donde el perfil cambia de signo."""
    k = np.where(np.diff(np.sign(u)) != 0)[0]
    return [float(s[i] - u[i] * (s[i + 1] - s[i]) / (u[i + 1] - u[i])) for i in k]


def validar(falla, observaciones, nu=0.25):
    """
    Compara el modelo con las observaciones (GPS, InSAR, costa).
    Devuelve filas con observado, modelado y residual, y el RMSE por componente.
    """
    if not observaciones:
        return [], {}
    lon = np.array([o["lon"] for o in observaciones])
    lat = np.array([o["lat"] for o in observaciones])
    uE, uN, uz = falla.desplazamiento(lon, lat, nu)
    filas, res = [], {"uE": [], "uN": [], "uz": []}
    for k, o in enumerate(observaciones):
        fila = dict(nombre=o["nombre"], tipo=o["tipo"])
        for c, m in (("uE", uE[k]), ("uN", uN[k]), ("uz", uz[k])):
            fila[c + "_mod"] = float(m)
            if o[c] is not None:
                fila[c + "_obs"] = o[c]
                fila[c + "_res"] = o[c] - float(m)
                res[c].append(o[c] - float(m))
        filas.append(fila)
    rmse = {c: float(np.sqrt(np.mean(np.square(v)))) for c, v in res.items() if v}
    return filas, rmse
