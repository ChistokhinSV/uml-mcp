import os
from pathlib import Path

# Example SVG data
svg_strings = [
    # Example 1: Red Circle
    """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="red" />
</svg>""",
    # Example 2: Blue Rectangle
    """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="60" height="60" fill="blue" />
</svg>""",
    # Example 3: Green Triangle
    """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <polygon points="50,15 90,85 10,85" fill="green" />
</svg>""",
    # Example 4: Purple Ellipse
    """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="50" cy="50" rx="30" ry="20" fill="purple" />
</svg>""",
    # Example 5: Yellow Star
    """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <polygon points="50,15 61,39 87,39 67,57 74,82 50,67 26,82 33,57 13,39 39,39" fill="yellow" />
</svg>"""
]

text_prompts = [
    "A big red circle",
    "A large blue square",
    "A striking green triangle",
    "A soft purple ellipse",
    "A bright yellow star"
]

def create_dataset():
    """Create dataset directories and files."""
    # Create directories
    data_root = Path("../../data")
    svg_dir = data_root / "svgs"
    text_dir = data_root / "texts"
    
    os.makedirs(svg_dir, exist_ok=True)
    os.makedirs(text_dir, exist_ok=True)
    
    # Create SVG files
    for i, svg in enumerate(svg_strings):
        with open(svg_dir / f"shape_{i+1:03d}.svg", "w") as f:
            f.write(svg)
    
    # Create text files
    for i, text in enumerate(text_prompts):
        with open(text_dir / f"prompt_{i+1:03d}.txt", "w") as f:
            f.write(text)
            
    print(f"Created {len(svg_strings)} SVG files in {svg_dir}")
    print(f"Created {len(text_prompts)} text files in {text_dir}")

if __name__ == "__main__":
    create_dataset()
