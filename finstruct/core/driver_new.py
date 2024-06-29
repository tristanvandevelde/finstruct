from finstruct.utils.types import Meta


class DriverMeta(Meta):

    def __validate__(self):

        """Validate that all the spaces are set correctly."""

        for dimension in self.spaces:
            """
            Implement typecheck for Spaces.
            """

        pass

    def __new__(cls, name, bases, attrs):
        # for space in attrs['_SPACES']:
        #     attrs[space] = property(SpaceGetter(space), SpaceSetter(space))

        return type.__new__(cls, name, bases, attrs)
    

class Driver:

    _SPACETYPES = {}

    def __init__(self):

        self.spaces = {}