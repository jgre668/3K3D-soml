from parameters import *
from pipeline import *
import shutil

def self_organised_clustering(data_file, solver_directory):

    # create an output folder
    print('\nCreating an output folder...')
    output_directory = create_output_directory(params)
    print(f"...results will be saved to {output_directory}")

    # read in data and find the equivalent grid indices
    print('\nReading in data...')
    data_points, data_idx = process_data(data_file, params)
    print('\n...arrays created')

    # solve for the stable stationary homogeneous states
    # and add these to params dictionary
    print('\nCalculating stable stationary homogeneous states...')
    states = find_stationary_states(params)
    params['states'] = states
    print(f'...states are {states[0]} and {states[1]}')
    
    # calculate an array of initial conditions
    print('\nCreating array of initial conditions...')
    create_initial_conditions_3d(data_idx, output_directory, params)
    print(f"...array saved to {output_directory}/binary")

    # configure the solver with the correct parameters and path names
    print('\nUpdating parameters in C++ solver...')
    configure_solver(solver_directory, output_directory, params)
    print('...solver configured')

    # run the solver
    print('\nRunning solver...')
    run_solver(solver_directory)
    print('...complete!')


    # move the binary files from the C++ solver to the output folder
    print("\nSaving all outputs...")
    shutil.move(solver_directory / "binaries/3K3D/3K3D_u.bin",
                output_directory / "binary/3K2D_u.bin")
    shutil.move(solver_directory / "binaries/3K3D/3K3D_v.bin",
                output_directory / "binary/3K2D_v.bin")
    shutil.move(solver_directory / "binaries/3K3D/3K3D_w.bin",
                output_directory / "binary/3K2D_w.bin")

    # save configuration
    with open(output_directory / 'config/parameters.txt', 'w') as f:
        for key, value in params.items():
            f.write(f'{key}: {value}\n')
    print(f"...saved to {output_directory}")




