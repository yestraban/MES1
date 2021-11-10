import gdata as gd

def funkcja_1d(x):
    wynik = 5*x*x
    wynik += 3*x
    wynik += 6
    return wynik


def funkcja_2d(x,y):
    wynik = 5*x*x*y*y
    wynik += 3*x*y
    wynik += 6
    return wynik


def calkowanie_gaussa_1d(funkcja, p):
    suma = 0
    gdata = gd.GlobalData()
    if p == 2:
        for i in range(p):
            suma += funkcja(gdata.wezly2p[i])

    elif p == 3:
        for i in range(p):
            suma += funkcja(gdata.wezly3p[i]) * gdata.wagi3p[i]

    return suma


def calkowanie_gaussa_2d(funkcja, p):
    suma = 0
    gdata = gd.GlobalData()
    if p == 2:
        for i in range(p) :
            for j in range(p) :
                suma += funkcja(gdata.wezly2p[i], gdata.wezly2p[j])

    elif p == 3:
        for i in range(p) :
            for j in range(p) :
                suma += funkcja(gdata.wezly3p[i], gdata.wezly3p[j]) * gdata.wagi3p[i] * gdata.wagi3p[j]

    return suma