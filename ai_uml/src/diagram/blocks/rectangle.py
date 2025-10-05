from .base import Block

class RoundRectBlock(Block):
    def draw(self, dwg):
        fill_color = "#AED6F1"
        stroke_color = "black"
        stroke_width = 2
        if self.angle:
            cx = self.x + self.width/2
            cy = self.y + self.height/2
            grp = dwg.g(transform=f"rotate({self.angle}, {cx}, {cy})")
            grp.add(dwg.rect(
                insert=(self.x, self.y),
                size=(self.width, self.height),
                rx=10, ry=10,
                stroke=stroke_color,
                fill=fill_color,
                stroke_width=stroke_width
            ))
            self.draw_label(grp)
            dwg.add(grp)
        else:
            dwg.add(dwg.rect(
                insert=(self.x, self.y),
                size=(self.width, self.height),
                rx=10, ry=10,
                stroke=stroke_color,
                fill=fill_color,
                stroke_width=stroke_width
            ))
            self.draw_label(dwg)