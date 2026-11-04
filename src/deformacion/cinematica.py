"""
Cinemática de la ruptura: cómo crece la deformación mientras la ruptura avanza.

Cada subfalla empieza a deslizar en su tiempo de ruptura t_rup y completa su
deslizamiento en t_sub segundos con una función de subida suave (coseno).
Por linealidad, el campo en el instante t es la suma de los campos de cada
subfalla multiplicados por la fracción de deslizamiento alcanzada.
"""
import numpy as np


def fraccion_subida(t, t0, T):
    """0 antes de t0, rampa coseno hasta 1 en t0 + T."""
    tau = np.clip((np.asarray(t, float) - t0) / max(T, 1e-6), 0.0, 1.0)
    return 0.5 * (1.0 - np.cos(np.pi * tau))


def tiempos_sugeridos(falla, n=40):
    t_fin = max(s.t_rup + s.t_sub for s in falla.subfallas)
    return np.linspace(0.0, t_fin, n)


def campo_en_el_tiempo(campos_subfalla, falla, tiempos):
    """
    campos_subfalla: array (n_subfallas, ny, nx) del campo final de cada subfalla.
    Devuelve (n_tiempos, ny, nx).
    """
    out = np.zeros((len(tiempos),) + campos_subfalla.shape[1:], dtype=np.float32)
    for k, t in enumerate(tiempos):
        w = np.array([fraccion_subida(t, s.t_rup, s.t_sub) for s in falla.subfallas],
                     dtype=np.float32)
        out[k] = np.tensordot(w, campos_subfalla, axes=1)
    return out


def frente_de_ruptura(falla, t):
    """Subfallas activas (deslizando) y terminadas en el instante t."""
    activa = np.array([(s.t_rup <= t) and (t < s.t_rup + s.t_sub) for s in falla.subfallas])
    hecha = np.array([t >= s.t_rup + s.t_sub for s in falla.subfallas])
    return activa, hecha
