# Image Generation from Text Descriptions

This directory contains scripts for generating images from text descriptions using various state-of-the-art image generation models.

## Overview

The system supports multiple image generation models:
- Stable Diffusion XL (SDXL)
- Stable Diffusion v1.5 and v2.1
- FLUX.1-dev (requires Hugging Face access)

## Usage

### Basic Usage

```bash
python generate_images.py --csv ../svgllms/train.csv --output ./images
```

### Select a Specific Model

```bash
# Use SDXL
python generate_images.py --model sdxl --csv ../svgllms/train.csv

# Use Stable Diffusion 1.5
python generate_images.py --model sd15 --csv ../svgllms/train.csv

# Use FLUX (requires HF login and access)
python generate_images.py --model flux --csv ../svgllms/train.csv
```

### Limit the Number of Images

```bash
python generate_images.py --limit 5 --csv ../svgllms/train.csv
```

### Force CPU Inference

```bash
python generate_images.py --cpu
```

## Output Structure

Generated images are saved in a structured directory format:

```
output_directory/
└── batch_[timestamp]/
    ├── [id1]/
    │   └── [id1]_[model].png
    ├── [id2]/
    │   └── [id2]_[model].png
    └── generation_log.csv
```

The `generation_log.csv` file contains details about each generation, including:
- ID
- Description
- Image path
- Model used
- Seed value for reproducibility
- Duration of generation
- Success/error status

## Dependencies

Requires the `diffusers` library and its dependencies:

```bash
pip install diffusers transformers torch accelerate pandas tqdm pillow
```

For FLUX.1-dev model access, you'll need to:
1. Create a Hugging Face account
2. Log in via the CLI: `huggingface-cli login`
3. Request access to the FLUX.1-dev model
