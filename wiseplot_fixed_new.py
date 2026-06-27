#!/usr/bin/env python3
# ==============================================================
# WISEPlot v2.0
#
# Modern version of Vanessa Moss's WISEPlot
#
# Improvements:
#   • Python 3 compatible
#   • Unlimited number of sources
#   • Publication-quality output
#   • Automatic colours & markers
#   • Legend outside figure
#   • No matplotlib warnings
#   • Correct Wright et al. (2010) background alignment
#
# Original paper:
# Wright et al. (2010), AJ, 140, 1868
#
# Background image credit:
# Chao-Wei Tsai
#
# ==============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colormaps
from astropy.io import ascii

# ---------------------------------------------------------
# Plot style
# ---------------------------------------------------------

plt.rcParams.update({

    "font.family": "STIXGeneral",
    "font.size": 18,

    "axes.linewidth": 2.0,

    "xtick.major.size": 8,
    "xtick.major.width": 1.5,

    "ytick.major.size": 8,
    "ytick.major.width": 1.5,

    "xtick.minor.visible": False,
    "ytick.minor.visible": False,

    "pdf.fonttype": 42,
    "ps.fonttype": 42,

})

# ---------------------------------------------------------
# User settings
# ---------------------------------------------------------

WISE1 = "w1mpro"
WISE2 = "w2mpro"
WISE3 = "w3mpro"

ERR1 = "w1sigmpro"
ERR2 = "w2sigmpro"
ERR3 = "w3sigmpro"

NAME = "Name"

PLOT_ERRORS = True

UNIQUE_MARKERS = True

DPI = 600

BACKGROUND = "wright2010data.png"

# ---------------------------------------------------------
# Read filename
# ---------------------------------------------------------

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "example.txt"

basename = os.path.splitext(filename)[0]

print("="*60)
print("WISEPlot v2")
print("="*60)

print("Reading :", filename)

if not os.path.exists(filename):
    raise FileNotFoundError(filename)

if not os.path.exists(BACKGROUND):
    raise FileNotFoundError(BACKGROUND)

# ---------------------------------------------------------
# Read table
# ---------------------------------------------------------

data = ascii.read(filename)

print("Number of sources :", len(data))

# ---------------------------------------------------------
# Extract columns
# ---------------------------------------------------------

try:

    w1 = np.asarray(data[WISE1], dtype=float)
    w2 = np.asarray(data[WISE2], dtype=float)
    w3 = np.asarray(data[WISE3], dtype=float)

except Exception:

    raise RuntimeError(
        "Cannot find WISE magnitude columns."
    )

if PLOT_ERRORS:

    try:

        w1e = np.asarray(data[ERR1], dtype=float)
        w2e = np.asarray(data[ERR2], dtype=float)
        w3e = np.asarray(data[ERR3], dtype=float)

    except Exception:

        PLOT_ERRORS = False

names = np.asarray(data[NAME]).astype(str)
legend_labels = names.tolist()

# ---------------------------------------------------------
# WISE colours
# ---------------------------------------------------------

x = w2 - w3

y = w1 - w2

# ---------------------------------------------------------
# Create figure
# ---------------------------------------------------------

fig = plt.figure(figsize=(9.5,9.0))

ax = fig.add_subplot(111)
# =============================================================
# PART 2/5
# Background image, correctly aligned axes, ticks
# =============================================================

# ---------------------------------------------------------
# Load Wright et al. (2010) background
#
# IMPORTANT:
# The Wright et al. image already has the correct top-to-bottom
# orientation, so use origin="upper". Using origin="lower" flips
# the classification regions vertically.
# ---------------------------------------------------------

img = plt.imread(BACKGROUND)

ax.imshow(
    img,
    extent=[-1.0, 7.0, -0.5, 4.0],
    origin="upper",
    interpolation="bilinear",
    aspect="auto",
    zorder=0
)

# ---------------------------------------------------------
# Axis limits
# ---------------------------------------------------------

ax.set_xlim(-1.0, 7.0)
ax.set_ylim(-0.5, 4.0)

# ---------------------------------------------------------
# Major ticks ONLY
# ---------------------------------------------------------

ax.set_xticks([0, 2, 4, 6])
ax.set_yticks([0, 1, 2, 3, 4])

# Remove all minor ticks
ax.minorticks_off()

# Remove top/right ticks completely
ax.tick_params(
    axis="both",
    which="major",
    direction="out",
    length=8,
    width=1.8,
    top=False,
    right=False,
    bottom=True,
    left=True,
    labelsize=18
)

ax.tick_params(
    axis="both",
    which="minor",
    bottom=False,
    top=False,
    left=False,
    right=False
)

# ---------------------------------------------------------
# Spine formatting
# ---------------------------------------------------------

for spine in ax.spines.values():
    spine.set_linewidth(2.0)

# ---------------------------------------------------------
# Axis labels
# ---------------------------------------------------------

ax.set_xlabel(
    r"$W2-W3$  (4.6$\mu$m - 12$\mu$m)  [mag]",
    fontsize=20
)

ax.set_ylabel(
    r"$W1-W2$  (3.4$\mu$m - 4.6$\mu$m)  [mag]",
    fontsize=20
)

# ---------------------------------------------------------
# Grid OFF
# ---------------------------------------------------------

ax.grid(False)

# ---------------------------------------------------------
# Credit (do not remove)
# ---------------------------------------------------------

ax.text(
    0.995,
    1.01,
    "Image credit: Chao-Wei Tsai; from Wright et al. (2010)",
    fontsize=8,
    ha="right",
    va="bottom",
    transform=ax.transAxes
)

# ---------------------------------------------------------
# Error bars
# ---------------------------------------------------------

if PLOT_ERRORS:

    xerr = np.sqrt(w2e**2 + w3e**2)
    yerr = np.sqrt(w1e**2 + w2e**2)

    ax.errorbar(
        x,
        y,
        xerr=xerr,
        yerr=yerr,
        fmt="none",
        ecolor="black",
        elinewidth=0.8,
        capsize=2,
        alpha=0.7,
        zorder=2
    )
# =============================================================
# PART 3/5
# Plot sources
# Unlimited markers and colours
# =============================================================

# ---------------------------------------------------------
# Colour map
# ---------------------------------------------------------

# Modern matplotlib (no deprecation warning)
cmap = colormaps["tab20"]

# Make at least one colour per source. This avoids IndexError when the
# input table has more rows than the default palette size.
if len(data) <= 20:
    colours = cmap(np.linspace(0, 1, 20))[:len(data)]
else:
    colours = plt.cm.nipy_spectral(np.linspace(0, 1, len(data)))

# ---------------------------------------------------------
# Filled markers ONLY
# (avoids edgecolor warnings)
# ---------------------------------------------------------

markers = [

    "o",
    "s",
    "^",
    "v",
    "D",

    "P",
    "X",
    "*",
    "<",
    ">",

    "h",
    "H",
    "8",
    "p",
    "d"

]

# ---------------------------------------------------------
# Marker size
# ---------------------------------------------------------

MARKER_SIZE = 70

EDGE_WIDTH = 0.6

ALPHA = 0.95

# ---------------------------------------------------------
# Plot sources
# ---------------------------------------------------------

handles = []

for i in range(len(data)):

    marker = markers[i % len(markers)]

    colour = colours[i]

    sc = ax.scatter(

        x[i],
        y[i],

        s=MARKER_SIZE,

        marker=marker,

        facecolor=colour,

        edgecolor="black",

        linewidth=EDGE_WIDTH,

        alpha=ALPHA,

        zorder=5,

        label=names[i]

    )

    handles.append(sc)

# ---------------------------------------------------------
# Optional labels beside points
#
# Uncomment if desired.
# ---------------------------------------------------------

# for i in range(len(data)):
#
#     ax.text(
#         x[i] + 0.03,
#         y[i] + 0.02,
#         names[i],
#         fontsize=7,
#         zorder=20
#     )

# ---------------------------------------------------------
# Improve appearance
# ---------------------------------------------------------

ax.set_facecolor("white")

# ---------------------------------------------------------
# Keep equal scaling
# ---------------------------------------------------------

ax.set_aspect("auto")

# ---------------------------------------------------------
# Tick padding
# ---------------------------------------------------------

ax.tick_params(
    pad=6
)

# ---------------------------------------------------------
# Nice margins
# ---------------------------------------------------------

ax.margins(
    x=0.02,
    y=0.02
)
# =============================================================
# PART 4/5
# Publication-quality legend outside the figure
# =============================================================

# ---------------------------------------------------------
# Decide number of legend columns
# ---------------------------------------------------------

nsource = len(data)

if nsource <= 20:
    legend_columns = 1
elif nsource <= 50:
    legend_columns = 2
elif nsource <= 100:
    legend_columns = 3
elif nsource <= 200:
    legend_columns = 4
else:
    legend_columns = 5

# ---------------------------------------------------------
# Shrink plotting region
# Leave room on right for legend
# ---------------------------------------------------------

fig.subplots_adjust(
    left=0.10,
    bottom=0.10,
    top=0.96,
    right=0.72
)

# ---------------------------------------------------------
# Legend
# ---------------------------------------------------------

legend = ax.legend(

    handles=handles,

    labels=legend_labels,

    loc="upper left",

    bbox_to_anchor=(1.02,1.00),

    borderaxespad=0.0,

    fontsize=8,

    frameon=True,

    fancybox=True,

    shadow=False,

    framealpha=1.0,

    edgecolor="black",

    title="Sources",

    title_fontsize=10,

    ncol=legend_columns,

    markerscale=1.2,

    handlelength=1.2,

    handletextpad=0.5,

    columnspacing=0.8,

    labelspacing=0.35

)

legend.get_frame().set_linewidth(1.0)

# ---------------------------------------------------------
# White legend background
# ---------------------------------------------------------

legend.get_frame().set_facecolor("white")

# ---------------------------------------------------------
# Make the legend symbols slightly larger
# ---------------------------------------------------------

legend_handles = getattr(legend, "legend_handles", None)
if legend_handles is None:
    legend_handles = getattr(legend, "legendHandles", [])

for h in legend_handles:

    try:
        h.set_sizes([70])
    except Exception:
        pass

# ---------------------------------------------------------
# Tick appearance
# ---------------------------------------------------------

ax.tick_params(

    axis="both",

    which="major",

    labelsize=16,

    direction="out",

    length=8,

    width=1.8

)

# ---------------------------------------------------------
# Remove ALL minor ticks
# ---------------------------------------------------------

ax.minorticks_off()

# ---------------------------------------------------------
# Remove top/right spines
# ---------------------------------------------------------

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Keep left/bottom slightly thicker

ax.spines["left"].set_linewidth(2)

ax.spines["bottom"].set_linewidth(2)

# ---------------------------------------------------------
# White figure background
# ---------------------------------------------------------

fig.patch.set_facecolor("white")

# ---------------------------------------------------------
# Make sure the legend stays outside
# ---------------------------------------------------------

plt.draw()
# =============================================================
# PART 5/5
# Save figure and finish
# =============================================================

# ---------------------------------------------------------
# Output filenames
# ---------------------------------------------------------

pdf_name = f"{basename}_allwise.pdf"
png_name = f"{basename}_allwise.png"

# ---------------------------------------------------------
# Save figure
# (bbox_extra_artists keeps the outside legend)
# ---------------------------------------------------------

fig.savefig(
    pdf_name,
    dpi=DPI,
    bbox_inches="tight",
    bbox_extra_artists=(legend,),
    facecolor="white"
)

fig.savefig(
    png_name,
    dpi=DPI,
    bbox_inches="tight",
    bbox_extra_artists=(legend,),
    facecolor="white"
)

print()
print("="*60)
print("WISEPlot completed successfully")
print("="*60)
print(f"Number of sources : {len(data)}")
print(f"PDF saved : {pdf_name}")
print(f"PNG saved : {png_name}")
print("="*60)

plt.show()

# =============================================================
# End of file
# =============================================================
