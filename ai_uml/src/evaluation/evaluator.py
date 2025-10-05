import gc
import io
from pathlib import Path
import torch
from PIL import Image
import cairosvg

class DiagramEvaluator:
    """Evaluates SVG diagrams based on their similarity to text descriptions using CLIP/SIGLIP.
    
    This class handles SVG conversion to PNG and CLIP-based scoring.
    """
    
    def __init__(self, model_name='openai/clip-vit-base-patch32'):
        """Initialize the evaluator with a CLIP-like model.
        
        Parameters
        ----------
        model_name : str
            The name of the CLIP/SIGLIP model to use.
        """
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Import here to make dependencies optional
        try:
            from transformers import CLIPProcessor, CLIPModel
            self.model = CLIPModel.from_pretrained(model_name).to(self.device)
            self.processor = CLIPProcessor.from_pretrained(model_name)
        except ImportError:
            print("Please install transformers: pip install transformers")
            self.model = None
            self.processor = None

    def svg_to_png(self, svg_code, size=(384, 384)):
        """Convert SVG string to a PNG image.
        
        Parameters
        ----------
        svg_code : str
            The SVG string to convert.
        size : tuple
            Target image size (width, height).
            
        Returns
        -------
        PIL.Image.Image
            The converted PNG image.
        """
        # Ensure SVG has proper size attributes
        if 'viewBox' not in svg_code:
            svg_code = svg_code.replace(
                '<svg', f'<svg viewBox="0 0 {size[0]} {size[1]}"'
            )

        # Convert SVG to PNG
        try:
            png_data = cairosvg.svg2png(bytestring=svg_code.encode('utf-8'))
            return Image.open(io.BytesIO(png_data)).convert('RGB').resize(size)
        except Exception as e:
            print(f"SVG conversion error: {e}")
            # Return a blank image as fallback
            return Image.new('RGB', size, color='white')

    def evaluate_svg(self, svg_code, description):
        """Evaluate how well an SVG matches a description.
        
        Parameters
        ----------
        svg_code : str
            The SVG code to evaluate.
        description : str
            The text description to compare against.
            
        Returns
        -------
        float
            Similarity score between 0 and 1.
        """
        if self.model is None:
            print("Model not loaded. Please check transformers installation.")
            return 0.0
            
        # Convert SVG to PNG
        image = self.svg_to_png(svg_code)
        
        # Add prompt engineering for better results
        prompt = f"Diagram of {description}"
        
        # Preprocess and get features
        inputs = self.processor(
            text=[prompt], images=image, return_tensors="pt", padding=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            
            # Normalize features
            image_features = outputs.image_embeds 
            text_features = outputs.text_embeds
            
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
            # Calculate similarity
            similarity = (image_features @ text_features.T).item()
            
        return similarity

    def evaluate_diagram(self, diagram, description):
        """Evaluate a diagram object against a description.
        
        Parameters
        ----------
        diagram : VaeDiagram
            The diagram object to evaluate.
        description : str
            The text description to compare against.
            
        Returns
        -------
        float
            Similarity score between 0 and 1.
        """
        # Save diagram to a temporary SVG string
        import svgwrite
        dwg = svgwrite.Drawing(profile='full')
        
        # Draw all blocks in the diagram
        for block in diagram.blocks:
            block.draw(dwg)
            
        # Draw connections
        from ..diagram.utils.geometry import get_right_connection, get_left_connection, draw_connection_line
        for i in range(len(diagram.blocks) - 1):
            start = get_right_connection(diagram.blocks[i])
            end = get_left_connection(diagram.blocks[i+1])
            draw_connection_line(dwg, start, end)
            
        # Convert to string
        svg_string = dwg.tostring()
        
        # Evaluate
        return self.evaluate_svg(svg_string, description)
        
    def clear_memory(self):
        """Clear GPU memory."""
        if hasattr(self, 'model'):
            del self.model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
