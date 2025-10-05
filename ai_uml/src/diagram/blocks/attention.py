from diagram.blocks.rectangle import RoundRectBlock


class AttentionBlock(RoundRectBlock):
    """Multi-Head Attention block"""
    def draw(self, dwg):
        dwg.add(dwg.rect(insert=(self.x, self.y), size=(self.width, self.height),
                         rx=5, ry=5, stroke="black", fill="#D1C4E9", stroke_width=2))
        self.draw_label(dwg)