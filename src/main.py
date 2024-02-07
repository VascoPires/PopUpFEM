
# Abaqus Python libs ##
from abaqus import *
from abaqusConstants import *
from caeModules import *


## Python Libs ##
import json
import os
import shutil
import numpy as np

# Creates the parts dictionaries
from parts_dics_gen import get_parts_dict, get_folds_dict


session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
TOL = 1E-6

def get_mid_point(point1,point2):
    x = (point1[0]+point2[0])/2
    y = (point1[1]+point2[1])/2
    z = (point1[2]+point2[2])/2
    return (x,y,z)

# Function to mirror a point across the X-Z plane
def mirror_point_y(point):
    x, y, z = point
    return (x, -y, z)


def generate_tie_sets(main_dict, fold_name, set_dict, assembly_obj, Assembly_name):
    a = assembly_obj
    part_1 = main_dict['my_Model'].parts[set_dict['Part_1']]
    part_2 = main_dict['my_Model'].parts[set_dict['Part_2']]

    set1_name = "%s_set1" % fold_name
    set2_name = "%s_set2" % fold_name

    if 'Triangle' in set_dict['Part_1'] or 'Triangle' in set_dict['Part_2']:
        md_point = get_mid_point(set_dict['Point1'],set_dict['Point2'])
        print(md_point)
        part_1.Set(name=set1_name, edges=part_1.edges.findAt((md_point, ), ))
        main_set = a.instances[Assembly_name+set_dict['Part_1']].sets[set1_name]
        part_2.Set(name=set2_name, edges=part_2.edges.findAt((md_point, ), ))
        sec_set = a.instances[Assembly_name+set_dict['Part_2']].sets[set2_name]
    else:
        md_point1 = get_mid_point(set_dict['Point1'],set_dict['Point2'])
        md_point2 = get_mid_point(set_dict['Point2'],set_dict['Point3'])
        
        part_1.Set(name=set1_name, edges=part_1.edges.findAt((md_point1, ), (md_point2, )))
        main_set = a.instances[Assembly_name+set_dict['Part_1']].sets[set1_name]
        part_2.Set(name=set2_name, edges=part_2.edges.findAt((md_point1, ), (md_point2, )))
        sec_set = a.instances[Assembly_name+set_dict['Part_2']].sets[set2_name]
    

    return main_set, sec_set

def gen_mesh(main_dict, part_name, size):

    p = main_dict['my_Model'].parts[part_name]
    p.seedPart(size=size, deviationFactor=0.1, minSizeFactor=0.1)

    f = p.faces

    pickedRegions = f.getByBoundingBox(zMin=-100*main_dict['l'])
    p.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=STRUCTURED)



    p.generateMesh() 


def generate_material_section(main_dict):
    main_dict['my_Model'].Material(name='Paper')
    main_dict['my_Model'].materials['Paper'].Elastic(table=((main_dict['E'], main_dict['Poisson']), ))
    main_dict['my_Model'].materials['Paper'].Density(table=((main_dict['density'], ), ))

    # Definte Section
    main_dict['my_Model'].HomogeneousShellSection(name='Paper_Shell_Sect', 
        preIntegrate=OFF, material='Paper', thicknessType=UNIFORM, thickness=main_dict['t'], 
        thicknessField='', nodalThicknessField='', idealization=NO_IDEALIZATION, 
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
        useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)


def assign_section(main_dict,p, part_name):

    # Assign Section
    f = p.faces
    model_face = f.getByBoundingBox(zMin=-100*main_dict['l'])
    region = p.Set(faces=model_face, name= part_name+'_side_Whole_Model')


    p.SectionAssignment(region=region, sectionName='Paper_Shell_Sect', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)


def gen_part(main_dict, part_name, points, assembly_obj, Assembly_name, ly_lid_box=1):
    if part_name == 'Table' or part_name == 'Box_Lid':
        p = main_dict['my_Model'].Part(name=part_name, dimensionality=THREE_D, type=DISCRETE_RIGID_SURFACE)
    else:
        p = main_dict['my_Model'].Part(name=part_name, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    
    datum_point_ids = []

    for coords in points:
        datum_point = p.DatumPointByCoordinate(coords=coords)
        datum_point_ids.append(datum_point.id)
    
    # Create the datum_wire tuple
    d = p.datums
    e = p.edges
    f = p.faces
    v = p.vertices
    datum_wire_pairs = []

    # Iterate over each index in the datum_point_ids list
    for i in range(len(datum_point_ids)):
        
        # Create a pair using datum IDs: current datum point and the next datum point
        pair = (d[datum_point_ids[i]], d[datum_point_ids[(i + 1) % len(datum_point_ids)]])
        
        # Append this pair to the list
        datum_wire_pairs.append(pair)

    # Use datum_wire_pairs in the WirePolyLine method
    p.WirePolyLine(points=datum_wire_pairs, mergeType=MERGE, meshable=ON)
    p.CoverEdges(edgeList=(e.getByBoundingBox(zMin=0-TOL)), tryAnalytical=False)

    if 'Part_shell_side' in part_name or part_name == 'Table':
        XZ_plane = p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
        pickedFaces = p.faces.getByBoundingBox(zMin=0-TOL)
        p.PartitionFaceByDatumPlane(datumPlane=d[XZ_plane.id], faces=pickedFaces)

        if part_name == 'Table':
            YZ_plane = p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)
            pickedFaces = p.faces.getByBoundingBox(zMin=0-TOL)
            p.PartitionFaceByDatumPlane(datumPlane=d[YZ_plane.id], faces=pickedFaces)
            



    ##### Assign Material and BC ####
    if part_name != 'Box_Lid':
        if part_name != 'Table':
            ## Assign material to part
            assign_section(main_dict,p,part_name)
            assembly_obj.Instance(name=Assembly_name+part_name, part=p, dependent=ON)
        else:
            assembly_obj.Instance(name=part_name, part=p, dependent=ON)
            
            ############
            faces_BC = assembly_obj.instances[part_name].faces.getByBoundingBox(zMin=-100*main_dict['l'])
            region = assembly_obj.Set(faces=faces_BC, name=part_name+'_Fixed_BC')
            main_dict['my_Model'].EncastreBC(name='BC_Box_Fixed', createStepName='Initial', region=region, localCsys=None)  
            
            # Apply BC to the RF
            RF = p.ReferencePoint(point=(0.0, 0.0, 0.0))
            r1 = assembly_obj.instances[part_name].referencePoints
            region_RF = assembly_obj.Set(referencePoints=(r1[RF.id], ), name=part_name+'_RF_Set')
            main_dict['my_Model'].EncastreBC(name=part_name+'_Fixed_RF', createStepName='Initial', region=region_RF, localCsys=None)
    else:       
            assembly_obj.Instance(name=part_name, part=p, dependent=ON)   
            
            faces_whole = assembly_obj.instances[part_name].faces.getByBoundingBox(zMin=-100*main_dict['l'])
            region = assembly_obj.Set(faces=faces_whole, name=part_name+'_Whole_instance')
              
            # Apply BC to the RF
            RF = p.ReferencePoint(point=(0.0, -ly_lid_box/2, 0.0))
            r1 = assembly_obj.instances[part_name].referencePoints
            region_RF = assembly_obj.Set(referencePoints = (r1[RF.id], ), name=part_name+'_RP')
            
            # Generate Amplitude
            main_dict['my_Model'].TabularAmplitude(name='Amp_Disp_Lid', timeSpan=STEP, 
                smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (0.025, 0.5), (0.05, 1.0)))

            main_dict['my_Model'].DisplacementBC(name=part_name+'_Disp_RF', 
                createStepName='Explicit_step', region=region_RF, 
                u1=0.0, u2=-ly_lid_box, u3=0.0, 
                ur1=0.0, ur2=0.0, ur3=0.0, amplitude='Amp_Disp_Lid', fixed=OFF, 
                distributionType=UNIFORM, fieldName='', localCsys=None)
            


    return

def gen_table(main_dict,assembly_obj):

    table_point_list = [ 
        (-main_dict['l']*main_dict['scale_factor']/2, -main_dict['l']*main_dict['scale_factor']/2, 0),
        (main_dict['l']*main_dict['scale_factor']/2, -main_dict['l']*main_dict['scale_factor']/2, 0),
        (main_dict['l']*main_dict['scale_factor']/2, main_dict['l']*main_dict['scale_factor']/2, 0),
        (-main_dict['l']*main_dict['scale_factor']/2, main_dict['l']*main_dict['scale_factor']/2, 0)   
    ]

    # Create Table
    gen_part(main_dict, 'Table', table_point_list, assembly_obj, Assembly_name = '')

    size = main_dict['l']*main_dict['scale_factor']/20
    gen_mesh(main_dict,'Table', size)


###################################

def gen_spring(main_dict, BC_dict, Geom_Prop, assembly_obj, Assembly_name):

    ### Create Spring Connector
    main_dict['my_Model'].ConnectorSection(name=Assembly_name + 'Spring', u1ReferenceLength=BC_dict['ref_length'], translationalType=AXIAL)
    spring_connector_section = main_dict['my_Model'].sections[Assembly_name + 'Spring']

    elastic_0 = connectorBehavior.ConnectorElasticity(components=(1, ), table=((BC_dict['band_stiff'], ), ))
    spring_connector_section.setValues(behaviorOptions =(elastic_0, ) )

    ### Generate the Wire and Set
    # Find the vertices for the wire
    v_shell_0 = assembly_obj.instances[Assembly_name + 'Part_shell_side-0'].vertices
    v_shell_1 = assembly_obj.instances[Assembly_name + 'Part_shell_side-1'].vertices

    v1 = (Geom_Prop['delta_x'],0.0,Geom_Prop['delta_z'])
    v2 = (-Geom_Prop['delta_x'],0.0,Geom_Prop['delta_z'])
    
    vertex_mid1 = v_shell_0.findAt(coordinates=v1)
    vertex_mid2  = v_shell_1.findAt(coordinates=v2)

    # Generate Wire
    assembly_obj.WirePolyLine(points=((vertex_mid1, vertex_mid2), ), mergeType=IMPRINT, meshable=OFF)

    # Generate Wire set
    assembly_obj.Set(edges=assembly_obj.edges.findAt(((0.0, 0.0, Geom_Prop['delta_z']), )), name=Assembly_name+'Wire_Spring')

    # Generate local Coordinate System for the spring
    datum_CSYS = assembly_obj.DatumCsysByThreePoints(origin=vertex_mid2, 
        point1=vertex_mid1, 
        point2=v_shell_1.findAt(coordinates=(-Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z'])), 
        name=Assembly_name + 'Spring_CSYS', coordSysType=CARTESIAN)

    connector_assign = assembly_obj.SectionAssignment(sectionName=Assembly_name+'Spring', region=assembly_obj.sets[Assembly_name+'Wire_Spring'])
    datum1 = main_dict['my_Model'].rootAssembly.datums[datum_CSYS.id]
    assembly_obj.ConnectorOrientation(region=connector_assign.getSet(), localCsys1=datum1)


###################################
###################################################################################################


def gen_box_unit(main_dict,BC_dict, Assembly_name, a):

    fold_angle_rad = BC_dict['fold_angle']*np.pi/180
    phi = np.arcsin(np.tan(fold_angle_rad))

    Geom_Prop = {
        'delta_x' : main_dict['l']*np.cos(fold_angle_rad),
        'delta_z' : main_dict['l']*np.sin(fold_angle_rad),
        'x_b'     : main_dict['l']/2*(np.cos(fold_angle_rad)-np.cos(fold_angle_rad)*np.tan(fold_angle_rad)),
        'y_b'     : main_dict['l']/2*(np.cos(phi)),
        'z_b'     : main_dict['l']/2*(np.sin(fold_angle_rad)+np.cos(fold_angle_rad)*np.tan(fold_angle_rad))
    }


    # Generates the Material Section
    generate_material_section(main_dict)

    # Creates the parts dictionaries
    parts_dict, triangles_dict = get_parts_dict(main_dict, Geom_Prop)
    folds_dict, inner_folds_dict = get_folds_dict(main_dict, Geom_Prop)

    if main_dict['Modeltype'] == '3D':
        parts_dict.update(triangles_dict)
        folds_dict.update(inner_folds_dict)

    # Generate all required instances    
        
    instance_name_list = []

    for part_name, points in parts_dict.items():
        gen_part(main_dict, part_name, points, a, Assembly_name)

    # Contact property
    contact_prop = main_dict['my_Model'].ContactProperty('Contact_Prop')
    contact_prop.TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        BC_dict['friction_coef'], ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)


    # Assign General contact in explicit
    main_dict['my_Model'].ContactExp(name='General_Contact', createStepName='Initial')
    main_dict['my_Model'].interactions['General_Contact'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
    main_dict['my_Model'].interactions['General_Contact'].contactPropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, SELF, 'Contact_Prop'), ))


    main_dict['my_Model'].interactionProperties['Contact_Prop'].tangentialBehavior.setValues(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        0.4, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)

    # Generate Spring Connector
    gen_spring(main_dict, BC_dict, Geom_Prop, a, Assembly_name)



    for fold_name, set_info in folds_dict.items():

        set_dict = set_info[0]

        main_set, sec_set = generate_tie_sets(main_dict, fold_name, set_dict, a, Assembly_name)

        
        main_dict['my_Model'].Tie(name=Assembly_name+fold_name, main=main_set, secondary=sec_set, 
                                positionToleranceMethod=COMPUTED, adjust=ON, 
                                tieRotations=OFF, thickness=ON)


    # Step
    main_dict['my_Model'].ExplicitDynamicsStep(name='Explicit_step', 
        previous='Initial', timePeriod=main_dict['time_period'], improvedDtMethod=ON)



    # Gravity
    main_dict['my_Model'].Gravity(name='Gravity', createStepName='Explicit_step', 
        comp3=-BC_dict['gravity_constant'], distributionType=UNIFORM, field='')

    # Generate Mesh
    for part_name in parts_dict:

        if 'Triangle' in part_name:
            size = main_dict['l']/15
        else:
            size = main_dict['l']/10
        gen_mesh(main_dict, part_name, size)


    # Generate History Output in the top node
    v = a.instances[Assembly_name+'Part_shell_side-3'].vertices
    top_v = a.Set(vertices=v.findAt(((0.0, main_dict['l']/2, 2*Geom_Prop['delta_z']), )), name=Assembly_name+'Top_node')

    # Generate Field Output
    main_dict['my_Model'].fieldOutputRequests['F-Output-1'].setValues(variables=(
        'S', 'U', 'V'), numIntervals=main_dict['num_intervals'])

    main_dict['my_Model'].HistoryOutputRequest(name=Assembly_name+'U3', 
        createStepName='Explicit_step', variables=('U3', ), region=top_v, sectionPoints=DEFAULT, rebar=EXCLUDE)



def gen_box(main_dict, box_info, assembly_obj, Assembly_name):

    lx = box_info['l_X']
    ly = box_info['l_Y']
    lz = box_info['l_Z']

   # Define points
    points = [
        (lx/2, ly/2), 
        (lx/2, -ly/2), 
        (-lx/2, -ly/2), 
        (-lx/2, ly/2),
        (lx/2, ly/2) 
    ]

    sketch = main_dict['my_Model'].ConstrainedSketch(name='Box_Sketch', sheetSize=200.0)

    # Create lines between consecutive points
    for i in range(len(points) - 1):
        sketch.Line(point1=points[i], point2=points[i + 1])

    p = main_dict['my_Model'].Part(name='Box', dimensionality=THREE_D, type=DISCRETE_RIGID_SURFACE)
    p.BaseShellExtrude(sketch=sketch, depth=lz)

    # Generate Reference Point
    RF = p.ReferencePoint(point=(0.0, 0.0, 0.0))

    mesh_box_size = np.max([lx,ly,lz])/15
    
    assembly_obj.Instance(name='Box', part=p, dependent=ON)
    r1 = assembly_obj.instances['Box'].referencePoints
    region_RF = assembly_obj.Set(referencePoints = (r1[RF.id], ), name='Box_RP_Box')
    main_dict['my_Model'].EncastreBC(name='Box_Fixed_RF', createStepName='Initial', region=region_RF, localCsys=None)
    
    gen_mesh(main_dict,'Box',mesh_box_size)


    # Gen top of the box
    if box_info['Lid']:
        points_lid = [(x, y, lz) for x, y in points[:-1]]
        gen_part(main_dict, 'Box_Lid', points_lid, assembly_obj, Assembly_name, ly)
        gen_mesh(main_dict, 'Box_Lid',mesh_box_size)
        


def change_dir(dir_name, if_change_directly = 0, if_change=0, if_clear=0):
    """Create folder and possibly change the work directory to it

    Args:
    dir_name (str): String that defines the directory name. Can also be a path if used with if_change_directly = True
    if_change_directly (bool): If yes the directory is changed directory if it is given in dir_name
    if_change (bool): If the directory should be set as the work directory
    if_clear (bool): If the directory already exists, should its content (including all sub-folders) be deleted 

    Returns:
    dir_abs (str): The absolute path of the created directory
    """
    dir_abs = os.path.abspath('')

    if if_change_directly:
        os.chdir(dir_name)
        return
    # if path does not exist: create
    if os.path.exists(dir_name) == 0:
        os.mkdir(dir_name)
    else:
        # if it exists: clear if if_clear==1
        if if_clear:
            shutil.rmtree(dir_name)
            os.mkdir(dir_name)
    dir1 = dir_abs + "/" + dir_name

    # change into the dir_name directory
    if if_change:
        os.chdir(dir1)
    return dir_abs


def run_model(model, job_name, n_proc=4, run_job = True):
    """Run Abaqus model with a job called job_name using n_proc processors. Use double precision.
    """
    # if job_name is empty, just use the model name
    if job_name == '':
        job_name = model.name
     
    # Save the cae, create and run job. Watch out: job.waitForCompletion() usually crashes if the script is not run using `abaqus cae nogui=...` in the command line
    mdb.saveAs(pathName=model.name + '.cae')
    job = mdb.Job(model=model.name, name=job_name, type=ANALYSIS,
                  multiprocessingMode=THREADS, numCpus=n_proc,
                  explicitPrecision=DOUBLE_PLUS_PACK, 
                  nodalOutputPrecision=FULL, numDomains=n_proc)
    
    if run_job:
        job.submit(consistencyChecking=OFF)
        # waitForCompletion() crashes, if run interactively
        #  --> try opening window to manually check when job is finished
        try:
            getWarningReply('Wait until job has finished (see .sta file), then press Yes.',buttons=(YES,NO))
        except:
            job.waitForCompletion()
        return
    else:
        return

#####################################################################################################3

# Function Create Model:

def create_model(main_dict, BC_dict, model_def):

    ### Define parameters for postprocessing and generates
    job_name = main_dict.get('Job_name', None)  # Provides None if 'Job_name' does not exist

    if not job_name:
        # Handle case where 'Job_name' is not provided - e.g., by generating an automatic name
        job_name = main_dict['modelName'] + main_dict['sim_name'] + main_dict['Modeltype'] + str(round(BC_dict['fold_angle'],1))

    ### Outputs json file with info
    # Combine dictionaries
    combined_dict = {
        'main_dict': main_dict,
        'BC_dict': BC_dict,
        'model_def': model_def
    }

    stack_count = 0
    for key in model_def.iterkeys():
        if key.startswith('S'):
            stack_count += 1
            
    dir_name = main_dict['sim_name'] + '-' + 'fold_angle_' + str(BC_dict['fold_angle']) + '-stacknum_' + str(stack_count)

    # Create directory
    dir_0 = os.path.abspath('')                             # Saves original dir
    dir_1 = change_dir(dir_name, if_change=1, if_clear=1)   # Changes dir


    # Write to JSON file
    with open('model_conditions.json', 'w') as json_file:
        json.dump(combined_dict, json_file, indent=4)

    #####################################################################

    #### Abaqus Model Gen ###
    mdb.Model(modelType=STANDARD_EXPLICIT, name=main_dict['modelName'])
    main_dict['my_Model'] = mdb.models[main_dict['modelName']]

    a = main_dict['my_Model'].rootAssembly
    z = 2*main_dict['l']*np.sin(BC_dict['fold_angle']*np.pi/180.0)  # total height of a box unit

    # Generates Table
    gen_table(main_dict,a)

    # Generate Stack
    k = 0
    max_n = 0


    for stack_name, stack_info in sorted(model_def.items()):
        
        if not stack_name == 'Box':
            n = stack_info['n']
            if max_n > n:
                max_n = n
            Assembly_name = stack_name+'_A'+str(k)+'_'
            
            for i in range(n):
                gen_box_unit(main_dict,BC_dict, Assembly_name , a)
                
                instance_ass_names = [name for name in a.instances.keys() if Assembly_name in name]
                a.translate(instanceList=instance_ass_names, vector=(0.0, 0.0, i*z))
                k = k+1
                Assembly_name = stack_name+'_A'+str(k)+'_'

            # Position the stack
            instance_stack_names = [name for name in a.instances.keys() if stack_name in name]
            a.translate(instanceList=instance_stack_names, vector=(stack_info['dX'], stack_info['dY'], 0.0))


    if 'Box' in model_def:
        gen_box(main_dict, model_def['Box'], a, Assembly_name)

        # Add BC to box
        
        faces_BC = a.instances['Box'].faces.getByBoundingBox(zMin=-100*main_dict['l'])
        region = a.Set(faces=faces_BC, name='Box_Sides')
        main_dict['my_Model'].EncastreBC(name='BC_Box_Fixed', createStepName='Initial', 
            region=region, localCsys=None)    

    # Runs the job - Be careful that this may only work with NoGUI on
    run_model(main_dict['my_Model'], job_name , main_dict['nCPU'], main_dict['run_job'])


    # Change back to the original folder
    change_dir(dir_0 , if_change_directly = 1)