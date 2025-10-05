import io
import torch
from PIL import Image
import cairosvg
import matplotlib.pyplot as plt
from transformers import AutoProcessor, AutoModel
from pathlib import Path

# Use GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model(model_path=None):
    """Load SigLIP model, either pretrained or finetuned."""
    model_name = "google/siglip-so400m-patch14-384"
    model = AutoModel.from_pretrained(model_name).to(device)
    processor = AutoProcessor.from_pretrained(model_name)
    
    if model_path:
        model.load_state_dict(torch.load(model_path))
        print(f"Loaded fine-tuned model from {model_path}")
    
    return model, processor

def svg_to_pil(svg_data, is_path=False):
    """Convert SVG to PIL image."""
    if is_path:
        with open(svg_data, 'r') as f:
            svg_content = f.read()
    else:
        svg_content = svg_data
    
    png_bytes = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))
    return Image.open(io.BytesIO(png_bytes)).convert("RGB")

def compute_similarity(model, processor, svg_data, text_prompt, is_path=False):
    """Compute similarity between SVG and text description using SigLIP."""
    # Convert SVG to PIL image
    image = svg_to_pil(svg_data, is_path)
    
    # Process inputs
    inputs = processor(
        text=[text_prompt],
        images=[image],
        return_tensors="pt",
        padding=True
    ).to(device)
    
    # Get embeddings
    with torch.no_grad():
        outputs = model(**inputs)
        
        # Normalize embeddings
        image_embeds = outputs.image_embeds / outputs.image_embeds.norm(dim=-1, keepdim=True)
        text_embeds = outputs.text_embeds / outputs.text_embeds.norm(dim=-1, keepdim=True)
        
        # Compute similarity
        similarity = (image_embeds @ text_embeds.T).item()
        
    return similarity

def batch_evaluation():
    """Evaluate multiple SVG-text pairs and visualize results."""
    model, processor = load_model("../../models/siglip_finetuned.pt")
    model.eval()
    
    # Load test data
    data_root = Path("../../data")
    svg_dir = data_root / "svgs"
    text_dir = data_root / "texts"
    
    svg_files = sorted(list(svg_dir.glob("*.svg")))
    text_files = sorted(list(text_dir.glob("*.txt")))
    
    # Create similarity matrix
    similarity_matrix = torch.zeros((len(svg_files), len(text_files)))
    
    text_prompts = []
    for text_file in text_files:
        with open(text_file, 'r') as f:
            text_prompts.append(f.read().strip())
    
    # Compute similarity scores
    for i, svg_file in enumerate(svg_files):
        for j, text_file in enumerate(text_files):
            with open(text_file, 'r') as f:
                text_prompt = f.read().strip()
            
            similarity = compute_similarity(model, processor, str(svg_file), text_prompt, is_path=True)
            similarity_matrix[i, j] = similarity
    
    # Plot heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(similarity_matrix, cmap='viridis')
    plt.colorbar(label='Similarity Score')
    plt.xticks(range(len(text_prompts)), text_prompts, rotation=45, ha="right")
    plt.yticks(range(len(svg_files)), [f.name for f in svg_files])
    plt.tight_layout()
    plt.title("SigLIP Similarity Scores")
    plt.savefig("../../outputs/similarity_heatmap.png")
    plt.show()

if __name__ == "__main__":
    batch_evaluation()
