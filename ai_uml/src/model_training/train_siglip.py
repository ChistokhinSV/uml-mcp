import io
import os
import torch
import cairosvg
import torch.nn as nn
from tqdm import tqdm
from PIL import Image
from torch.nn.utils.rnn import pad_sequence
import matplotlib.pyplot as plt
import numpy as np
import umap
from pathlib import Path
from transformers import AutoProcessor, AutoModel

#############################################
# Check GPU availability
#############################################
device = "cuda" if torch.cuda.is_available() else "cpu"
if device != "cuda":
    print("Warning: GPU not available. Using CPU instead.")
print("Using device:", device)

#############################################
# Dataset paths
#############################################
DATA_ROOT = Path("../../data")
SVG_DIR = DATA_ROOT / "svgs"
TEXT_DIR = DATA_ROOT / "texts"

def svg_to_pil(svg_path: str) -> Image.Image:
    """Convert SVG file to PIL image."""
    with open(svg_path, 'r') as f:
        svg_data = f.read()
    
    png_bytes = cairosvg.svg2png(bytestring=svg_data.encode('utf-8'))
    return Image.open(io.BytesIO(png_bytes)).convert("RGB")

def load_text(text_path: str) -> str:
    """Load text prompt from file."""
    with open(text_path, 'r') as f:
        return f.read().strip()

#############################################
# Create a PyTorch Dataset
#############################################
class SVGPairsDataset(torch.utils.data.Dataset):
    def __init__(self, svg_dir, text_dir, processor):
        super().__init__()
        self.processor = processor
        
        # Get all SVG files
        self.svg_paths = sorted(list(Path(svg_dir).glob("*.svg")))
        
        # Get all text files
        self.text_paths = sorted(list(Path(text_dir).glob("*.txt")))
        
        # Verify matching counts
        assert len(self.svg_paths) == len(self.text_paths), "Mismatch in SVG vs text count!"
        
        # Store prompts for visualization
        self.prompts = [load_text(text_path) for text_path in self.text_paths]

    def __len__(self):
        return len(self.svg_paths)

    def __getitem__(self, idx):
        pil_img = svg_to_pil(self.svg_paths[idx])
        text_prompt = load_text(self.text_paths[idx])
        
        # Process with SigLIP processor
        inputs = self.processor(
            text=[text_prompt],
            images=[pil_img],
            return_tensors="pt",
            padding=True
        )
        
        # Remove batch dimension
        pixel_values = inputs["pixel_values"].squeeze(0)  
        input_ids = inputs["input_ids"].squeeze(0)          
        attention_mask = inputs["attention_mask"].squeeze(0)  

        return pixel_values, input_ids, attention_mask, text_prompt

#############################################
# Custom Collate Function
#############################################
def custom_collate_fn(batch):
    pixel_values_list, input_ids_list, attention_mask_list, text_prompts = zip(*batch)
    
    pixel_values_batch = torch.stack(pixel_values_list, dim=0)
    
    pad_token_id = processor.tokenizer.pad_token_id
    input_ids_batch = pad_sequence(input_ids_list, batch_first=True, padding_value=pad_token_id)
    attention_mask_batch = pad_sequence(attention_mask_list, batch_first=True, padding_value=0)
    
    return pixel_values_batch, input_ids_batch, attention_mask_batch, text_prompts

#############################################
# Initialize SigLIP Model & Processor
#############################################
model_name = "google/siglip-so400m-patch14-384"
model = AutoModel.from_pretrained(model_name).to(device)
processor = AutoProcessor.from_pretrained(model_name)

#############################################
# Prepare DataLoader with custom collate_fn
#############################################
dataset = SVGPairsDataset(SVG_DIR, TEXT_DIR, processor)
dataloader = torch.utils.data.DataLoader(
    dataset, 
    batch_size=2, 
    shuffle=True, 
    collate_fn=custom_collate_fn
)

#############################################
# Training Loop Setup
#############################################
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
loss_img = nn.CrossEntropyLoss()
loss_txt = nn.CrossEntropyLoss()

epochs = 3

model.train()
for epoch in range(epochs):
    loop = tqdm(dataloader, desc=f"Epoch {epoch+1}/{epochs}")
    for batch in loop:
        pixel_values, input_ids, attention_mask, _ = batch

        pixel_values = pixel_values.to(device)
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)

        # Forward pass with SigLIP model
        outputs = model(
            input_ids=input_ids,
            pixel_values=pixel_values,
            attention_mask=attention_mask,
        )
        
        # Get image and text embeddings
        image_embeds = outputs.image_embeds
        text_embeds = outputs.text_embeds
        
        # Normalize embeddings
        image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)
        text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)
        
        # Compute similarity
        logit_scale = model.logit_scale.exp()
        logits_per_image = logit_scale * image_embeds @ text_embeds.t()
        logits_per_text = logits_per_image.t()

        batch_size = pixel_values.size(0)
        ground_truth = torch.arange(batch_size, dtype=torch.long, device=device)

        total_loss = (loss_img(logits_per_image, ground_truth) +
                      loss_txt(logits_per_text, ground_truth)) / 2

        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        loop.set_postfix(loss=total_loss.item())

print("Training complete!")

#############################################
# UMAP Visualization of the Image Embedding Space
#############################################
try:
    import umap
    
    model.eval()
    embeddings = []
    labels = []

    with torch.no_grad():
        for i in range(len(dataset)):
            pixel_values, _, _, text_prompt = dataset[i]
            pixel_values = pixel_values.unsqueeze(0).to(device)
            outputs = model(pixel_values=pixel_values)
            image_features = outputs.image_embeds
            embeddings.append(image_features.cpu().numpy().squeeze())
            labels.append(text_prompt)

    embeddings = np.array(embeddings)

    reducer = umap.UMAP(n_components=2, random_state=42)
    embedding_2d = reducer.fit_transform(embeddings)

    plt.figure(figsize=(8, 6))
    plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1], s=50, c='blue')
    for i, label in enumerate(labels):
        plt.annotate(label, (embedding_2d[i, 0], embedding_2d[i, 1]),
                     textcoords="offset points", xytext=(5, 5), ha='right')
    plt.title("UMAP Visualization of SigLIP Image Embedding Space")
    plt.xlabel("UMAP Dimension 1")
    plt.ylabel("UMAP Dimension 2")
    plt.savefig("../../outputs/siglip_embeddings.png")
    plt.show()
except ImportError:
    print("UMAP not installed. Skipping visualization.")

# Save the model
os.makedirs("../../models", exist_ok=True)
torch.save(model.state_dict(), "../../models/siglip_finetuned.pt")
print("Model saved to ../../models/siglip_finetuned.pt")
