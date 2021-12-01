import hmatrix
import gdata
import gridElements

class MacierzC:
    def __init__(self, element, npc, jakobian):
        self.C = [[0 for _ in range(4)] for _ in range(4)]
        data = gdata.GlobalData()
        npcCounter = 0
        for n in range(npc):
            for i in range(npc):
                for j in range(4):
                    for k in range (4):
                        temp = element.ksztaltN[j][npcCounter]*element.ksztaltN[k][npcCounter]
                        temp *= data.ro * data.cp * jakobian.det * data.wagi3p[n] * data.wagi3p[i]
                        self.C[j][k] += temp
                npcCounter += 1