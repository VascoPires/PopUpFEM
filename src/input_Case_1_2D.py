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
    'Job_name': '1_c_2D',     # Job name. If no name is given, an automatic name is attributed
    'run_job': True}            # Runs the job after generating the model - Typically work best with ABAQUS noGui 

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
       {'n':1,'dX':0.0,'dY':0.0, 'colors' : ['Salmon', 'Light Orange', 'Sand Red']}}


create_model(main_dict,BC_dict,model_def)

# Example:
# model_def = {
#    'Box':
#        {'l_X':2*main_dict['l']+20,'l_Y':3*main_dict['l']+100,'l_Z':3*z,'Lid':False},
#    'S1':
#        {'n':1,'dX':0.0,'dY':0.0, 'colors' : ['Very Light Gray', 'Light Gray', 'Dark Gray']},
#    'S2':
#        {'n':1,'dX':0.0,'dY':main_dict['l']+10.0 , 'colors' : ['Salmon', 'Light Orange', 'Sand Red']},
#    'S3':
#        {'n':1,'dX':0.0,'dY':-main_dict['l']-10.0, 'colors' : ['Very Light Gray', 'Light Gray', 'Dark Gray']}}