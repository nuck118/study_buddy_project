from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from io import BytesIO
import os

def generate_certificate_image(username, subject_name, date_str):
    # 1. Create a blank white image (Landscape)
    width, height = 1000, 700
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # 2. Draw Borders
    # Outer Indigo Border
    draw.rectangle([(20, 20), (width-20, height-20)], outline="#4f46e5", width=10)
    # Inner Gold Border
    draw.rectangle([(40, 40), (width-40, height-40)], outline="#fbbf24", width=5)

    # 3. Load Fonts (Using default for safety, but you can load .ttf files)
    # Note: On a real server, you would load a nice .ttf font file
    try:
        # Try loading a default font - size is approximate
        font_large = ImageFont.truetype("Arial.ttf", 60)
        font_medium = ImageFont.truetype("Arial.ttf", 40)
        font_small = ImageFont.truetype("Arial.ttf", 25)
    except IOError:
        # Fallback if system fonts aren't found
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 4. Draw Text
    # Title
    draw.text((width/2, 150), "CERTIFICATE OF COMPLETION", fill="#333", anchor="mm", font=font_large)
    
    # "Presented to"
    draw.text((width/2, 250), "This is to certify that", fill="#666", anchor="mm", font=font_small)

    # User Name (Indigo Color)
    draw.text((width/2, 320), username.upper(), fill="#4f46e5", anchor="mm", font=font_large)

    # "Has successfully completed the course"
    draw.text((width/2, 400), "Has successfully completed the course", fill="#666", anchor="mm", font=font_small)

    # Subject Name
    draw.text((width/2, 460), subject_name, fill="#111", anchor="mm", font=font_medium)

    # Date
    draw.text((width/2, 580), f"Issued on: {date_str}", fill="#888", anchor="mm", font=font_small)

    # Badge Icon Placeholder (Gold Circle)
    draw.ellipse([(width/2 - 40, 620), (width/2 + 40, 700)], fill="#fbbf24", outline=None)
    draw.text((width/2, 660), "SB", fill="white", anchor="mm", font=font_medium)

    # 5. Save to Memory
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue())