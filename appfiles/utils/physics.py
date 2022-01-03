import math

from PyQt5.QtCore import QPoint


def rotate_point(origin, point, angle):
    angle = math.radians(angle)
    ox, oy = origin[0], origin[1]
    px, py = point.x(), point.y()

    return QPoint(
        ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy),
        oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy),
    )


def process_diamond(shape, pos):
    def translate_point(point, pos):
        return QPoint(pos.x() + point.x(), pos.y() + point.y())
    new_diamond = [
    ]

    for point in shape:
        new_diamond.append(translate_point(point, pos))
    new_diamond.append(translate_point(shape[0], pos))

    return new_diamond
