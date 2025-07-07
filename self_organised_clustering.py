from parameters import *
from pipeline import *
import shutil

def self_organised_clustering():

    # define file paths
    data_file = Path(params['data_file'])
    solver_directory = Path(params['solver_directory'])

    # create an output folder
    print('\nCreating an output folder...')
    output_directory = create_output_directory(params)
    print(f"...results will be saved to {output_directory}")

    Time = Timer(output_directory / "config/time_log.txt")

    # read in data and find the equivalent grid indices
    print('\nReading in data...')
    data_points, data_idx = process_data(data_file, params)
    print('...arrays created')
    Time.checkpoint("Process data")

    # solve for the stable stationary homogeneous states
    # and add these to params dictionary
    print('\nCalculating stable stationary homogeneous states...')
    states = find_stationary_states(params)
    params['states'] = states
    print(f'...states are {states[0]} and {states[1]}')
    Time.checkpoint("Solve for stable states")
    
    # calculate an array of initial conditions
    print('\nCreating array of initial conditions...')
    create_initial_conditions_3d(data_idx, output_directory, params)
    print(f"...array saved to {output_directory}/binary")
    Time.checkpoint("Calculate initial conditions")

    # configure the solver with the correct parameters and path names
    print('\nUpdating parameters in C++ solver...')
    configure_solver(solver_directory, output_directory, params)
    print('...solver configured')
    Time.checkpoint("Configure solver")

    # run the solver
    print('\nRunning solver...')
    run_solver(params)
    print('...complete!')
    Time.checkpoint("Run solver")


    # move the folder of binary files from the C++ solver to the output folder
    print("\nSaving all outputs...")
    shutil.move(solver_directory / "binaries/3K3D", output_directory / "binary")

    # save configuration
    with open(output_directory / 'config/parameters.txt', 'w') as f:
        for key, value in params.items():
            f.write(f'{key}: {value}\n')
    print(f"...saved to {output_directory}")
    Time.checkpoint("Save all outputs")

    print('\nComplete!')

    Time.total()


