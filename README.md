
<div align="center">
    <img src="images/Pop_up_box_logo.png">
</div>

# PopUpFEM : Automated Abaqus/Python model generation for jumping cubes

### Introduction
Poping boxes is a project developed using Abaqus/Python scripting, in order to simulate the behavior of origami like folded boxes, with a rubber band attached. This is commonly known as Pop Jumping Cubes, and there are a lot of videos on Youtube on how to make them yourself.

Examples:
- [Pop Up Cubes Card Tutorial - From DIY Blaster](https://www.youtube.com/watch?v=PdaHHFXTUxQ)
-  [Pop up Cubes in a box Tutorial - From Srushti Patil](https://www.youtube.com/watch?v=h3P-WZ2uPx0&t)
-  [How to Make BOOMF Jumping Box Pop Up Cube - From Joy in Crafting](https://www.youtube.com/watch?v=jKvsseAAZmo)

This project was initially conceived as a "Kitchen Mechanics" project using Abaqus Python scripting, which was challenged to me by a colleague.
<div align="center">
   <img src="images/pop_boxes_video.gif">
    Figure 1: Jumping cubes.
</div>

### Dependencies
* [Simulia Abaqus](https://www.3ds.com/products-services/simulia/products/abaqus) 2017 or later
* [FFmpeg](https://ffmpeg.org) (optional, to create animated gifs of the results)

### Quick start

The files `main.py.py`, `parts_dics_gen.py` and an input file must be in your working directory. You can choose one of the provided input files, such as `input_Case_1_2D.py`. You can run the PopUpFEM with the command `abaqus cae noGui=input_Case_1_2D.py` or `abaqus cae script=input_Case_1_2D.py` if you desire the Abaqus CAE GUI. This runs the first test case of PopUpFEM which is a simple "2D" Pop Up Box (more will be detailed later). The file can be changed and is customizable and the dictionaries `main_dict` `BC_dict` and `model_def` can be changed according to your preferences.

The syntax in the input dictionaries and the details of the model are described in the following sections. 

### 1. Using the script

The script is mainly composed by three main dictionaries, the `main_dict` where the main model parameters are defined, the `BC_dict` with the important boundary conditions and the `model_def` where stacks of box units are defined with the specified colors.

```python
main_dict = {
    'sim_name': 'Case_1',       # Simulation name
    'modelName': 'Pop_Box',     # Model name
    'Modeltype' : '3D',         # Model type: can be either "2D" or "3D"
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
    'run_job': True}            # Runs the job after generating the model - Typically work best with ABAQUS noGui 
```


```python
BC_dict = {
    'fold_angle': 6.0,          # Fold angle [deg]
    'band_stiff': 0.0077,       # Spring stiffness [N/mm]
    'ref_length': 85.0,         # Spring reference length [mm]
    'gravity_constant': 9810,   # Gravity constant [mm/s^2]   
    'friction_coef': 0.4}       # Coefficient of friction [-]
```

jjj

```python
model_def = {
    'Box':
        {'l_X':2*main_dict['l']+20,'l_Y':3*main_dict['l']+100,'l_Z':3*z,'Lid':False},
    'S1':
        {'n':3,'dX':0.0,'dY':0.0, 'colors' : ['Very Light Gray', 'Light Gray', 'Dark Gray']},
    'S2':
        {'n':3,'dX':0.0,'dY':main_dict['l']+10.0 , 'colors' : ['Salmon', 'Light Orange', 'Sand Red']},
    'S3':
        {'n':3,'dX':0.0,'dY':-main_dict['l']-10.0, 'colors' : ['Very Light Gray', 'Light Gray', 'Dark Gray']}}
```

![](images/lego-functions0.png)
<p align="center">

Figure 2: Structure of the model function <code>make_model</code> that creates, runs, and evaluates the Lego model from the input dictionaries <code>assembly</code>, <code>explicit_par</code>, and <code>lego_geom</code>. Note that <code>lego_geom</code> is optional. By default, it contains  basic Lego dimensions and the Lego material properties.
</p>

#### 1.1 Definition of the stack and box unit

#### 1.2 Dimensions and other parameters

#### 1.3 Running the model

#### 1.4 Output of the model

### 2. Under the hood

#### 2.1 General assumptions

#### 2.2 Definition 
