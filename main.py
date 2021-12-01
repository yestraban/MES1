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
    grid = gridElements.Grid(nodes, elements)

    # jak = Jakobian(nds, element, 0)
    # print(jak.dXdZ, " ", jak.dYdZ)
    # print(jak.dXdE, " ", jak.dYdE)
    # odwJak = JakobianOdw(jak);
    # print()
    # print(odwJak.dYdE, " ", odwJak.mdYdZ)
    # print(odwJak.mdXdE, " ", odwJak.dXdZ)

    for i in range(len(grid.elements)):
        for j in range(element.npc*element.npc):
            jak = hmatrix.Jakobian(grid, i, element, j)
            odwJak = hmatrix.JakobianOdw(jak)
            h = hmatrix.MacierzSztywnosciH(odwJak, npc, element)
            c = cmatrix.MacierzC(element, npc, jak)
            grid.elements[i].H = h
            grid.elements[i].Cmatrix = c
            hbc = hmatrix.Hbc(element, npc, grid, i)
            grid.elements[i].Hbc = hbc
            pm = pmatrix.Pmatrix(element, npc, grid, i)
            grid.elements[i].Pmatrix = pm

    print("==================================")
    print()
    print("Macierz C:")

    # for i in range(len(grid.elements)):
    #     for j in range(4):
    #         #print(grid.elements[i].H.H[j])  #macierz H
    #         print(grid.elements[i].Hbc.Hbc[j])   #macierz Hbc
    #     print("++++++++++++++++++++++++++++++++++")
    temp = generate.hAgregate(grid)
    temp2 = generate.pAgregate(grid)
    temp3 = generate.cAgregate(grid)
    for i in range(len(grid.nodes)):
            #print(temp[i])
            #print(temp2[i])
            print(temp3[i])