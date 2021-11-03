# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Element:
    def __init__(self, id1, id2, id3, id4):
        self.id = [id1, id2, id3, id4]
    H = [[0 for _ in range(4)] for _ in range(4)]

class Element4w:
    def __init__(self, npc):

        self.dNdZ = [[0 for _ in range(npc*npc)]  for _ in range(4)]
        self.dNdE = [[0 for _ in range(npc*npc)]  for _ in range(4)]
        self.npc = npc
        data = GlobalData()

        if npc == 2:
            wezly = data.wezly2p

        elif npc == 3:
            wezly=data.wezly3p
        self.pc =[]
        for i in range(npc*npc):
            self.pc.append(Node(0,0))
        i = 0
        for x in range(npc):
            for y in range(npc):
                self.pc[i].x = wezly[x]
                self.pc[i].y = wezly[y]
                i += 1

        for i in range(len(self.pc)):
            self.dNdZ[0][i] = -1.0 / 4*(1 - self.pc[i].y)
            self.dNdZ[1][i] = 1.0 / 4*(1 - self.pc[i].y)
            self.dNdZ[2][i] = 1.0 / 4*(1 + self.pc[i].y)
            self.dNdZ[3][i] = -1.0 / 4*(1 + self.pc[i].y)

        for j in range(len(self.pc)):
            self.dNdE[0][j] = -1.0 / 4*(1 - self.pc[j].x)
            self.dNdE[1][j] = -1.0 / 4*(1 + self.pc[j].x)
            self.dNdE[2][j] = 1.0 / 4*(1 + self.pc[j].x)
            self.dNdE[3][j] = 1.0 / 4*(1 - self.pc[j].x)
        del data

class Jakobian:
    # def __init__(self, nkfs : list, element4w, npc):
    #     self.dXdZ = 0
    #     self.dXdE = 0
    #     self.dYdZ = 0
    #     self.dYdE = 0
    #     for b in range(4):
    #         self.dXdZ += nkfs[b].x * element4w.dNdZ[b][npc]
    #         self.dXdE += nkfs[b].x * element4w.dNdE[b][npc]
    #         self.dYdZ += nkfs[b].y * element4w.dNdZ[b][npc]
    #         self.dYdE += nkfs[b].y * element4w.dNdE[b][npc]
    #     self.det = (self.dXdZ * self.dYdE) - (self.dXdE * self.dYdZ)

    def __init__(self, grid, i, element4w, npc):
        self.dXdZ = 0
        self.dXdE = 0
        self.dYdZ = 0
        self.dYdE = 0
        nodes = []
        print(grid.elements[i].id)
        for a in range(4):
            temp = grid.elements[i].id[a]
            nodes.append(grid.nodes[temp-1])

        for b in range(4):
            self.dXdZ += nodes[b].x * element4w.dNdZ[b][npc]
            self.dXdE += nodes[b].x * element4w.dNdE[b][npc]
            self.dYdZ += nodes[b].y * element4w.dNdZ[b][npc]
            self.dYdE += nodes[b].y * element4w.dNdE[b][npc]

        self.det = (self.dXdZ * self.dYdE) - (self.dXdE * self.dYdZ)

class JakobianOdw:
    def __init__(self, jakobian):
        self.dYdE = (1/jakobian.det) * jakobian.dYdE
        self.mdYdZ = (1/jakobian.det) * (-jakobian.dYdZ)
        self.mdXdE = (1/jakobian.det) * (-jakobian.dXdE)
        self.dXdZ = (1/jakobian.det) * (jakobian.dXdZ)
        self.det = jakobian.det

class MacierzSztywnosciH:
    def __init__(self, jakobianOdw, npc, element):
        self.H = [[0 for _ in range(4)] for _ in range(4)]
        data = GlobalData()
        for i in range(npc*npc):
            self.dNdX = []
            self.dNdY = []
            for j in range(4):
                self.dNdX.append(jakobianOdw.dYdE * element.dNdZ[j][i] + jakobianOdw.mdYdZ * element.dNdE[j][i])
                self.dNdY.append(jakobianOdw.mdXdE * element.dNdZ[j][i] + jakobianOdw.dXdZ * element.dNdE[j][i])
            tempH = [[0 for _ in range(4)] for _ in range(4)]

            for i in range(4):
                for j in range(4):
                    tempH[i][j] = self.dNdX[j]*self.dNdX[i] + self.dNdY[i]*self.dNdY[j]
                    tempH[i][j] *= data.k * jakobianOdw.det
                    self.H[i][j] += tempH[i][j]

class GlobalData:
    h = 0.5
    b = 0.4
    nH = 5
    nB = 4
    wagi3p = [5/9, 8/9, 5/9]
    wezly2p = [-1/numpy.sqrt(3), 1/numpy.sqrt(3)]
    wezly3p = [-numpy.sqrt(3/5), 0, numpy.sqrt(3/5)]
    k = 30

def funkcja_1d(x):
    wynik = 5*x*x
    wynik += 3*x
    wynik += 6
    return wynik


def funkcja_2d(x,y):
    wynik = 5*x*x*y*y
    wynik += 3*x*y
    wynik += 6
    return wynik


def calkowanie_gaussa_1d(funkcja, p):
    suma = 0
    gdata = GlobalData()
    if p == 2:
        for i in range(p):
            suma += funkcja(gdata.wezly2p[i])

    elif p == 3:
        for i in range(p):
            suma += funkcja(gdata.wezly3p[i]) * gdata.wagi3p[i]

    return suma


def calkowanie_gaussa_2d(funkcja, p):
    suma = 0
    gdata = GlobalData()
    if p == 2:
        for i in range(p) :
            for j in range(p) :
                suma += funkcja(gdata.wezly2p[i], gdata.wezly2p[j])

    elif p == 3:
        for i in range(p) :
            for j in range(p) :
                suma += funkcja(gdata.wezly3p[i], gdata.wezly3p[j]) * gdata.wagi3p[i] * gdata.wagi3p[j]

    return suma


class Grid:
    def __init__(self, nodes, elements):
        self.nodes = nodes
        self.elements = elements


def generate_nodes(data):
    nodes = []
    for i in range(data.nB):
        for j in range(data.nH):
            nodes.append(Node((i/(data.nB-1))*data.b, (j/(data.nH-1))*data.h))
    return nodes


def generate_elements(data):
    elements = []
    n = 1
    for i in range(data.nB-1):
        for j in range(data.nH-1):
            elements.append(Element(n+j, n+data.nH+j, n+data.nH+1+j, n+1+j))
        n += data.nH
    return elements



if __name__ == '__main__':
    nodes = generate_nodes(GlobalData)
  #  for i in range(len(nodes)):
   #     print(nodes[i].x, " ", nodes[i].y)

    elements = generate_elements(GlobalData)
  #  for i in range(len(elements)):
   #     print(elements[i].id)

  #  wynik = calkowanie_gaussa_1d(funkcja_1d, 2)
   # print(wynik)

  #  wynik = calkowanie_gaussa_1d(funkcja_1d, 3)
 #   print(wynik)

 #   wynik = calkowanie_gaussa_2d(funkcja_2d, 2)
 #   print(wynik)

 #   wynik = calkowanie_gaussa_2d(funkcja_2d, 3)
  #  print(wynik)


    tabx = [0, 0.025, 0.025, 0]
    taby = [0, 0, 0.025, 0.025]
    nds = []
    for i in range(4):
        nds.append(Node(tabx[i], taby[i]))
    element = Element4w(2)
    grid = Grid(nodes, elements)
    # jak = Jakobian(nds, element, 0)
    # print(jak.dXdZ, " ", jak.dYdZ)
    # print(jak.dXdE, " ", jak.dYdE)
    # odwJak = JakobianOdw(jak);
    # print()
    # print(odwJak.dYdE, " ", odwJak.mdYdZ)
    # print(odwJak.mdXdE, " ", odwJak.dXdZ)

    for i in range(len(grid.elements)):
        for j in range(element.npc*element.npc):
            jak = Jakobian(grid, i, element, j)
            print(jak.dXdZ, " ", jak.dYdZ)
            print(jak.dXdE, " ", jak.dYdE)
            odwJak = JakobianOdw(jak)
            print()
            print(odwJak.dYdE, " ", odwJak.mdYdZ)
            print(odwJak.mdXdE, " ", odwJak.dXdZ)
            print()
            h = MacierzSztywnosciH(odwJak, 2, element)
            grid.elements[i].H = h

    print("==================================")
    print()
    print("Macierze sztywnosci H:")

    for i in range(len(grid.elements)):
        for j in range(4):
            print(grid.elements[i].H.H[j])
        print("++++++++++++++++++++++++++++++++++")