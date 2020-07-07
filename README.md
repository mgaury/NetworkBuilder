
# Network Builder

## Features

This package is using different project in order to download spatial geometries, visualize and analyse them :

  * [OSMnx](https://github.com/gboeing/osmnx): Python package that lets you download spatial geometries and model, project, visualize, and analyze real-world street networks from OpenStreetMap's APIs.
  * [Herepy](https://github.com/abdullahselek/HerePy): Python interface for the [HERE API](https://developer.here.com).
  * [Scipy](https://github.com/scipy/scipy): Open-source software for mathematics, science, and engineering.
  * [Matplotlib](https://github.com/matplotlib/matplotlib): Comprehensive library for creating static, animated, and interactive visualizations in Python.


## How to use OSMnx

### main_osmnx

The first step consist in downloading street data from cities and create the associated graphs using the Osmnx package.
As the result, users can obtain json file containing all street data that can be useful (id, osmid, type ...).
The json file (file_command.csv) can be updated at the end using a file containing all command from cities.
The file containing all command must be, at least, like this : ID, lon, lat, ...
Then, we use the following function [get_nearest_edges()](https://osmnx.readthedocs.io/en/stable/osmnx.html) to project commands on streets.
The scipy package is used in order to create a KD-Tree. this allows to update the json rapidly, even if users is dealing with billions of commands.

Users can also obtain a visualized graph from the city chose :

![](data/figures/Bordeaux.png)

On the left, we can see that roads are represented with different color :
  * red : primary road
  * orange : secondary road
  * yellow : tertiary road
  * grey : other
