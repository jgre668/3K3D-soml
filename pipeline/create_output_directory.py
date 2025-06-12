from pathlib import Path
import subprocess

def create_output_directory(params):

    output_path = params['output_path']
    label = params['label']

    # generate the name using contexere
    name = (subprocess.run(["name", "--project", "SOML", "--next"],
                          capture_output=True,
                          text=True,
                          check=True,
                          cwd=output_path).stdout.strip()
                          + '_' + label)

    # create the output folder
    output_directory = Path(output_path) / name
    output_directory.mkdir(parents=True, exist_ok=True)

    # create subdirectories: plot, config, binary
    for subfolder in ['plots', 'config', 'binary']:
        (output_directory / subfolder).mkdir(parents=True, exist_ok=True)

    return output_directory