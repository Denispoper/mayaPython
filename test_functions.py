import maya.cmds as mc

# convert hex string to rgb tuple
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    temp = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    res = [float(i)/255.0 for i in temp]
    return res

def applyRPRUberMaterial(node):
    if mc.objExists(node):
        shd = mc.shadingNode('RPRUberMaterial', name="%s_uber" % node, asShader=True)
        shdSG = mc.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)

        mc.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        mc.sets(node, e=True, forceElement=shdSG)

def createBasicPlane(color):
    if len(color) == 6:     # weak check 
        plane = mc.polyPlane(n="BasicPlane", w=25, h=25)
        color = hex_to_rgb(color)

        applyRPRUberMaterial('BasicPlane')

        mc.setAttr('BasicPlane_uber.diffuseColor', color[0], color[1], color[2], type='double3')


def setRenderOptions():
    return ''

def createLight(lightType):
    light = mc.createNode('transform', n='PhysicalLight')
    mc.createNode('RPRPhysicalLight', n='RPRPhLightShape', p='PhysicalLight')

    mc.move(0, 10, 0, light)
    mc.rotate(-90, 0, 0, light)

    mc.setAttr('RPRPhLightShape.lightType', lightType)
    mc.setAttr('RPRPhLightShape.spotLightOuterConeFalloff', 150)
    mc.setAttr('RPRPhLightShape.spotLightInnerConeAngle', 0)
    mc.setAttr('RPRPhLightShape.luminousEfficacy', 7)
    mc.setAttr('RPRPhLightShape.lightIntensity', 6)
    mc.setAttr('RPRPhLightShape.colorMode', 0)
    mc.setAttr('RPRPhLightShape.temperature', 3500)

def createCubScene():

    floor = mc.polyCube(n='Floor')

    mc.move(0, 0.1, 0, floor)
    mc.scale(10, 0.2, 10, floor)

    rightWall = mc.polyCube(n='RightWall')

    mc.move(0, 2.5, -4.75, rightWall)
    mc.scale(10, 5, 0.5, rightWall)

    leftWall = mc.polyCube(n='LeftWall')

    mc.move(-4.75, 2.5, 0, leftWall)
    mc.scale(0.5, 5, 10, leftWall)


def createIBL():
    light = mc.createNode( 'transform', n='RPRIBL' )
    mc.createNode('RPRIBL', n='RPRIBLLight', p='RPRIBL')

    mc.scale(1000, 1000, 1000, light)

    mc.setAttr('RPRIBLLight.intensity', 0.003)
