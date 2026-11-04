"""Pruebas del paquete deformacion. Ejecutar: python -m pytest -q tests/"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import deformacion as dfm  # noqa: E402


def test_tabla2_okada1985_caso2():
    # Okada (1985), Tabla 2, caso 2: x=2, y=3, d=4, δ=70°, L=3, W=2 (4 cifras publicadas)
    ux, uy, uz = dfm.okada85(2.0, 3.0, 4.0, 70.0, 3.0, 2.0, U1=1.0)
    assert np.allclose([ux, uy, uz], [-8.689e-3, -4.298e-3, -2.747e-3], rtol=5e-4, atol=0)
    ux, uy, uz = dfm.okada85(2.0, 3.0, 4.0, 70.0, 3.0, 2.0, U2=1.0)
    assert np.allclose([ux, uy, uz], [-4.682e-3, -3.527e-2, -3.564e-2], rtol=5e-4, atol=0)


def test_linealidad_y_escala():
    x = np.linspace(-50, 150, 51); y = np.linspace(-80, 80, 41)
    X, Y = np.meshgrid(x, y)
    a = dfm.okada85(X, Y, 20, 15, 100, 50, U2=1.0)[2]
    b = dfm.okada85(X, Y, 20, 15, 100, 50, U2=2.0)[2]
    c = dfm.okada85(2 * X, 2 * Y, 40, 15, 200, 100, U2=1.0)[2]
    assert np.allclose(b, 2 * a) and np.allclose(c, a)


def test_inversa_levanta_sobre_el_borde_superior():
    f = dfm.falla_uniforme(-80, 0, 15, 0, 15, 90, L=100, W=50, slip=2.0)
    s = f.subfallas[0]
    # rumbo 0 → buza al este: el borde superior está al oeste del centroide
    lon_sup, _ = dfm.km_a_geo(-0.5 * s.W * np.cos(np.radians(15)), 0, -80, 0)
    uz_sup = f.desplazamiento(np.array([lon_sup]), np.array([0.0]))[2][0]
    assert uz_sup > 0.5


def test_convencion_rake_aki_richards():
    # λ = 0 (lateral izquierda): el bloque de techo se mueve en la dirección del rumbo.
    # Falla vertical-ish de rumbo 0 que buza al este: el techo está al este.
    f = dfm.falla_uniforme(-80, 0, 10, 0, 80, 0, L=60, W=20, slip=1.0)
    lon_e, _ = dfm.km_a_geo(15, 0, -80, 0)
    uE, uN, uz = f.desplazamiento(np.array([lon_e]), np.array([0.0]))
    assert uN[0] > 0


def test_subdividir_equivale_a_uniforme():
    f = dfm.falla_uniforme(-80, 0, 20, 30, 20, 90, L=80, W=40, slip=1.5)
    g = dfm.subdividir(f, 8, 4)
    LON, LAT = dfm.malla((-81.5, -78.5, -1.5, 1.5), 0.1)
    a = f.desplazamiento(LON, LAT)[2]
    b = g.desplazamiento(LON, LAT)[2]
    assert np.max(np.abs(a - b)) < 1e-4 * np.abs(a).max()
    assert abs(f.momento() - g.momento()) / f.momento() < 1e-9


def test_rotacion_coherente():
    LON, LAT = dfm.malla((-81.5, -78.5, -1.5, 1.5), 0.05)
    a = dfm.falla_uniforme(-80, 0, 20, 0, 20, 90, L=80, W=40, slip=1.0).desplazamiento(LON, LAT)[2]
    b = dfm.falla_uniforme(-80, 0, 20, 90, 20, 90, L=80, W=40, slip=1.0).desplazamiento(LON, LAT)[2]
    # Rumbo 90 = rumbo 0 rotado 90° en sentido horario: comparar máximos y simetría
    assert np.isclose(a.max(), b.max(), rtol=2e-2) and np.isclose(a.min(), b.min(), rtol=2e-2)


def test_kajiura():
    LON, LAT = dfm.malla((-82, -78, -2, 2), 1 / 60)
    z = -4000 * np.ones_like(LON)
    r2 = dfm.geo_a_km(LON, LAT, -80, 0)
    R2 = r2[0] ** 2 + r2[1] ** 2
    ancho = np.exp(-R2 / (2 * 80.0 ** 2))       # 80 km >> 4 km: casi sin cambio
    angosto = np.exp(-R2 / (2 * 3.0 ** 2))      # 3 km < 4 km: se atenúa mucho
    assert dfm.filtro_kajiura(ancho, z, LON, LAT).max() > 0.97
    assert dfm.filtro_kajiura(angosto, z, LON, LAT).max() < 0.5


def test_param_usgs_y_dtopo(tmp_path):
    p = tmp_path / "f.param"
    p.write_text(
        "#Total number of fault_segments=     1\n"
        "#Fault_segment =   1 nx(Along-strike)=   2 Dx= 20.00km ny(downdip)=   1 Dy= 20.00km\n"
        "#Boundary of Fault_segment     1. EQ in cell (1,1). Lon:  -80.0000   Lat:    0.0000\n"
        "#Lat. Lon. depth slip rake strike dip t_rup t_ris t_fal mo\n"
        "  0.0000  -80.0000  15.0  150.0  90.0  20.0  15.0  0.0  4.0  4.0  1.8e+27\n"
        "  0.1700  -79.9400  15.0  250.0  95.0  20.0  15.0  8.0  4.0  4.0  3.0e+27\n")
    f = dfm.leer_param_usgs(str(p))
    assert len(f) == 2 and np.isclose(f.slip.max(), 2.5) and f.subfallas[0].L == 20.0
    from deformacion.exportar import escribir_dtopo_tt3
    LON, LAT = dfm.malla((-80.5, -79.5, -0.5, 0.5), 0.1)
    dz = f.desplazamiento(LON, LAT)[2]
    escribir_dtopo_tt3(str(tmp_path / "d.tt3"), LON, LAT, dz)
    lineas = (tmp_path / "d.tt3").read_text().splitlines()
    assert int(lineas[0].split()[0]) == LON.shape[1] and len(lineas) == 9 + LON.shape[0]


def test_subfalla_que_asoma_se_recorta():
    # Centroide a 0,5 km con W = 10 km y δ = 15°: el borde superior quedaría sobre el fondo
    s = dfm.Subfalla(-80, 0, 0.5, 0, 15, 90, 10, 10, 1.0)
    assert s.prof_sup < 0
    LON, LAT = dfm.malla((-80.5, -79.5, -0.5, 0.5), 0.02)
    uz = s.desplazamiento(LON, LAT)[2]
    assert np.all(np.isfinite(uz)) and 0.1 < np.abs(uz).max() < 2.0
