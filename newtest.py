import maya.cmds as mc

plane = mc.polyPlane(n="BasicPlane", w=25, h=25)

torus = mc.polyTorus(n="Torus")

mc.move(0, 5, 0, torus)
mc.scale(5, 5, 5, torus)

mc.createNode( 'transform', n='RPRPhysicalLightTop' )
phLightTop = mc.createNode('RPRPhysicalLight', n='RPRPhysicalLightShapeTop', p='RPRPhysicalLightTop')

mc.move(0, 25, 0, phLightTop)
mc.rotate(-90, 0, 0, phLightTop)
mc.scale(5, 5, 1, phLightTop)

mc.setAttr('RPRPhysicalLightShapeTop.lightType', 3)
mc.setAttr('RPRPhysicalLightShapeTop.lightIntensity', 1.5)

mc.createNode( 'transform', n='RPRPhysicalLightBottom' )
phLightBottom = mc.createNode('RPRPhysicalLight', n='RPRPhysicalLightShapeBottom', p='RPRPhysicalLightBottom')

mc.move(0, 2, 0, phLightBottom)
mc.rotate(90, 0, 0, phLightBottom)
mc.scale(5, 5, 1, phLightBottom)

