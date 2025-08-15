from parameters import *
from pipeline import *
import shutil

def self_organised_clustering():

    # STEP 0: set directories
    data_file = Path(params['data_file'])
    solver_directory = Path(params['solver_directory'])
    print('\nCreating an output folder...')
    output_directory = create_output_directory(params)
    print(f"...results will be saved to {output_directory}")
    params['output_directory'] = output_directory

    # starts the timer and creates a time log file in the output dir
    Time = Timer(output_directory / "config/time_log.txt")

    # STEP 1: read in data and find the equivalent grid indices
    print('\nReading in data...')
    data_points, data_idx = process_data(data_file, params)
    print(f'...dataset shape is {data_points.shape}')
    Time.checkpoint("Process data")

    # STEP 2: solve for the stable stationary homogeneous states
    # and add these to params dictionary
    print('\nCalculating stable stationary homogeneous states...')
    states = find_stationary_states(params)
    params['states'] = states
    print(f'...states are {states[0]} and {states[1]}')
    Time.checkpoint("Solve for stable states")
    
    # STEP 3: calculate an array of initial conditions
    # and save as a binary file
    print('\nCreating array of initial conditions...')
    create_initial_conditions_3d(data_idx, output_directory, params)
    print(f"...array saved to {output_directory}/binary")
    Time.checkpoint("Calculate initial conditions")

    # STEP 4: configure the solver with the correct parameters and path names
    print('\nUpdating parameters in C++ solver...')
    configure_solver(solver_directory, output_directory, params)
    print('...solver configured')
    Time.checkpoint("Configure solver")

    # STEP 5: compile the solver
    print('\nCompiling solver...')
    compile_solver(params)
    print('...complete!')
    Time.checkpoint("Compile solver")

    # STEP 6: run the solver
    print('\nRunning solver...')
    run_solver(params)
    print('...complete!')
    Time.checkpoint("Run solver")

    """ Other clustering steps have not yet been implemented."""


    # STEP 11: save outputs that haven't been saved yet
    # move the binary files from the C++ solver to the output folder
    print("\nSaving all outputs...")
    shutil.move(solver_directory / "binaries/3K3D", output_directory / "binary")
    with open(output_directory / 'config/parameters.txt', 'w') as f:
        for key, value in params.items():
            f.write(f'{key}: {value}\n')
    print(f"...saved to {output_directory}")
    Time.checkpoint("Save all outputs")

    print('\nComplete!')

    Time.total()


