# MES1
Repository for FEM classes 2021 <br>
Code calculates changes in custom (detailed in main.py, gdata.py) grids composed of 4-node elements over time. <br>
Code files are located in venv folder with contents detiailed below: <br>
- cmatrix.py - Class MacierzC, where C matrix is calculated for provided arguments
- diff.py - Contains methods for calculatig values of N shape functions and basic Gauss integral calculations
- hmatrix.py - Classes for calculating Jakobian, H and HBC matrixes of provided grid element
- pmatrix.py - Calculatig P vector of provided grid element
- gdata.py - Contains basic variables for grid creation and necessary lists for Gauss integrals
- generate.py - Methods for generating nodes/elements and aggregation of all matrixes
- gridElements.py - Basic structures for grid calculations
