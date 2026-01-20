"""
Test Script for Photobooth QR Automation
========================================
Generates sample placeholder photos to test the popup display.
"""

import os
import time
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random

# Configuration - match with photobooth.py
WATCH_FOLDER = r"C:\Photobooth\Outputs"

# Sample photo settings
PHOTO_WIDTH = 1200
PHOTO_HEIGHT = 800


def create_placeholder_photo(filename: str, text: str = None) -> Path:
    """
    Create a colorful placeholder photo with text overlay.
    
    Args:
        filename: Name for the output file
        text: Optional text to display on the image
        
    Returns:
        Path to the created image
    """
    # Random gradient colors for variety
    color_schemes = [
        [(70, 130, 180), (255, 182, 193)],    # Steel blue to pink
        [(255, 165, 0), (255, 69, 0)],         # Orange gradient
        [(0, 206, 209), (138, 43, 226)],       # Turquoise to purple
        [(50, 205, 50), (0, 100, 0)],          # Green gradient
        [(255, 20, 147), (255, 105, 180)],     # Pink gradient
        [(65, 105, 225), (0, 191, 255)],       # Royal blue to sky blue
    ]
    
    colors = random.choice(color_schemes)
    
    # Create gradient background
    img = Image.new('RGB', (PHOTO_WIDTH, PHOTO_HEIGHT))
    draw = ImageDraw.Draw(img)
    
    for y in range(PHOTO_HEIGHT):
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * y / PHOTO_HEIGHT)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * y / PHOTO_HEIGHT)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * y / PHOTO_HEIGHT)
        draw.line([(0, y), (PHOTO_WIDTH, y)], fill=(r, g, b))
    
    # Add decorative elements
    for _ in range(15):
        x = random.randint(0, PHOTO_WIDTH)
        y = random.randint(0, PHOTO_HEIGHT)
        size = random.randint(20, 100)
        opacity = random.randint(30, 80)
        circle_color = (255, 255, 255, opacity)
        
        # Create a circle overlay
        overlay = Image.new('RGBA', (size*2, size*2), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.ellipse([0, 0, size*2, size*2], fill=(255, 255, 255, 50))
        img.paste(overlay, (x-size, y-size), overlay)
    
    # Add text
    if text is None:
        text = f"📸 Sample Photo\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Try to use a nice font, fall back to default
    try:
        # Try common Windows fonts
        for font_name in ['arial.ttf', 'calibri.ttf', 'segoeui.ttf']:
            try:
                font_large = ImageFont.truetype(font_name, 60)
                font_small = ImageFont.truetype(font_name, 30)
                break
            except:
                continue
        else:
            font_large = ImageFont.load_default()
            font_small = font_large
    except:
        font_large = ImageFont.load_default()
        font_small = font_large
    
    # Draw text with shadow effect
    draw = ImageDraw.Draw(img)
    
    # Center the text
    lines = text.split('\n')
    y_offset = PHOTO_HEIGHT // 2 - 60
    
    for i, line in enumerate(lines):
        font = font_large if i == 0 else font_small
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (PHOTO_WIDTH - text_width) // 2
        
        # Shadow
        draw.text((x+3, y_offset+3), line, font=font, fill=(0, 0, 0, 128))
        # Main text
        draw.text((x, y_offset), line, font=font, fill=(255, 255, 255))
        
        y_offset += 70 if i == 0 else 50
    
    # Add "SAMPLE" watermark
    watermark_font = font_small
    draw.text((20, PHOTO_HEIGHT - 50), "SAMPLE PHOTO - Photobooth Test", 
              font=watermark_font, fill=(255, 255, 255, 180))
    
    # Save the image
    watch_path = Path(WATCH_FOLDER)
    watch_path.mkdir(parents=True, exist_ok=True)
    
    output_path = watch_path / filename
    img.save(output_path, 'JPEG', quality=95)
    
    return output_path


def main():
    """Run the test - generate sample photos."""
    print("\n" + "="*60)
    print("  🧪 PHOTOBOOTH TEST SCRIPT")
    print("="*60)
    print(f"  Output folder: {WATCH_FOLDER}")
    print("="*60 + "\n")
    
    # Ensure watch folder exists
    Path(WATCH_FOLDER).mkdir(parents=True, exist_ok=True)
    
    print("⚠️  Make sure photobooth.py is running first!")
    print("   Run: python photobooth.py\n")
    
    input("Press ENTER to generate a sample photo...")
    
    # Generate test photos
    for i in range(1, 4):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_photo_{timestamp}_{i}.jpg"
        
        print(f"\n📷 Generating: {filename}")
        
        photo_path = create_placeholder_photo(
            filename,
            f"📸 Test Photo #{i}\n{datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        )
        
        print(f"✅ Created: {photo_path}")
        print("   → Popup should appear now!")
        
        if i < 3:
            # Wait a bit between photos
            print("\n⏳ Waiting 5 seconds before next photo...")
            time.sleep(5)
    
    print("\n" + "="*60)
    print("  ✅ Test complete! Generated 3 sample photos.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

