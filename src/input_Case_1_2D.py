import numpy as np

from main import create_model

main_dict = {
    'sim_name': 'Case_1_1cube_2D',
    'modelName': 'Pop_Box',
    'Modeltype' : '2D',
    'l': 65.0,                  # Side length [mm]                 
    't': 0.3,                   # Shell/Paper thickness [mm]
    'E': 2000.0,                # Young's Modulus of the material [MPa]
    'Poisson': 0.3,             # Poisson of the material [-]
    'density': 5.0E-10,         # Density of the material [tonne/mm^3]
    'scale_factor': 20.0,       # Table scale in relation with the box [-]
    'time_period': 1.2,         # Simulation time [s] 
    'num_intervals': 20,        # Number of frames/intervals [-]
    'nCPU' : 6,                 # Number of CPUs to be used
    'Job_name': '1_c_2D',       # Job name. If no name is given, an automatic name is attributed
    'run_job': True,            # Runs the job after generating the model - Typically work best with ABAQUS noGui 
    'Make_gif': False}          # Generates a gif using FFmpeg      

BC_dict = {
    'fold_angle': 6.0,          # Fold angle [deg]
    'band_stiff': 0.0077,       # Spring stiffness [N/mm]
    'ref_length': 85.0,         # Spring reference length [mm]
    'gravity_constant': 9810,   # Gravity constant [mm/s^2]   
    'friction_coef': 0.4}       # Coefficient of friction [-]

# So that the box has the same height as the the stack
z = 2*main_dict['l']*np.sin(BC_dict['fold_angle']*np.pi/180.0)  # total height of a box unit

model_def = {
   'S1':
       {'n':1,'dX':0.0,'dY':0.0, 'colors' : ['Salmon']}}


create_model(main_dict,BC_dict,model_def)

# Color Library
# color_lib = {
#     'White': 'ffffff', 'Very Light Gray': 'e5e5e5', 'Light Gray': '919191', 'Dark Gray': '615050',
#     'Black': '1e1e1e', 'Dark Red': '631116',
#     'Red': 'b10b0f', 'Coral': 'ff7669', 'Dark Salmon': 'ff592a', 'Salmon': 'ff7256',
#     'Light Salmon': 'ffc0af', 'Sand Red': 'c28276', 'Brown': '633721',
#     'Dark Orange': 'b04a17', 'Rust': 'af401c', 'Neon Orange': 'ff5041', 'Orange': 'ff7324',
#     'Medium Orange': 'ff9a38', 'Bright Light Orange': 'ffbe2c', 'Light Orange': 'ffb23f',
#     'Very Light Orange': 'ffd69e', 'Dark Yellow': 'de8c34', 'Yellow': 'ffda32',
#     'Light Yellow': 'ffe39a', 'Bright Light Yellow': 'ffec89', 'Neon Yellow': 'fff938',
#     'Neon Green': 'd5ef5b', 'Light Lime': 'e9eab8','Medium Lime': 'dcd931', 
#     'Fabuland Lime': 'a1ca41', 'Lime': 'bbd930', 'Dark Olive Green': '6b693b',
#     'Medium Green': '7ed986', 'Light Green': 'cfebcc', 'Sand Green': '95b69a',
#     'Dark Turquoise': '009794', 'Light Turquoise': '00bdb4', 'Aqua': 'afe1d7', 'Light Aqua': 'c5ece7',
#     'Dark Blue': '1e314c', 'Blue': '004f99', 'Dark Azure': '0096d8', 'Little Robots Blue': '43b7de',
#     'Maersk Blue': '69b9d1', 'Medium Azure': '50c7da', 'Sky Blue': '76cedc', 'Medium Blue': '71a4d0',
#     'Bright Light Blue': 'b1cbe9', 'Light Blue': 'bfd4dc', 'Sand Blue': '7b8fa0',
#     'Dark Blue-Violet': '1731a2', 'Violet': '2a4296', 'Blue-Violet': '4065e7', 'Lilac': '6d5bc3'}