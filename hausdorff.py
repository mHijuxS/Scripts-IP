import numpy as np

layer = iface.activeLayer()
pontos_1 = []
pontos_2 = []
pontos = []
contador = 0
for feature in layer.getFeatures():
    geom = feature.geometry()
    if geom.type() == QgsWkbTypes.PolygonGeometry:
        for point in geom.asMultiPolygon()[0]:
            if contador == 0:
                pontos_1 = point
                contador += 1
            else:
                pontos_2 = point

pontos_1.pop()
pontos_2.pop()


def hd_dist(pontos_1,pontos_2):
    dists = []
    dists_min_1 = []
    dists_min_2 = []
    for origem in pontos_2:
        for destino in pontos_1:
            d = np.sqrt((origem[0]-destino[0])**2 + (origem[1] - destino[1])**2)
            dists.append(d)
        dists_min_1.append(min(dists))

    hd = max(dists_min_1)
    dists = []
    for origem in pontos_1:
        for destino in pontos_2:
            d = np.sqrt((origem[0]-destino[0])**2 + (origem[1] - destino[1])**2)
            dists.append(d)
        dists_min_2.append(min(dists))

    if max(dists_min_2) > hd:
        hd = max(dists_min_2)
    return hd
hd = hd_dist(pontos_1,pontos_2)
print(hd)