from .rectangle import RoundRectBlock
from .base import Block

class MLPBlock(RoundRectBlock):
    def draw(self, dwg):
        fill_color = "#C3E6CB"  # Light green fill
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
            super().draw(dwg)

class FFNBlock(RoundRectBlock):
    def draw(self, dwg):
        fill_color = "#FFF3CD"  # Light yellow fill
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
            super().draw(dwg)

class TransformerAddBlock(RoundRectBlock):
    def draw(self, dwg):
        fill_color = "#D1C4E9"  # Light purple fill
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
            super().draw(dwg)
