import gdata
import diff
import numpy

class Jakobian:
    def __init__(self, grid, i, element4w, npc):
        self.dXdZ = 0
        self.dXdE = 0
        self.dYdZ = 0
        self.dYdE = 0
        nodes = []
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
    def __init__(self, jakobianOdw, npc, element, conductivity):
        data = gdata.GlobalData()
        self.H = [[0 for _ in range(4)] for _ in range(4)]
        npcCounter = 0;
        for n in range(npc):
            for i in range(npc):
                self.dNdX = []
                self.dNdY = []
                for j in range(4):
                    self.dNdX.append(jakobianOdw[npcCounter].dYdE * element.dNdZ[j][npcCounter] + jakobianOdw[npcCounter].mdYdZ * element.dNdE[j][npcCounter])
                    self.dNdY.append(jakobianOdw[npcCounter].mdXdE * element.dNdZ[j][npcCounter] + jakobianOdw[npcCounter].dXdZ * element.dNdE[j][npcCounter])
                tempH = [[0 for _ in range(4)] for _ in range(4)]
                if(npc == 3):
                    for k in range(4):
                        for j in range(4):
                            tempH[k][j] = self.dNdX[j]*self.dNdX[k] + self.dNdY[k]*self.dNdY[j]
                            tempH[k][j] *= conductivity * jakobianOdw[npcCounter].det * data.wagi3p[n]*data.wagi3p[i]
                            self.H[k][j] += tempH[k][j]
                else:
                    for k in range(4):
                        for j in range(4):
                            tempH[k][j] = self.dNdX[j]*self.dNdX[k] + self.dNdY[k]*self.dNdY[j]
                            tempH[k][j] *= conductivity * jakobianOdw[npcCounter].det
                            self.H[k][j] += tempH[k][j]
                npcCounter += 1


class Hbc:
    def __init__(self, element, npc, grid, i, alpha):
        data = gdata.GlobalData()
        self.Hbc = [[0 for _ in range(4)] for _ in range(4)]
        tempH = [[0 for _ in range(4)] for _ in range(4)]
        nodes = []
        sides = []
        for a in range(4):
            temp = grid.elements[i].id[a]
            nodes.append(grid.nodes[temp - 1])

        sides.append((numpy.sqrt((nodes[3].x - nodes[0].x) * (nodes[3].x - nodes[0].x) + (nodes[3].y - nodes[0].y) * (
                    nodes[3].y - nodes[0].y)))*nodes[0].bc*nodes[3].bc)

        for b in range(3):
            sides.append(numpy.sqrt(
                ((nodes[b].x - nodes[b + 1].x) * (nodes[b].x - nodes[b + 1].x) + (nodes[b].y - nodes[b + 1].y) * (
                        nodes[b].y - nodes[b + 1].y)))*nodes[b].bc*nodes[b+1].bc)


        if(npc == 3):
                                        #to jest bardzo nieczytelne rozwiązanie
            for i in range(4):              #pętla dla ilości boków
                for j in range(4):          #pętla dla N poziomych
                    for k in range(4):      #pętla dla N pionowych
                        temp = 0
                        for l in range(npc):  #pętla dla ilości punktów całkowania
                            temp += data.wagi3p[l] * diff.funkcjaKsztaltuN(element.pcb[i][l],j) * diff.funkcjaKsztaltuN(element.pcb[i][l],k)
                            #dodawanie osobno wartości dla każdego miejsca w macierzy Hbc[j][k]
                            #praktycznie: waga pc * N[j] * N[k], to powtórzone dla każdego punktu całkowania na boku i, oraz zsumowane
                        temp *= alpha * sides[i]/2       #mnożenie przez stałe dla każdej wartości i jakobian boku
                        self.Hbc[j][k] += temp

        else:
            for i in range(4):              #to samo co wyżej, tylko nie ma tu wag bo w dwupunktowym całkowaniu są równe 1
                for j in range(4):
                    for k in range(4):
                        temp = 0.0
                        for l in range(npc):  #pętla dla ilości punktów całkowania
                            temp += diff.funkcjaKsztaltuN(element.pcb[i][l],j) * diff.funkcjaKsztaltuN(element.pcb[i][l],k)
                        temp *= alpha * sides[i]/2
                        self.Hbc[j][k] += temp