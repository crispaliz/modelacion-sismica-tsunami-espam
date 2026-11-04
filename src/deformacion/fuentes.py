"""
Fuentes sísmicas para Okada: subfallas, fallas uniformes y modelos de falla
finita del USGS, con conversión entre coordenadas geográficas y los ejes de
Okada (1985).

Unidades internas: longitudes en km, deslizamiento en m, momento en N·m,
rigidez en Pa, tiempos en s, ángulos en grados.
"""
from dataclasses import dataclass, field, replace
import re
import numpy as np

from .okada import okada85

KM_POR_GRADO_LAT = 110.574
KM_POR_GRADO_LON_ECUADOR = 111.320
MU_REF = 30e9  # Pa, rigidez de referencia
Z_MIN_SUP = 0.05  # km, profundidad mínima del borde superior de una subfalla


# ---------------------------------------------------------------------------
# Geografía
# ---------------------------------------------------------------------------
def _dlon(lon, lon0):
    """Diferencia de longitud en (-180, 180]."""
    return (np.asarray(lon) - lon0 + 180.0) % 360.0 - 180.0


def geo_a_km(lon, lat, lon0, lat0):
    """Proyección plana local (equirectangular) alrededor de (lon0, lat0): ΔE, ΔN en km."""
    dE = _dlon(lon, lon0) * KM_POR_GRADO_LON_ECUADOR * np.cos(np.radians(lat0))
    dN = (np.asarray(lat) - lat0) * KM_POR_GRADO_LAT
    return dE, dN


def km_a_geo(dE, dN, lon0, lat0):
    lon = lon0 + np.asarray(dE) / (KM_POR_GRADO_LON_ECUADOR * np.cos(np.radians(lat0)))
    lat = lat0 + np.asarray(dN) / KM_POR_GRADO_LAT
    return (lon + 180.0) % 360.0 - 180.0, lat


def momento_a_mw(M0):
    """Mw de Hanks y Kanamori (1979) con M0 en N·m."""
    return 2.0 / 3.0 * (np.log10(M0) - 9.1)


def mw_a_momento(Mw):
    return 10 ** (1.5 * Mw + 9.1)


# ---------------------------------------------------------------------------
# Subfalla
# ---------------------------------------------------------------------------
@dataclass
class Subfalla:
    """Rectángulo con deslizamiento uniforme. (lon, lat, prof) es el CENTROIDE."""
    lon: float
    lat: float
    prof: float          # km, profundidad del centroide
    rumbo: float         # grados
    buz: float           # grados
    rake: float          # grados
    L: float             # km, largo según el rumbo
    W: float             # km, ancho según el buzamiento
    slip: float          # m
    t_rup: float = 0.0   # s, inicio del deslizamiento
    t_sub: float = 1.0   # s, duración del deslizamiento (subida + bajada)

    @property
    def prof_sup(self):
        return self.prof - 0.5 * self.W * np.sin(np.radians(self.buz))

    @property
    def prof_inf(self):
        return self.prof + 0.5 * self.W * np.sin(np.radians(self.buz))

    def momento(self, mu=MU_REF):
        return mu * self.L * 1e3 * self.W * 1e3 * self.slip

    def esquinas(self):
        """Las 4 esquinas en planta (lon, lat) y su profundidad, en orden de recorrido."""
        phi, dl = np.radians(self.rumbo), np.radians(self.buz)
        s = np.array([np.sin(phi), np.cos(phi)])          # rumbo (E, N)
        b = np.array([np.cos(phi), -np.sin(phi)])         # buzamiento hacia abajo (E, N)
        hw = 0.5 * self.W * np.cos(dl)
        pts = []
        for a, c in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            e, n = a * 0.5 * self.L * s + c * hw * b
            pts.append((e, n, self.prof + c * 0.5 * self.W * np.sin(dl)))
        pts = np.array(pts)
        lon, lat = km_a_geo(pts[:, 0], pts[:, 1], self.lon, self.lat)
        return lon, lat, pts[:, 2]

    def desplazamiento(self, lon, lat, nu=0.25):
        """(uE, uN, uz) en metros en los puntos (lon, lat)."""
        dE, dN = geo_a_km(lon, lat, self.lon, self.lat)
        phi = np.radians(self.rumbo)
        dl = np.radians(self.buz)
        # Ejes de la falla: x según el rumbo, y hacia arriba del buzamiento
        x = dN * np.cos(phi) + dE * np.sin(phi)
        y = dN * np.sin(phi) - dE * np.cos(phi)
        # Del centroide al origen de Okada (esquina del borde profundo)
        x_ok = x + 0.5 * self.L
        y_ok = y + 0.5 * self.W * np.cos(dl)
        d = self.prof + 0.5 * self.W * np.sin(dl)
        # Si la subfalla asoma sobre la superficie (pasa en algunos modelos del USGS
        # cerca de la fosa), se recorta la parte que queda fuera del semiespacio:
        # el borde profundo (origen de Okada) no cambia, solo el ancho efectivo.
        W_ef = self.W
        if d - self.W * np.sin(dl) < Z_MIN_SUP:
            W_ef = max((d - Z_MIN_SUP) / max(np.sin(dl), 1e-6), 1e-3)
        U1 = self.slip * np.cos(np.radians(self.rake))
        U2 = self.slip * np.sin(np.radians(self.rake))
        ux, uy, uz = okada85(x_ok, y_ok, d, self.buz, self.L, W_ef, U1, U2, nu)
        uE = ux * np.sin(phi) - uy * np.cos(phi)
        uN = ux * np.cos(phi) + uy * np.sin(phi)
        return uE, uN, uz


# ---------------------------------------------------------------------------
# Falla (conjunto de subfallas)
# ---------------------------------------------------------------------------
@dataclass
class Falla:
    subfallas: list
    nombre: str = ""
    origen: str = ""                 # "USGS falla finita", "uniforme", ...
    hipocentro: tuple = None         # (lon, lat, prof)

    def __len__(self):
        return len(self.subfallas)

    @property
    def slip(self):
        return np.array([s.slip for s in self.subfallas])

    def momento(self, mu=MU_REF):
        return float(sum(s.momento(mu) for s in self.subfallas))

    def mw(self, mu=MU_REF):
        return float(momento_a_mw(self.momento(mu)))

    def resumen(self, mu=MU_REF):
        sl = self.slip
        pz = np.array([s.prof for s in self.subfallas])
        return dict(nombre=self.nombre, origen=self.origen, n_subfallas=len(self),
                    slip_max_m=float(sl.max()), slip_medio_m=float(sl.mean()),
                    prof_min_km=float(min(s.prof_sup for s in self.subfallas)),
                    prof_max_km=float(max(s.prof_inf for s in self.subfallas)),
                    centroide_prof_km=float(np.average(pz, weights=np.maximum(sl, 1e-9))),
                    M0_Nm=self.momento(mu), Mw=self.mw(mu))

    def extension(self, margen=1.0):
        """Caja (lon_min, lon_max, lat_min, lat_max) que contiene la falla + margen en grados."""
        lons, lats = [], []
        for s in self.subfallas:
            lo, la, _ = s.esquinas()
            lons += list(lo); lats += list(la)
        return (min(lons) - margen, max(lons) + margen, min(lats) - margen, max(lats) + margen)

    def desplazamiento(self, lon, lat, nu=0.25, umbral_slip=1e-3):
        uE = np.zeros(np.shape(lon)); uN = np.zeros_like(uE); uz = np.zeros_like(uE)
        for s in self.subfallas:
            if s.slip < umbral_slip:
                continue
            e, n, z = s.desplazamiento(lon, lat, nu)
            uE += e; uN += n; uz += z
        return uE, uN, uz

    def desplazamiento_por_subfalla(self, lon, lat, nu=0.25, componentes=("uz",)):
        """Campos de cada subfalla apilados (n, ...) en float32, para la cinemática."""
        idx = {"uE": 0, "uN": 1, "uz": 2}
        out = {c: np.zeros((len(self),) + np.shape(lon), dtype=np.float32) for c in componentes}
        for i, s in enumerate(self.subfallas):
            u = s.desplazamiento(lon, lat, nu)
            for c in componentes:
                out[c][i] = u[idx[c]]
        return out

    def con_slip(self, nuevo_slip, origen=None):
        subs = [replace(s, slip=float(v)) for s, v in zip(self.subfallas, nuevo_slip)]
        return Falla(subs, self.nombre, origen or self.origen, self.hipocentro)


# ---------------------------------------------------------------------------
# Modelos de falla finita del USGS
# ---------------------------------------------------------------------------
def leer_param_usgs(ruta, nombre=""):
    """
    Lee un archivo .param de falla finita del USGS (formato UCSB).

    Cada fila: Lat. Lon. depth(km) slip(cm) rake strike dip t_rup t_ris t_fal mo(dyn·cm).
    Las coordenadas corresponden al centro de la subfalla. Dx y Dy (km) se leen
    del encabezado de cada segmento.
    """
    subs, Dx, Dy = [], None, None
    hipo = None
    with open(ruta, encoding="utf-8", errors="ignore") as fh:
        for linea in fh:
            t = linea.strip()
            if not t:
                continue
            if t.startswith("#"):
                m = re.search(r"Dx\s*=\s*([\d.]+)\s*km.*Dy\s*=\s*([\d.]+)\s*km", t)
                if m:
                    Dx, Dy = float(m.group(1)), float(m.group(2))
                m = re.search(r"Lon:\s*([-\d.]+)\s+Lat:\s*([-\d.]+)", t)
                if m and hipo is None:
                    hipo = (float(m.group(1)), float(m.group(2)), None)
                continue
            c = t.split()
            if len(c) < 11 or Dx is None:
                continue
            try:
                v = [float(a) for a in c[:11]]
            except ValueError:
                continue
            lat, lon, z, slip_cm, rake, rumbo, buz, t_rup, t_ris, t_fal, mo = v
            subs.append(Subfalla(lon=lon, lat=lat, prof=z, rumbo=rumbo, buz=buz,
                                 rake=rake, L=Dx, W=Dy, slip=slip_cm / 100.0,
                                 t_rup=t_rup, t_sub=max(t_ris + t_fal, 1.0)))
    if not subs:
        raise ValueError(f"No se encontraron subfallas en {ruta}")
    return Falla(subs, nombre, "USGS falla finita", hipo)


def leer_fsp(ruta, nombre=""):
    """Lector básico de archivos .fsp (SRCMOD / USGS). Usa .param si está disponible."""
    subs, rumbo, buz, Dx, Dz = [], None, None, None, None
    cols = None
    with open(ruta, encoding="utf-8", errors="ignore") as fh:
        for linea in fh:
            t = linea.strip()
            if t.startswith("%"):
                m = re.search(r"STRI?K?E?\s*=\s*([-\d.]+)", t)
                if m: rumbo = float(m.group(1))
                m = re.search(r"DIP\s*=\s*([-\d.]+)", t)
                if m: buz = float(m.group(1))
                m = re.search(r"Dx\s*=\s*([\d.]+)\s*km.*Dz\s*=\s*([\d.]+)\s*km", t)
                if m: Dx, Dz = float(m.group(1)), float(m.group(2))
                if "LAT" in t and "LON" in t and "SLIP" in t:
                    cols = t.lstrip("%").split()
                continue
            if not t or cols is None:
                continue
            v = t.split()
            try:
                d = dict(zip(cols, [float(a) for a in v]))
            except ValueError:
                continue
            subs.append(Subfalla(lon=d["LON"], lat=d["LAT"], prof=d.get("Z", 10.0),
                                 rumbo=rumbo, buz=buz, rake=d.get("RAKE", 90.0),
                                 L=Dx, W=Dz, slip=d["SLIP"],
                                 t_rup=d.get("TRUP", 0.0), t_sub=max(d.get("RISE", 1.0), 1.0)))
    if not subs:
        raise ValueError(f"No se encontraron subfallas en {ruta}")
    return Falla(subs, nombre, "falla finita (.fsp)")


# ---------------------------------------------------------------------------
# Falla uniforme a partir de la ficha (Unidad 1) o de leyes de escala
# ---------------------------------------------------------------------------
def escalamiento(Mw, tipo="interfase"):
    """
    Largo y ancho (km) a partir de Mw.
    - interfase: Strasser et al. (2010), sismos de interfase de subducción.
    - otro: Wells y Coppersmith (1994), todas las fallas (RLD y RW).
    """
    if tipo == "interfase":
        return 10 ** (-2.477 + 0.585 * Mw), 10 ** (-0.882 + 0.351 * Mw)
    return 10 ** (-2.44 + 0.59 * Mw), 10 ** (-1.01 + 0.32 * Mw)


def falla_uniforme(lon, lat, prof, rumbo, buz, rake, Mw=None, M0=None, L=None, W=None,
                   slip=None, mu=MU_REF, tipo_escala="interfase", nombre=""):
    """
    Rectángulo uniforme centrado en (lon, lat, prof) = centroide.
    Lo que no se entregue se completa: L y W por escalamiento; slip = M0 / (mu L W).
    Si el borde superior quedara sobre la superficie, se profundiza el centroide.
    """
    if M0 is None and Mw is not None:
        M0 = mw_a_momento(Mw)
    if Mw is None and M0 is not None:
        Mw = momento_a_mw(M0)
    if L is None or W is None:
        Le, We = escalamiento(Mw, tipo_escala)
        L = L or Le
        W = W or We
    if slip is None:
        slip = M0 / (mu * L * 1e3 * W * 1e3)
    sup = prof - 0.5 * W * np.sin(np.radians(buz))
    aviso = ""
    if sup < 1.0:
        prof = prof + (1.0 - sup)
        aviso = f" (centroide profundizado a {prof:.1f} km para que el borde superior quede a 1 km)"
    s = Subfalla(lon, lat, prof, rumbo, buz, rake, L, W, slip)
    f = Falla([s], nombre, "uniforme" + aviso)
    return f


def subdividir(falla_un, nx=10, ny=5, hipocentro=None, vr=2.5, t_sub=None):
    """
    Divide una falla uniforme (una subfalla) en nx × ny subfallas con el mismo slip
    y asigna tiempos de ruptura = distancia al hipocentro / vr (km/s).
    """
    s0 = falla_un.subfallas[0]
    phi, dl = np.radians(s0.rumbo), np.radians(s0.buz)
    sv = np.array([np.sin(phi), np.cos(phi)])          # rumbo en (E, N)
    bv = np.array([np.cos(phi), -np.sin(phi)])         # hacia abajo del buzamiento
    dx, dy = s0.L / nx, s0.W / ny
    if t_sub is None:
        t_sub = max(2.0, 0.1 * min(dx, dy) / vr * 10)
    centros = []
    for j in range(ny):
        for i in range(nx):
            a = -0.5 * s0.L + (i + 0.5) * dx
            c = -0.5 * s0.W + (j + 0.5) * dy
            e, n = a * sv + c * np.cos(dl) * bv
            z = s0.prof + c * np.sin(dl)
            centros.append((e, n, z))
    centros = np.array(centros)
    if hipocentro is None:
        h = np.array([0.0, 0.0, s0.prof])
    else:
        he, hn = geo_a_km(hipocentro[0], hipocentro[1], s0.lon, s0.lat)
        h = np.array([float(he), float(hn), hipocentro[2] if hipocentro[2] else s0.prof])
    dist = np.sqrt(((centros - h) ** 2).sum(axis=1))
    lon, lat = km_a_geo(centros[:, 0], centros[:, 1], s0.lon, s0.lat)
    subs = [Subfalla(float(lo), float(la), float(z), s0.rumbo, s0.buz, s0.rake, dx, dy,
                     s0.slip, float(d / vr), float(t_sub))
            for lo, la, z, d in zip(lon, lat, centros[:, 2], dist)]
    return Falla(subs, falla_un.nombre, falla_un.origen + f" subdividida {nx}x{ny}",
                 hipocentro or (s0.lon, s0.lat, s0.prof))


# ---------------------------------------------------------------------------
# Rigidez variable con la profundidad
# ---------------------------------------------------------------------------
def mu_rampa(prof_km, mu_somero=10e9, mu_profundo=40e9, z1=5.0, z2=20.0):
    """Rigidez ilustrativa: mu_somero hasta z1, rampa lineal hasta mu_profundo en z2."""
    z = np.asarray(prof_km, dtype=float)
    f = np.clip((z - z1) / (z2 - z1), 0.0, 1.0)
    return mu_somero + f * (mu_profundo - mu_somero)


def reescalar_por_rigidez(falla, funcion_mu=mu_rampa, mu_ref=MU_REF, **kw):
    """
    Mantiene el momento de cada subfalla (calculado con mu_ref) y recalcula el
    deslizamiento con una rigidez que depende de la profundidad:
        slip_nuevo = slip · mu_ref / mu(z)
    Donde la roca es más blanda, el mismo momento exige más deslizamiento.
    """
    mu = funcion_mu(np.array([s.prof for s in falla.subfallas]), **kw)
    return falla.con_slip(falla.slip * mu_ref / mu, origen=falla.origen + " · mu(z)")
