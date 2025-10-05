from .base import Block

class EncoderBlock(Block):
    def __init__(self, label, x, y, width, height, indent=20, angle=0):
        super().__init__(label, x, y, width, height, angle)
        self.indent = indent

    def draw(self, dwg):
        fill_color = "#AED6F1"
        stroke_color = "black"
        stroke_width = 2
        if self.angle:
            cx = self.x + self.width/2
            cy = self.y + self.height/2
            grp = dwg.g(transform=f"rotate({self.angle}, {cx}, {cy})")
            points = [
                (self.x, self.y),
                (self.x + self.width, self.y),
                (self.x + self.width - self.indent, self.y + self.height),
                (self.x + self.indent, self.y + self.height)
            ]
            grp.add(dwg.polygon(points, stroke=stroke_color, fill=fill_color, stroke_width=stroke_width))
            self.draw_label(grp)
            dwg.add(grp)
        else:
            points = [
                (self.x, self.y),
                (self.x + self.width, self.y),
                (self.x + self.width - self.indent, self.y + self.height),
                (self.x + self.indent, self.y + self.height)
            ]
            dwg.add(dwg.polygon(points, stroke=stroke_color, fill=fill_color, stroke_width=stroke_width))
            self.draw_label(dwg)

