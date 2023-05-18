import numpy as np

layer = iface.activeLayer()
provider = layer.dataProvider()
coord_x= QgsField('coord_x', QVariant.Double)
coord_y= QgsField('coord_y', QVariant.Double)
dist = QgsField('dist',QVariant.Double)
azimute= QgsField('azimute', QVariant.Double)
provider.addAttributes([coord_x,coord_y,dist,azimute])
layer.updateFields()

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
expression1 = QgsExpression('$x')
expression2 = QgsExpression('$y')

with edit(layer):
    for f in layer.getFeatures():
        context.setFeature(f)
        f['coord_x'] = expression1.evaluate(context)
        f['coord_y'] = expression2.evaluate(context)
        layer.updateFeature(f)
    for i,f in enumerate(layer.getFeatures()):
        context.setFeature(f)
        if i == 0:
            f['dist'] = 0
            f['azimute'] = 0
            point1 = QgsPointXY(expression1.evaluate(context),expression2.evaluate(context))
            layer.updateFeature(f) 
        else:
            point2 = QgsPointXY(expression1.evaluate(context),expression2.evaluate(context))
            f['dist'] = ((point2.x()-point1.x())**2 + (point2.y()-point1.y())**2)**(1/2)
            f['azimute'] = point1.azimuth(point2) 
            layer.updateFeature(f)
            point1=point2