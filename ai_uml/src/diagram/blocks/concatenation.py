from .base import Block

class ConcatenationBlock(Block):
    """Concatenation block (circle with a cross)"""
    def draw(self, dwg):
        dwg.add(dwg.circle(center=(self.x, self.y), r=self.width / 2, stroke="black", fill="none", stroke_width=2))
        dwg.add(dwg.line(start=(self.x - 10, self.y), end=(self.x + 10, self.y), stroke="black"))
        dwg.add(dwg.line(start=(self.x, self.y - 10), end=(self.x, self.y + 10), stroke="black"))
        self.draw_label(dwg)