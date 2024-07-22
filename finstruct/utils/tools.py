import numpy as np

def create_grid(*args):
        
    """
    """

    grid = np.meshgrid(*args, indexing='ij')
    grid = np.array(grid).reshape(len(args),-1).T
        
    return grid