import gdata
import numpy as np

def temperatureStep(grid, t0):
    hctemp = [[0 for _ in range(len(grid.nodes))] for _ in range(len(grid.nodes))]
    pctemp = [0 for _ in range(len(grid.nodes))]
    data = gdata.GlobalData()
    for i in range(len(grid.nodes)):
        for j in range(len(grid.nodes)):
            hctemp[i][j] = grid.Haggr[i][j] + (grid.Caggr[i][j]/data.dT)

    for i in range(len(grid.nodes)):
        for j in range(len(grid.nodes)):
            pctemp[i] += (grid.Caggr[i][j]/data.dT)*t0[j]
        pctemp[i] += grid.Paggr[i]

    solveTemp = np.linalg.solve(hctemp,pctemp)
    return solveTemp