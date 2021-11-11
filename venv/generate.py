import gridElements

def generate_nodes(data):
    nodes = []
    for i in range(data.nB):
        for j in range(data.nH):
            nodes.append(gridElements.Node((i/(data.nB-1))*data.b, (j/(data.nH-1))*data.h))
    return nodes


def generate_elements(data):
    elements = []
    n = 1
    for i in range(data.nB-1):
        for j in range(data.nH-1):
            if ((i==0) or (i==data.nB-1)) or ((j==0) or (j==data.nB-1)):
                elements.append(gridElements.Element(n+j, n+data.nH+j, n+data.nH+1+j, n+1+j, 1))
            else:
                elements.append(gridElements.Element(n+j, n+data.nH+j, n+data.nH+1+j, n+1+j, 0))
        n += data.nH
    return elements