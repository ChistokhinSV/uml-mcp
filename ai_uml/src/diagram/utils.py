import math
import svgwrite

def get_center(block):
    """Return the center of the block (based on its unrotated bounding box)."""
    return (block.x + block.width / 2, block.y + block.height / 2)

def get_right_connection(block):
    """
    Returns the global coordinates of the right connection point.
    If the block is rotated (about its center), this is computed as:
      center + (width/2) rotated by block.angle.
    """
    cx, cy = get_center(block)
    if block.angle:
        rad = math.radians(block.angle)
        return (cx + (block.width / 2) * math.cos(rad),
                cy + (block.width / 2) * math.sin(rad))
    else:
        return (block.x + block.width, block.y + block.height / 2)

def get_left_connection(block):
    """
    Returns the global coordinates of the left connection point.
    If the block is rotated (about its center), this is computed as:
      center - (width/2) rotated by block.angle.
    """
    cx, cy = get_center(block)
    if block.angle:
        rad = math.radians(block.angle)
        return (cx - (block.width / 2) * math.cos(rad),
                cy - (block.width / 2) * math.sin(rad))
    else:
        return (block.x, block.y + block.height / 2)

def draw_connection_line(dwg, start, end, transform=""):
    """
    Draws a connection line from start to end.
    Optionally wraps the line in a group with the given SVG transform.
    """
    line = dwg.line(start=start, end=end, stroke="black", stroke_width=2)
    if transform:
        grp = dwg.g(transform=transform)
        grp.add(line)
        dwg.add(grp)
    else:
        dwg.add(line)
