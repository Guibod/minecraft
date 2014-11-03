from math import radians, cos, sin

__author__ = 'gboddaert'


class Block(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Block<%d,%d,%d>' % (self.x, self.y, self.z)

    def __eq__(self, other):
        if self.x != other.x:
            return False

        if self.y != other.y:
            return False

        if self.z != other.z:
            return False

        return True


class Rectangle(object):
    def __init__(self, a, b):
        """

        :type a: Block
        :type b: Block
        """
        self.a = a
        self.b = b

    def width(self):
        return abs(self.a.x - self.b.x) + 1

    def height(self):
        return abs(self.a.y - self.b.y) + 1

    def depth(self):
        return abs(self.a.z - self.b.z) + 1

    def size(self):
        return self.width() * self.height() * self.depth()

    def __repr__(self):
        return 'Rectangle[%s,%s]' % (self.a, self.b)

    def __eq__(self, other):
        if self.a == other.a and self.b == other.b:
            return True

        if self.a == other.b and self.b == other.a:
            return True

        return False

    def is_contiguous(self, other):
        self.a.x == self.b.


class MinecraftCircle(object):
    def __init__(self, center, radius):
        """
        :type center: Block
        """
        self.c = center
        self.r = radius

    def points(self):
        points = []
        for angle in range(0, 360):
            rad = radians(angle)
            x = int(round(cos(rad) * self.r)) + self.c.x
            z = int(round(sin(rad) * self.r)) + self.c.z
            points.append((x, z))
        return sorted(set(points))


class MinecraftCylinder(MinecraftCircle):

    def __init__(self, center, radius, height):
        """
        :type center: Block
        """
        super(MinecraftCylinder, self).__init__(center, radius)
        self.h = height

    def rectangles(self):
        rectangles = []
        for p in self.points():
            x, z = p
            b = Block(x, self.c.y, z)
            t = Block(x, self.c.y + self.h, z)

            rectangles.append(Rectangle(b, t))
        return rectangles


def fill(rectangles, tile_name, data_value = '0', old_block_handling='replace', data_tag=''):
    """

    :type rectangles: list of Rectangle
    """
    commands = []
    for rectangle in rectangles:
        commands.append('/fill {x1} {y1} {z1} {x2} {y2} {z2} {tile_name} {data_value} {old_block_handling} {data_tag}'.format(
            x1=rectangle.a.x,
            y1=rectangle.a.y,
            z1=rectangle.a.z,
            x2=rectangle.b.x,
            y2=rectangle.b.y,
            z2=rectangle.b.z,
            tile_name=tile_name,
            data_value=data_value,
            old_block_handling=old_block_handling,
            data_tag=data_tag
        ))
    return commands

cylinder = MinecraftCylinder(Block(0, 0, 0), 10, 10)

for rect in cylinder.rectangles():
    print rect
    print "width: %d" % rect.width()
    print "height: %d" % rect.height()
    print "depth: %d" % rect.depth()
    print "size: %d" % rect.size()

for cmd in fill(cylinder.rectangles(), 'minecraft:air'):
    print cmd