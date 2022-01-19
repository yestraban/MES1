import numpy
import gdata
import gridElements

def loadFile(fileName):
    file = open(fileName, 'r')
    data = gdata.GlobalData()
    nodes = []
    elements = []

    temp = file.readline().split()      #odczytanie charakterystycznych wartości
    simulationTime = float(temp[1])

    temp = file.readline().split()
    dt = float(temp[1])

    temp = file.readline().split()
    conductivity = float(temp[1])

    temp = file.readline().split()
    alpha = float(temp[1])

    temp = file.readline().split()
    tot = float(temp[1])

    temp = file.readline().split()
    initialT = float(temp[1])

    temp = file.readline().split()
    ro = float(temp[1])

    temp = file.readline().split()
    cp = float(temp[1])

    temp = file.readline().split()
    nNodes = int(temp[2])

    temp = file.readline().split()
    nElements = int(temp[2])

    file.readline()

    for i in range(nNodes):                             #czytanie elementow
        temp = file.readline().split(',')
        nodes.append(gridElements.Node(float(temp[1]), float(temp[2])))

    file.readline()

    for i in range(nElements):
        temp = file.readline().split(',')
        elements.append(gridElements.Element(int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4])))

    file.readline()

    temp = file.readline().split(',')
    for i in range(len(temp)):
        nodes[int(temp[i])-1].bc = 1

    elementsk = [conductivity for _ in range(len(elements))]  # generowanie danych do elementu, tu można zmienić w razie potrzeby
    elementsalpha = [alpha for _ in range(len(elements))]
    elementstemp = [tot for _ in range(len(elements))]
    elementsro = [ro for _ in range(len(elements))]
    elementscp = [cp for _ in range(len(elements))]
    npc = 3

    grid = gridElements.Grid(nodes, elements, npc, elementsk, elementsalpha, elementstemp, elementsro, elementscp)

    return grid, simulationTime, dt, initialT