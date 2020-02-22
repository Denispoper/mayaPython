import maya.cmds as mc

#convert hex string to rgb tuple
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
    plane = mc.polyPlane(n="BasicPlane", w=25, h=25)
    color = hex_to_rgb(color)
    mc.setAttr('lambert1.color', color[0], color[1], color[2], type='double3')

