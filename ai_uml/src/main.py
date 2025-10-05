import io
import matplotlib.pyplot as plt
from PIL import Image
from wand.image import Image as WandImage
from diagram import VaeDiagram, load_diagram_from_json
from os import path

def plot_svg(filename):
    with WandImage(filename=filename, resolution=300) as img:
        png_blob = img.make_blob("png")
    image = Image.open(io.BytesIO(png_blob))
    plt.figure(figsize=(12, 4))
    plt.imshow(image)
    plt.axis('off')
    plt.title("Diagram from JSON")
    plt.show()

def main():
    filename = "vae_diagram.svg"
    config_path = path.join("../config", "diagram_config.json")
    blocks = load_diagram_from_json(config_path)
    diagram = VaeDiagram(filename)
    diagram.setup_blocks(blocks)
    diagram.draw()
    plot_svg(filename)

if __name__ == "__main__":
    main()
