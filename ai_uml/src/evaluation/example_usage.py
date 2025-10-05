import os
from os import path
import sys

# Add parent directory to path
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '../..')))

from src.diagram import VaeDiagram, load_diagram_from_json
from src.evaluation import DiagramEvaluator

def main():
    """Demonstrate SVG evaluation against text descriptions."""
    # Load a diagram from JSON
    config_path = path.join("config", "diagram_config.json")
    blocks = load_diagram_from_json(config_path)
    
    # Create diagram
    diagram = VaeDiagram("temp_diagram.svg")
    diagram.setup_blocks(blocks)
    diagram.draw()
    
    # Evaluate against text descriptions
    evaluator = DiagramEvaluator()
    
    # List of descriptions to test against
    descriptions = [
        "a neural network diagram with encoder and decoder",
        "a variational autoencoder architecture",
        "a chart showing data flow in machine learning",
        "a sequence of blocks connected by arrows"
    ]
    
    print("Evaluating diagram against various descriptions:")
    print("-" * 50)
    
    # Load SVG content
    with open("temp_diagram.svg", "r") as f:
        svg_content = f.read()
    
    # Run evaluation for each description
    for desc in descriptions:
        score = evaluator.evaluate_svg(svg_content, desc)
        print(f"Description: '{desc}'")
        print(f"Similarity score: {score:.4f}")
        print("-" * 50)
    
    # Clean up
    evaluator.clear_memory()
    if path.exists("temp_diagram.svg"):
        os.remove("temp_diagram.svg")

if __name__ == "__main__":
    main()
