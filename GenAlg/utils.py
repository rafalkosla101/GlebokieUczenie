#!/usr/bin/python
# -*- coding: utf-8 -*-

# BUILT-IN PACKAGES
import matplotlib.axes as Axes

from matplotlib import patches


# FUNCTIONS
def draw_rect(x: int, y: int, w: int, h: int, color: str, ax: Axes.SubplotBase, text: str, to_fill: bool = True) -> None:
    """
    Helpful function to draw a rectangle
    :param x: Horizontal coordinate
    :param y: Vertical coordinate
    :param w: Width
    :param h: Height
    :param color: Color
    :param ax: Axis
    :param text: Text
    :param to_fill: Flag information if to fill the rectangle
    """

    if to_fill:
        rect = patches.Rectangle((x, y), w, h, edgecolor="black", facecolor=color, linewidth=1)

    else:
        rect = patches.Rectangle((x, y), w, h, edgecolor=color, facecolor="white", linewidth=1)

    ax.add_patch(rect)
    rx, ry = rect.get_xy()
    cx = rx + rect.get_width() / 2.0
    cy = ry + rect.get_height() / 2.0

    if to_fill:
        ax.annotate(text, (cx, cy), color="black", fontsize=5, ha="center", va="center")

    else:
        ax.annotate(text, (cx, cy), color=color, fontsize=5, ha="center", va="center")