import gridElements
import gdata

def generate_nodes(data):
    nodes = []
    for i in range(data.nB):
        for j in range(data.nH):
            nodes.append(gridElements.Node((i / (data.nB - 1)) * data.b, (j / (data.nH - 1)) * data.h, 0))

        #    if ((i == 0) or (i == data.nB - 1)) or ((j == 0) or (j == data.nB - 1)):
        #        nodes.append(gridElements.Node((i/(data.nB-1))*data.b, (j/(data.nH-1))*data.h, 1))
        #    else:
        #        nodes.append(gridElements.Node((i/(data.nB-1))*data.b, (j/(data.nH-1))*data.h, 0))
    return nodes


def generate_elements(data):
    elements = []
    n = 1
    nn = 0
    for i in range(data.nB-1):
        for j in range(data.nH-1):
                elements.append(gridElements.Element(n+j, n+data.nH+j, n+data.nH+1+j, n+1+j))
                nn += 1
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

def hbcAggregate(grid):
    hbcaggr = [[0 for _ in range(len(grid.nodes))] for _ in range(len(grid.nodes))]
    for i in range(len(grid.elements)):
        for x in range(4):
            for y in range(4):
                hbcaggr[grid.elements[i].id[x] - 1][grid.elements[i].id[y] - 1] += grid.elements[i].Hbc.Hbc[x][y]
    return hbcaggr

def addHandHBC(grid):
    HHBCaggr = [[0 for _ in range(len(grid.nodes))] for _ in range(len(grid.nodes))]
    for i in range (len(grid.nodes)):
        for j in range(len(grid.nodes)):
            HHBCaggr[i][j] = grid.Haggr[i][j] + grid.Hbcaggr[i][j]
    return HHBCaggr


def generateConstants(elements, nodes):
    k = []
    alpha = []
    tempAmbient = [30 for _ in range(len(elements))]
    ro = []
    cp = []
    initTemp = [100 for _ in range(len(nodes))]

    for i in range(len(elements)):
        xsr, ysr = 0.0, 0.0
        for j in range(4):
            xsr += nodes[elements[i].id[j]-1].x
            ysr += nodes[elements[i].id[j]-1].y
        xsr /= 4.0
        ysr /= 4.0

        if gdata.warunekMiedz(xsr, ysr):
            k.append(386)
            alpha.append(0)
            ro.append(8933)
            cp.append(386)

        elif gdata.warunekAluminium(xsr, ysr):
            k.append(239)
            alpha.append(-11)
            ro.append(2720)
            cp.append(900)
            nodes[elements[i].id[2]-1].bc = 1
            nodes[elements[i].id[3]-1].bc = 1

        else:
            k.append(0.43)
            alpha.append(0)
            ro.append(1070)
            cp.append(3380)

    return k, alpha, tempAmbient, ro, cp, initTemp


def fixTemp(temperatures, elements, nodes):
    for i in range(len(elements)):
        xsr, ysr = 0.0, 0.0
        for j in range(4):
            xsr += nodes[elements[i].id[j]-1].x
            ysr += nodes[elements[i].id[j]-1].y
        xsr /= 4.0
        ysr /= 4.0
        if gdata.warunekGlikol(xsr, ysr):
            for j in range(4):
                temperatures[elements[i].id[j]-1] = 40.0
    return temperatures
