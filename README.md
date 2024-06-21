# finStruct

The finStruct library provides an environment for (quantitative) finance typical structures.

On the one hand, functional structures (where a combination of variables is mapped to one or more values) such as Interest Rate Curves and Volatility Surfaces are implemented. These are implemented in a general way, such that the user also has the freedom to construct any functional surface possible, without being restricted to certain dimensions or variables. It is implemented in a way similar to the implementation of sparse matrices. 
A diversity on operations is also implementede for the most frequently occuring structures, with a clear focus on Interest Rate Curves. Interpolation, Bootstrapping from market instruments, combining of curves and calculating different types of rates and converting curves is implemented.

On the other hand, more specific convention-related objects are implemented as well. A major example of this is the Calendar, which can be used in the construction of Fixed Income instruments but is used in the bootstrapping of curves as well.

This library does not have as goal to be a one-stop-shop for all financial analysis, but rather serves as a research environment in which to more easily conduct all the data manipulation and benchmarking required.


## Timeline

[ ] Curves
    [ ] Basic Gridinterpolator
    [ ] Implement Axis
    [ ] Termunit and converting: how to store rates?
        [ ] Spot
        [ ] Discount
        [ ] Forward
        [ ] Par
    
[ ] Implement framework for interpolation