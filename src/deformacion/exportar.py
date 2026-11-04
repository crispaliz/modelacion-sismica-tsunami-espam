"""
Exportación de resultados para la modelación de tsunamis (Unidades 3 y 4).

- dtopo de GeoClaw, tipo 3 (estático o con tiempo).
- topo de GeoClaw, tipo 3 (ASCII) y NetCDF.
- NetCDF/NPZ con todos los campos de la Unidad 2.
"""
import json
import numpy as np


def _asegurar_lat_creciente(lat, *campos):
    if lat[1, 0] < lat[0, 0]:
        return (lat[::-1],) + tuple(c[..., ::-1, :] for c in campos)
    return (lat,) + campos


def escribir_dtopo_tt3(ruta, lon, lat, dz, tiempos=None):
    """
    Archivo dtopo tipo 3 de GeoClaw.
    dz: (ny, nx) para deformación estática o (nt, ny, nx) con tiempos (s).
    """
    dz = np.asarray(dz, dtype=float)
    if dz.ndim == 2:
        dz = dz[None]
        tiempos = np.array([0.0]) if tiempos is None else np.atleast_1d(tiempos)
    lat, dz = _asegurar_lat_creciente(lat, dz)
    nt, ny, nx = dz.shape
    x0, y0 = float(lon[0, 0]), float(lat[0, 0])
    dx = float(lon[0, 1] - lon[0, 0]); dy = float(lat[1, 0] - lat[0, 0])
    t0 = float(tiempos[0]); dt = float(tiempos[1] - tiempos[0]) if nt > 1 else 0.0
    with open(ruta, "w") as fh:
        fh.write(f"{nx:7d}       mx\n{ny:7d}       my\n{nt:7d}       mt\n")
        fh.write(f"{x0:20.14e}   xlower\n{y0:20.14e}   ylower\n{t0:20.14e}   t0\n")
        fh.write(f"{dx:20.14e}   dx\n{dy:20.14e}   dy\n{dt:20.14e}   dt\n")
        for k in range(nt):
            for j in range(ny - 1, -1, -1):          # de norte a sur
                fh.write(" ".join(f"{v:.6e}" for v in dz[k, j]) + "\n")


def escribir_topo_tt3(ruta, lon, lat, z, nodata=-99999):
    """Archivo topo tipo 3 de GeoClaw (encabezado valor-etiqueta, filas de norte a sur)."""
    lat, z = _asegurar_lat_creciente(lat, np.asarray(z, float))
    ny, nx = z.shape
    dx = float(lon[0, 1] - lon[0, 0])
    with open(ruta, "w") as fh:
        fh.write(f"{nx}  ncols\n{ny}  nrows\n{float(lon[0,0]):.10f}  xllcorner\n")
        fh.write(f"{float(lat[0,0]):.10f}  yllcorner\n{dx:.10f}  cellsize\n{nodata}  nodata_value\n")
        for j in range(ny - 1, -1, -1):
            fh.write(" ".join(f"{v:.2f}" for v in z[j]) + "\n")


def guardar_campos(ruta_base, lon, lat, campos, atributos=None):
    """
    Guarda un conjunto de campos 2D (dict nombre -> array) en NetCDF si xarray
    está disponible, y siempre en NPZ. Devuelve la lista de archivos escritos.
    """
    escritos = []
    atributos = atributos or {}
    np.savez_compressed(ruta_base + ".npz", lon=lon, lat=lat, **campos)
    escritos.append(ruta_base + ".npz")
    try:
        import xarray as xr
        ds = xr.Dataset(
            {k: (("lat", "lon"), np.asarray(v, dtype="float32")) for k, v in campos.items()
             if np.ndim(v) == 2},
            coords={"lon": lon[0, :], "lat": lat[:, 0]},
            attrs={k: (json.dumps(v) if not isinstance(v, (str, int, float)) else v)
                   for k, v in atributos.items()})
        ds.to_netcdf(ruta_base + ".nc")
        escritos.append(ruta_base + ".nc")
    except Exception as e:  # pragma: no cover
        print("NetCDF no escrito:", e)
    return escritos
