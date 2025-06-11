
from self_organised_clustering import *

def main():

    # path to data
    data_file = "/Users/josiegreenwood/Desktop/3K3D-soml/two_points_0.35_0.65.csv"

    # path to solver
    solver_directory = Path.home()/"Desktop/3K3D-solver"

    self_organised_clustering(data_file, solver_directory)

    return

if __name__ == "__main__":
    main()
    
