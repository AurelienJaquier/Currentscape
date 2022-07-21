This package contains code based on [Leandro M. Alonso and Eve Marder, ”Visualization of the relative contributions of conductances in neuronal models with similar behavior and different conductance densities” (2018)](https://datadryad.org/stash/dataset/doi:10.5061/dryad.d0779mb).
The code in this package is able to reproduce the currentscape figure in the susmentioned article, including the labels, ticks and legend.


### Loading currentscape in Python

After installing currentscape, your PYTHONPATH environment variable should normally
contain the directory where the currentscape module is installed. Loading currentscape
in Python becomes then as easy as:

    import currentscape

### Plotting your first currentscape

Given voltage and current data (see 'Extracting currents' section below for how to get voltage and currents from a cell), as well as an adequate config json file, producing a currenscape figure should be as simple as

    import os
    import numpy as np
    from currentscape.currentscape import plot_currentscape

    data_dir = "/gpfs/bbp.cscs.ch/home/ajaquier/Eve-Marder-style-module/output/memodel_dirs/L23_BP/bNAC/L23_BP_bNAC_150/python_recordings"
    currs = [
        "ihcn_Ih",
        "ica_Ca_HVA2",
        "ica_Ca_LVAst",
        "ik_SK_E2",
        "ik_SKv3_1",
        "ik_K_Pst",
        "ik_K_Tst",
        "ina_NaTg",
    ]

    # load voltage data
    v_path = os.path.join(data_dir, "_".join(("soma_step1", "v")) + ".dat")
    voltage = np.loadtxt(v_path)[:, 1] # load 2nd column. 1st column is time.

    # load currents from files
    currents = []
    for curr in currs:
        file_path = os.path.join(data_dir, "_".join(("soma_step1", curr)) + ".dat")
        currents.append(np.loadtxt(file_path)[:, 1]) # load 2nd column. 1st column is time.
    currents = np.array(currents)

    # define config
    config = "path/to/config"
    # can also pass config as a dictionnary, as commented below
    # curr_names = ["Ih", "Ca_HVA2", "Ca_LVAst", "SK_E2", "SKv3_1", "K_Pst", "K_Tst", "NaTg"]
    # config = {
    #     "current": {"names": curr_names},
    #     "legendtextsize": 5,
    # }

    # produce currentscape figure
    fig = plot_currentscape(voltage, currents, config)
    fig.show()

The voltage should be a list of floats corresponding to the voltage at each timestep.

The currents should be a list of lists of floats corresponding to each current at each timestep.

Each current list and the voltage list should have the same size.


### About the config


Here is an example of a config file containing all defaults values :

    {
        "show": {
            "currentscape": true,
            "ylabels": true,
            "yticklabels": true,
            "xlabels": false,
            "xticklabels": false,
            "_comment1": "If enabled, xgridlines plot vertical lines in all plots at xticks positions.",
            "xgridlines": false,
            "legend": true,
            "all_currents": false,
            "_comment2": "total contribution plots two pie charts (positive and negative) showing the contribution of each current over the whole simulation.",
            "total_contribution": false
        },
        "current": {
            "_comment1": "is not set by default.  The current names should appear in the same order as in the currents argument. is mandatory if ['show']['legend'] is true",
            "names": [
                "Na",
                "CaT",
                "CaS",
                "A",
                "KCa",
                "Kd",
                "H",
                "L"
            ],
            "_comment2": "if True, reorder currents with decreasing order of %.",
            "reorder": true,
            "_comment3": "if True, do not take into account ticks and ylim below.",
            "autoscale_ticks_and_ylim": true,
            "_comment4": "only taken into account if autoscale_ticks_and_ylim is False",
            "ticks": [
                5,
                50,
                500
            ],
            "_comment5": "only taken into account if autoscale_ticks_and_ylim is False",
            "ylim": [
                0.01,
                1500
            ],
            "units": "[pA]",
            "_comment6": "color for summed currents.",
            "color": "black",
            "_comment7": "True to plot absolute currents with stackplots, False to plot them with lines",
            "stackplot": false,
            "_comment8": "thickness of black line separating the inward & outward stackplots. in %age of y size of plot.",
            "black_line_thickness": 2
        },
        "currentscape": {
            "in_label": "inward %",
            "out_label": "outward %",
            "_comment1": "if too low, white pixels can appear at the bottom of currentscape plots because of rounding errors.",
            "y_resolution": 10000
        },
        "ions": {
            "_comment1": "if True, do not take into account ticks and ylim below.",
            "autoscale_ticks_and_ylim": true,
            "_comment2": "only taken into account if autoscale_ticks_and_ylim is False",
            "ticks": [
                5,
                50,
                500
            ],
            "_comment3": "only taken into account if autoscale_ticks_and_ylim is False",
            "ylim": [
                0.01,
                1500
            ],
            "units": "[mM]",
            "_comment4": "if True, reorder currents with decreasing order",
            "reorder": true,
            "_comment5": "is not set by default.  The ions concentration names should appear in the same order as in the ions argument. is mandatory if ['show']['legend'] is true",
            "names": [
                "cai",
                "ki",
                "nai"
            ]
        },
        "colormap": {
            "name": "Set1",
            "_comment1": "color number. Taken into account only if pattern use is True",
            "n_colors": 8
        },
        "stackplot": {
            "_comment3": "data along x axis are summed up into chunks when pattern use is True. Put to 1 to disable.",
            "x_chunksize": 50
        },
        "pattern": {
            "use": false,
            "patterns": ["", "/", "\\", "x", ".", "o", "+"],
            "density": 5,
            "linewidth": 0.2,
            "_comment1": "since the pattern color is defined by the edgecolor, this parameter also changes the edgecolor of the pie charts",
            "color": "black"
        },
        "line": {
            "_comment1": "Is used when pattern:use and show:all_currents are True and current:stackplot is False. Should have the same length as pattern:patterns",
            "styles": [
                "solid",
                [0, [1, 1]],
                [0, [2, 1]],
                [0, [2, 1, 1, 1]],
                [0, [2, 1, 1, 1, 1, 1]],
                [0, [2, 1, 2, 1, 1, 1]],
                [0, [2, 1, 2, 1, 1, 1, 1, 1]]
            ]
        },
        "voltage": {
            "ylim": [-90, 30],
            "ticks":[-50, -20],
            "units": "[mV]",
            "color": "black",
            "horizontal_lines": true
        },
        "xaxis": {
            "units": "[ms]",
            "_comment1": "if None, xticks are generated automatically. Can put a list of xticks to force custom xticks.",
            "xticks": null,
            "gridline_width": 1,
            "gridline_color": "black",
            "gridline_style": "--"
        },
        "output": {
            "savefig": false,
            "dir": ".",
            "fname": "test_1",
            "extension": "png",
            "dpi": 400,
            "transparent": false
        },
        "legend": {
            "textsize": 4,
            "bgcolor": "lightgrey",
            "_comment1": "1. : top of legend is at the same level as top of currentscape plot. higher value put legend higher in figure.",
            "ypos": 1.0,
            "_comment2": "forced to 0 if pattern:use is False and current:stackplot is False",
            "handlelength": 1.4
        },
        "figsize": [
            3,
            4
        ],
        "title": null,
        "titlesize": 12,
        "labelpad": 1,
        "textsize": 6,
        "lw": 0.5,
        "adjust": {
            "left": 0.15,
            "right": 0.85,
            "top": null,
            "bottom": null
        }
    }

If you do not want to modify the default values, you should at least specify the current names if you want to plot with the legend.
Your configuration file could be as small as:

    {
        "current": {
            "names": [
                "Na",
                "CaT",
                "CaS",
                "A",
                "KCa",
                "Kd",
                "H",
                "L"
            ],
    }

The config argument can be passed as a dictionnary, or as a path to a json file.

As data can vary greatly, it is recommended to adapt the config file consequently.

One may want to change the y axis limits, or the ticks, for example.

If the legend is cut, one may decrease the legendsize, the adjust right parameter or increase the figsize.


### Setting the colormap

Since each color of the colormap applies to one category (one current), using categorical / qualitative colormaps is recommended.
These colormaps have colors chosen to easily distinguish each category.

Also, be careful not to use any colormap that uses white, since white is the default color when there is no data (no inward or outward currents).
It would be then hard to know if there is a "white" current, or no current at all.
Using a colormap that uses black is also not advised, since the plots on top and bottom of currentscapes, 
as well as the line separating the inward and outward currentscapes, are black. 
If a black current end up near the top or bottom of the plot, it would decrease readability.

You can set your colormap using "colormap":{"name": "the_name_of_the_colormap"} in the config file.
The name of the colormap can be one of the matplotlib colormaps (https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html), 
or one of the palettable module (https://jiffyclub.github.io/palettable/).
The palettable colormaps should be inputted in the form "origin.palette_N", N being the number of different colors (i.e. the number of currents if patterns are not used.)
Example:
    "cartocolors.qualitative.Safe_8"


### Showing x axis label, ticklabel, gridlines

You can use the configuration to show x axis label, ticklabels and vertical gridlines. 
The label and ticklabels are only shown on the bottom plot, and the vertical gridlines are shown on all plots, and correspond to the x ticks (generated automatically, if not set in the config). 
However, to show ticklabels and gridlines, you have to also input time as an argument to the plot_currentscape function. Here is an example:

    # load voltage data
    data_dir = path/to/data/dir
    v_path = os.path.join(data_dir, "_".join(("soma_step1", "v")) + ".dat")
    time = np.loadtxt(v_path)[:, 0]
    voltage = np.loadtxt(v_path)[:, 1]

    currents = load_current_fct(data_dir)
    config = path/to/config

    # produce currentscape figure
    fig = plot_currentscape(voltage, currents, config, time=time)

Be aware that the time data are expected to grow monotonically.

Also, when setting custom x ticks through the config, try to stick with ticks within time data limits for optimal display.

### Using patterns

If you have a lot of currents to display and do not find a colormap with enough colors to distinguish them all, you can use patterns (also called hatches).
Note: if you are using a lot of currents, you may want to increase the "legend":"ypos" (e.g. to 1.5) in your config to have a legend higher in the figure.

By putting "pattern": {"use": True} in your config, currentscape will put patterns like stripes or dots on top of your currents, 
and it will mix colors and patterns so that two successive currents do not have the same pattern or color.
In the "pattern" key of your config, you can increase the 'density' (frequency) or your patterns, the pattern linewidth, color, etc.
You can also change the patterns or the number of different colors to use with the adequate config.

However, using patterns come with a cost: it takes more computing time (mainly because bar plots are used instead of imshow).
To decrease computing time, you have two possibilities: decrease the pattern density (default=5), or increase x_chunksize.
x_chunksize is related to the x resolution, with x_chunksize = 1 being maximum resolution. The default is x_chunksize=50.

You could also want to use pattern if you are using a non-qualitative colormap that do not have a lot of distinguishable colors.


### Showing all absolute currents

By putting "show":{"all_currents": True} in the config file, two subplots showing all the positive and negative currents are added at the bottom of the figure.
The currents can be displayed as stackplots by putting "current":{"stackplot": True} in the config, or as lines, by putting "current":{"stackplot": False} in the config. In case they are displayed with lines, while using patterns for the current shares, the lines will be displayed with styles (dashed, dotted, etc.). In such a case, the number of line styles should be equal to the number of patterns (which they are, be default). Keep this in mind when changing either the line styles or the patterns.


### Showing ionic concentrations

You can plot the ionic concentrations in a subplot at the bottom of the figure by passing your ionic concentration data to the main function: plot_currentscape(voltage, currents, config, ions), and by passing the ion names to the config under: "ions":{"names":your_list}. Note that, as for the currents, the ion names should correspond to the ion data (i.e. be listed in the same order).


### Showing overall contribution pie charts

By setting "show":{"total_contribution": True} in the configuration, two pie charts are added at the bottom of the figure, each showing the overall contribution of each current over the whole simulation, one for the outward currents, and the other one for the inward currents.


### Extracting currents

You can now use the currentscape module to easily extract currents at different locations with custom protocols.
This should be as simple as:

    from extract_currs.main_func import extract
    extract("extraction_config_filename")

Where you have a config file (not the same as for the ploting module) in a json format. The config file can also be passed as a dictionary.
The segment area from neuron is used in the module to output the currents (and not the current densities).

#### The config file for extractng currents

Below is an example of a config file used to extract currents.

    {
        "emodel": "bNAC_L23SBC",
        "output_dir": "output",
        "join_emodel_to_output_dir_name": true,
        "use_recipes": false,
        "recipe_path": "/gpfs/bbp.cscs.ch/home/ajaquier/Eve-Marder-style-module/output/config/recipes/recipes.json",
        "morph_name": "_",
        "morph_dir": "/gpfs/bbp.cscs.ch/home/ajaquier/Eve-Marder-style-module/output/memodel_dirs/L23_BP/bNAC/L23_BP_bNAC_150/morphology",
        "morph_filename": "C230998A-I3_-_Scale_x1.000_y0.975_z1.000_-_Clone_2.asc",
        "apical_point_isec": null,
        "params_path": "/gpfs/bbp.cscs.ch/home/ajaquier/Eve-Marder-style-module/output/config/params/int.json",
        "final_params_path": "/gpfs/bbp.cscs.ch/home/ajaquier/Eve-Marder-style-module/output/config/params/final.json",
        "var_list": [
            "v",
            "ihcn_Ih",
            "ica_Ca_HVA",
            "ica_Ca_HVA2",
            "ica_Ca_LVAst",
            "ik_K_Pst",
            "ik_K_Tst",
            "ik_KdShu2007",
            "ina_Nap_Et2",
            "ina_NaTg",
            "ina_NaTg2",
            "ik_SK_E2",
            "ik_SKv3_1",
            "ik_StochKv2",
            "ik_StochKv3",
            "i_pas"
        ],
        "apical_point_from_recipe": false,
        "protocols_path": "./protocol_test.json",
        "features_path": "/gpfs/bbp.cscs.ch/home/ajaquier/Eve-Marder-style-module/output/config/features/bNAC.json"
    }

The following keys are mandatory: emodel, output_dir, var_list, use_recipes.
Protocols can now record in multiple places in the neuron, the available variables on those places can differ. So now, if a current that is in the var_list is not present in the recording location, the script does not crash, and the variable is simply ignored for this location.

The extract currents module has two main modes: using recipes, or using custom protocols and parameters.

###### recipe mode

When you set use_recipes to true, the script will retrieve the default protocols, features and parameters in the recipes file.
When use_recipes is set to true, recipe_path and apical_point_filepath_from_recipe should also be present in the config file. 
If apical_point_from_recipe is true, the script will retrieve the apical point section index from recipes. 
Depending on the emodel, you might have an error if you set use_recipes to true, but leave apical_point_from_recipe to false.
When use_recipes, the recipe file expects that you have the following folder structure in the directory you launched the script from:

./
    config/
        features/
        params/
        protocols/

with a config folder filled as in /gpfs/bbp.cscs.ch/project/proj38/singlecell/optimization/config/ . You can also find there the recipes file.

###### custom mode

When use_recipes is set to false, the following keys should be filled in the config:

morph_name, morph_dir, morph_filename, apical_point_isec, params_path, final_params_path (usually points to a final.json), protocols_path, features_path

with protocols_path pointing to your cutomized protocols file. If there is no "Main" key in your protocols file, features are not used and features_path can be set to an empty string (""). morph_name is used solely for the naming of the output files.

Your protocols file should follow the same structure as in /gpfs/bbp.cscs.ch/project/proj38/singlecell/optimization/config/protocols/ .
Note that all protocols are recorded in the soma by default, but you can add recording locations using the extra_recordings key.

Below is an example of a simple custom protocol, recording a step protocol in the soma and in the ais.

    {
        "test": {
            "type": "StepProtocol",
            "stimuli": {
                "step": {
                    "delay": 700.0,
                    "amp": 0.063014185402,
                    "duration": 2000.0,
                    "totduration": 3000.0
                },
                "holding": {
                    "delay": 0.0,
                    "amp": -0.0144071499339,
                    "duration": 3000.0,
                    "totduration": 3000.0
                }
            },
            "extra_recordings": [
                {
                    "comp_x": 0.5,
                    "type": "nrnseclistcomp",
                    "name": "ais",
                    "seclist_name": "axon",
                    "sec_index": 0
                }
            ]
        }
    }

Note that if you want to use a "StepThresholdProtocol", you should follow the same procedure as in a protocol from /gpfs/bbp.cscs.ch/project/proj38/singlecell/optimization/config/protocols/ with a "Main" protocol calling the others, in order to collect threshold data needed for the Step Threshold Protocol.

### Extracting ionic concentrations

Ionic concentrations can be extracted by using the same method as the currents extraction. The ionic concentration variables simply have to be added to the "var_list" in the config file. The ionic concentration variables should end with an 'i', e.g. cai, nai, ki, etc.

### Known caveats

Since currentscape can deal with a lot of data, it sometimes crashes with an error message such as `Bus error` or `Killed` when it runs out of memory. You can solve this error by allocating more memory. 

In bb5, interactive jobs usually have 4G. You can increase them by specifying e.g. `--mem=16G` when asking for a job. If you are asking for a full node, you can also use all of its available memory with `--exclusive --mem=0`.
