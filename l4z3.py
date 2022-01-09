"""
a11x + a12y + a13z = b1
a21x + a22y + a23z = b2
a31x + a32y + a33z = b3

a13z = b1 - a11x - a12y
z = (b1 - a11x - a12y) / a13
"""

"""
2x + y - z = 3
-3x + 2y + 5z = 5
x - 2y + 2z = 1
"""

import matplotlib.pyplot as mpl
import numpy as np
import pandas as pd
import matplotlib.lines as mlines


def parse_coef(path):
    coef = pd.read_csv(path, sep=",", header=None)
    return coef.values


def create_axis(c, solx, soly):
    X = np.linspace(solx - 2, solx + 2, 20)
    Y = np.linspace(soly - 2, soly + 2, 20)
    x, y = np.meshgrid(X, Y)
    zs = []
    for i in range(3):
        zs.append((c[i][3] - c[i][0] * x - c[i][1] * y) / c[i][2])
    z1, z2, z3 = zs
    return x, y, z1, z2, z3


def create_labels(coef):
    labels = list()
    for i in range(3):
        a_s = lambda a: f"-{abs(a[i][0])}" if a[i][0] < 0 else ("" if a[i][0] == 0 else f"{abs(a[i][0])}")
        b_s = lambda a: f" - {abs(a[i][1])}" if a[i][1] < 0 else (" " if a[i][1] == 0 else f" + {abs(a[i][1])}")
        c_s = lambda a: f" - {abs(a[i][2])}" if a[i][2] < 0 else (" " if a[i][2] == 0 else f" + {abs(a[i][2])}")
        labels.append(f"{a_s(coef)}x{b_s(coef)}y{c_s(coef)}z = {coef[i][3]}")

    return labels


def solve(coef):
    cx, cy, cz, c = coef.T
    b = np.array(c)
    a = np.array([[cx[0], cy[0], cz[0]], [cx[1], cy[1], cz[1]], [cx[2], cy[2], cz[2]]])
    return np.linalg.solve(a, b)


def create_plot(axis, pt, l, solvable):
    fig = mpl.figure()
    mpl3d = fig.add_subplot(111, projection="3d")

    if solvable is True:
        mpl3d.scatter(pt[0], pt[1], pt[2], color="black")
        mpl3d.text(pt[0] - 1.6, pt[1] - 1.6, pt[2] + 0.2, f"({round(pt[0], 2)}, {round(pt[1],2)}, {round(pt[2], 2)})")
    else:
        mpl3d.text(pt[0] + 5.7, pt[1] - 7, pt[2] + 2, "Układ nie ma jednoznacznego\n rozwiązania", color="red")

    surf1 = mpl3d.plot_surface(axis[0], axis[1], axis[2], alpha=0.45, label=l[0])
    surf2 = mpl3d.plot_surface(axis[0], axis[1], axis[3], alpha=0.45, label=l[1])
    surf3 = mpl3d.plot_surface(axis[0], axis[1], axis[4], alpha=0.45, label=l[2])

    #tworzenie legendy z płaszczyzn, ręczne przypisanie brakujących atrybutów
    surf1._facecolors2d = surf1._facecolor3d
    surf2._facecolors2d = surf2._facecolor3d
    surf3._facecolors2d = surf3._facecolor3d
    surf1._edgecolors2d = surf1._edgecolor3d
    surf2._edgecolors2d = surf2._edgecolor3d
    surf3._edgecolors2d = surf3._edgecolor3d

    mpl3d.legend(loc="upper center", bbox_to_anchor=[0.5, 1.15])
    mpl.show()


c = parse_coef("wspolczynniki.csv")
try:
    p = solve(c)
    solvable = True
except np.linalg.LinAlgError:
    p = (0, 0, 0)
    solvable = False
axis = create_axis(c, p[0], p[1])
create_plot(axis, p, create_labels(c), solvable)
