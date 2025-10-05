import json
from os import path
from ..blocks.rectangle import RoundRectBlock
from ..blocks.encoder import EncoderBlock
from ..blocks.decoder import DecoderBlock
from ..blocks.advanced import MLPBlock, FFNBlock, TransformerAddBlock
from ..blocks.latent import LatentCubeBlock

# Mapping of type string to block class.
BLOCK_TYPES = {
    "RoundRectBlock": RoundRectBlock,
    "LatentCubeBlock": LatentCubeBlock,
    "EncoderBlock": EncoderBlock,
    "DecoderBlock": DecoderBlock,
    "MLPBlock": MLPBlock,
    "FFNBlock": FFNBlock,
    "TransformerAddBlock": TransformerAddBlock
}

def load_diagram_from_json(json_file):
    """
    Load diagram configuration from JSON and create block objects.
    Nodes are assumed to be in left-to-right order.
    """
    with open(json_file, 'r') as f:
        config = json.load(f)
    
    blocks = []
    for node in config.get("nodes", []):
        label = node.get("label")
        x = node.get("x", 50)
        y = node.get("y", 125)
        width = node.get("width", 100)
        height = node.get("height", 50)
        angle = node.get("angle", 0)
        text_orientation = node.get("textOrientation", "horizontal")
        block_type = node.get("type", "RoundRectBlock")
        
        # Look up the block class from the mapping
        BlockClass = BLOCK_TYPES.get(block_type, RoundRectBlock)
        
        # For Encoder and Decoder, pass indent if provided.
        if block_type in ["EncoderBlock", "DecoderBlock"]:
            indent = node.get("indent", 20)
            block = BlockClass(label, x, y, width, height, indent, angle)
        else:
            block = BlockClass(label, x, y, width, height, angle)
        
        # Apply text orientation if the block supports it.
        if hasattr(block, "set_text_direction"):
            block.set_text_direction(text_orientation)
        
        blocks.append(block)
    return blocks
