from .base import Block

class LatentCubeBlock(Block):
    def draw(self, dwg):
        fill_color = "#AED6F1"
        stroke_color = "black"
        stroke_width = 2
        dx, dy = 15, -15
        if self.angle:
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            grp = dwg.g(transform=f"rotate({self.angle}, {cx}, {cy})")
            front = [
                (self.x, self.y),
                (self.x + self.width, self.y),
                (self.x + self.width, self.y + self.height),
                (self.x, self.y + self.height),
            ]
            top = [
                (self.x, self.y),
                (self.x + dx, self.y + dy),
                (self.x + self.width + dx, self.y + dy),
                (self.x + self.width, self.y),
            ]
            side = [
                (self.x + self.width, self.y),
                (self.x + self.width + dx, self.y + dy),
                (self.x + self.width + dx, self.y + dy + self.height),
                (self.x + self.width, self.y + self.height),
            ]
            top_fill = "#D6EAF8"
            side_fill = "#A9CCE3"
            grp.add(
                dwg.polygon(
                    top, stroke=stroke_color, fill=top_fill, stroke_width=stroke_width
                )
            )
            grp.add(
                dwg.polygon(
                    side, stroke=stroke_color, fill=side_fill, stroke_width=stroke_width
                )
            )
            grp.add(
                dwg.polygon(
                    front,
                    stroke=stroke_color,
                    fill=fill_color,
                    stroke_width=stroke_width,
                )
            )
            cx_label = self.x + self.width / 2
            cy_label = self.y + self.height / 2 - 5
            grp.add(
                dwg.text(
                    "Latent Space",
                    insert=(cx_label, cy_label),
                    text_anchor="middle",
                    font_size="12px",
                    font_family="Arial",
                    fill="black",
                )
            )
            grp.add(
                dwg.text(
                    "N(0,1)",
                    insert=(cx_label, cy_label + 20),
                    text_anchor="middle",
                    font_size="12px",
                    font_family="Arial",
                    fill="black",
                )
            )
            dwg.add(grp)
        else:
            front = [
                (self.x, self.y),
                (self.x + self.width, self.y),
                (self.x + self.width, self.y + self.height),
                (self.x, self.y + self.height),
            ]
            top = [
                (self.x, self.y),
                (self.x + dx, self.y + dy),
                (self.x + self.width + dx, self.y + dy),
                (self.x + self.width, self.y),
            ]
            side = [
                (self.x + self.width, self.y),
                (self.x + self.width + dx, self.y + dy),
                (self.x + self.width + dx, self.y + dy + self.height),
                (self.x + self.width, self.y + self.height),
            ]
            top_fill = "#D6EAF8"
            side_fill = "#A9CCE3"
            dwg.add(
                dwg.polygon(
                    top, stroke=stroke_color, fill=top_fill, stroke_width=stroke_width
                )
            )
            dwg.add(
                dwg.polygon(
                    side, stroke=stroke_color, fill=side_fill, stroke_width=stroke_width
                )
            )
            dwg.add(
                dwg.polygon(
                    front,
                    stroke=stroke_color,
                    fill=fill_color,
                    stroke_width=stroke_width,
                )
            )
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2 - 5
            dwg.add(
                dwg.text(
                    "Latent Space",
                    insert=(cx, cy),
                    text_anchor="middle",
                    font_size="12px",
                    font_family="Arial",
                    fill="black",
                )
            )
            dwg.add(
                dwg.text(
                    "N(0,1)",
                    insert=(cx, cy + 20),
                    text_anchor="middle",
                    font_size="12px",
                    font_family="Arial",
                    fill="black",
                )
            )


class LatentCloudBlock(Block):
    """Represents a Latent Space cloud shape"""

    def draw(self, dwg):
        fill_color = "#AED6F1"  # Light blue fill
        stroke_color = "black"
        stroke_width = 2

        # Approximate cloud shape using Bézier curves
        cloud_path = dwg.path(
            d="M {} {} C {} {} {} {} {} {} "
            "C {} {} {} {} {} {} "
            "C {} {} {} {} {} {} "
            "C {} {} {} {} {} {} Z".format(
                self.x + 5,
                self.y + 15,  # Starting point
                self.x - 10,
                self.y - 5,
                self.x + 10,
                self.y - 15,
                self.x + 30,
                self.y - 5,  # Left curve
                self.x + 40,
                self.y - 20,
                self.x + 70,
                self.y - 10,
                self.x + 65,
                self.y + 10,  # Top curve
                self.x + 80,
                self.y + 5,
                self.x + 85,
                self.y + 30,
                self.x + 60,
                self.y + 35,  # Right curve
                self.x + 55,
                self.y + 50,
                self.x + 15,
                self.y + 50,
                self.x + 10,
                self.y + 30,  # Bottom curve
                self.x + 5,
                self.y + 15,
            ),
            stroke=stroke_color,
            fill=fill_color,
            stroke_width=stroke_width,
        )

        # Add cloud shape
        dwg.add(cloud_path)

        # Add label inside the cloud
        cx = self.x + 40  # Approximate center
        cy = self.y + 20
        dwg.add(
            dwg.text(
                "Latent Space",
                insert=(cx, cy),
                text_anchor="middle",
                font_size="12px",
                font_family="Arial",
                fill="black",
            )
        )

        dwg.add(
            dwg.text(
                "N(0,1)",
                insert=(cx, cy + 15),
                text_anchor="middle",
                font_size="12px",
                font_family="Arial",
                fill="black",
            )
        )
