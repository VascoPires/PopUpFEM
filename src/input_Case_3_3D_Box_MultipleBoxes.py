import numpy as np

from main import create_model

main_dict = {
    'sim_name': 'Case_4_NoBox', # Simulation name. Will affect the folder name
    'modelName': 'Pop_Box',     # ABAQUS CAE Model name
    'Modeltype' : '3D',         # Model box type. Available options: 2D and 3D
    'l': 65.0,                  # Side length [mm]                 
    't': 0.3,                   # Shell/Paper thickness [mm]
    'E': 2000.0,                # Young's Modulus of the material [MPa]
    'Poisson': 0.3,             # Poisson of the material [-]
    'density': 5.0E-10,         # Density of the material [tonne/mm^3]
    'scale_factor': 20.0,       # Table scale in relation with the box [-]
    'time_period': 1.2,         # Simulation time [s] 
    'num_intervals': 20,        # Number of frames/intervals [-]
    'nCPU' : 6,                 # Number of CPUs to be used
    'Job_name': '1_c',          # Job name. If no name is given, an automatic name is attributed
    'run_job': True}            # Runs the job after generating the model - Typically work best with ABAQUS noGui 

BC_dict = {
    'fold_angle': 6.0,          # Fold angle [deg]
    'band_stiff': 1.2*0.0077,   # Spring stiffness [N/mm]
    'ref_length': 85.0,         # Spring reference length [mm]
    'gravity_constant': 9810,   # Gravity constant [mm/s^2]   
    'friction_coef': 0.4}       # Coefficient of friction [-]

# So that the box has the same height as the the stack
z = 2*main_dict['l']*np.sin(BC_dict['fold_angle']*np.pi/180.0)  # total height of a box unit

model_def = {
   'S1':
       {'n':3,'dX':0.0,'dY':0.0, 'colors' : ['Brown', 'Orange', 'Dark Orange']},
   'S2':
       {'n':3,'dX':0.0,'dY':main_dict['l']+10.0 , 'colors' : ['Salmon', 'Light Orange', 'Sand Red']},
   'S3':
       {'n':3,'dX':0.0,'dY':-main_dict['l']-10.0, 'colors' : ['Dark Olive Green', 'Medium Green', 'Lime']}}


create_model(main_dict,BC_dict,model_def)