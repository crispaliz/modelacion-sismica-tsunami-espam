"""Gráficos de apoyo para el cuaderno de la Unidad 2 (matplotlib, sin cartopy)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import TwoSlopeNorm

CMAP_DEF = "RdBu_r"


def aspecto(ax, lat):
    ax.set_aspect(1.0 / np.cos(np.radians(float(np.mean(lat)))))


def mapa_base(ax, lon, lat, z, sombreado=True, contornos=(-6000, -4000, -2000, -1000, -200)):
    """Batimetría en grises con la línea de costa (z = 0)."""
    if sombreado and z is not None:
        ax.pcolormesh(lon, lat, np.where(z < 0, z, np.nan), cmap="Blues_r", shading="auto",
                      vmin=-7000, vmax=0, alpha=0.35, rasterized=True)
        ax.pcolormesh(lon, lat, np.where(z >= 0, z, np.nan), cmap="Greys", shading="auto",
                      vmin=-500, vmax=4000, alpha=0.35, rasterized=True)
    if z is not None:
        ax.contour(lon, lat, z, levels=list(contornos), colors="0.55", linewidths=0.4)
        ax.contour(lon, lat, z, levels=[0], colors="k", linewidths=1.0)
    ax.set_xlabel("Longitud (°)"); ax.set_ylabel("Latitud (°)")
    aspecto(ax, lat)


def dibujar_falla(ax, falla, campo="slip", cmap="YlOrRd", vmax=None, borde="0.3", alpha=0.8,
                  solo=None):
    """Subfallas en planta coloreadas por deslizamiento (o una lista de valores).
    solo: máscara booleana para dibujar únicamente algunas subfallas."""
    polys = [np.column_stack(s.esquinas()[:2]) for s in falla.subfallas]
    vals = falla.slip if isinstance(campo, str) else np.asarray(campo, dtype=float)
    if solo is not None:
        solo = np.asarray(solo, bool)
        polys = [p for p, m in zip(polys, solo) if m]
        vals = vals[solo]
        if len(polys) == 0:
            return None
    pc = PolyCollection(polys, array=vals, cmap=cmap, edgecolors=borde, linewidths=0.3,
                        alpha=alpha)
    pc.set_clim(0, vmax or max(float(np.max(vals)), 1e-6))
    ax.add_collection(pc)
    return pc


def contorno_falla(ax, falla, color="k", lw=1.2, ls="-"):
    """Contorno exterior aproximado: borde de cada subfalla sin relleno."""
    polys = [np.column_stack(s.esquinas()[:2]) for s in falla.subfallas]
    ax.add_collection(PolyCollection(polys, facecolors="none", edgecolors=color,
                                     linewidths=lw * 0.4, linestyles=ls))


def mapa_campo(ax, lon, lat, u, z=None, titulo="", vmax=None, unidad="m", cmap=CMAP_DEF,
               barra=True, niveles_linea=None):
    vmax = vmax or max(float(np.nanmax(np.abs(u))), 1e-6)
    if z is not None:
        ax.contour(lon, lat, z, levels=[0], colors="k", linewidths=1.0, zorder=3)
    m = ax.pcolormesh(lon, lat, u, cmap=cmap, norm=TwoSlopeNorm(0, -vmax, vmax),
                      shading="auto", rasterized=True)
    ax.contour(lon, lat, u, levels=[0], colors="0.2", linewidths=0.8, linestyles="--")
    if niveles_linea is not None:
        ax.contour(lon, lat, u, levels=niveles_linea, colors="0.3", linewidths=0.5)
    ax.set_title(titulo); ax.set_xlabel("Longitud (°)"); ax.set_ylabel("Latitud (°)")
    aspecto(ax, lat)
    if barra:
        plt.colorbar(m, ax=ax, shrink=0.8, label=unidad)
    return m


def marcar(ax, lon, lat, texto, marcador="*", color="k", tam=12):
    ax.plot(lon, lat, marcador, color=color, ms=tam, mec="w", mew=0.8, zorder=5)
    ax.annotate(texto, (lon, lat), xytext=(5, 5), textcoords="offset points", fontsize=9,
                zorder=6, bbox=dict(boxstyle="round,pad=0.2", fc="w", ec="none", alpha=0.7))
