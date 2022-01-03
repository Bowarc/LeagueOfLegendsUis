import math


def rotate_point(origin, point, angle):
    angle = math.radians(angle)
    ox, oy = origin[0], origin[1]
    px, py = point[0], point[1]

    return (
        ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy),
        oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy),
    )
