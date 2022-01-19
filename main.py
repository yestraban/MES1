# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import calculateT
import fileLoad
import generate
import gdata
import gridElements
import plot

if __name__ == '__main__':

    #grid, simTime, dt, initT = fileLoad.loadFile("testcase2.txt")

    nodes = generate.generate_nodes(gdata.GlobalData)
    elements = generate.generate_elements(gdata.GlobalData)

    npc = 3
    elementsk, elementsalpha, elementstemp, elementsro, elementscp, t0 = generate.generateConstants(elements, nodes)

    # element = gridElements.Element4w(npc)
    # elementsk = [25 for _ in range(len(elements))]          #generowanie danych do elementu, tu można zmienić w razie potrzeby
    # elementsalpha = [300 for _ in range(len(elements))]
    # elementstemp = [1200 for _ in range(len(elements))]
    # elementsro = [7800 for _ in range(len(elements))]
    # elementscp = [700 for _ in range(len(elements))]
    data = gdata.GlobalData()
    #
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
    tt = 0
    dt = 1
    tend = 100
    while(tt <= tend):
        tt += dt
        t0 = generate.fixTemp(t0, elements, nodes)
        temp = calculateT.temperatureStep(grid, t0, dt)
        min = 100000
        max = 0
        for i in range(len(grid.nodes)):
            #print(temp[i])
            if(temp[i]<min):
                min = temp[i]
            if (temp[i] > max):
                max = temp[i]
        print("czas ",tt,": min: ", min, "  max: ", max)
        t0 = temp
    print()
    t0 = generate.fixTemp(t0, elements, nodes)
    plot.plot_all(grid, t0)
