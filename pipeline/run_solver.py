import subprocess
import os

def run_solver(params):

    solver_directory = params['solver_directory']
    output_path = params['output_directory']

    # define paths
    build_dir = os.path.join(solver_directory, 'build')
    executable_path = os.path.join(build_dir, '3K3D-solver')
    config_dir = os.path.join(output_path, 'config')

    # run solver and capture output to file
    log_path = os.path.join(config_dir, 'solver_output.txt')
    with open(log_path, 'w') as log_file:
        subprocess.run(
            [executable_path],
            check = True,
            cwd = build_dir,
            stdout = log_file,
            stderr = subprocess.STDOUT
        )