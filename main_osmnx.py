import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import math
import json

import osm_data
import generate_json

cs = '[out:json][timeout:600]'

villes = [
    'Bordeaux, France'
]

graphs = []
graphs_p = []
edges = []
edges_p = []
nodes = []
nodes_p = []
buildings = []

fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()

for i in range(0, np.size(villes)):

    # Retreiving graph from a town
    graphs.append(ox.graph_from_place(villes[i], network_type = 'drive'))

    # Retreiving nodes and edges from a town
    n, e = ox.graph_to_gdfs(graphs[i])
    name = f"{villes[i].split(',')[0]}.json"
    generate_json.json_generator(e, name) # in comment if json are already created

    nodes.append(n)
    edges.append(e)

    # Retreiving buildings from a town
    #buildings.append(ox.footprints_from_place(villes[i], timeout = 1500, custom_settings=cs))

    # Retreiving parc from a town
    leisure = ox.footprints_from_place(villes[i], timeout = 1500, footprint_type = "leisure")

    # Retreiving waterways from a town
    water = ox.footprints_from_place(villes[i], timeout = 1500, footprint_type = "water")
    waterways = ox.footprints_from_place(villes[i], timeout = 1500, footprint_type = "waterway")

    leisure.plot(ax = ax, color="green")
    water.plot(ax = ax, color="blue")
    waterways.plot(ax = ax, color="blue")

    #buildings[i].plot(ax = ax, facecolor = 'khaki', alpha = 0.7)
    osm_data.road_type(edges[i], ax)
    #osm_data.building_height(buildings[i], ax)

    edges[i].plot(ax = ax2, linewidth = 1, edgecolor = 'grey')
    nodes[i].plot(ax = ax2, linewidth = 1, edgecolor = 'black')

#generate_json.update_json(f"{villes[0].split(',')[0]}.json", graphs[0])

plt.show()
