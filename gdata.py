import numpy


class GlobalData:
    h = 27.5
    b = 27
    nH = 55
    nB = 54
    dT = 0.1
    wagi3p = [5 / 9, 8 / 9, 5 / 9]
    wezly2p = [-1 / numpy.sqrt(3), 1 / numpy.sqrt(3)]
    wezly3p = [-numpy.sqrt(3 / 5), 0, numpy.sqrt(3 / 5)]


def warunekAluminium(x, y):
    if (y) >= 27.0:
        return True
    else:
        return False


def warunekMiedz(x, y):
    if (y <= 1.0) or ((y >= 26.0) and (y <= 27.0)):
        return True
    elif ((x <= 1.0) or (x >= 26.0)) and (y <= 27.0):
        return True
    else:
        return False


def warunekGlikol(x, y):
    if ((y >= 1.0) and (y <= 26.0)) and ((x >= 1.0) and (x <= 26.0)):
        return True
    else:
        return False
