import svgwrite
from ..utils.geometry import get_right_connection, get_left_connection, draw_connection_line

class VaeDiagram:
    def __init__(self, filename='vae_diagram.svg'):
        self.filename = filename
        self.gap = 50
        self.start_x = 50
        self.start_y = 125
        self.block_width = 100
        self.block_height = 50
        self.blocks = []  # ordered list of blocks

    def setup_blocks(self, blocks):
        """Setup blocks from a list (e.g., loaded from JSON)."""
        self.blocks = blocks

    def draw(self):
        total_width = self.start_x + (self.block_width + self.gap) * len(self.blocks)
        dwg = svgwrite.Drawing(self.filename, profile='full', size=(f'{total_width}px', '300px'))
        for block in self.blocks:
            block.draw(dwg)
        for i in range(len(self.blocks) - 1):
            start = get_right_connection(self.blocks[i])
            end = get_left_connection(self.blocks[i+1])
            draw_connection_line(dwg, start, end)
        dwg.save()
        print(f"SVG diagram saved as {self.filename}")
