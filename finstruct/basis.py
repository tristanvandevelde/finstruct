
class Space:


    """
    The Space defines the dimensions and the units of structures.
    """

    def __init__(self,
                 coords,
                 vals):
        
        self.coords = coords
        self.vals = vals

        # each of these is a numpy array of units