layer = iface.activeLayer()
crs = layer.crs()
new_layer = QgsVectorLayer("Polygon", "BBoxes", "memory")
new_layer.setCrs(crs)
new_layer_data = new_layer.dataProvider()
new_layer_data.addAttributes([QgsField("Name", QVariant.String)])
new_layer.updateFields()

for i,feature in enumerate(layer.getFeatures()):
    points = []
    geom = feature.geometry()
    for point in geom.asMultiPolygon()[0]:
        points = point
    points.pop()

    xs = [vertex[0] for vertex in points]
    ys = [vertex[1] for vertex in points]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    bbox = QgsRectangle(min_x,min_y,max_x,max_y)

    new_feature = QgsFeature()
    geometry = QgsGeometry.fromRect(bbox)
    new_feature.setGeometry(geometry)
    new_feature.setAttributes([f"BBox{i}"])
    new_layer_data.addFeatures([new_feature])

QgsProject.instance().addMapLayer(new_layer)

