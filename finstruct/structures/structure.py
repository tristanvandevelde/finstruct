


#     def get_values(self,
#                    **kwargs):
        
#         """
#         Get values given by condition.
#         """
        
#         names = list(kwargs.keys())
#         values = list(kwargs.values())

#         grid = self.create_grid(*values)
#         for value in grid.T:
#             conditions = dict(zip(names, value))
#             idx = self.filter(**conditions)
#             if idx.any():
#                 val = self.values[idx]
#             else:
#                 # interpolate
#                 pass

