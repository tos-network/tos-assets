#!/usr/bin/env python3
"""
Replace TOS logo in banners and add TOS Network text
"""

from PIL import Image, ImageDraw, ImageFont
import os
import shutil

# Configuration
BANNER_SIZE = None  # Will be calculated based on content
LOGO_SIZE = (250, 250)  # Logo size in banner
PADDING = 60  # Padding on all sides
TEXT = "TOS Network"
TEXT_COLOR_MAP = {
    'white': (255, 255, 255, 255),
    'black': (0, 0, 0, 255),
    'green': (0, 255, 0, 255),
}

# Background color configuration
BACKGROUND_COLORS = {
    'black_background_white_logo': ((0, 0, 0, 255), 'white'),
    'white_background_black_logo': ((255, 255, 255, 255), 'black'),
    'green_background_black_logo': ((0, 128, 0, 255), 'black'),
    'transparent_background_black_logo': (None, 'black'),
    'transparent_background_white_logo': (None, 'white'),
    'transparent_background_green_logo': (None, 'green'),
}

# Gradient backgrounds need special handling
GRADIENT_BANNERS = ['gradient_green_background_white_logo']

def create_gradient_background(size, start_color, end_color):
    """Create gradient background"""
    base = Image.new('RGBA', size, start_color)
    top = Image.new('RGBA', size, end_color)
    mask = Image.new('L', size)
    mask_data = []
    for y in range(size[1]):
        for x in range(size[0]):
            mask_data.append(int(255 * (x / size[0])))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def calculate_banner_size(text_width, text_height):
    """Calculate banner size based on content"""
    spacing = 40  # Spacing between logo and text
    width = PADDING * 2 + LOGO_SIZE[0] + spacing + text_width
    height = PADDING * 2 + max(LOGO_SIZE[1], text_height)
    return (int(width), int(height))

def load_logo(logo_path):
    """Load logo and resize"""
    logo = Image.open(logo_path)
    logo = logo.convert('RGBA')
    logo = logo.resize(LOGO_SIZE, Image.Resampling.LANCZOS)
    return logo

def create_banner(logo, bg_color, text_color, name):
    """Create banner"""
    # First create temporary image to measure text size
    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    # Try to use system font, fall back to default if failed
    try:
        # macOS system font
        font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 90)
    except:
        try:
            # Try other common fonts
            font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 90)
        except:
            # Use default font
            font = ImageFont.load_default()

    # Get text bounding box
    bbox = temp_draw.textbbox((0, 0), TEXT, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate banner size
    banner_size = calculate_banner_size(text_width, text_height)

    # Create background
    if name in GRADIENT_BANNERS:
        # Green gradient
        banner = create_gradient_background(banner_size, (0, 50, 0, 255), (0, 200, 100, 255))
    elif bg_color is None:
        # Transparent background
        banner = Image.new('RGBA', banner_size, (0, 0, 0, 0))
    else:
        # Solid color background
        banner = Image.new('RGBA', banner_size, bg_color)

    draw = ImageDraw.Draw(banner)

    # Logo position (left padding)
    logo_x = PADDING
    logo_y = (banner_size[1] - LOGO_SIZE[1]) // 2  # Vertically centered

    # Paste logo
    banner.paste(logo, (logo_x, logo_y), logo)

    # Text position
    spacing = 40
    text_x = logo_x + LOGO_SIZE[0] + spacing
    text_y = (banner_size[1] - text_height) // 2

    # Draw text
    draw.text((text_x, text_y), TEXT, fill=TEXT_COLOR_MAP[text_color], font=font)

    return banner

def main():
    """Main function"""
    print("Starting banner generation...")

    # Ensure output directories exist
    os.makedirs('png', exist_ok=True)
    os.makedirs('svg', exist_ok=True)

    # Load new logo
    new_logo_path = '/Users/tomisetsu/tos-network/tos-assets/tos/logo512x512.png'
    if not os.path.exists(new_logo_path):
        print(f"Error: Logo file not found: {new_logo_path}")
        return

    logo = load_logo(new_logo_path)
    print(f"Loaded new logo: {new_logo_path}")

    # Process each banner
    for name, (bg_color, text_color) in BACKGROUND_COLORS.items():
        print(f"Processing: {name}")
        banner = create_banner(logo, bg_color, text_color, name)

        # Save PNG
        output_path = f'png/{name}.png'
        banner.save(output_path, 'PNG')
        print(f"  Saved: {output_path}")

    # Process gradient background banners
    for name in GRADIENT_BANNERS:
        print(f"Processing: {name}")
        banner = create_banner(logo, None, 'white', name)
        output_path = f'png/{name}.png'
        banner.save(output_path, 'PNG')
        print(f"  Saved: {output_path}")

    print("\nAll PNG banners generated successfully!")
    print("\nNote: SVG files should be manually processed using design software due to complexity.")
    print("You can refer to the generated PNG files to manually update SVG.")

if __name__ == '__main__':
    main()
