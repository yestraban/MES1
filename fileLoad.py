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

def saveTemperatures(t, filename):
    file = open(filename, 'w')
    for i in range(len(t)):
        file.write(str(t[i]))
        file.write('\n')

def exportParaView(grid, t, filename):
    file = open(filename, 'w')
    file.write('# vtk DataFile Version 2.0\n')
    file.write('Unstructured Grid Example\n')
    file.write('ASCII\n')
    file.write('DATASET UNSTRUCTURED_GRID\n\n')
    file.write('POINTS '+str(len(grid.nodes))+' float\n')
    for i in range(len(grid.nodes)):
        file.write(str(grid.nodes[i].x))
        file.write(' ')
        file.write(str(grid.nodes[i].y))
        file.write(' ')
        file.write('0')
        file.write('\n')

    file.write('\nCELLS ')
    file.write(str(len(grid.elements)))
    file.write(' ')
    file.write(str(len(grid.elements)*5))
    file.write('\n')

    for i in range(len(grid.elements)):
        file.write('4 ')
        file.write(str(grid.elements[i].id[0]-1))
        file.write(' ')
        file.write(str(grid.elements[i].id[1]-1))
        file.write(' ')
        file.write(str(grid.elements[i].id[2]-1))
        file.write(' ')
        file.write(str(grid.elements[i].id[3]-1))
        file.write('\n')

    file.write('\nCELL_TYPES ')
    file.write(str(len(grid.elements)))
    file.write('\n')
    for i in range(len(grid.elements)):
        file.write('9\n')

    file.write('\nPOINT_DATA ')
    file.write(str(len(grid.nodes)))
    file.write('\nSCALARS scalars float 1\n')
    file.write('LOOKUP_TABLE default\n')

    for i in range(len(grid.nodes)):
        file.write(str(t[i]))
        file.write('\n')
    file.close()