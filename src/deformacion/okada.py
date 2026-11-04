"""
Okada (1985): desplazamiento en la superficie de un semiespacio elástico
producido por una falla rectangular con deslizamiento uniforme.

Referencia
----------
Okada, Y. (1985). Surface deformation due to shear and tensile faults in a
half-space. Bulletin of the Seismological Society of America, 75(4), 1135-1154.

Convenciones (las del artículo)
-------------------------------
- Origen en la superficie, verticalmente sobre la esquina del BORDE PROFUNDO.
- x: a lo largo del rumbo. y: horizontal, hacia arriba del buzamiento.
  z: hacia arriba. d: profundidad del borde profundo (positiva hacia abajo).
- La falla ocupa 0 <= xi <= L (rumbo) y 0 <= eta <= W (buzamiento, desde
  el borde profundo hacia el superior).
- U1: componente de rumbo, U2: componente de buzamiento (U2 > 0 = inversa).
- Unidades: cualquier unidad de longitud coherente para x, y, d, L, W;
  el desplazamiento sale en la unidad de U1 y U2.

Verificada contra la Tabla 2 del artículo (caso 2). Ver tests/test_okada.py.
"""
import numpy as np

_EPS = 1e-12


def _terminos_I(xi, eta, q, dip, nu):
    """Términos I1..I5 de Okada (1985), ec. 28 (cos δ != 0) y ec. 29 (cos δ = 0)."""
    cd, sd = np.cos(dip), np.sin(dip)
    R = np.sqrt(xi**2 + eta**2 + q**2)
    yb = eta * cd + q * sd           # y tilde
    db = eta * sd - q * cd           # d tilde
    m = 1.0 - 2.0 * nu               # mu / (lambda + mu)
    with np.errstate(divide="ignore", invalid="ignore"):
        if abs(cd) > 1e-6:
            X = np.sqrt(xi**2 + q**2)
            I5 = m * 2.0 / cd * np.arctan(
                (eta * (X + q * cd) + X * (R + X) * sd) / (xi * (R + X) * cd))
            I5 = np.where(np.abs(xi) < _EPS, 0.0, I5)
            I4 = m / cd * (np.log(R + db) - sd * np.log(R + eta))
            I3 = m * (yb / (cd * (R + db)) - np.log(R + eta)) + sd / cd * I4
            I2 = m * (-np.log(R + eta)) - I3
            I1 = m * (-xi / (cd * (R + db))) - sd / cd * I5
        else:  # falla vertical
            I1 = -m / 2.0 * xi * q / (R + db) ** 2
            I3 = m / 2.0 * (eta / (R + db) + yb * q / (R + db) ** 2 - np.log(R + eta))
            I2 = m * (-np.log(R + eta)) - I3
            I4 = -m * q / (R + db)
            I5 = -m * xi * sd / (R + db)
    return R, yb, db, I1, I2, I3, I4, I5


def _f_esquina(xi, eta, q, dip, U1, U2, nu):
    """Expresión de Okada evaluada en una esquina (antes de la notación de Chinnery)."""
    cd, sd = np.cos(dip), np.sin(dip)
    R, yb, db, I1, I2, I3, I4, I5 = _terminos_I(xi, eta, q, dip, nu)
    with np.errstate(divide="ignore", invalid="ignore"):
        at = np.arctan(xi * eta / (q * R))
        at = np.where(np.abs(q) < _EPS, 0.0, at)
        ux = (-U1 / (2 * np.pi) * (xi * q / (R * (R + eta)) + at + I1 * sd)
              - U2 / (2 * np.pi) * (q / R - I3 * sd * cd))
        uy = (-U1 / (2 * np.pi) * (yb * q / (R * (R + eta)) + q * cd / (R + eta) + I2 * sd)
              - U2 / (2 * np.pi) * (yb * q / (R * (R + xi)) + cd * at - I1 * sd * cd))
        uz = (-U1 / (2 * np.pi) * (db * q / (R * (R + eta)) + q * sd / (R + eta) + I4 * sd)
              - U2 / (2 * np.pi) * (db * q / (R * (R + xi)) + sd * at - I5 * sd * cd))
    return ux, uy, uz


def okada85(x, y, d, dip_grados, L, W, U1=0.0, U2=0.0, nu=0.25):
    """
    Desplazamiento (ux, uy, uz) en la superficie en los ejes de Okada (1985).

    x, y : arrays de coordenadas de observación (ejes de Okada).
    d    : profundidad del borde profundo (> 0).
    Devuelve tres arrays con la forma de x.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    dip = np.radians(dip_grados)
    p = y * np.cos(dip) + d * np.sin(dip)
    q = y * np.sin(dip) - d * np.cos(dip)

    def f(xi, eta):
        return np.array(_f_esquina(xi, eta, q, dip, U1, U2, nu))

    # Notación de Chinnery: f(x,p) - f(x,p-W) - f(x-L,p) + f(x-L,p-W)
    u = f(x, p) - f(x, p - W) - f(x - L, p) + f(x - L, p - W)
    u = np.nan_to_num(u, nan=0.0, posinf=0.0, neginf=0.0)
    return u[0], u[1], u[2]
