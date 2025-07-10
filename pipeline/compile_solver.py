import subprocess
import os

def compile_solver(params):

    # define paths
    solver_directory = params['solver_directory']
    output_path = params['output_path']
    build_dir = os.path.join(solver_directory, 'build')

    # ensure build and config output directories exist
    os.makedirs(build_dir, exist_ok=True)
    config_dir = os.path.join(output_path, 'config')
    os.makedirs(config_dir, exist_ok=True)

    # configure with CMake using GCC 11
    cmake_configure_cmd = [
        'cmake',
        '-S', solver_directory,
        '-B', build_dir,
        '-DCMAKE_C_COMPILER=gcc-11',
        '-DCMAKE_CXX_COMPILER=g++-11'
    ]

    subprocess.run(cmake_configure_cmd, check=True)
    cmake_build_cmd = ['cmake', '--build', build_dir]
    subprocess.run(cmake_build_cmd, check=True)