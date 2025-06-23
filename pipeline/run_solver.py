import subprocess
import os

def run_solver(params):

    solver_directory = params['solver_directory']
    output_directory = params['output_directory']

    # define paths
    build_dir = os.path.join(solver_directory, 'build')
    executable_path = os.path.join(build_dir, '3K3D-solver')

    # ensure build and config output directories exist
    os.makedirs(build_dir, exist_ok=True)
    config_dir = os.path.join(output_directory, 'config')
    os.makedirs(config_dir, exist_ok=True)

    # configure with CMake using GCC 11
    cmake_configure_cmd = [
        'cmake',
        '-S', solver_directory,
        '-B', build_dir,
        '-DCMAKE_C_COMPILER=gcc-11',
        '-DCMAKE_CXX_COMPILER=g++-11'
    ]

    print("\nConfiguring the project with CMake...")
    subprocess.run(cmake_configure_cmd, check=True)

    cmake_build_cmd = ['cmake', '--build', build_dir]
    print("\nBuilding the project...")
    subprocess.run(cmake_build_cmd, check=True)

    print("\nRunning the executable and capturing output...")
    # run solver and capture output to file
    log_path = os.path.join(config_dir, 'solver_output.txt')
    with open(log_path, 'w') as log_file:
        subprocess.run(
            [executable_path],
            check=True,
            cwd=build_dir,
            stdout=log_file,
            stderr=subprocess.STDOUT
        )

    print(f"Solver output saved to {log_path}")