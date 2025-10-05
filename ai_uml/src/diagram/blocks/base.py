import svgwrite

class Block:
    def __init__(self, label, x, y, width, height, angle=0):
        """
        Base block class.
        
        Parameters:
          label: Text label to display.
          x, y: Top-left coordinates.
          width, height: Dimensions of the block.
          angle: Rotation angle in degrees.
        """
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.text_direction = "horizontal"  # default

    def set_text_direction(self, direction):
        """Set text orientation; options: 'horizontal', 'vertical_up', 'vertical_down'."""
        self.text_direction = direction

    def draw_label(self, container):
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2 + 5
        text = svgwrite.text.Text(
            self.label,
            insert=(cx, cy),
            text_anchor="middle",
            font_size="14px",
            font_family="Arial",
            fill="black"
        )
        if self.text_direction == "vertical_up":
            text['transform'] = f"rotate(-90, {cx}, {cy})"
        elif self.text_direction == "vertical_down":
            text['transform'] = f"rotate(90, {cx}, {cy})"
        container.add(text)

    def rotate(self, angle):
        self.angle = angle

    def draw(self, dwg):
        raise NotImplementedError("Subclasses must implement draw()")

