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
        shd = mc.shadingNode('RPRUberMaterial', name="%s_plane" % node, asShader=True)
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

    mc.setAttr('RPRPhLightShape.colorPicker', 1,1,1, type='double3');
    mc.setAttr('RPRPhLightShape.lightType', lightType)
    mc.setAttr('RPRPhLightShape.spotLightOuterConeFalloff', 100)
    mc.setAttr('RPRPhLightShape.spotLightInnerConeAngle', 0)
    mc.setAttr('RPRPhLightShape.luminousEfficacy', 7)
    mc.setAttr('RPRPhLightShape.lightIntensity', 6)
    mc.setAttr('RPRPhLightShape.colorMode', 0)
    mc.setAttr('RPRPhLightShape.temperature', 3500)
