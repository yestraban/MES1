import hmatrix
import gdata
import gridElements

class MacierzC:
    def __init__(self, element, npc, jakobianOdw, ro, cp):
        data = gdata.GlobalData()
        self.C = [[0 for _ in range(4)] for _ in range(4)]
        npcCounter = 0
        for n in range(npc):
            for i in range(npc):
                for j in range(4):
                    for k in range (4):
                        temp = element.ksztaltN[j][npcCounter]*element.ksztaltN[k][npcCounter]
                        temp *= ro * cp * jakobianOdw[npcCounter].det * data.wagi3p[n] * data.wagi3p[i]
                        self.C[j][k] += temp
                npcCounter += 1