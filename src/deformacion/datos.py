"""
Descarga y lectura de los datos de cada evento.

Estructura en disco (una carpeta por evento):

    datos/eventos/<evento>/
        evento.json            origen, tensor de momento, planos nodales, productos USGS
        falla_finita.param     modelo de falla finita del USGS (si existe)
        falla_finita.fsp       (alternativa, si no hay .param)
        batimetria_regional.nc ETOPO 2022, 1 minuto de arco, región del evento
        batimetria_costa_<localidad>.nc   ETOPO 2022, 15 segundos, ±0,3° alrededor de cada localidad
        slab2_profundidad.grd  geometría de la placa (si se pudo descargar)
        observaciones.csv      desplazamientos medidos (GPS, InSAR, costa) — los completa el grupo
        modelo_U2/             resultados del cuaderno de la Unidad 2

Fuentes: USGS ComCat (FDSN), NOAA ERDDAP (ETOPO 2022), USGS ScienceBase (Slab2).
"""
import datetime as dt
import json
import os
import time
import urllib.parse

import numpy as np

from .eventos import EVENTOS, LOCALIDADES, slug, region_sugerida
from .fuentes import leer_param_usgs, leer_fsp

USGS_FDSN = "https://earthquake.usgs.gov/fdsnws/event/1/query"
ERDDAP = "https://coastwatch.pfeg.noaa.gov/erddap/griddap"
ETOPO_15S = "ETOPO_2022_v1_15s"      # variable z, 15 segundos de arco
ETOPO_1M = "etopo180"                # variable altitude, 1 minuto (respaldo)
SCIENCEBASE = "https://www.sciencebase.gov/catalog"
SLAB2_TITULOS = {"sam": "South America", "kur": "Kuril", "sum": "Sumatra",
                 "cam": "Central America", "ker": "Kermadec"}

OBS_COLUMNAS = "nombre,lat,lon,uE_m,uN_m,uz_m,sigma_m,tipo,fuente\n"


# ---------------------------------------------------------------------------
# Utilidades de red
# ---------------------------------------------------------------------------
def _get(url, params=None, intentos=3, timeout=90, binario=False):
    import requests
    ultimo = None
    for k in range(intentos):
        try:
            r = requests.get(url, params=params, timeout=timeout,
                             headers={"User-Agent": "IRD505-ESPAM-curso"})
            r.raise_for_status()
            return r.content if binario else r.text
        except Exception as e:
            ultimo = e
            time.sleep(2 * (k + 1))
    raise RuntimeError(f"No se pudo descargar {url}: {ultimo}")


def carpeta_evento(nombre, raiz="datos"):
    c = os.path.join(raiz, slug(nombre))
    os.makedirs(c, exist_ok=True)
    return c


# ---------------------------------------------------------------------------
# USGS: evento, tensor de momento y falla finita
# ---------------------------------------------------------------------------
def buscar_evento_usgs(nombre):
    ev = EVENTOS[nombre]
    f0 = dt.date.fromisoformat(ev["fecha"])
    params = dict(format="geojson", starttime=str(f0), endtime=str(f0 + dt.timedelta(days=1)),
                  latitude=ev["lat"], longitude=ev["lon"], maxradiuskm=500,
                  minmagnitude=ev["Mw"] - 0.7, orderby="magnitude", limit=3)
    js = json.loads(_get(USGS_FDSN, params))
    if not js.get("features"):
        raise RuntimeError(f"El USGS no devolvió eventos para {nombre}")
    feat = js["features"][0]
    detalle = json.loads(_get(feat["properties"]["detail"]))
    return detalle


def _producto_preferido(lista):
    return sorted(lista, key=lambda p: p.get("preferredWeight", 0), reverse=True)[0]


def extraer_metadatos(detalle):
    p = detalle["properties"]
    g = detalle["geometry"]["coordinates"]
    meta = dict(id_usgs=detalle["id"], titulo=p.get("title"), tiempo_utc=
                dt.datetime.fromtimestamp(p["time"] / 1000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                hipocentro=dict(lon=g[0], lat=g[1], prof_km=g[2]), magnitud=p.get("mag"),
                tipo_magnitud=p.get("magType"), url=p.get("url"), productos={})
    prods = p.get("products", {})
    if "moment-tensor" in prods:
        mt = _producto_preferido(prods["moment-tensor"])
        q = mt["properties"]
        def fl(k):
            try: return float(q[k])
            except (KeyError, TypeError, ValueError): return None
        meta["tensor"] = dict(
            fuente=mt.get("source"), metodo=q.get("derived-magnitude-type") or q.get("beachball-type"),
            M0_Nm=fl("scalar-moment"), Mw=fl("derived-magnitude"),
            centroide=dict(lon=fl("derived-longitude"), lat=fl("derived-latitude"),
                           prof_km=fl("derived-depth")),
            plano1=dict(rumbo=fl("nodal-plane-1-strike"), buz=fl("nodal-plane-1-dip"),
                        rake=fl("nodal-plane-1-rake") or fl("nodal-plane-1-slip")),
            plano2=dict(rumbo=fl("nodal-plane-2-strike"), buz=fl("nodal-plane-2-dip"),
                        rake=fl("nodal-plane-2-rake") or fl("nodal-plane-2-slip")))
        meta["productos"]["moment-tensor"] = mt.get("source")
    if "finite-fault" in prods:
        ff = _producto_preferido(prods["finite-fault"])
        cont = ff.get("contents", {})
        meta["productos"]["finite-fault"] = {k: v.get("url") for k, v in cont.items()
                                             if k.endswith((".param", ".fsp"))}
    return meta


def descargar_falla_finita(meta, carpeta):
    arch = meta["productos"].get("finite-fault") or {}
    for ext in (".param", ".fsp"):
        for nombre, url in arch.items():
            if nombre.endswith(ext) and url:
                destino = os.path.join(carpeta, "falla_finita" + ext)
                with open(destino, "wb") as fh:
                    fh.write(_get(url, binario=True))
                return destino
    return None


# ---------------------------------------------------------------------------
# Batimetría ETOPO 2022 (ERDDAP)
# ---------------------------------------------------------------------------
def descargar_etopo(region, destino, paso=4):
    """
    region = (lon_min, lon_max, lat_min, lat_max). paso=4 → 1 minuto de arco;
    paso=1 → 15 segundos de arco. Escribe un NetCDF.
    """
    lo0, lo1, la0, la1 = region
    q = f"z[({la0}):{paso}:({la1})][({lo0}):{paso}:({lo1})]"
    url = f"{ERDDAP}/{ETOPO_15S}.nc?" + urllib.parse.quote(q, safe="[]():")
    try:
        contenido = _get(url, binario=True, timeout=300)
    except RuntimeError:
        paso1 = max(1, paso // 4)
        q = f"altitude[({la0}):{paso1}:({la1})][({lo0}):{paso1}:({lo1})]"
        url = f"{ERDDAP}/{ETOPO_1M}.nc?" + urllib.parse.quote(q, safe="[]():")
        contenido = _get(url, binario=True, timeout=300)
    with open(destino, "wb") as fh:
        fh.write(contenido)
    return destino


def leer_batimetria(ruta):
    """Devuelve lon2d, lat2d, z (m; negativo en el mar) con latitud creciente."""
    if ruta.endswith(".npz"):
        d = np.load(ruta)
        return d["lon"], d["lat"], d["z"]
    import xarray as xr
    ds = xr.open_dataset(ruta)
    var = "z" if "z" in ds else ("altitude" if "altitude" in ds else list(ds.data_vars)[0])
    z = ds[var].values.astype(float)
    lat = ds["latitude"].values; lon = ds["longitude"].values
    if lat[1] < lat[0]:
        lat = lat[::-1]; z = z[::-1]
    LON, LAT = np.meshgrid(lon, lat)
    return LON, LAT, z


# ---------------------------------------------------------------------------
# Slab2 (USGS ScienceBase) — opcional
# ---------------------------------------------------------------------------
def descargar_slab2(codigo, destino):
    """
    Intenta descargar la malla de profundidad de Slab2 de la región indicada.
    Si falla, devuelve None y el cuaderno usa la geometría de la falla finita.
    Descarga manual: https://doi.org/10.5066/F7PV6JNV (archivo <codigo>_slab2_dep_*.grd).
    """
    if not codigo:
        return None
    try:
        q = dict(q=f"Slab2 {SLAB2_TITULOS[codigo]}", format="json", max=20, fields="title")
        items = json.loads(_get(f"{SCIENCEBASE}/items", q))["items"]
        for it in items:
            if "Slab2" not in it.get("title", ""):
                continue
            js = json.loads(_get(f"{SCIENCEBASE}/item/{it['id']}", dict(format="json")))
            for f in js.get("files", []):
                n = f.get("name", "")
                if n.startswith(codigo) and "_dep_" in n and n.endswith(".grd"):
                    with open(destino, "wb") as fh:
                        fh.write(_get(f["url"], binario=True, timeout=300))
                    return destino
    except Exception as e:
        print(f"   Slab2 ({codigo}) no descargado: {e}")
    return None


def leer_slab2(ruta):
    """Profundidad de la placa (km, positiva hacia abajo) en una malla lon/lat."""
    import xarray as xr
    ds = xr.open_dataset(ruta)
    var = list(ds.data_vars)[0]
    z = -ds[var].values.astype(float)        # Slab2 guarda la profundidad negativa
    xn = "x" if "x" in ds.coords else "lon"; yn = "y" if "y" in ds.coords else "lat"
    lon = ds[xn].values; lat = ds[yn].values
    lon = np.where(lon > 180, lon - 360, lon)
    if lat[1] < lat[0]:
        lat = lat[::-1]; z = z[::-1]
    LON, LAT = np.meshgrid(lon, lat)
    return LON, LAT, z


# ---------------------------------------------------------------------------
# Orquestador: preparar todos los datos de un evento
# ---------------------------------------------------------------------------
def preparar_evento(nombre, raiz="datos", slab=True, costa=True):
    c = carpeta_evento(nombre, raiz)
    informe = dict(evento=nombre, carpeta=c, fecha_descarga=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    print(f"■ {nombre}")
    detalle = buscar_evento_usgs(nombre)
    meta = extraer_metadatos(detalle)
    meta["catalogo_curso"] = EVENTOS[nombre]
    meta["localidades"] = LOCALIDADES[nombre]
    meta["region"] = region_sugerida(nombre)
    ff = descargar_falla_finita(meta, c)
    meta["archivo_falla_finita"] = os.path.basename(ff) if ff else None
    print(f"   USGS {meta['id_usgs']} · M{meta['magnitud']} · falla finita: {'sí' if ff else 'no'}")
    descargar_etopo(meta["region"], os.path.join(c, "batimetria_regional.nc"), paso=4)
    print("   batimetría regional (1′) lista")
    if costa:
        meta["batimetria_costa"] = {}
        for loc, (la, lo) in LOCALIDADES[nombre].items():
            arch = f"batimetria_costa_{slug(loc).replace('(', '').replace(')', '').replace(',', '')}.nc"
            try:
                descargar_etopo((lo - 0.3, lo + 0.3, la - 0.3, la + 0.3), os.path.join(c, arch), paso=1)
                meta["batimetria_costa"][loc] = arch
            except Exception as e:
                print(f"   batimetría costera de {loc} no descargada: {e}")
        print("   batimetría costera (15″) lista")
    if slab and EVENTOS[nombre]["slab"]:
        s = descargar_slab2(EVENTOS[nombre]["slab"], os.path.join(c, "slab2_profundidad.grd"))
        meta["archivo_slab2"] = os.path.basename(s) if s else None
        print(f"   Slab2: {'sí' if s else 'no (usar geometría de la falla finita)'}")
    obs = os.path.join(c, "observaciones.csv")
    if not os.path.exists(obs):
        with open(obs, "w", encoding="utf-8") as fh:
            fh.write(OBS_COLUMNAS)
    meta["informe_descarga"] = informe
    with open(os.path.join(c, "evento.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    return meta


# ---------------------------------------------------------------------------
# Lectura en el cuaderno de los estudiantes
# ---------------------------------------------------------------------------
def cargar_evento(nombre, raiz="datos"):
    c = os.path.join(raiz, slug(nombre))
    ruta_meta = os.path.join(c, "evento.json")
    if not os.path.exists(ruta_meta):
        raise FileNotFoundError(
            f"No hay datos de {nombre} en {c}. Ejecuten preparar_evento('{nombre}') "
            "o el cuaderno 00 del docente.")
    with open(ruta_meta, encoding="utf-8") as fh:
        meta = json.load(fh)
    out = dict(meta=meta, carpeta=c, falla_finita=None, slab2=None)
    for ext, lector in ((".param", leer_param_usgs), (".fsp", leer_fsp)):
        r = os.path.join(c, "falla_finita" + ext)
        if os.path.exists(r):
            out["falla_finita"] = lector(r, nombre)
            break
    for cand in ("batimetria_regional.nc", "batimetria_regional.npz"):
        r = os.path.join(c, cand)
        if os.path.exists(r):
            out["batimetria"] = leer_batimetria(r)
            break
    r = os.path.join(c, "slab2_profundidad.grd")
    if os.path.exists(r):
        try:
            out["slab2"] = leer_slab2(r)
        except Exception as e:
            print("Slab2 no se pudo leer:", e)
    out["observaciones"] = leer_observaciones(os.path.join(c, "observaciones.csv"))
    return out


def leer_observaciones(ruta):
    import csv
    if not os.path.exists(ruta):
        return []
    filas = []
    with open(ruta, encoding="utf-8") as fh:
        for f in csv.DictReader(fh):
            try:
                filas.append(dict(nombre=f["nombre"], lat=float(f["lat"]), lon=float(f["lon"]),
                                  uE=_num(f.get("uE_m")), uN=_num(f.get("uN_m")),
                                  uz=_num(f.get("uz_m")), sigma=_num(f.get("sigma_m")),
                                  tipo=f.get("tipo", ""), fuente=f.get("fuente", "")))
            except (KeyError, ValueError):
                continue
    return filas


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None
