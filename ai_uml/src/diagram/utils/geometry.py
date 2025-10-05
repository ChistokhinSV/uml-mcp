def get_center(block):
    return (block.x + block.width / 2, block.y + block.height / 2)

def get_right_connection(block):
    cx, cy = get_center(block)
    if block.angle:
        import math
        rad = math.radians(block.angle)
        return (cx + (block.width/2) * math.cos(rad),
                cy + (block.width/2) * math.sin(rad))
    else:
        return (block.x + block.width, block.y + block.height/2)

def get_left_connection(block):
    cx, cy = get_center(block)
    if block.angle:
        import math
        rad = math.radians(block.angle)
        return (cx - (block.width/2) * math.cos(rad),
                cy - (block.width/2) * math.sin(rad))
    else:
        return (block.x, block.y + block.height/2)

def draw_connection_line(dwg, start, end, transform=""):
    line = dwg.line(start=start, end=end, stroke="black", stroke_width=2)
    if transform:
        grp = dwg.g(transform=transform)
        grp.add(line)
        dwg.add(grp)
    else:
        dwg.add(line)
