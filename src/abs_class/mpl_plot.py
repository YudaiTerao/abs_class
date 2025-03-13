
import os
import re
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import Normalize

class PlotClass():
    def __init__(
        self,
        fig: Figure | None = None,
        ax: Axes | Axes3D | None = None,
    ):
        if ax is None or fig is None:
            self.fig, self.ax = self.make_fig_axes_3d()
        elif ax is not None and fig is not None:
            self.fig = fig
            self.ax = ax

    def make_fig_axes(self):
        fig = plt.figure(figsize=(self.cminch(20),self.cminch(20)))
        ax = fig.add_axes([ 0.05, 0.05, 0.9, 0.9])
        return fig, ax 

    def cminch(self, cm: float) -> float:
        return cm * 0.3937

    def array_nomalization(
        self,
        arr: np.ndarray,
        amin: float | None = None,
        amax: float | None = None,
    ):
        if amin is None: amin = arr.min()
        if amax is None: amax = arr.max()
        assert amax >= amin, "cmin is larger than cmax"
        assert arr.max() >= amin, "cmin is larger than array_max"
        assert arr.min() <= amax, "cmax is smaller than array_min"
        return (arr - amin) / (amax - amin)

    def add_colorbar(
        self,
        fig: Figure,
        ax: Axes | Axes3D,
        amin: float = 0.0,
        amax: float = 1.0,
        colormap_name: str = 'viridis_r',
        orientation: str = 'vertical'
    ):
        assert amax >= amin, "cmin is larger than cmax"
        cm = mpl.colormaps[colormap_name] 
        mappable = mpl.cm.ScalarMappable(Normalize(cmin, cmax), cm)
        pp = fig.colorbar(mappable, ax=ax, orientation=orientation)
        return pp, cm, mappable

class Plot3dClass(PlotClass):
    def __init__(
        self,
        fig: Figure | None = None,
        ax: Axes3D | None = None,
    ):
        if ax is None or fig is None:
            self.fig, self.ax = self.make_fig_axes_3d()
        elif ax is not None and fig is not None:
            self.fig = fig
            self.ax = ax

    def make_fig_axes_3d(self):
        fig = plt.figure(figsize=(self.cminch(20),self.cminch(20)))
        ax = fig.add_axes([ 0.05, 0.05, 0.9, 0.9], projection='3d')
        return fig, ax 

    def adjust_aspect(self, ax: Axes3D):
        axis_len = np.zeros(3, dtype = np.float64)
        axis_rate = np.zeros(3, dtype = np.float64)
        for i, axis in enumerate(['x', 'y', 'z']):
            amn, amx = eval("ax.get_{}lim".format(axis))()
            axis_len[i] = amx - amn
            eval("ax.set_{}lim".format(axis))(amn-axis_len[i]*0.2, amx+axis_len[i]*0.2)
        for i, axis in enumerate(['x', 'y', 'z']):
            if i == axis_len[i].argmin():
                len_base = axis_len[i]
                axis_rate[i] = 1
            else: axis_rate[i] = axis_len[i]/len_base
        ax.set_box_aspect(tuple(axis_rate))

