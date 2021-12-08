import gdata
import diff
import hmatrix
import pmatrix
import cmatrix
import generate

class Node:
    def __init__(self, x, y, bc=0):
        self.x = x
        self.y = y
        self.bc = bc


class Element:
    def __init__(self, id1, id2, id3, id4):
        self.id = [id1, id2, id3, id4]
    H = [[0 for _ in range(4)] for _ in range(4)]
    Hbc = [[0 for _ in range(4)] for _ in range(4)]
    Pmatrix = [0 for _ in range(4)]
    Cmatrix = [[0 for _ in range(4)] for _ in range(4)]
    k = 0
    alpha = 0
    temp = 0
    ro = 0
    cp = 0


class Element4w:
    def __init__(self, npc):

        self.dNdZ = [[0 for _ in range(npc*npc)]  for _ in range(4)]
        self.dNdE = [[0 for _ in range(npc*npc)]  for _ in range(4)]
        self.npc = npc
        self.pcb = [[0 for _ in range(npc)] for _ in range(4)]
        self.ksztaltN = [[0 for _ in range(npc*npc)] for _ in range(4)]
        data = gdata.GlobalData()
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


        for i in range(npc):
            self.pcb[0][i] = Node(-1, wezly[i])
            self.pcb[1][i] = Node(wezly[i], -1)
            self.pcb[2][i] = Node(1, wezly[i])
            self.pcb[3][i] = Node(wezly[i], 1)

        for i in range(len(self.pc)):
            for j in range(4):
                self.ksztaltN[j][i] = diff.funkcjaKsztaltuN(self.pc[i], j)
        del data


class Grid:
    def __init__(self, nodes, elements, npc, k, alpha, temp, ro, cp):
        self.nodes = nodes
        self.elements = elements
        self.Haggr = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        self.Hbcaggr = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        self.Caggr = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        self.Paggr = [0 for _ in range(len(nodes))]
        odwJak = [0 for _ in range(npc*npc)]
        element = Element4w(npc)
        for i in range(len(self.elements)):
            for j in range(npc * npc):
                jak = hmatrix.Jakobian(self, i, element, j)
                odwJak[j] = hmatrix.JakobianOdw(jak)
            self.elements[i].k = k[i]
            self.elements[i].alpha = alpha[i]
            self.elements[i].temp = temp[i]
            self.elements[i].ro = ro[i]
            self.elements[i].cp = cp[i]
            self.elements[i].H = hmatrix.MacierzSztywnosciH(odwJak, npc, element, elements[i].k)
            self.elements[i].Cmatrix = cmatrix.MacierzC(element, npc, odwJak, elements[i].ro, elements[i].cp)
            self.elements[i].Hbc = hmatrix.Hbc(element, npc, self, i, elements[i].alpha)
            # print("element ", i)
            # for l in range(4):
            #     print(self.elements[i].Hbc.Hbc[l])
            # print()
            self.elements[i].Pmatrix = pmatrix.Pmatrix(element, npc, self, i, elements[i].alpha, elements[i].temp)

        self.Haggr = generate.hAgregate(self)
        self.Paggr = generate.pAgregate(self)
        self.Caggr = generate.cAgregate(self)
        self.Hbcaggr = generate.hbcAggregate(self)
        self.Haggr = generate.addHandHBC(self)
