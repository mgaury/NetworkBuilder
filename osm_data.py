import osmnx as ox
import numpy as np
import math
import json

##### Locate and print raod sorted by type : primary, secondary and tertiary #####
def road_type(edges, ax):
    type_road = ['primary', 'secondary', 'tertiary']
    color = ['red', 'orange', 'yellow']

    for i in range(0, (np.size(type_road))):
        a = edges.loc[edges['highway'] == type_road[i]]
        a.plot(ax = ax, linewidth = 0.4, edgecolor = color[i])

    edges.loc[(edges['highway'] != 'primary') & (edges['highway'] != 'secondary') & (edges['highway'] != 'tertiary')].plot(ax = ax, linewidth = 0.4, edgecolor = 'grey')

##### Print buildings sorted by height in building_height function #####
def plot_buildings(ax, buildings, size_array, array, search = ''):
    colour_code = ['#5C110F', '#901811', '#BF5C00', '#E2AD3B', '#F0C755']
    for i in range(0, np.size(colour_code)):
        for j in range(int((i*max(5, size_array))/5), int(((i+1)*max(5, size_array)/5) - 1)):
            building = buildings.loc[buildings[search] == str(array[j])]
            building.plot(ax = ax, facecolor = colour_code[i], alpha = 0.7)

##### Splitting value of building height in order to reteive them #####
def split_value(array):
    for i in range(0, np.size(array)):
        if str(array[i])[-1] == '0':
            array[i] = int(str(array[i]).split('.')[0])

##### Locate building_height #####
def building_height(buildings, ax):
    heights = []
    roof_heights = []
    for i in range(0, int(np.size(buildings) / np.size(buildings.iloc[0]) - 1)):
        if ('height' in buildings.columns):
            if (type(buildings.iloc[i]['height']) == type('string')):
                if buildings.iloc[i]['height'] == 'RDC':
                    buildings.iloc[i]['height'] = 0
                    heights.append(0)
                else:
                    buildings.iloc[i]['height'] = float(buildings.iloc[i]['height'].split(',')[-1])
                    heights.append(float(buildings.iloc[i]['height'].split(',')[-1]))

        if ('building:levels' in buildings.columns):
            if ('height' in buildings.columns):
                if (type(buildings.iloc[i]['building:levels']) == type('string')) & (type(buildings.iloc[i]['height']) != type('string')):
                    if buildings.iloc[i]['building:levels'] == 'RDC':
                        buildings.iloc[i]['building:levels'] = 0
                        roof_heights.append(0)
                    else:
                        buildings.iloc[i]['building:levels'] = float(buildings.iloc[i]['building:levels'].split(',')[-1])
                        roof_heights.append(float(buildings.iloc[i]['building:levels'].split(',')[-1]))
            else:
                if (type(buildings.iloc[i]['building:levels']) == type('string')):
                    if buildings.iloc[i]['building:levels'] == 'RDC':
                        buildings.iloc[i]['building:levels'] = 0
                        roof_heights.append(0)
                    else:
                        buildings.iloc[i]['building:levels'] = float(buildings.iloc[i]['building:levels'].split(',')[-1])
                        roof_heights.append(float(buildings.iloc[i]['building:levels'].split(',')[-1]))

    heights = np.unique(heights)
    heights = sorted(heights)

    roof_heights = np.unique(roof_heights)
    roof_heights = sorted(roof_heights)

    split_value(heights)
    split_value(roof_heights)

    plot_buildings(ax, buildings, np.size(heights), heights, search = 'height')
    plot_buildings(ax, buildings, np.size(roof_heights), roof_heights, search = 'building:levels')
