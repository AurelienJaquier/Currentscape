"""Plotting-related functions."""

# pylint: disable=too-many-locals, wrong-import-position
import logging
import os

import numpy as np
import matplotlib

matplotlib.use("agg")  # to avoid tkinter error
import matplotlib.pyplot as plt

import palettable as pltb

from currentscape.data_processing import sum_chunks

logger = logging.getLogger(__name__)


def configure_mpl_rcParams(c):
    """Configure matplotlib rcParams."""
    # set text size
    plt.rcParams["axes.labelsize"] = c["textsize"]
    plt.rcParams["xtick.labelsize"] = c["textsize"]
    plt.rcParams["ytick.labelsize"] = c["textsize"]
    plt.rcParams["legend.fontsize"] = c["legend"]["textsize"]
    if c["pattern"]["use"]:
        plt.rcParams["hatch.linewidth"] = c["pattern"]["linewidth"]
        plt.rcParams["legend.handlelength"] = c["legend"]["handlelength"]
    else:
        # remove legend handles
        plt.rcParams["legend.handletextpad"] = 0
        plt.rcParams["legend.labelspacing"] = 0
        plt.rcParams["legend.handlelength"] = 0


def get_rows_tot(c, ions):
    """Return the total number of rows cumulated by all the subplots."""
    rows_tot = 7
    if c["pattern"]["use"]:
        rows_tot += 1
    if c["show"]["all_currents"]:
        rows_tot += 2
    if ions.data is not None:
        rows_tot += 1
    if c["show"]["total_contribution"]:
        rows_tot += 2

    return rows_tot


def get_colors_and_hatches_lists(c, col_idxs, cmap, mapper):
    """Get colors and hatches lists from color indexes list.

    Args:
        c (dict): config
        col_idxs (ndarray of ints): list of indexes of colors
        cmap (matplotlib.colors.Colormap): colormap
        mapper (int): number used to mix colors and patterns
    """
    n_colors = c["colormap"]["n_colors"]
    patterns = np.array([x * c["pattern"]["density"] for x in c["pattern"]["patterns"]])

    if c["pattern"]["use"]:
        colors = cmap((mapper * col_idxs) % n_colors)
        hatches = patterns[((mapper * col_idxs) // n_colors) % len(patterns)]
    else:
        colors = cmap(col_idxs)
        hatches = None

    return colors, hatches


def stackplot_with_bars(
    ax,
    cnorm,
    inames,
    cmap,
    c,
    N_curr,
    mapper=None,
    top_to_bottom=True,
):
    """Plot currentscape using bars instead of imshow.

    That way, hatches (patterns) can be used.

    Args:
        ax (matplotlib.axes): currentscape axis
        cnorm (DataSet): object containing data (e.g. currents data and idxs)
        inames (ndarray of ints): indexes to new name order (new_names = names[inames])
        cmap (matplotlib.colors.Colormap): colormap
        c (dict): config
        N_curr (int): total number of currents
        mapper (int): number used to mix colors and patterns
        top_to_bottom (bool): if True, plot from top to bottom. if False, plot from bottom to top

    Returns the size modified by sum chunks (reduced x resolution)
    """
    patterns = [x * c["pattern"]["density"] for x in c["pattern"]["patterns"]]
    n_colors = c["colormap"]["n_colors"]
    chunksize = c["stackplot"]["x_chunksize"]

    currs = sum_chunks(np.abs(cnorm.data), chunksize)  # reduce data x resolution
    currs = currs / chunksize  # get the mean over each chunk

    imap = np.zeros(N_curr, dtype=int)
    imap[inames] = np.arange(N_curr)

    size = len(currs[0])
    step = float(cnorm.time[-1] - cnorm.time[0]) / size

    x = np.arange(cnorm.time[0], cnorm.time[-1], step)

    if top_to_bottom:
        # stack from the top to bottom, like in create_cscape_image func.
        bottom = np.ones(size)
    else:
        bottom = np.zeros(size)

    for idx, curr in zip(cnorm.idxs, currs):
        if not np.all(curr == 0):
            i = imap[idx]

            if c["pattern"]["use"]:
                color = cmap((mapper * i) % n_colors)
                hatch = patterns[((mapper * i) // n_colors) % len(patterns)]
            else:
                color = select_color(cmap, i, N_curr)
                hatch = None

            if top_to_bottom:
                bottom -= curr

            ax.bar(
                x,
                curr,
                color=color,
                edgecolor=c["pattern"]["color"],
                linewidth=0,  # do not draw edges
                width=step,  # fill all the space between two bars
                hatch=hatch,
                bottom=bottom,
                align="edge",  # Align the left edges of the bars with the x positions.
                zorder=2,
            )

            if not top_to_bottom:
                bottom += curr


def black_line_log_scale(ax, ylim, xlim, bl_thickness):
    """Produce a black line meant to distinguish between 2 plots in log scales.

    The black line is plotted at the bottom of the upper plot.
    This is a trick to avoid frames masking some of the data.

    Args:
        ax (matplotlib.axes): currentscape axis
        ylim (list of 2 floats): limits of the y axis
        xlim (list of 2 floats): limits of the x axis
        bl_thickness (float): thickness of the black line separating the two plots,
            in percentage of the y axis size

    Returns ylim, because the bottom y limit is changing by adding the black line.
    """
    # should produce a black line with a thickness approaching
    # the one in the currentscape (non log scale) black line
    percent_to_log = abs(ylim[1] / ylim[0]) ** (bl_thickness / 64.0)
    y_bottom = ylim[0] / (percent_to_log)

    ax.fill_between(
        xlim,
        [y_bottom, y_bottom],
        [ylim[0], ylim[0]],
        color="black",
        lw=0,
        zorder=3,
    )
    ylim[0] = y_bottom

    return ylim


def remove_ticks_and_frame(ax):
    """Remove ticks (but not ytick label) and frame."""
    ax.tick_params(
        axis="x",  # changes apply to the x-axis
        which="both",  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False,  # labels along the bottom edge are off
    )
    ax.tick_params(
        axis="y",  # changes apply to the x-axis
        which="both",  # both major and minor ticks are affected
        left=False,  # ticks along the left edge are off
        right=False,  # ticks along the right edge are off
        pad=0,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)


def remove_ticks_and_frame_for_bar_plot(ax):
    """Remove all ticks (including ytick label) and top & bottom frames."""
    ax.tick_params(
        axis="x",  # changes apply to the x-axis
        which="both",  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False,  # labels along the bottom edge are off
    )
    ax.tick_params(
        axis="y",  # changes apply to the x-axis
        which="both",  # both major and minor ticks are affected
        left=False,  # ticks along the left edge are off
        right=False,  # ticks along the right edge are off
        labelleft=False,  # labels along left edge are off
    )
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)


def adjust(adjust_left, adjust_right, adjust_top, adjust_bottom):
    """Adjust Subplots."""
    plt.subplots_adjust(wspace=0, hspace=0)
    if adjust_left:
        plt.subplots_adjust(left=adjust_left)
    if adjust_right:
        plt.subplots_adjust(right=adjust_right)
    if adjust_top:
        plt.subplots_adjust(top=adjust_top)
    if adjust_bottom:
        plt.subplots_adjust(bottom=adjust_bottom)


def set_label(ax, x, y, label, textsize):
    """Set text as label on the y axis."""
    ax.text(
        x,
        y,
        label,
        horizontalalignment="right",
        verticalalignment="center",
        rotation="vertical",
        size=textsize,
    )


def show_xgridlines(ax, c, xticks, ylim=None):
    """Show vertical gridlines corresponding to the x ticks."""
    lw = c["xaxis"]["gridline_width"]
    ls = c["xaxis"]["gridline_style"]
    color = c["xaxis"]["gridline_color"]

    # plot on top of everything else
    ax.vlines(xticks, ylim[0], ylim[1], lw=lw, color=color, zorder=5, ls=ls)


def apply_labels_ticks_and_lims(
    ax, c, xticks, xlim, ylim, xsize, positive=True, config_key="current"
):
    """Apply labels, ticks, xlim and ylim to current / ion concentration plots.

    Args:
        ax (matplotlib.axes): currentscape axis
        c (dict): config
        xticks (list): tick positions on the x axis
        xlim (list of 2 floats): limits of x axis
        ylim (list of 2 floats): limits of y axis (can be different from ylim from config)
        xsize (int): size of the x axis
        positive (bool): True for positive data, False for negative data
        config_key (str): key for getting data from config. Should be 'current' or 'ions'
    """
    # plot the horizontal dotted lines
    for tick in c[config_key]["ticks"]:
        ax.plot(tick * np.ones(xsize), color="black", ls=":", lw=1, zorder=1)

    ax.set_yscale("log")

    # labels
    if c["show"]["ylabels"]:
        if positive:
            ax.set_ylabel(c[config_key]["units"], labelpad=c["labelpad"])
        else:
            ax.set_ylabel("-" + c[config_key]["units"], labelpad=c["labelpad"])

    # ticks
    if c["show"]["yticklabels"]:
        ax.set_yticks(c[config_key]["ticks"])
        ax.get_yaxis().set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
    remove_ticks_and_frame(ax)

    # show x axis gridline
    if c["show"]["xgridlines"]:
        show_xgridlines(ax, c, xticks, ylim)

    # somehow, set_ylim is not taken into account if it is set before set_yticks
    ax.set_xlim(xlim)
    if positive:
        ax.set_ylim(ylim[0], ylim[1])
    else:
        ax.set_ylim(ylim[1], ylim[0])


def plot_x_labels(ax, c, xticks):
    """Plot x labels and x ticklabels."""
    if c["show"]["xlabels"]:
        ax.set_xlabel(c["xaxis"]["units"], labelpad=c["labelpad"])

    if c["show"]["xticklabels"]:
        # enable label bottom
        ax.tick_params(
            axis="x",  # changes apply to the x-axis
            which="both",  # both major and minor ticks are affected
            pad=0,
            labelbottom=True,
        )
        ax.set_xticks(xticks)
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))


def select_color(cmap, i, N_col):
    """Select color of the ith element when not using patterns.

    There is a +2 in the formula to account for the black and white in colormap.

    Args:
        cmap (matplotlib.colors.Colormap): colormap
        i (int): index of element (current/ion)
        N_col (int): total number of elements
    """
    return cmap(i / float(N_col + 2))


def get_colors(cmap, n_col):
    """Get colors from colormap, depending on maximum number of colors.

    Args:
        cmap (str): colormap name
        n_col (int): number of colors to extract
    Returns:
        a list of matplotlib colors
        launch_warning (bool): True to warn that colormap lacks colors
    """
    # is from palettable module
    if "." in cmap:
        x = pltb
        # we want to retrieve e.g. pltb.cartocolors.qualitative.Antique_8.mpl_colors
        # from string "cartocolors.qualitative.Antique_8"
        for attr in cmap.split("."):
            x = getattr(x, attr)

        # if colormap lacks colors
        if len(x.mpl_colors) < n_col:
            return (
                list(x.mpl_colormap(np.array(range(n_col)) / float(n_col))),
                True,
            )

        return x.mpl_colors[:n_col], False

    # is from matplotlib
    new_cmap = matplotlib.cm.get_cmap(cmap, n_col)
    # check number of colors
    if matplotlib.cm.get_cmap(cmap).N < n_col:
        return list(new_cmap(range(n_col))), True

    return list(new_cmap(range(n_col))), False


def get_colormap(cmap, n_colors, use_patterns, N_curr, N_ion):
    """Get colormap according to input, and add black then white colors at the end.

    The black color is used to create a black line separating currentscapes plots,
    and the white color is used when there is no data (e.g. no inward or outward current).

    Args:
        cmap (str): colormap name
        n_colors (int): number of colors to extract IF use_patterns and n_colors>N_curr
        use_patterns (bool): True if currentscape plot uses bars and mixes color and pattern
        N_curr (int): number of currents
        N_ion (int): number of ion concentrations
    """
    # choose the right number of colors for the colormap
    if N_ion is not None and N_ion > N_curr:
        N_max = N_ion
    else:
        N_max = N_curr

    if use_patterns and N_max > n_colors:
        N_colormap = n_colors
    else:
        N_colormap = N_max

    # get colors from colormap
    colors, launch_warning = get_colors(cmap, N_colormap)

    # append black, for black line separating currentscapes
    colors.append(np.array([0.0, 0.0, 0.0, 1.0]))
    # append white. default color when there is no current.
    colors.append(np.array([1.0, 1.0, 1.0, 1.0]))

    # display warning if the colormap lacks colors
    if launch_warning:
        if use_patterns:
            logger.warning(
                "'n_colors' in 'colormap' in config is larger than "
                "the number of colors in the colormap. "
                "Please, choose a colormap with more colors "
                "or decrease n_colors for optimal display."
            )
        else:
            logger.warning(
                "The number of colors in the colormap "
                "is smaller than the number of currents. "
                "Please, choose a colormap with more colors "
                "or use patterns for optimal display."
            )

    return matplotlib.colors.ListedColormap(colors)


def save_figure(fig, c):
    """Save figure in output according to config file."""
    if not os.path.exists(c["output"]["dir"]):
        os.makedirs(c["output"]["dir"])
    out_path = (
        os.path.join(c["output"]["dir"], c["output"]["fname"])
        + "."
        + c["output"]["extension"]
    )
    fig.savefig(
        out_path, dpi=c["output"]["dpi"], transparent=c["output"]["transparent"]
    )
