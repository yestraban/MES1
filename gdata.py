import numpy


class GlobalData:
    h = 0.0275
    b = 0.027
    nH = 56
    nB = 55
    dT = 0.1
    wagi3p = [5 / 9, 8 / 9, 5 / 9]
    wezly2p = [-1 / numpy.sqrt(3), 1 / numpy.sqrt(3)]
    wezly3p = [-numpy.sqrt(3 / 5), 0, numpy.sqrt(3 / 5)]


def warunekAluminium(x, y):
    if (y) >= 0.027:
        return True
    else:
        return False


def warunekMiedz(x, y):
    if (y <= 0.001) or ((y >= 0.026) and (y <= 0.027)):
        return True
    elif ((x <= 0.001) or (x >= 0.026)) and (y <= 0.027):
        return True
    else:
        return False


def warunekGlikol(x, y):
    if ((y >= 0.001) and (y <= 0.026)) and ((x >= 0.001) and (x <= 0.026)):
        return True
    else:
        return False
