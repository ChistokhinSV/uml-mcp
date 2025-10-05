"""
Unified image generation script supporting multiple models.
This script handles generation from text descriptions using various models.
"""

import os
import torch
import pandas as pd
from tqdm import tqdm
import argparse
from pathlib import Path
import time
import random
from PIL import Image
import importlib.util

def is_model_available(model_name):
    """Check if a model is available by attempting to load it."""
    try:
        if model_name == "flux":
            # Try to import FluxPipeline
            from diffusers import FluxPipeline
            # Try to load the model index (this will fail if gated and not logged in)
            from huggingface_hub import hf_hub_download
            hf_hub_download(
                repo_id="black-forest-labs/FLUX.1-dev",
                filename="model_index.json",
                repo_type="model"
            )
            return True
        elif model_name == "sdxl":
            # Try to import StableDiffusionXLPipeline
            from diffusers import StableDiffusionXLPipeline
            return True
        elif model_name == "sd":
            # Try to import StableDiffusionPipeline
            from diffusers import StableDiffusionPipeline
            return True
        else:
            return False
    except:
        return False

class ImageGenerator:
    """Base class for image generation from text descriptions."""
    
    def __init__(self, output_dir="./generated_images"):
        """Initialize the image generator."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def process_csv(self, csv_path, id_col="id", desc_col="description", limit=None):
        """Process descriptions from a CSV file."""
        # This is an abstract method to be implemented by subclasses
        raise NotImplementedError("Subclasses must implement this method")

class SDImageGenerator(ImageGenerator):
    """Generate images using Stable Diffusion or SDXL."""
    
    def __init__(self, model_name="stabilityai/stable-diffusion-xl-base-1.0", 
                 output_dir="./generated_images", device=None, 
                 use_half_precision=True):
        """Initialize the Stable Diffusion image generator."""
        super().__init__(output_dir)
        self.model_name = model_name
        
        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"Using device: {self.device}")
        
        # Load the model based on whether it's SDXL or regular SD
        print(f"Loading {model_name}...")
        torch_dtype = torch.float16 if use_half_precision and self.device == "cuda" else None
        
        if "xl" in model_name.lower():
            from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                model_name,
                torch_dtype=torch_dtype,
                use_safetensors=True,
                variant="fp16" if use_half_precision else None
            )
            # Use DPM-Solver++ for faster inference
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        else:
            from diffusers import StableDiffusionPipeline
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_name,
                torch_dtype=torch_dtype,
                use_safetensors=True
            )
        
        if self.device == "cuda":
            self.pipe = self.pipe.to(self.device)
            # Enable memory optimization if on CUDA
            self.pipe.enable_attention_slicing()
        else:
            print("Using CPU for inference. This will be slow!")
        
        print("Model loaded successfully")
    
    def generate_image(self, description, height=1024, width=1024, 
                     guidance_scale=7.5, num_inference_steps=30, seed=None):
        """Generate an image from a text description."""
        # Set random seed if provided
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
            
        generator = torch.Generator(self.device if self.device != "cpu" else "cpu").manual_seed(seed)
        
        # Generate the image
        image = self.pipe(
            prompt=description,
            height=height,
            width=width,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=generator
        ).images[0]
        
        return image, seed
    
    def process_csv(self, csv_path, id_col="id", desc_col="description", limit=None):
        """Process descriptions from a CSV file and generate images."""
        # Load CSV
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} descriptions from {csv_path}")
        
        # Apply limit if specified
        if limit is not None:
            df = df.head(limit)
            print(f"Limited to {limit} descriptions")
        
        # Create subdirectory for this batch
        batch_dir = os.path.join(self.output_dir, f"batch_{int(time.time())}")
        os.makedirs(batch_dir, exist_ok=True)
        
        # Create a log file
        log_file = os.path.join(batch_dir, "generation_log.csv")
        logs = []
        
        # Generate images for each description
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Generating images"):
            svg_id = row[id_col]
            description = row[desc_col]
            
            # Create subdirectory for this ID
            id_dir = os.path.join(batch_dir, svg_id)
            os.makedirs(id_dir, exist_ok=True)
            
            try:
                # Generate image
                start_time = time.time()
                image, seed = self.generate_image(description)
                duration = time.time() - start_time
                
                # Save image
                model_suffix = "sdxl" if "xl" in self.model_name.lower() else "sd"
                image_path = os.path.join(id_dir, f"{svg_id}_{model_suffix}.png")
                image.save(image_path)
                
                # Log details
                logs.append({
                    'id': svg_id,
                    'description': description,
                    'image_path': image_path,
                    'model': self.model_name,
                    'seed': seed,
                    'duration': duration,
                    'success': True
                })
                
                print(f"Generated image for '{svg_id}' in {duration:.2f}s - saved to {image_path}")
                
            except Exception as e:
                print(f"Error generating image for '{svg_id}': {e}")
                logs.append({
                    'id': svg_id,
                    'description': description,
                    'model': self.model_name,
                    'error': str(e),
                    'success': False
                })
        
        # Save log
        log_df = pd.DataFrame(logs)
        log_df.to_csv(log_file, index=False)
        print(f"Generation log saved to {log_file}")
        
        return batch_dir

class FluxImageGenerator(ImageGenerator):
    """Generate images using FLUX.1-dev model."""
    
    def __init__(self, output_dir="./generated_images", device=None, 
                use_half_precision=True):
        """Initialize the Flux image generator."""
        super().__init__(output_dir)
        self.model_name = "black-forest-labs/FLUX.1-dev"
        
        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"Using device: {self.device}")
        
        # Load the model
        print(f"Loading {self.model_name}...")
        from diffusers import FluxPipeline
        torch_dtype = torch.bfloat16 if use_half_precision and self.device == "cuda" else None
        self.pipe = FluxPipeline.from_pretrained(self.model_name, torch_dtype=torch_dtype)
        
        if self.device == "cuda":
            self.pipe.enable_model_cpu_offload()
        elif self.device == "cpu":
            print("Using CPU for inference. This will be slow!")
        
        print("Model loaded successfully")
    
    def generate_image(self, description, height=1024, width=1024, 
                      guidance_scale=3.5, num_inference_steps=50, seed=None):
        """Generate an image from a text description."""
        # Set random seed if provided
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
            
        generator = torch.Generator(self.device if self.device != "cpu" else "cpu").manual_seed(seed)
        
        # Generate the image
        image = self.pipe(
            description,
            height=height,
            width=width,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            max_sequence_length=512,
            generator=generator
        ).images[0]
        
        return image, seed
    
    def process_csv(self, csv_path, id_col="id", desc_col="description", limit=None):
        """Process descriptions from a CSV file and generate images."""
        # Load CSV
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} descriptions from {csv_path}")
        
        # Apply limit if specified
        if limit is not None:
            df = df.head(limit)
            print(f"Limited to {limit} descriptions")
        
        # Create subdirectory for this batch
        batch_dir = os.path.join(self.output_dir, f"batch_{int(time.time())}")
        os.makedirs(batch_dir, exist_ok=True)
        
        # Create a log file
        log_file = os.path.join(batch_dir, "generation_log.csv")
        logs = []
        
        # Generate images for each description
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Generating images"):
            svg_id = row[id_col]
            description = row[desc_col]
            
            # Create subdirectory for this ID
            id_dir = os.path.join(batch_dir, svg_id)
            os.makedirs(id_dir, exist_ok=True)
            
            try:
                # Generate image
                start_time = time.time()
                image, seed = self.generate_image(description)
                duration = time.time() - start_time
                
                # Save image
                image_path = os.path.join(id_dir, f"{svg_id}_flux.png")
                image.save(image_path)
                
                # Log details
                logs.append({
                    'id': svg_id,
                    'description': description,
                    'image_path': image_path,
                    'model': self.model_name,
                    'seed': seed,
                    'duration': duration,
                    'success': True
                })
                
                print(f"Generated image for '{svg_id}' in {duration:.2f}s - saved to {image_path}")
                
            except Exception as e:
                print(f"Error generating image for '{svg_id}': {e}")
                logs.append({
                    'id': svg_id,
                    'description': description,
                    'model': self.model_name,
                    'error': str(e),
                    'success': False
                })
        
        # Save log
        log_df = pd.DataFrame(logs)
        log_df.to_csv(log_file, index=False)
        print(f"Generation log saved to {log_file}")
        
        return batch_dir

def main():
    """Main function to select and run appropriate image generator."""
    parser = argparse.ArgumentParser(description="Generate images from text descriptions")
    parser.add_argument("--csv", type=str, default="../svgllms/train.csv", help="Path to CSV file with descriptions")
    parser.add_argument("--output", type=str, default="./generated_images", help="Output directory for images")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of images to generate")
    parser.add_argument("--cpu", action="store_true", help="Force CPU inference")
    parser.add_argument("--model", type=str, default="auto", 
                       help="Model to use (auto, flux, sdxl, sd, sd15)")
    
    args = parser.parse_args()
    
    # Auto-detect models if not explicitly specified
    if args.model == "auto":
        # Try models in order of preference
        for model_name in ["flux", "sdxl", "sd"]:
            if is_model_available(model_name):
                args.model = model_name
                print(f"Auto-selected model: {args.model}")
                break
        else:
            print("No suitable models found. Please install one of: FLUX.1, Stable Diffusion XL, or Stable Diffusion")
            return
    
    # Initialize and run the appropriate generator
    device = "cpu" if args.cpu else None
    
    if args.model == "flux":
        # Use FLUX.1-dev model
        print("Using FLUX.1-dev model")
        try:
            generator = FluxImageGenerator(
                output_dir=args.output,
                device=device
            )
            generator.process_csv(args.csv, limit=args.limit)
        except Exception as e:
            print(f"Error with FLUX model: {e}")
            print("Falling back to Stable Diffusion XL")
            args.model = "sdxl"
    
    if args.model in ["sdxl", "sd", "sd15"]:
        # Select the appropriate SD model
        if args.model == "sdxl":
            model_name = "stabilityai/stable-diffusion-xl-base-1.0"
        elif args.model == "sd15":
            model_name = "runwayml/stable-diffusion-v1-5"
        else:  # Default to newer SD model
            model_name = "stabilityai/stable-diffusion-2-1"
            
        print(f"Using Stable Diffusion model: {model_name}")
        generator = SDImageGenerator(
            model_name=model_name,
            output_dir=args.output,
            device=device
        )
        generator.process_csv(args.csv, limit=args.limit)

if __name__ == "__main__":
    main()