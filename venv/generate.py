import gridElements

def generate_nodes(data):
    nodes = []
    for i in range(data.nB):
        for j in range(data.nH):
            if ((i == 0) or (i == data.nB - 1)) or ((j == 0) or (j == data.nB - 1)):
                nodes.append(gridElements.Node((i/(data.nB-1))*data.b, (j/(data.nH-1))*data.h, 1))
            else:
                nodes.append(gridElements.Node((i/(data.nB-1))*data.b, (j/(data.nH-1))*data.h, 0))
    return nodes


def generate_elements(data):
    elements = []
    n = 1
    for i in range(data.nB-1):
        for j in range(data.nH-1):
                elements.append(gridElements.Element(n+j, n+data.nH+j, n+data.nH+1+j, n+1+j))

        n += data.nH
    return elements

def hAgregate(grid):
    Haggr = [[0 for _ in range(len(grid.nodes))] for _ in range(len(grid.nodes))]
    for i in range(len(grid.elements)):
        for x in range(4):
            for y in range(4):
                Haggr[grid.elements[i].id[x]-1][grid.elements[i].id[y]-1] += grid.elements[i].H.H[x][y]
    return Haggr

def pAgregate(grid):
    Paggr = [0 for _ in range(len(grid.nodes))]
    for i in range(len(grid.elements)):
        for x in range(4):
            Paggr[grid.elements[i].id[x] - 1] += grid.elements[i].Pmatrix.pmatrix[x]
    return Paggr

def cAgregate(grid):
    Caggr = [[0 for _ in range(len(grid.nodes))] for _ in range(len(grid.nodes))]
    for i in range(len(grid.elements)):
        for x in range(4):
            for y in range(4):
                Caggr[grid.elements[i].id[x] - 1][grid.elements[i].id[y] - 1] += grid.elements[i].Cmatrix.C[x][y]
    return Caggr