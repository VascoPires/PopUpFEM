


#### Parts dictionaries ####

def get_parts_dict(main_dict, Geom_Prop):
    parts_dict = {
        'Part_shell_side-0': [
            (0, -main_dict['l']/2, 0),
            (0, main_dict['l']/2, 0),
            (Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            (Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z'])
        ],
        'Part_shell_side-1': [
            (0, -main_dict['l']/2, 0),
            (0, main_dict['l']/2, 0),
            (-Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            (-Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z'])
        ],
        'Part_shell_side-2': [
            (0, -main_dict['l']/2, 2*Geom_Prop['delta_z']),
            (0, main_dict['l']/2, 2*Geom_Prop['delta_z']),
            (-Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            (-Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z'])
        ],
        'Part_shell_side-3': [
            (0, -main_dict['l']/2, 2*Geom_Prop['delta_z']),
            (0, main_dict['l']/2, 2*Geom_Prop['delta_z']),
            (Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            (Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z'])
        ]
    }

    triangles_dict = {    
        'Triangle_shell_side-0': [
            (0, -main_dict['l']/2, 0),
            (Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            (Geom_Prop['x_b'], -main_dict['l']/2 + Geom_Prop['y_b'], Geom_Prop['z_b'])],
        'Triangle_shell_side-1': [
            (0, -main_dict['l']/2, 0),
            (-Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            (-Geom_Prop['x_b'], -main_dict['l']/2 + Geom_Prop['y_b'], Geom_Prop['z_b'])],
        'Triangle_shell_side-2': [
            (0, -main_dict['l']/2, 2*Geom_Prop['delta_z']),
            (Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            (Geom_Prop['x_b'], -main_dict['l']/2 + Geom_Prop['y_b'], Geom_Prop['z_b'])], 
        'Triangle_shell_side-3': [
            (0, -main_dict['l']/2, 2*Geom_Prop['delta_z']),
            (-Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            (-Geom_Prop['x_b'], -main_dict['l']/2 + Geom_Prop['y_b'], Geom_Prop['z_b'])],
        'Triangle_shell_side-4': [
            (0, main_dict['l']/2, 0),
            (Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            (Geom_Prop['x_b'], main_dict['l']/2 - Geom_Prop['y_b'], Geom_Prop['z_b'])],
        'Triangle_shell_side-5': [
            (0, main_dict['l']/2, 0),
            (-Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            (-Geom_Prop['x_b'], main_dict['l']/2 - Geom_Prop['y_b'], Geom_Prop['z_b'])],
        'Triangle_shell_side-6': [
            (0, main_dict['l']/2, 2*Geom_Prop['delta_z']),
            (Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            (Geom_Prop['x_b'], main_dict['l']/2 - Geom_Prop['y_b'], Geom_Prop['z_b'])], 
        'Triangle_shell_side-7': [
            (0, main_dict['l']/2, 2*Geom_Prop['delta_z']),
            (-Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            (-Geom_Prop['x_b'], main_dict['l']/2 - Geom_Prop['y_b'], Geom_Prop['z_b'])],      
    }
    
    return parts_dict,triangles_dict

def get_folds_dict(main_dict, Geom_Prop):
    
    folds_dict = {
        'O_Fold_1':[
            {'Point1':(0, -main_dict['l']/2, 0),
            'Point2':(0.0,0.0,0.0),
            'Point3': (0, main_dict['l']/2, 0),
            'Part_1':'Part_shell_side-0','Part_2':'Part_shell_side-1'}
        ],
        'O_Fold_2':[
            {'Point1':(-Geom_Prop['delta_x'],-main_dict['l']/2,Geom_Prop['delta_z']),
            'Point2':(-Geom_Prop['delta_x'],0.0,Geom_Prop['delta_z']),
            'Point3':(-Geom_Prop['delta_x'],main_dict['l']/2,Geom_Prop['delta_z']),
            'Part_1':'Part_shell_side-1','Part_2':'Part_shell_side-2'}
        ],
        'O_Fold_3':[
            {'Point1':(0.0,-main_dict['l']/2,2*Geom_Prop['delta_z']),
            'Point2':(0.0,0.0,2*Geom_Prop['delta_z']),
            'Point3':(0.0,main_dict['l']/2,2*Geom_Prop['delta_z']),
            'Part_1':'Part_shell_side-2','Part_2':'Part_shell_side-3'}
        ],
        'O_Fold_4':[
            {'Point1':(Geom_Prop['delta_x'],-main_dict['l']/2,Geom_Prop['delta_z']),
            'Point2':(Geom_Prop['delta_x'],0.0,Geom_Prop['delta_z']),
            'Point3':(Geom_Prop['delta_x'],main_dict['l']/2,Geom_Prop['delta_z']),
            'Part_1':'Part_shell_side-0','Part_2':'Part_shell_side-3'}
        ]
    }

    inner_folds_dict = {
        'I_Fold_1':[
            {'Point1':(0, -main_dict['l']/2, 0),
            'Point2':(Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            'Part_1':'Triangle_shell_side-0','Part_2':'Part_shell_side-0'}
        ],
        'I_Fold_2':[
            {'Point1':(0, -main_dict['l']/2, 0),
            'Point2':(-Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            'Part_1':'Triangle_shell_side-1','Part_2':'Part_shell_side-1'}
            ],
        'I_Fold_3':[
            {'Point1':(0, -main_dict['l']/2, 2*Geom_Prop['delta_z']),
            'Point2':(-Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            'Part_1':'Triangle_shell_side-3','Part_2':'Part_shell_side-2'}
        ],
        'I_Fold_4':[
            {'Point1':(0, -main_dict['l']/2, 2*Geom_Prop['delta_z']),
            'Point2':(Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            'Part_1':'Triangle_shell_side-2','Part_2':'Part_shell_side-3'}
        ],
        'I_Fold_5':[
            {'Point1':(Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            'Point2':(Geom_Prop['x_b'], -main_dict['l']/2 + Geom_Prop['y_b'], Geom_Prop['z_b']),
            'Part_1':'Triangle_shell_side-0','Part_2':'Triangle_shell_side-2'}
        ], 
        'I_Fold_6':[
            {'Point1':(-Geom_Prop['delta_x'], -main_dict['l']/2, Geom_Prop['delta_z']),
            'Point2':(-Geom_Prop['x_b'], -main_dict['l']/2 + Geom_Prop['y_b'], Geom_Prop['z_b']),
            'Part_1':'Triangle_shell_side-1','Part_2':'Triangle_shell_side-3'}
        ],
        'I_Fold_7':[
            {'Point1':(0, main_dict['l']/2, 0),
            'Point2':(Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            'Part_1':'Triangle_shell_side-4','Part_2':'Part_shell_side-0'}
        ],
        'I_Fold_8':[
            {'Point1':(0, main_dict['l']/2, 0),
            'Point2':(-Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            'Part_1':'Triangle_shell_side-5','Part_2':'Part_shell_side-1'}
            ],
        'I_Fold_9':[
            {'Point1':(0, main_dict['l']/2, 2*Geom_Prop['delta_z']),
            'Point2':(-Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            'Part_1':'Triangle_shell_side-7','Part_2':'Part_shell_side-2'}
        ],
        'I_Fold_10':[
            {'Point1':(0, main_dict['l']/2, 2*Geom_Prop['delta_z']),
            'Point2':(Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            'Part_1':'Triangle_shell_side-6','Part_2':'Part_shell_side-3'}
        ],
        'I_Fold_11':[
            {'Point1':(Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            'Point2':(Geom_Prop['x_b'], main_dict['l']/2 - Geom_Prop['y_b'], Geom_Prop['z_b']),
            'Part_1':'Triangle_shell_side-4','Part_2':'Triangle_shell_side-6'}
        ], 
        'I_Fold_12':[
            {'Point1':(-Geom_Prop['delta_x'], main_dict['l']/2, Geom_Prop['delta_z']),
            'Point2':(-Geom_Prop['x_b'], main_dict['l']/2 - Geom_Prop['y_b'], Geom_Prop['z_b']),
            'Part_1':'Triangle_shell_side-5','Part_2':'Triangle_shell_side-7'}
        ]
    }
    
    return folds_dict, inner_folds_dict