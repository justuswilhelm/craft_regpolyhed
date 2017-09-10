#!/usr/bin/env python
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import numpy as np

EDGE_LENGTH = 3.5 * cm
WITH_MERGIN = True
MARGIN_SIZE = .6 * cm
MARGIN_ANG = np.pi * 36 / 180


def get_rotmat(a):
    return np.array([[np.cos(a), -np.sin(a)],
                     [np.sin(a), np.cos(a)]])

ROTMAT = get_rotmat(np.pi * 72 / 180)


def polygon(v1, v2, n=5):
    v = v2 - v1
    vs = v2.copy()
    v3 = v2.copy()
    for i in range(min(n, 3)):
        v = np.dot(ROTMAT, v)
        v3 += v
        vs = np.c_[vs, v3]
    if n >= 4:
        vs = np.c_[vs, v1]
    if n == 5:
        vs = np.c_[vs, v2]
    return vs.T


def margin(v1, v2):
    vv = v2 - v1
    vv = vv / np.sqrt((vv**2).sum())
    edgelen = MARGIN_SIZE / np.sin(MARGIN_ANG)
    v3 = v1 + edgelen * np.dot(get_rotmat(MARGIN_ANG), vv)
    v4 = v2 - edgelen * np.dot(get_rotmat(-MARGIN_ANG), vv)
    return np.c_[v2, v4, v3, v1].T


def draw(pdf, vs):
    for i in range(len(vs) - 1):
        pdf.line(vs[i, 0], vs[i, 1], vs[i + 1, 0], vs[i + 1, 1])


def main():
    # Paper size (A4)
    width = 21.0 * cm
    height = 29.7 * cm

    pdf = canvas.Canvas("./dodecahedron.pdf")
    pdf.saveState()

    pdf.setAuthor("Kimikazu Kato")
    pdf.setTitle("Regular Dodecahedron")

    pdf.setPageSize((width, height))

    # Lower half
    v1 = np.array([width / 2 + EDGE_LENGTH / 2, height / 2])
    v2 = np.array([width / 2 - EDGE_LENGTH / 2, height / 2])
    vs = polygon(v1, v2)
    draw(pdf, vs)
    if WITH_MERGIN:
        for j in range(2, 4):
            mvs = margin(vs[j + 1, :], vs[j, :])
            draw(pdf, mvs)

    vs2 = polygon(vs[2, :], vs[1, :], 4)
    draw(pdf, vs2)
    for i in range(4):
        vs3 = polygon(vs2[i + 1, :], vs2[i, :], 4)
        draw(pdf, vs3)
        if WITH_MERGIN:
            for j in range(3):
                mvs = margin(vs3[j + 1, :], vs3[j, :])
                draw(pdf, mvs)

    # Upper half
    vs = polygon(v2, v1)
    draw(pdf, vs)
    if WITH_MERGIN:
        mvs = margin(vs[1, :], vs[0, :])
        draw(pdf, mvs)
        mvs = margin(vs[3, :], vs[2, :])
        draw(pdf, mvs)

    vs2 = polygon(vs[2, :], vs[1, :], 4)
    draw(pdf, vs2)
    for i in range(4):
        vs3 = polygon(vs2[i + 1, :], vs2[i, :], 4)
        draw(pdf, vs3)
        if WITH_MERGIN:
            if i != 3:
                mvs = margin(vs3[4, :], vs3[3, :])
                draw(pdf, mvs)

    pdf.saveState()
    pdf.save()


if __name__ == '__main__':
    main()
