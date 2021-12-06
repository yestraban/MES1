import gdata
import diff
import numpy

class Pmatrix:
    def __init__(self, element, npc, grid, i, alpha, temperature):
        data = gdata.GlobalData()
        self.pmatrix = [0 for _ in range(4)]
        nodes = []
        sides = []
        for a in range(4):
            temp = grid.elements[i].id[a]
            nodes.append(grid.nodes[temp - 1])

        sides.append((numpy.sqrt((nodes[3].x - nodes[0].x) * (nodes[3].x - nodes[0].x) + (nodes[3].y - nodes[0].y) * (
                nodes[3].y - nodes[0].y))) * nodes[0].bc * nodes[3].bc)

        for b in range(3):
            sides.append(numpy.sqrt(
                ((nodes[b].x - nodes[b + 1].x) * (nodes[b].x - nodes[b + 1].x) + (nodes[b].y - nodes[b + 1].y) * (
                        nodes[b].y - nodes[b + 1].y)))*nodes[b].bc*nodes[b+1].bc)

        if (npc == 3):
            # to jest bardzo nieczytelne rozwiązanie
            for i in range(4):  # pętla dla ilości boków
                for j in range(4): #pętla dla funkcji kształtu
                    temp = 0
                    for k in range(npc):
                        temp += data.wagi3p[k] * diff.funkcjaKsztaltuN(element.pcb[i][k],j)
                    temp *= alpha * temperature * sides[i]/2
                    self.pmatrix[j] += temp

        else:
            for i in range(4):  # pętla dla ilości boków
                for j in range(4): #pętla dla funkcji kształtu
                    temp = 0
                    for k in range(npc):
                        temp += diff.funkcjaKsztaltuN(element.pcb[i][k],j)
                    temp *= alpha * temperature * sides[i]/2
                    self.pmatrix[j] += temp