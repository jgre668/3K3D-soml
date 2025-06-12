import subprocess
import os

def run_solver(solver_directory, verbose = True):

    # define paths
    build_dir = os.path.join(solver_directory, 'build')
    executable_path = os.path.join(build_dir, '3K3D-solver')

    # ensure the build directory exists
    os.makedirs(build_dir, exist_ok=True)

    # configure with CMake using GCC 14
    cmake_configure_cmd = [
        'cmake',
        '-S', solver_directory,
        '-B', build_dir,
        '-DCMAKE_C_COMPILER=gcc-11',
        '-DCMAKE_CXX_COMPILER=g++-11'
    ]

    if verbose: print("\nConfiguring the project with CMake...")
    subprocess.run(cmake_configure_cmd, check=True)

    cmake_build_cmd = ['cmake', '--build', build_dir]
    if verbose: print("\nBuilding the project...")
    subprocess.run(cmake_build_cmd, check=True)

    if verbose: print("\nRunning the executable...")
    subprocess.run([executable_path], check=True, cwd=build_dir)
