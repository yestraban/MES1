import gdata
import diff

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
        data = gdata.GlobalData()
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

class Hbc:
    def __init__(self, element, npc, jakobian):
        data = gdata.GlobalData()
        self.Hbc = [[0 for _ in range(4)] for _ in range(4)]
        tempH = [[0 for _ in range(4)] for _ in range(4)]
        if(npc == 3):
                                        #to jest bardzo nieczytelne rozwiązanie
            for i in range(4):              #pętla dla ilości boków
                for j in range(4):          #pętla dla N poziomych
                    for k in range(4):      #pętla dla N pionowych
                        temp = 0
                        for l in range(npc):  #pętla dla ilości punktów całkowania
                            temp += data.wagi3p[npc] * diff.funkcjaKsztaltuN(element.pcb[i][npc],j) * diff.funkcjaKsztaltuN(element.pcb[i][npc],k)
                            #dodawanie osobno wartości dla każdego miejsca w macierzy Hbc[j][k]
                            #praktycznie: waga pc * N[j] * N[k], to powtórzone dla każdego punktu całkowania na boku i, oraz zsumowane
                        temp *= data.alpha * jakobian.det       #mnożenie przez stałe dla każdej wartości
                        self.Hbc[j][k] += temp

        else:
            for i in range(4):              #to samo co wyżej, tylko nie ma tu wag bo w dwupunktowym całkowaniu są równe 1
                for j in range(4):
                    for k in range(4):
                        temp = 0.0
                        for l in range(npc):  #pętla dla ilości punktów całkowania
                            temp += diff.funkcjaKsztaltuN(element.pcb[i][l],j) * diff.funkcjaKsztaltuN(element.pcb[i][l],k)
                        temp *= data.alpha * jakobian.det
                        self.Hbc[j][k] += temp