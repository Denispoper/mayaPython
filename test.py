import maya.mel as mel
import maya.cmds as mc
import pymel.core as pm


# clear demo-objects
# mc.delete('sphere1', 'RPRIBL', 'RPRIES1', 'RPRPhysicalLight1')

# test object
mc.sphere( radius = 2, n='sphere' )

#render (.jpg)
mc.setAttr('defaultRenderGlobals.imageFormat', 8)

# root path
rootPath = 'D:\MayaMaterials'

#----------------------IES Light -----------------------------

# Mel 
#mel.eval('createIESLight()')

# Nodes
def createIESLight(fileTextureName): 
    light = mc.createNode( 'transform', n='RPRIES' )
    mc.createNode('RPRIES', n='RPRIESLight', p='RPRIES')

    mc.move(0, 8, 0, light)
    mc.rotate(90, 0, 0, light)

    filePath = rootPath + '/ies-lights-pack/' + fileTextureName
    mc.setAttr('RPRIESLight.iesFile', filePath, type='string')
    mc.setAttr('RPRIESLight.color', 1,0,1, type='double3')


#-----------------------Physical Light------------------------

# Mel 
#mel.eval('createPhysicalLight()')

# Nodes
def createPhysicalLight(lightType):
    light = mc.createNode( 'transform', n='RPRPhysicalLight1' )
    mc.createNode('RPRPhysicalLight', n='RPRPhysicalLight1Shape', p='RPRPhysicalLight1')

    mc.move(5, 0, 0, light)
    mc.rotate(0, 90, 0, light)

    mc.setAttr('RPRPhysicalLight1Shape.colorPicker', 1,0,0, type='double3');
    mc.setAttr('RPRPhysicalLight1Shape.lightType', lightType)

#-----------------------IBL Light------------------------------

# Mel 
# mel.eval('createIBLNodeRPR()')

# Nodes
def createIBLLight(fileTextureName, size):
    light = mc.createNode( 'transform', n='RPRIBL' )
    mc.createNode('RPRIBL', n='RPRIBLLight', p='RPRIBL')
    mc.scale(size, size, size, light)

    filePath = rootPath + '/IBL/' + fileTextureName
    mc.setAttr('RPRIBLLight.filePath', filePath, type='string')

#------------RBRUberMaterial + File Node------------------------

# file node
def createFileTexture(fileTextureName, p2dName):
    tex = pm.shadingNode('file', name=fileTextureName, asTexture=True, isColorManaged=True)
    if not pm.objExists(p2dName):
        pm.shadingNode('place2dTexture', name=p2dName, asUtility=True)
    p2d = pm.PyNode(p2dName)
    tex.filterType.set(0)
    pm.connectAttr(p2d.outUV, tex.uvCoord)
    pm.connectAttr(p2d.outUvFilterSize, tex.uvFilterSize)
    pm.connectAttr(p2d.vertexCameraOne, tex.vertexCameraOne)
    pm.connectAttr(p2d.vertexUvOne, tex.vertexUvOne)
    pm.connectAttr(p2d.vertexUvThree, tex.vertexUvThree)
    pm.connectAttr(p2d.vertexUvTwo, tex.vertexUvTwo)
    pm.connectAttr(p2d.coverage, tex.coverage)
    pm.connectAttr(p2d.mirrorU, tex.mirrorU)
    pm.connectAttr(p2d.mirrorV, tex.mirrorV)
    pm.connectAttr(p2d.noiseUV, tex.noiseUV)
    pm.connectAttr(p2d.offset, tex.offset)
    pm.connectAttr(p2d.repeatUV, tex.repeatUV)
    pm.connectAttr(p2d.rotateFrame, tex.rotateFrame)
    pm.connectAttr(p2d.rotateUV, tex.rotateUV)
    pm.connectAttr(p2d.stagger, tex.stagger)
    pm.connectAttr(p2d.translateFrame, tex.translateFrame)
    pm.connectAttr(p2d.wrapU, tex.wrapU)
    pm.connectAttr(p2d.wrapV, tex.wrapV)
    return tex

def applyFileTexture(fileTextureName):

    createFileTexture('file', 'p2dOne')

    filePath = rootPath + '/Textures/' + fileTextureName

    mc.setAttr('file1.fileTextureName', filePath, type='string')
    mc.connectAttr('file1.outColor', 'sphere_uber.diffuseColor', force=True)

# RPRUberMaterial
def applyRPRUberMaterial(node):
    if mc.objExists(node):
        shd = mc.shadingNode('RPRUberMaterial', name="%s_uber" % node, asShader=True)
        shdSG = mc.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        mc.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        mc.sets(node, e=True, forceElement=shdSG)

#---------------------------------------------------------------

createIBLLight('iblback.hdr', 1000)

createIESLight('comet.ies')
# type 1 - spot
createPhysicalLight(1)

applyRPRUberMaterial('sphere')

applyFileTexture('texture.jpg')

mel.eval('startProductionRenderRPR()');