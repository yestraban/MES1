# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy
import gridElements
import diff
import hmatrix
import gdata
import generate
import pmatrix
import cmatrix
import calculateT


if __name__ == '__main__':
    nodes = generate.generate_nodes(gdata.GlobalData)
  #  for i in range(len(nodes)):
   #     print(nodes[i].x, " ", nodes[i].y)

    elements = generate.generate_elements(gdata.GlobalData)
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


    # tabx = [0, 0.025, 0.025, 0]
    # taby = [0, 0, 0.025, 0.025]
    # nds = []
    # for i in range(4):
    #     nds.append(gridElements.Node(tabx[i], taby[i]))
    npc = 3

    element = gridElements.Element4w(npc)
    elementsk = [25 for _ in range(len(elements))]          #generowanie danych do elementu, tu można zmienić w razie potrzeby
    elementsalpha = [300 for _ in range(len(elements))]
    elementstemp = [1200 for _ in range(len(elements))]
    elementsro = [7800 for _ in range(len(elements))]
    elementscp = [700 for _ in range(len(elements))]
    data = gdata.GlobalData()

    grid = gridElements.Grid(nodes, elements, npc, elementsk, elementsalpha, elementstemp, elementsro, elementscp)


    # jak = Jakobian(nds, element, 0)
    # print(jak.dXdZ, " ", jak.dYdZ)
    # print(jak.dXdE, " ", jak.dYdE)
    # odwJak = JakobianOdw(jak);
    # print()
    # print(odwJak.dYdE, " ", odwJak.mdYdZ)
    # print(odwJak.mdXdE, " ", odwJak.dXdZ)


    print("==================================")
    print()
    #print("Macierz C:")

    # for i in range(len(grid.elements)):
    #     for j in range(4):
    #         #print(grid.elements[i].H.H[j])  #macierz H
    #         print(grid.elements[i].Hbc.Hbc[j])   #macierz Hbc
    #     print("++++++++++++++++++++++++++++++++++")

    # for i in range(len(grid.nodes)):
    #     print(grid.Haggr[i])
    t0  = [100 for _ in range(len(nodes))]
    temp = calculateT.temperatureStep(grid, t0)
    min =100000
    max = 0
    for i in range(len(grid.nodes)):
        print(temp[i])
        if(temp[i]<min):
            min = temp[i]
        if (temp[i] > max):
            max = temp[i]

    print("min: ", min, "  max: ", max)
    print("iteracja 1:")

    t0 = temp
    temp = calculateT.temperatureStep(grid, t0)
    min = 100000
    max = 0
    for i in range(len(grid.nodes)):
        print(temp[i])
        if (temp[i] < min):
            min = temp[i]
        if (temp[i] > max):
            max = temp[i]

    print("min: ", min, "  max: ", max)