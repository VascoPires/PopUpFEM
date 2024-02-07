# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2022 replay file
# Internal Version: 2021_09_15-19.57.30 176069
# Run by p2321038 on Wed Feb  7 13:50:58 2024
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=107.916664123535, 
    height=190.350006103516)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
#: Executing "onCaeStartup()" in the site directory ...
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
execfile('input_Case_1_2D.py', __main__.__dict__)
#: The model "Pop_Box" has been created.
#: The interaction property "Contact_Prop" has been created.
#: The interaction "General_Contact" has been created.
#: The section "S1_A0_Spring" has been assigned to 1 wire or attachment line.
#: The model database has been saved to "C:\Users\p2321038\Documents\GitHub\PopingBoxesFEM\src\Case_1_1cube_2D-fold_angle_6.0-stacknum_1\Pop_Box.cae".
#: Job 1_c_2D: Analysis Input File Processor completed successfully.
#: Job 1_c_2D: Abaqus/Explicit Packager completed successfully.
#: Job 1_c_2D: Abaqus/Explicit completed successfully.
#: Job 1_c_2D completed successfully. 
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=ON, geometricRestrictions=ON, stopConditions=ON)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
o1 = session.openOdb(
    name='C:/Users/p2321038/Documents/GitHub/PopingBoxesFEM/src/Case_1_1cube_2D-fold_angle_6.0-stacknum_1/1_c_2D.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Users/p2321038/Documents/GitHub/PopingBoxesFEM/src/Case_1_1cube_2D-fold_angle_6.0-stacknum_1/1_c_2D.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     5
#: Number of Meshes:             6
#: Number of Element Sets:       16
#: Number of Node Sets:          21
#: Number of Steps:              1
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3130.69, 
    farPlane=4332.59, width=2196.72, height=1390.38, cameraPosition=(1592.01, 
    430.853, 3384.38), cameraUpVector=(-0.710013, 0.691897, -0.130999), 
    cameraTarget=(36.2186, 7.40309, -31.6327))
session.viewports['Viewport: 1'].view.setValues(nearPlane=2754.07, 
    farPlane=4713.63, width=1932.46, height=1223.12, cameraPosition=(1851.21, 
    -2297.75, 2325.29), cameraUpVector=(-0.351996, 0.781318, 0.515404), 
    cameraTarget=(33.0381, 40.8849, -18.6369))
session.viewports['Viewport: 1'].view.setValues(nearPlane=2816.92, 
    farPlane=4630.17, width=1976.56, height=1251.03, cameraPosition=(1241.68, 
    -2633.7, 2358.14), cameraUpVector=(-0.135466, 0.854452, 0.501558), 
    cameraTarget=(40.1507, 44.8051, -19.0202))
session.viewports['Viewport: 1'].view.setValues(nearPlane=2879.22, 
    farPlane=4567.87, width=1310.1, height=829.207, viewOffsetX=14.4745, 
    viewOffsetY=-12.8797)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=4 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=5 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=6 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=7 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=8 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=9 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=10 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=11 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=12 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=13 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=14 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=16 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=17 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=18 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=19 )
