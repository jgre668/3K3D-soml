import os
import re

def configure_solver(solver_directory, output_directory, params):

    # pull parameters from dictionary
    x_min = params['x_min']
    x_max = params['x_max']
    y_min = params['y_min']
    y_max = params['y_max']
    z_min = params['z_min']
    z_max = params['z_max']
    t_min = params['t_min']
    t_max = params['t_max']

    dx = params['dx']
    dy = params['dy']
    dz = params['dz']
    dt = params['dt']

    Du = params['Du']
    Dv = params['Dv']
    Dw = params['Dw']

    lambda_ = params['lambda']

    theta = params['theta']
    tau = params['tau']
    kappa1 = params['kappa1']
    kappa3 = params['kappa3']
    kappa4 = params['kappa4']

    bc = params['boundary_condition']

    # path to the C++ file
    param_file = os.path.join(solver_directory, 'src', '3K3D.cpp')  # Adjusted for 3D solver

    # read original file content
    with open(param_file, 'r') as file:
        content = file.read()

    # define regex patterns and their replacements
    replacements = {
        r'constexpr\s+std::pair<double,\s*double>\s+xlim\s*=\s*\{[^}]+\};':
            f'constexpr std::pair<double, double> xlim = {{{x_min}, {x_max}}};',

        r'constexpr\s+std::pair<double,\s*double>\s+ylim\s*=\s*\{[^}]+\};':
            f'constexpr std::pair<double, double> ylim = {{{y_min}, {y_max}}};',

        r'constexpr\s+std::pair<double,\s*double>\s+zlim\s*=\s*\{[^}]+\};':
            f'constexpr std::pair<double, double> zlim = {{{z_min}, {z_max}}};',

        r'constexpr\s+std::pair<double,\s*double>\s+tlim\s*=\s*\{[^}]+\};':
            f'constexpr std::pair<double, double> tlim = {{{t_min}, {t_max}}};',

        r'constexpr\s+double\s+dx\s*=\s*[^;]+;':
            f'constexpr double dx = {dx};',

        r'constexpr\s+double\s+dy\s*=\s*[^;]+;':
            f'constexpr double dy = {dy};',

        r'constexpr\s+double\s+dz\s*=\s*[^;]+;':
            f'constexpr double dz = {dz};',

        r'constexpr\s+double\s+dt\s*=\s*[^;]+;':
            f'constexpr double dt = {dt};',

        r'constexpr\s+double\s+Du\s*=\s*[^;]+;':
            f'constexpr double Du = {Du};',

        r'constexpr\s+double\s+Dv\s*=\s*[^;]+;':
            f'constexpr double Dv = {Dv};',

        r'constexpr\s+double\s+Dw\s*=\s*[^;]+;':
            f'constexpr double Dw = {Dw};',

        r'constexpr\s+double\s+lambda\s*=\s*[^;]+;':
            f'constexpr double lambda = {lambda_};',

        r'constexpr\s+double\s+theta\s*=\s*[^;]+;':
            f'constexpr double theta = {theta};',

        r'constexpr\s+double\s+tau\s*=\s*[^;]+;':
            f'constexpr double tau = {tau};',  # ← Added this line

        r'constexpr\s+double\s+kappa1\s*=\s*[^;]+;':
            f'constexpr double kappa1 = {kappa1};',

        r'constexpr\s+double\s+kappa3\s*=\s*[^;]+;':
            f'constexpr double kappa3 = {kappa3};',

        r'constexpr\s+double\s+kappa4\s*=\s*[^;]+;':
            f'constexpr double kappa4 = {kappa4};',

        r'constexpr\s+int\s+bc\s*=\s*[^;]+;':
            f'constexpr int bc = {bc};',

        r'const std::string filename_ics\s*=.*?;':
            fr'const std::string filename_ics = "{str(output_directory)}/binary/initial_conditions.bin";'
    }

    # apply replacements
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    # write back to file
    with open(param_file, 'w') as file:
        file.write(content)