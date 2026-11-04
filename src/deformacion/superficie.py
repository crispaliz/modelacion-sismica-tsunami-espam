"""
Del fondo marino a la superficie del mar.

1. Aporte del desplazamiento horizontal sobre la pendiente del fondo
   (Tanioka y Satake, 1996):  u_h = uE ∂H/∂E + uN ∂H/∂N,  H = profundidad del agua.
2. Filtro de Kajiura (1963): el agua no copia los detalles de la deformación del
   fondo más pequeños que su profundidad. En el número de onda k la superficie es
   η(k) = u_fondo(k) / cosh(k h).

Referencias
-----------
Tanioka, Y., & Satake, K. (1996). Tsunami generation by horizontal displacement
of ocean bottom. Geophysical Research Letters, 23(8), 861-864.
Kajiura, K. (1963). The leading wave of a tsunami. Bulletin of the Earthquake
Research Institute, 41, 535-571.
"""
import numpy as np

from .fuentes import KM_POR_GRADO_LAT, KM_POR_GRADO_LON_ECUADOR


def pasos_metros(lon, lat):
    """Espaciamiento de la malla (dx, dy) en metros, usando la latitud media."""
    lon = np.asarray(lon); lat = np.asarray(lat)
    dlon = float(np.abs(lon[0, 1] - lon[0, 0]))
    dlat = float(np.abs(lat[1, 0] - lat[0, 0]))
    latm = float(np.mean(lat))
    dx = dlon * KM_POR_GRADO_LON_ECUADOR * 1e3 * np.cos(np.radians(latm))
    dy = dlat * KM_POR_GRADO_LAT * 1e3
    return dx, dy


def aporte_horizontal(uE, uN, lon, lat, z_topo):
    """
    Levantamiento aparente del fondo por el movimiento horizontal sobre la pendiente.
    z_topo: elevación (m), negativa en el mar. Devuelve 0 en tierra.
    """
    H = np.where(z_topo < 0, -z_topo, 0.0)
    dx, dy = pasos_metros(lon, lat)
    signo_y = 1.0 if lat[1, 0] > lat[0, 0] else -1.0
    dHdy, dHdx = np.gradient(H, dy, dx)
    dHdy = signo_y * dHdy
    uh = uE * dHdx + uN * dHdy
    return np.where(z_topo < 0, uh, 0.0)


def filtro_kajiura(u_fondo, z_topo, lon, lat, niveles=None, relleno=0.5):
    """
    Superficie inicial del mar a partir del levantamiento del fondo.

    Como la profundidad cambia de un punto a otro, se filtra el campo completo
    para varias profundidades de referencia y en cada punto se interpola según
    su profundidad local. En tierra devuelve 0.
    """
    h = np.where(z_topo < 0, -z_topo, 0.0)
    if niveles is None:
        hmax = max(float(h.max()), 100.0)
        niveles = np.unique(np.concatenate([[0.0], np.geomspace(50.0, hmax, 12)]))
    dx, dy = pasos_metros(lon, lat)
    ny, nx = u_fondo.shape
    py, px = int(ny * relleno), int(nx * relleno)
    U = np.pad(np.where(z_topo < 0, u_fondo, 0.0), ((py, py), (px, px)))
    F = np.fft.fft2(U)
    ky = 2 * np.pi * np.fft.fftfreq(U.shape[0], d=dy)
    kx = 2 * np.pi * np.fft.fftfreq(U.shape[1], d=dx)
    K = np.sqrt(kx[None, :] ** 2 + ky[:, None] ** 2)
    capas = []
    for hj in niveles:
        filt = np.real(np.fft.ifft2(F / np.cosh(np.minimum(K * hj, 700.0))))
        capas.append(filt[py:py + ny, px:px + nx])
    capas = np.array(capas)
    # interpolación lineal en profundidad
    idx = np.clip(np.searchsorted(niveles, h) - 1, 0, len(niveles) - 2)
    h0 = niveles[idx]; h1 = niveles[idx + 1]
    w = np.clip((h - h0) / np.maximum(h1 - h0, 1e-9), 0.0, 1.0)
    jj, ii = np.indices(h.shape)
    eta = (1 - w) * capas[idx, jj, ii] + w * capas[idx + 1, jj, ii]
    return np.where(z_topo < 0, eta, 0.0)


def volumen_desplazado(eta, lon, lat, z_topo=None):
    """Volumen de agua levantado y hundido (m³) sobre el mar."""
    dx, dy = pasos_metros(lon, lat)
    m = np.ones_like(eta, bool) if z_topo is None else (z_topo < 0)
    pos = float(np.sum(np.where(m & (eta > 0), eta, 0.0)) * dx * dy)
    neg = float(np.sum(np.where(m & (eta < 0), eta, 0.0)) * dx * dy)
    return pos, neg


def energia_potencial(eta, lon, lat, z_topo=None, rho=1025.0, g=9.81):
    """Energía potencial inicial del tsunami: E = ½ ρ g ∬ η² dA (J)."""
    dx, dy = pasos_metros(lon, lat)
    m = np.ones_like(eta, bool) if z_topo is None else (z_topo < 0)
    return float(0.5 * rho * g * np.sum(np.where(m, eta, 0.0) ** 2) * dx * dy)
