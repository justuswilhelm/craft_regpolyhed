#!/usr/bin/env python
from functools import partial
import numpy as np

from craftmath import margin, regular_polygon, rotation_matrix
from craftdraw import polyline
import craftutil


def range_circle(seq):
    length = len(seq)
    for i in range(length):
        if i == 0:
            yield seq[-1], seq[0]
        else:
            yield seq[i - 1], seq[i]


def main(args):
    mrg = partial(margin, args.margin_angle, args.margin_size)
    width, height = craftutil.paper_size(args.paper_size)
    pdf = craftutil.pdf_context(
        width, height, 'cube.pdf',
        author='Justus',
        title='cube',
    )
    factor = 1.7
    v = np.array([args.edge_length, args.edge_length]) / factor * 2
    v1 = v + np.array([-args.edge_length, args.edge_length]) / factor
    v2 = v - np.array([args.edge_length, args.edge_length]) / factor
    box_edge_length = args.edge_length / factor * 2

    middle = width / 2 - box_edge_length

    for i in range(4):
        offset = [middle, box_edge_length * i]
        box = regular_polygon(4, v1, v2, draw_extra=i == 3) + offset
        polyline(pdf, box)
        if i == 0:
            mapping = [
                ((1, 2), np.pi * 1),
                ((0, 1), np.pi * 3/2),
                ((1, 0), np.pi * 4/2),
            ]
            for i, rotation in mapping:
                margin_offset = offset + v * i
                shape = (
                    mrg(v1, v2).dot(rotation_matrix(rotation).T) +
                    margin_offset
                )
                polyline(pdf, shape)

    for i in range(-1, 2):
        if i == -1:
            mapping = [
                ((0, 1), np.pi * 3/2),
                ((2, 1), np.pi * 1/2),
            ]
        elif i == 1:
            mapping = [
                ((0, 1), np.pi * 3/2),
                ((2, 1), np.pi * 1/2),
            ]
        else:
            continue
        offset = [middle + box_edge_length * i, box_edge_length * 2]
        box = regular_polygon(4, v1, v2, draw_extra=True) + offset
        for i, rotation in mapping:
            shape = (
                mrg(v1, v2).dot(rotation_matrix(rotation).T) + offset + v * i
            )
            polyline(pdf, shape)
        polyline(pdf, box)
    craftutil.pdf_close(pdf)


if __name__ == '__main__':
    parser = craftutil.get_parser()
    main(parser.parse_args())
