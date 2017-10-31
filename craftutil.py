from argparse import ArgumentParser

import numpy as np
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


EDGE_LENGTH = 5 * cm
MARGIN_ANG = np.pi * 28 / 180
MARGIN_SIZE = 1 * cm


def get_parser():
    parser = ArgumentParser()
    parser.add_argument(
        'destination',
        type=str,
    )
    parser.add_argument(
        '--with-margin',
        action='store_true',
    )
    parser.add_argument(
        '--margin-angle',
        type=lambda angle: np.pi * angle / 180,
        default=MARGIN_ANG,
        help='Angle of margin',
    )
    parser.add_argument(
        '--margin-size',
        type=lambda size: size * cm,
        default=MARGIN_SIZE,
        help='Size of margin',
    )
    parser.add_argument(
        '--edge-length',
        type=lambda length: length * cm,
        default=EDGE_LENGTH,
    )
    parser.add_argument(
        '--paper-size',
        type=str,
        default='a4',
    )
    return parser


def paper_size(name):
    """Return width and height for paper format."""
    if name == 'a4':
        width = 21.0 * cm
        height = 29.7 * cm
    else:
        raise ValueError("Unknown paper size {}".format(name))
    return width, height


def pdf_context(width, height, path, author, title):
    """Return pdf context."""
    pdf = canvas.Canvas(path)
    pdf.saveState()
    pdf.setAuthor(author)
    pdf.setTitle(title)
    pdf.setPageSize((width, height))
    return pdf


def pdf_close(pdf):
    """Close and save pdf document."""
    pdf.saveState()
    pdf.save()
