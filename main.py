import matplotlib.pyplot as plt
from math import sqrt


def citire_date(file):
    v = []
    with open(file, "r") as fin:
        for line in fin:
            aux = [float(a) for a in line.split()]
            x, y = aux[0], aux[1]
            v.append([x, y])
    return v


def delta(p, q, r):
    """
    return: valoare negativa daca r este la dreapta, pozitiva daca este la stanga si 0 daca este pe dreapta
    """
    return (q[0] * r[1] + p[0] * q[1] + r[0] * p[1]) - (q[0] * p[1] + r[0] * q[1] + r[1] * p[0])


def test_orientare(p, q, r):
    """
    verifica daca r este la stanga sau la dreapta dreptei pq
    """
    poz = delta(p, q, r)
    if poz < 0:
        return "dr"
    elif poz > 0:
        return "st"
    else:
        return "pe"


def distanta(p1, p2):
    return sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def arie(p0, p1, p2):
    a = distanta(p0, p1)
    b = distanta(p0, p2)
    c = distanta(p1, p2)

    s = (a + b + c) / 2
    if (s * (s - a) * (s - b) * (s - c)) < 1e-3:
        return 0
    return round(sqrt(s * (s - a) * (s - b) * (s - c)), 2)


def d_in_interriorul_abc(a, b, c, d):
    a1, a2, a3 = arie(a, b, d), arie(a, c, d), arie(b, c, d)
    if arie(a, b, c) == a1 + a2 + a3:
        return True
    return False


def unghi_principal(puncte, i):
    a = puncte[(i - 1) % len(puncte)]
    b = puncte[i]
    c = puncte[(i + 1) % len(puncte)]
    for p_index in range(len(puncte)):
        if p_index != (i - 1) % len(puncte) and p_index != i and p_index != (i + 1) % len(puncte):
            if d_in_interriorul_abc(a, b, c, puncte[p_index]):
                return 0
    return 1


def unghi_convex(puncte, i, dir):
    a = puncte[(i - 1) % len(puncte)]
    b = puncte[i]
    c = puncte[(i + 1) % len(puncte)]
    if (test_orientare(a, b, c) == dir or test_orientare(a, b, c) == "pe"):
        return 1
    return 0


def toate(puncte):
    minim = 10000
    n = len(puncte);
    convex = [0] * n
    principal = [0] * n

    for p_index in range(n):
        if puncte[p_index][0] < minim:
            minim = puncte[p_index][0]
            start = p_index

    while (puncte[start % n][1] == puncte[(start - 1) % n][1]):
        start = (start - 1) % n;

    p_index = start
    a = puncte[(p_index - 1) % n]
    b = puncte[p_index % n]
    c = puncte[(p_index + 1) % n]
    convex[start] = 1
    principal[start] = unghi_principal(puncte, start)
    p_index = (start + 1) % n
    dir = test_orientare(a, b, c)

    while (p_index % len(puncte)) != start:
        a = puncte[(p_index - 1) % n]
        b = puncte[p_index % n]
        c = puncte[(p_index + 1) % n]
        principal[p_index % n] = unghi_principal(puncte, p_index % n)
        convex[p_index % n] = unghi_convex(puncte, p_index % n, dir)
        p_index += 1

    return list(zip(principal, convex))


def getmatrixminor(m, i, j):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def getmatrixdeternminant(m):
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * getmatrixdeternminant(getmatrixminor(m, 0, c))
    return determinant


def segmentele_se_intersecteaza(A1, A2, A3, A4):
    line1 = [0, 0, 0]
    line2 = [0, 0, 0]

    if A1[0] == A2[0]:
        slope = "inf"
    else:
        slope = (A2[1] - A1[1]) / (A2[0] - A1[0])
    if slope == "inf":
        line1 = [1, 0, -A1[0]]
    elif slope == 0:
        line1 = [0, 1, -A1[1]]
    else:
        line1 = [1, (-1) / slope, 1 / slope * A1[1] - A1[0]]

    if A3[0] == A4[0]:
        slope = "inf"
    else:
        slope = (A4[1] - A3[1]) / (A4[0] - A3[0])
    if slope == "inf":
        line2 = [1, 0, -A3[0]]
    elif slope == 0:
        line2 = [0, 1, -A4[1]]
    else:
        line2 = [1, (-1) / slope, 1 / slope * A3[1] - A3[0]]

    #     print("ecuatiile liniilor:")
    #     print(line1, line2)

    delta = getmatrixdeternminant([[line1[0], line1[1]], [line2[0], line2[1]]])
    #     print("delta:", delta)

    if delta != 0:
        x = getmatrixdeternminant([[-line1[2], line1[1]], [-line2[2], line2[1]]]) / delta
        y = getmatrixdeternminant([[line1[0], -line1[2]], [line2[0], -line2[2]]]) / delta
        if (A1[0] - x) * (A2[0] - x) <= 0 and (A3[0] - x) * (A4[0] - x) <= 0 and (A1[1] - y) * (A2[1] - y) <= 0 and (
                A3[1] - y) * (A4[1] - y) <= 0:
            #             print("Segmentele se intersecteaza in:")
            #             print(x, y)
            return True
        else:
            #             print("Punctul e in afara segmentelor (multimea vida)")
            return False

    det1 = getmatrixdeternminant([[line1[0], line1[2]], [line2[0], line2[2]]])
    det2 = getmatrixdeternminant([[line1[1], line1[2]], [line2[1], line2[2]]])

    if det1 != 0 or det2 != 0:
        #         print("Liniile sunt paralele si nu se intersecteaza (multimea vida)")
        return False

    # sunt coliniare
    v = [[A1, 1], [A2, 2], [A3, 3], [A4, 4]]
    if A1[0] == A2[0]:
        v.sort(key=lambda a: a[0][1])
    else:
        v.sort(key=lambda a: a[0][0])

    if v[1][0][0] == v[2][0][0] and v[1][0][1] == v[2][0][1]:
        #         print(f"Segmentele se intersecteaza in:")
        #         print(v[1][0][0], v[2][0][0])
        return True
    if {v[0][1], v[1][1]} == {1, 2} or {v[0][1], v[1][1]} == {3, 4}:  # de modificat
        #         print("Punctele sunt coliniare si nu se intersecteaza (multimea vida)")
        return False


#     print(f"Intersectia este segmentul: [A{v[1][1]} A{v[2][1]}]")

def exista_autointersectii(points):
    #     polygon = points
    #     polygon.append(polygon[0])
    n = len(points)
    for i in range(n - 3):
        if i == 0:
            dontTakeLast = 1
        else:
            dontTakeLast = 0
        a = points[i]
        b = points[i + 1]
        for j in range(i + 2, n - dontTakeLast):
            c = points[j]
            d = points[(j + 1) % n]
            if segmentele_se_intersecteaza(a, b, c, d):
                return True
    return False


def show_polygon(points, properties):
    # setup
    plt.figure(figsize=(15, 9))

    # plot the polygon
    polygon = points
    polygon.append(polygon[0])
    xs, ys = zip(*polygon)
    plt.plot(xs, ys, color='black', ls='-')
    plt.fill(xs, ys, '#fff8e0')

    princ = 0

    # plot the points with the curresponding colors
    for point, prop in zip(points, properties):
        if prop[0] == 1:
            ex_principal, = plt.plot(point[0], point[1], color='red', marker='o', ls='', ms=13, mfc='white', mew='3')
            princ = 1
        if prop[1] == 1:
            ex_convex, = plt.plot(point[0], point[1], color='blue', marker='o', ls='',
                                  ms=8)  # save the encounter for legend

    if princ == 0:
        stanga = min(points, key=lambda a: a[0])
        ex_principal, = plt.plot(stanga[0] - 5, stanga[1], color='red', marker='o', ls='', ms=13, mfc='white', mew='3')
    # attach legend and show the figure
    plt.legend((ex_principal, ex_convex), ('principal', 'convex'))
    plt.show()


points = citire_date("date.in")
print(points)
if len(points) < 3:
    print("Figura nu este poligon")
else:
    c = toate(points)
    print(c)
    if (exista_autointersectii(points)):
        print("Atentie! Exista autointersectii.")
    show_polygon(points, c)


# 0 0
# 1 1
# 2 0
# 1 3

# 0 0
# 3 -2
# 5 -8
# 8 -3
# 2.5 -5
# 6 -1
# 6.5 -3
# 9 3
# 3 3
# 0 4
# 0 2

