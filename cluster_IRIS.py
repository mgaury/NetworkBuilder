import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import json
from shapely.geometry import Point,Polygon
import herepy
from time import perf_counter
import copy
from math import *

routingApi = herepy.RoutingApi('api key')

ville = 'Bordeaux, France'
cs = '[out:json][timeout:600]'
name = 'Bordeaux_cluster.json'

colour_code = [
                '#566D7E', '#000080', '#357EC7', '#3BB9FF', '#ADDFFF', '#7FFFD4',
                '#3EA99F', '#728C00', '#52D017', '#00FF00', '#FFFF00', '#FFD801',
                '#FFA62F', '#D4A017', '#B87333', '#966F33', '#6F4E37', '#C36241',
                '#CC6600', '#F87217', '#F9966B', '#E77471', '#FF0000', '#9F000F',
                '#7D0552', '#7F525D', '#EDC9AF', '#FAAFBE', '#F778A1', '#F52887',
                '#FF00FF', '#4B0082', '#A74AC7', '#8E35EF'
              ]

ville_street = ox.graph_from_place(ville, timeout = 1500, network_type = 'drive')
nodes, edges = ox.graph_to_gdfs(ville_street)

file2 = open("data/json/contours-iris_Bordeaux.json", "r", encoding='utf-8')
data = json.load(file2)

fig, ax = plt.subplots()
fig, ax2 = plt.subplots()

edges.plot(ax = ax2, linewidth = 0.7, edgecolor = 'black')

j = 0
compt = 0
long = 0
id_index = 0
dict = []
matrices = []
all_points = []

for dat in data:
    if 'Bordeaux' in dat['fields']['nom_com']: # If not Bordeaux, you must add a space at the end : 'Paris '

        print(dat['fields']['nom_com'])
        compt += 1
        print (compt)
        if j == (np.size(colour_code) -1):
            j = 0
        j += 1

        if np.size(dat['fields']['geo_shape']['coordinates']) == 2:
            range_dat = 2
        else:
            range_dat = 1

        for i in range(0, range_dat):
            #try:
            t = 0
            if range_dat == 2:
                try:
                    poly = Polygon(dat['fields']['geo_shape']['coordinates'][i][0])
                except:
                    poly = Polygon(dat['fields']['geo_shape']['coordinates'][i])
            else:
                poly = Polygon(dat['fields']['geo_shape']['coordinates'][0])
            try:
                g = ox.graph_from_polygon(poly, network_type='drive', clean_periphery=True, retain_all=True, truncate_by_edge=True)
            except:
                print('')
                print('NO GRAPH IN TAHT ONE')
                print('')

            n, e = ox.graph_to_gdfs(g)

            e.plot(ax = ax, linewidth = 0.7, edgecolor = colour_code[j])
            for i in range(0, int(np.size(e) / np.size(e.iloc[0]) - 1)):
                id_index += 1
                rue = {
                    'id' : id_index,
                    'u' : int(e.iloc[i]['u']),
                    'v' : int(e.iloc[i]['v']),
                    'cluster_number' : compt
                }
                dict.append(rue)


            points = []
            sizing = int(np.size(n) / np.size(n.iloc[0]))
            for i in range(0, sizing):
                points.append([n.iloc[i]['y'], n.iloc[i]['x']])

            print (points)
            print(np.size(points))
            all_points.append(points)
            count = 0
            tic = perf_counter()
            matice_test = []
            for k in range(0, sizing):

                matrix = []
                count = ceil(sizing/100)
                for l in range(0, count):
                    bool = False
                    while bool == False:
                        try :
                            response = routingApi.matrix(
                                                        start_waypoints = [points[k]],
                                                        destination_waypoints = points[l*100:min(sizing, 100 + l*100)],
                                                        departure='2020-07-01T13:38:00+02',
                                                        modes=[herepy.RouteMode.fastest, herepy.RouteMode.car]
                                                        )
                            bool = True
                        except:
                            bool = False
                            print('Nope')

                    # Must create a temp file in order to work with the response from Here.
                    f = open("data/json/temp.json", "w")
                    c = copy.copy(response)
                    f.write(str(c))
                    f.close()
                    file = open("data/json/temp.json", "r", encoding='utf-8')
                    data = json.load(file)
                    for rep in data['response']['matrixEntry']:
                        matrix.append(rep['summary']['travelTime'])


                matice_test.append(matrix)

            matrices.append(matice_test)
            toc = perf_counter()
            t += toc - tic

            print(f"it took {t} seconde to get this matrix")

            #except:
            #    print('')
            #    print('POLYGON BUG')
            #    print('')


j = json.dumps(dict, indent=4, sort_keys=True, ensure_ascii=False)
f = open(name, "w")
f.write(j)
f.close()

f = open("data/json/matrices_Bordeaux.json", "w")
f.write(f"{matrices}")
f.close()

f = open("data/json/points_Bordeaux.json", "w")
f.write(f"{all_points}")
f.close()



print('')
print(int(np.size(edges) / np.size(edges.iloc[0])))

plt.show()
