
# Include this file in the same folder as the odb 

# Abaqus Python libs ##
from abaqus import *
from abaqusConstants import *


## Python Libs ##
import json
import os
import shutil
import numpy as np
import subprocess
from collections import OrderedDict

########### Post_Processsing ######

def remove_files(dir0,type_list=('.log', '.msg')):
    """Remove all files in the directory dir that end with the strings
    given in type_list and additional predefined strings. Some only with
    'ms.mdl' because they are needed for the first, implicit model to
    load the results
    
    Args:
    dir0 (str): The directory path where files are to be removed.
    type_list (tuple, optional): A tuple of file extensions to be removed. Defaults to ('.log', '.msg').
    
    Returns:
    None
    """
    type0_list = ('.com', '.sim', '.SMABulk', '.pac', '.abq',
                  '.dmp', '.exception', '.simdir', 'ms.mdl', 'ms.prt',
                  'ms.res', 'ms.res', 'ms.sel', 'ms.stt')
    
    # all files in the folder
    file_list = [i for i in os.listdir(dir0) if '.' in i]

    # number-Types
    number_list = tuple('.'+str(i) for i in range(1,21))

    # select files
    for file_name in file_list:
        for end_str in (type0_list + type_list + number_list):
            if file_name.endswith(end_str):
                try:
                    os.remove(file_name)
                except:
                    None
    return


def color_box_unit(vp1,instances):
    """Assign colors to the displayed instances either from the defined colors in the `assembly` dictionary or as random colors.
    
    Args:
    vp1 (Abaqus viewport): The viewport, needed to set the display colors.
    instances (dict): The instances of the model or the odb.
    
    Returns:
    None
    """

    # Lego colors from bricklink (only solid colors): https://www.bricklink.com/catalogColors.asp
    color_lib = {
        'White': 'ffffff', 'Very Light Gray': 'e5e5e5', 'Light Gray': '919191', 'Dark Gray': '615050',
        'Black': '1e1e1e', 'Dark Red': '631116',
        'Red': 'b10b0f', 'Coral': 'ff7669', 'Dark Salmon': 'ff592a', 'Salmon': 'ff7256',
        'Light Salmon': 'ffc0af', 'Sand Red': 'c28276', 'Brown': '633721',
        'Dark Orange': 'b04a17', 'Rust': 'af401c', 'Neon Orange': 'ff5041', 'Orange': 'ff7324',
        'Medium Orange': 'ff9a38', 'Bright Light Orange': 'ffbe2c', 'Light Orange': 'ffb23f',
        'Very Light Orange': 'ffd69e', 'Dark Yellow': 'de8c34', 'Yellow': 'ffda32',
        'Light Yellow': 'ffe39a', 'Bright Light Yellow': 'ffec89', 'Neon Yellow': 'fff938',
        'Neon Green': 'd5ef5b', 'Light Lime': 'e9eab8','Medium Lime': 'dcd931', 
        'Fabuland Lime': 'a1ca41', 'Lime': 'bbd930', 'Dark Olive Green': '6b693b',
        'Medium Green': '7ed986', 'Light Green': 'cfebcc', 'Sand Green': '95b69a',
        'Dark Turquoise': '009794', 'Light Turquoise': '00bdb4', 'Aqua': 'afe1d7', 'Light Aqua': 'c5ece7',
        'Dark Blue': '1e314c', 'Blue': '004f99', 'Dark Azure': '0096d8', 'Little Robots Blue': '43b7de',
        'Maersk Blue': '69b9d1', 'Medium Azure': '50c7da', 'Sky Blue': '76cedc', 'Medium Blue': '71a4d0',
        'Bright Light Blue': 'b1cbe9', 'Light Blue': 'bfd4dc', 'Sand Blue': '7b8fa0',
        'Dark Blue-Violet': '1731a2', 'Violet': '2a4296', 'Blue-Violet': '4065e7', 'Lilac': '6d5bc3'}
    
    # load the assembly dictionary from file
    with open('_dict-assembly.json', 'r') as f:
        assembly = json.load(f)['assembly']
    


    # check if there are colors stated in the assembly dictionary
    if "c" in assembly['parts']['1'].keys():
        # if 'c' keys in the parts: use those colors for video
        cm_set = set(cm_lego.keys())
        print(assembly['parts'].items())
        col_list = [get_color(assembly['parts'][str(i_part+1)],cm_set) for i_part in range(len(assembly['parts']))]+['1e1e1e']*4

    else:
        # if no colors are defined in parts of assembly dictionary:
        #    use random colors
        try:
            # if file exists, use the file for color scheme
            with open('_color-file.dat', 'r') as f:
                col_list = f.read().split(', ')
            print('loaded')
        except:
            # if file does not exist: shuffle colors and write file
            # use the color list 5 times such that more than 11 bricks can be used
            col_list = list(cm_lego.values())
            random.shuffle(col_list)
            with open('_color-file.dat', 'w') as f:
                f.write(', '.join(col_list))

    # if brick is divided into two parts, it should still have the same color
    inst_names = instances.keys()
    i = 0
    cmap_dict = {inst_names[0]:(True, '#' + col_list[i], 'Default', '#' + col_list[i])}
    i_name_temp = inst_names[0]
    #
    for inst_name in inst_names[1:]:
        if inst_name[:-4] != i_name_temp[:-4]:
            i += 1
        cmap_dict[inst_name] = (True, '#' + col_list[i], 'Default', '#' + col_list[i])
        i_name_temp = inst_name
    
    # set the color mapping
    cmap = vp1.colorMappings['Part instance']
    vp1.setColor(colorMapping=cmap)
    vp1.disableMultipleColors()
    
    cmap.updateOverrides(overrides=cmap_dict)
    cmap = vp1.colorMappings['Part instance']
    vp1.setColor(colorMapping=cmap)
    vp1.disableMultipleColors()
    return


#################

def assign_colors_to_assemblies_with_hex(model_def, color_lib, default_color='White'):
    """Assign colors to assemblies based on a provided model definition and color library.
    
    Args:
    model_def (dict): The model definition containing assembly information.
    color_lib (dict): A dictionary mapping color names to hexadecimal color codes.
    default_color (str, optional): The default color to use if a specific color is not provided. Defaults to 'White'.
    
    Returns:
    dict: A dictionary mapping assembly names to hexadecimal color codes.
    """
    assembly_colors_dict = {}
    assembly_index = 0  # Initialize an assembly index that increments across stacks
    for stack, details in sorted(model_def.items()):  # Sort to ensure consistent order in Python 2.7
        if stack.startswith('S'):  # Check if it's a stack
            num_assemblies = details['n']
            colors = details.get('colors', [])
            for i in range(num_assemblies):
                assembly_name = "{}_A{}".format(stack, assembly_index)
                if i < len(colors):
                    color_name = colors[i]
                    hex_color = color_lib.get(color_name, color_lib[default_color])
                else:
                    hex_color = color_lib[default_color]  # Use default color if not enough colors are provided or if color not found in lib
                assembly_colors_dict[assembly_name] = hex_color
                assembly_index += 1  # Increment global assembly index after each assignment
    return assembly_colors_dict


color_lib = {
    'White': 'ffffff', 'Very Light Gray': 'e5e5e5', 'Light Gray': '919191', 'Dark Gray': '615050',
    'Black': '1e1e1e', 'Dark Red': '631116',
    'Red': 'b10b0f', 'Coral': 'ff7669', 'Dark Salmon': 'ff592a', 'Salmon': 'ff7256',
    'Light Salmon': 'ffc0af', 'Sand Red': 'c28276', 'Brown': '633721',
    'Dark Orange': 'b04a17', 'Rust': 'af401c', 'Neon Orange': 'ff5041', 'Orange': 'ff7324',
    'Medium Orange': 'ff9a38', 'Bright Light Orange': 'ffbe2c', 'Light Orange': 'ffb23f',
    'Very Light Orange': 'ffd69e', 'Dark Yellow': 'de8c34', 'Yellow': 'ffda32',
    'Light Yellow': 'ffe39a', 'Bright Light Yellow': 'ffec89', 'Neon Yellow': 'fff938',
    'Neon Green': 'd5ef5b', 'Light Lime': 'e9eab8','Medium Lime': 'dcd931', 
    'Fabuland Lime': 'a1ca41', 'Lime': 'bbd930', 'Dark Olive Green': '6b693b',
    'Medium Green': '7ed986', 'Light Green': 'cfebcc', 'Sand Green': '95b69a',
    'Dark Turquoise': '009794', 'Light Turquoise': '00bdb4', 'Aqua': 'afe1d7', 'Light Aqua': 'c5ece7',
    'Dark Blue': '1e314c', 'Blue': '004f99', 'Dark Azure': '0096d8', 'Little Robots Blue': '43b7de',
    'Maersk Blue': '69b9d1', 'Medium Azure': '50c7da', 'Sky Blue': '76cedc', 'Medium Blue': '71a4d0',
    'Bright Light Blue': 'b1cbe9', 'Light Blue': 'bfd4dc', 'Sand Blue': '7b8fa0',
    'Dark Blue-Violet': '1731a2', 'Violet': '2a4296', 'Blue-Violet': '4065e7', 'Lilac': '6d5bc3'}


#################

#################
# Def main_postprocessing:
# Remove the files that are not important
dir_0 = os.path.abspath('') 
remove_files(dir_0,type_list=('.log', '.msg'))

with open('model_conditions.json', 'r') as f:
    model_dicts = json.load(f)


def extract_stacks_and_colors(model_dicts):
    stacks_and_colors = {}
    for key in model_dicts['model_def']:
        if key.startswith('S'):  # Checking if the key represents a stack
            colors = model_dicts['model_def'][key].get('colors', [])  # Getting the colors, with a default of empty list
            stacks_and_colors[key] = colors
    return stacks_and_colors

def find_odb_file(directory):
    for file in os.listdir(directory):
        if file.endswith(".odb"):
            return os.path.join(directory, file)
    return None

main_dict = model_dicts['main_dict']
model_def =  model_dicts['model_def']

# Use the function to find the ODB file
odb_file_path = find_odb_file(dir_0)
odb = session.openOdb(name=odb_file_path )


# Extract stacks and their associated colors
stacks_and_colors = extract_stacks_and_colors(model_dicts)
instances = odb.rootAssembly.instances.keys()

# Sort stack keys by extracting the numerical part for comparison
sorted_stacks = sorted([key for key in model_def.keys() if key.startswith('S')], key=lambda x: int(x[1:]))

# Create an OrderedDict for stacks with colors, following the sorted order
stacks_with_colors = OrderedDict((stack, model_def[stack]["colors"]) for stack in sorted_stacks)

assigned_colors_hex_dict = assign_colors_to_assemblies_with_hex(model_def, color_lib)

i = 0
instance_color_list = []
c_default = 'ffffff'

# # Process instances
# for entity in instances:

# Determine if entity is a special case or falls within a stack
for entity in instances:
    if entity.upper() in ['ASSEMBLY', 'BOX', 'TABLE', 'BOX_LID']:
        if entity == 'TABLE':
            color_instance = c_default
        else:    
            color_instance = c_default
    else:
        # Extract stack and assembly identifiers from entity name
        stack_id, assembly_id = entity.split('_')[0], entity.split('_')[1]
        key_id = stack_id + '_' + assembly_id 
        if key_id in assigned_colors_hex_dict.keys():
            color_instance = assigned_colors_hex_dict[key_id]
        else:
            color_instance = c_default
    instance_color_list.append([entity, color_instance])

# Create cmap_dict
cmap_dict = {}
i = 0
for inst_name in instances:
    cmap_dict[inst_name] = (True, '#' + instance_color_list[i][1], 'Default', '#' + instance_color_list[i][1])
    i += 1


# display the assembly
vp1 = session.viewports['Viewport: 1']
vp1.assemblyDisplay.setValues(optimizationTasks=OFF, geometricRestrictions=OFF,
                                stopConditions=OFF)

# select the iso view and fit model into the viewport
vp1.view.fitView()


# set the color mapping
cmap = vp1.colorMappings['Part instance']
vp1.setColor(colorMapping=cmap)
vp1.disableMultipleColors()

cmap.updateOverrides(overrides=cmap_dict)
cmap = vp1.colorMappings['Part instance']
vp1.setColor(colorMapping=cmap)
vp1.disableMultipleColors()

vp1.setValues(width=160, height=160)
vp1.odbDisplay.display.setValues(plotState=(DEFORMED, ))
vp1.odbDisplay.setFrame(step=0, frame=-1)
vp1.odbDisplay.commonOptions.setValues(visibleEdges=FEATURE)

# possibility to use a manual view
session.View(name='User-1', nearPlane=2822.5, farPlane=4778.9, width=1086.1, 
    height=605.3, projection=PERSPECTIVE, cameraPosition=(2767.4, 1986.4, 
    1706), cameraUpVector=(-0.58618, -0.41153, 0.69788), cameraTarget=(-24.003, 
    -30.932, 6.2948), viewOffsetX=64.843, viewOffsetY=11.598, autoFit=OFF)

vp1.view.setValues(session.views['User-1'])

vp1.viewportAnnotationOptions.setValues(triad=OFF, state=OFF, legendBackgroundStyle=MATCH,
                                        annotations=OFF, compass=OFF, title=OFF, legend=OFF)

session.pngOptions.setValues(imageSize=(160*8, 160*8))


# Generate folder for images
dir_0 = os.path.abspath('')

if main_dict.get('Make_gif', False):
    change_dir('img-video', if_change=1, if_clear=1)

    # print png images for all frames in the load step
    for i_frame in range(len(odb.steps['Explicit_step'].frames)):

        vp1.odbDisplay.setFrame(step=0, frame=i_frame)
        session.printToFile(fileName='anim-' + str(i_frame).zfill(3),format=PNG, canvasObjects=(vp1,))

    cmd = 'ffmpeg -f image2 -framerate 25 -i anim-%03d.png -loop -0 pop_box_3stacks.gif'

    # Use subprocess.call
    try:
        result = subprocess.call(cmd, shell=True)
    except Exception as e:
        print("An error occurred in the gif generation:", e)

    change_dir(dir_0 , if_change_directly = 1)