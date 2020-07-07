import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import math
import json
from scipy import spatial
import csv

##### Generate json of road #####
def json_generator(edges, name):
    dict = []
    for i in range(0, int(np.size(edges) / np.size(edges.iloc[0]) - 1)):
        if type(edges.iloc[i]['name']) == type(['a']):
            rue = {
                'id' : i,
                'osmid' : edges.iloc[i]['osmid'],
                'type' : edges.iloc[i]['highway'],
                'name' : edges.iloc[i]['name'][0],
                'lat_min' : edges.iloc[i]['geometry'].bounds[1],
                'lon_min' : edges.iloc[i]['geometry'].bounds[0],
                'lat_max' : edges.iloc[i]['geometry'].bounds[3],
                'lon_max' : edges.iloc[i]['geometry'].bounds[2],
                'u' : int(edges.iloc[i]['u']),
                'v' : int(edges.iloc[i]['v']),
                'command_number' : int(0),
                'postal_code' : ''
            }
            dict.append(rue)
        elif type(edges.iloc[i]['name']) != type(float(2.2)):
            rue = {
                'id' : i,
                'osmid' : edges.iloc[i]['osmid'],
                'type' : edges.iloc[i]['highway'],
                'name' : edges.iloc[i]['name'],
                'lat_min' : edges.iloc[i]['geometry'].bounds[1],
                'lon_min' : edges.iloc[i]['geometry'].bounds[0],
                'lat_max' : edges.iloc[i]['geometry'].bounds[3],
                'lon_max' : edges.iloc[i]['geometry'].bounds[2],
                'u' : int(edges.iloc[i]['u']),
                'v' : int(edges.iloc[i]['v']),
                'command_number' : int(0),
                'postal_code' : ''
            }
            dict.append(rue)
        else:
            rue = {
                'id' : i,
                'osmid' : edges.iloc[i]['osmid'],
                'type' : edges.iloc[i]['highway'],
                'name' : edges.iloc[i]['name'],
                'lat_min' : edges.iloc[i]['geometry'].bounds[1],
                'lon_min' : edges.iloc[i]['geometry'].bounds[0],
                'lat_max' : edges.iloc[i]['geometry'].bounds[3],
                'lon_max' : edges.iloc[i]['geometry'].bounds[2],
                'u' : int(edges.iloc[i]['u']),
                'v' : int(edges.iloc[i]['v']),
                'command_number' : int(0),
                'postal_code' : ''
            }
            dict.append(rue)

    j = json.dumps(dict, indent=4, sort_keys=True, ensure_ascii=False)
    f = open(name, "w")
    f.write(j)
    f.close()


def update_json(ville_name, ville_street):
    file2 = open(ville_name, "r", encoding='latin-1')
    data = json.load(file2)
    UV = []
    for dat in data:
        UV.append([dat['u'], dat['v']])
    file2.close()

    T = spatial.KDTree(UV)

    file = open("file-command.csv", "r", encoding='latin-1') # ouvrir le fichier
    reader = csv.reader(file, delimiter = ";")

    lat = []
    lon = []
    for row in reader:
        lon.append(float(row[1]))
        lat.append(float(row[2]))

    real2 = ox.get_nearest_edges(ville_street, lon, lat, method='balltree', dist=0.0001)

    with open(ville_name) as f:
        data = json.load(f)
        for i in range(0, int(np.size(real2) / np.size(real2[0])) - 1):
            print ('######################')
            print (i)
            idx = T.query_ball_point([real2[i][0], real2[i][1]], r=0)
            if len(idx) == 0:
                idx = T.query_ball_point([real2[i][1], real2[i][0]], r=0)
            print(idx)
            data[idx[0]]['command_number'] += 1
            data[idx[0]]['postal_code'] = f"{real2[i][-1]}"

    j = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
    f = open("final_json.json","w")
    f.write(j)
    f.close()
