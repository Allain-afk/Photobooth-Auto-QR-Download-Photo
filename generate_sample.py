"""Generate a single sample photo for testing."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime
import random

WATCH_FOLDER = r'C:\Photobooth\Outputs'

# Create gradient photo
img = Image.new('RGB', (1200, 800))
draw = ImageDraw.Draw(img)

# Blue to purple gradient
for y in range(800):
    r = int(65 + (147 - 65) * y / 800)
    g = int(105 + (112 - 105) * y / 800)
    b = int(225 + (219 - 225) * y / 800)
    draw.line([(0, y), (1200, y)], fill=(r, g, b))

# Add decorative circles
for _ in range(20):
    x, y = random.randint(0, 1200), random.randint(0, 800)
    size = random.randint(30, 120)
    draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 255, 40))

# Add text
try:
    font = ImageFont.truetype('arial.ttf', 60)
    small_font = ImageFont.truetype('arial.ttf', 30)
except:
    font = ImageFont.load_default()
    small_font = font

# Main text with shadow
text1 = "Sample Photobooth Image"
text2 = datetime.now().strftime('%B %d, %Y at %I:%M:%S %p')

# Center text
bbox1 = draw.textbbox((0, 0), text1, font=font)
bbox2 = draw.textbbox((0, 0), text2, font=small_font)
x1 = (1200 - (bbox1[2] - bbox1[0])) // 2
x2 = (1200 - (bbox2[2] - bbox2[0])) // 2

# Shadow
draw.text((x1+3, 303), text1, font=font, fill=(0, 0, 0))
draw.text((x2+3, 403), text2, font=small_font, fill=(0, 0, 0))
# Main text
draw.text((x1, 300), text1, font=font, fill=(255, 255, 255))
draw.text((x2, 400), text2, font=small_font, fill=(255, 255, 255))

# Watermark
draw.text((20, 750), 'TEST IMAGE - Photobooth Demo', font=small_font, fill=(200, 200, 200))

# Save
Path(WATCH_FOLDER).mkdir(parents=True, exist_ok=True)
filename = f'demo_photo_{datetime.now().strftime("%H%M%S")}.jpg'
output_path = Path(WATCH_FOLDER) / filename
img.save(output_path, 'JPEG', quality=95)
print(f'Created: {output_path}')
print('Popup should appear now!')

