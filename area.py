layer = iface.activeLayer()
provider = layer.dataProvider()
area = QgsField('area', QVariant.Double)
percdif = QgsField('perc_dif', QVariant.Double)
boulean = QgsField('boulean', QVariant.Double)
provider.addAttributes([area,percdif,boulean])
layer.updateFields()

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
expression1 = QgsExpression('$area')
with edit(layer):
    for f in layer.getFeatures():
        context.setFeature(f)
        f['area'] = expression1.evaluate(context)
        layer.updateFeature(f)
    for f in layer.getFeatures():
        context.setFeature(f)
        if f.id() == 0:
            f['perc_dif'] = 0
            f['boulean'] = 0
            area1 = expression1.evaluate(context)
            layer.updateFeature(f)
        else:
            area2 = expression1.evaluate(context)
            f['perc_dif'] = 100*(area2-area1)/area2
            if area2-area1 > 0:
                f['boulean'] = 1
            else:
                f['boulean'] = 0
            layer.updateFeature(f)
            area1 = area2    