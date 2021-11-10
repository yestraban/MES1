import gdata

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Element:
    def __init__(self, id1, id2, id3, id4):
        self.id = [id1, id2, id3, id4]
    H = [[0 for _ in range(4)] for _ in range(4)]
    bc = 0


class Element4w:
    def __init__(self, npc):

        self.dNdZ = [[0 for _ in range(npc*npc)]  for _ in range(4)]
        self.dNdE = [[0 for _ in range(npc*npc)]  for _ in range(4)]
        self.npc = npc
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

        
        del data


class Grid:
    def __init__(self, nodes, elements):
        self.nodes = nodes
        self.elements = elements
