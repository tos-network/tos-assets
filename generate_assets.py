#!/usr/bin/env python3
"""
Generate TOS banners and icons from logo.png
"""

from PIL import Image, ImageDraw, ImageFont
import os
import base64
from io import BytesIO

# Paths
LOGO_PATH = "logo/logo.png"
BANNERS_PNG_DIR = "banners/png"
BANNERS_SVG_DIR = "banners/svg"
ICONS_PNG_DIR = "icons/png"
ICONS_SVG_DIR = "icons/svg"

# Colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
GREEN = (2, 255, 207, 255)  # #02FFCF
GOLD = (212, 175, 55, 255)  # Golden color from logo
TRANSPARENT = (0, 0, 0, 0)

def create_banner_with_text(logo_img, bg_color, logo_color, text_color, width=1500, height=500):
    """Create a banner with logo and TOS text"""
    # Create banner background
    banner = Image.new('RGBA', (width, height), bg_color)

    # Resize logo to fit banner
    logo_height = int(height * 0.6)
    logo = logo_img.copy()
    logo.thumbnail((logo_height, logo_height), Image.Resampling.LANCZOS)

    # Paste logo on the left
    logo_x = int(height * 0.2)
    logo_y = (height - logo.size[1]) // 2
    banner.paste(logo, (logo_x, logo_y), logo)

    # Add TOS text
    draw = ImageDraw.Draw(banner)
    try:
        # Try to use a nice font
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(height * 0.4))
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    text = "TOS"
    text_x = logo_x + logo.size[0] + int(height * 0.15)
    text_y = height // 2

    # Draw text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_height = bbox[3] - bbox[1]
    draw.text((text_x, text_y - text_height//2), text, fill=text_color, font=font)

    return banner

def create_icon_circle(logo_img, bg_color, logo_color, size=1000):
    """Create circular icon"""
    icon = Image.new('RGBA', (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(icon)

    # Draw circle background
    if bg_color != TRANSPARENT:
        draw.ellipse([0, 0, size-1, size-1], fill=bg_color)

    # Resize and paste logo
    logo = logo_img.copy()
    logo_size = int(size * 0.6)
    logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Change logo color if needed
    if logo_color != GOLD:
        logo = colorize_logo(logo, logo_color)

    logo_x = (size - logo.size[0]) // 2
    logo_y = (size - logo.size[1]) // 2
    icon.paste(logo, (logo_x, logo_y), logo)

    return icon

def create_icon_square(logo_img, bg_color, logo_color, size=1000):
    """Create square icon"""
    icon = Image.new('RGBA', (size, size), bg_color)

    # Resize and paste logo
    logo = logo_img.copy()
    logo_size = int(size * 0.6)
    logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Change logo color if needed
    if logo_color != GOLD:
        logo = colorize_logo(logo, logo_color)

    logo_x = (size - logo.size[0]) // 2
    logo_y = (size - logo.size[1]) // 2
    icon.paste(logo, (logo_x, logo_y), logo)

    return icon

def create_icon_transparent(logo_img, logo_color, size=1000):
    """Create transparent icon with just the logo"""
    logo = logo_img.copy()
    logo.thumbnail((size, size), Image.Resampling.LANCZOS)

    # Change logo color if needed
    if logo_color != GOLD:
        logo = colorize_logo(logo, logo_color)

    return logo

def colorize_logo(logo, color):
    """Change logo color while preserving alpha"""
    logo = logo.convert('RGBA')
    colored = Image.new('RGBA', logo.size, (0, 0, 0, 0))

    # Extract alpha channel
    r, g, b, a = logo.split()

    # Create new image with desired color
    colored_img = Image.new('RGBA', logo.size, color)

    # Paste with alpha mask
    result = Image.new('RGBA', logo.size, (0, 0, 0, 0))
    result.paste(colored_img, (0, 0), a)

    return result

def image_to_base64(img):
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def create_svg_banner(logo_img, bg_color, logo_color, text_color, width=1500, height=500):
    """Create SVG banner with logo"""
    # Prepare logo
    logo = logo_img.copy()
    logo_height = int(height * 0.6)
    logo.thumbnail((logo_height, logo_height), Image.Resampling.LANCZOS)

    # Change logo color if needed
    if logo_color != GOLD:
        logo = colorize_logo(logo, logo_color)

    # Convert logo to base64
    logo_base64 = image_to_base64(logo)

    # Calculate positions
    logo_x = int(height * 0.2)
    logo_y = (height - logo.height) // 2

    # Background color
    if bg_color == TRANSPARENT:
        bg_fill = "none"
        svg_bg = ""
    else:
        bg_fill = f"rgba({bg_color[0]},{bg_color[1]},{bg_color[2]},{bg_color[3]/255})"
        svg_bg = f'<rect width="{width}" height="{height}" fill="{bg_fill}"/>'

    # Text color
    text_fill = f"rgba({text_color[0]},{text_color[1]},{text_color[2]},{text_color[3]/255})"

    # Text position
    text_x = logo_x + logo.width + int(height * 0.15)
    text_y = height // 2

    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
{svg_bg}
<image x="{logo_x}" y="{logo_y}" width="{logo.width}" height="{logo.height}" href="{logo_base64}"/>
<text x="{text_x}" y="{text_y}" font-family="Arial, sans-serif" font-size="{int(height * 0.35)}" font-weight="bold" fill="{text_fill}" dominant-baseline="middle">TOS</text>
</svg>'''

    return svg

def create_svg_icon_circle(logo_img, bg_color, logo_color, size=1000):
    """Create SVG circular icon"""
    # Prepare logo
    logo = logo_img.copy()
    logo_size = int(size * 0.6)
    logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Change logo color if needed
    if logo_color != GOLD:
        logo = colorize_logo(logo, logo_color)

    # Convert logo to base64
    logo_base64 = image_to_base64(logo)

    # Calculate positions
    logo_x = (size - logo.width) // 2
    logo_y = (size - logo.height) // 2

    # Background
    if bg_color == TRANSPARENT:
        circle_fill = "none"
    else:
        circle_fill = f"rgba({bg_color[0]},{bg_color[1]},{bg_color[2]},{bg_color[3]/255})"

    svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
<circle cx="{size//2}" cy="{size//2}" r="{size//2-1}" fill="{circle_fill}"/>
<image x="{logo_x}" y="{logo_y}" width="{logo.width}" height="{logo.height}" href="{logo_base64}"/>
</svg>'''

    return svg

def create_svg_icon_square(logo_img, bg_color, logo_color, size=1000):
    """Create SVG square icon"""
    # Prepare logo
    logo = logo_img.copy()
    logo_size = int(size * 0.6)
    logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Change logo color if needed
    if logo_color != GOLD:
        logo = colorize_logo(logo, logo_color)

    # Convert logo to base64
    logo_base64 = image_to_base64(logo)

    # Calculate positions
    logo_x = (size - logo.width) // 2
    logo_y = (size - logo.height) // 2

    # Background
    bg_fill = f"rgba({bg_color[0]},{bg_color[1]},{bg_color[2]},{bg_color[3]/255})"

    svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
<rect width="{size}" height="{size}" fill="{bg_fill}"/>
<image x="{logo_x}" y="{logo_y}" width="{logo.width}" height="{logo.height}" href="{logo_base64}"/>
</svg>'''

    return svg

def create_svg_icon_transparent(logo_img, logo_color, size=1000):
    """Create SVG transparent icon"""
    # Prepare logo
    logo = logo_img.copy()
    logo.thumbnail((size, size), Image.Resampling.LANCZOS)

    # Change logo color if needed
    if logo_color != GOLD:
        logo = colorize_logo(logo, logo_color)

    # Convert logo to base64
    logo_base64 = image_to_base64(logo)

    # Center the logo
    logo_x = (size - logo.width) // 2
    logo_y = (size - logo.height) // 2

    svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
<image x="{logo_x}" y="{logo_y}" width="{logo.width}" height="{logo.height}" href="{logo_base64}"/>
</svg>'''

    return svg

def main():
    # Load logo
    logo = Image.open(LOGO_PATH).convert('RGBA')

    print("Generating banners...")

    # Generate PNG banners
    os.makedirs(BANNERS_PNG_DIR, exist_ok=True)

    banners = [
        ("black_background_white_logo.png", BLACK, GOLD, WHITE),
        ("white_background_black_logo.png", WHITE, GOLD, BLACK),
        ("green_background_black_logo.png", GREEN, GOLD, BLACK),
        ("gradient_green_background_white_logo.png", GREEN, GOLD, WHITE),
        ("transparent_backgroud_black_logo.png", TRANSPARENT, GOLD, BLACK),
        ("transparent_background_white_logo.png", TRANSPARENT, GOLD, WHITE),
        ("transparent_background_green_logo.png", TRANSPARENT, GOLD, GREEN),
    ]

    for filename, bg, logo_c, text_c in banners:
        banner = create_banner_with_text(logo, bg, logo_c, text_c)
        banner.save(os.path.join(BANNERS_PNG_DIR, filename))
        print(f"  Created {filename}")

    print("\nGenerating circle icons...")

    # Generate circle icons
    circle_dir = os.path.join(ICONS_PNG_DIR, "circle")
    os.makedirs(circle_dir, exist_ok=True)

    circle_icons = [
        ("black_background_green_logo.png", BLACK, GREEN),
        ("black_background_white_logo.png", BLACK, WHITE),
        ("green_background_black_logo.png", GREEN, BLACK),
        ("green_background_white_logo.png", GREEN, WHITE),
        ("white_background_black_logo.png", WHITE, BLACK),
        ("white_background_green_logo.png", WHITE, GREEN),
    ]

    for filename, bg, logo_c in circle_icons:
        icon = create_icon_circle(logo, bg, logo_c)
        icon.save(os.path.join(circle_dir, filename))
        print(f"  Created {filename}")

    print("\nGenerating square icons...")

    # Generate square icons
    square_dir = os.path.join(ICONS_PNG_DIR, "square")
    os.makedirs(square_dir, exist_ok=True)

    for filename, bg, logo_c in circle_icons:  # Same variants as circle
        icon = create_icon_square(logo, bg, logo_c)
        icon.save(os.path.join(square_dir, filename))
        print(f"  Created {filename}")

    print("\nGenerating transparent icons...")

    # Generate transparent icons
    transparent_dir = os.path.join(ICONS_PNG_DIR, "transparent")
    os.makedirs(transparent_dir, exist_ok=True)

    transparent_icons = [
        ("black.png", BLACK),
        ("white.png", WHITE),
        ("green.png", GREEN),
    ]

    for filename, logo_c in transparent_icons:
        icon = create_icon_transparent(logo, logo_c)
        icon.save(os.path.join(transparent_dir, filename))
        print(f"  Created {filename}")

    print("\nDone! PNG files generated.")

    # Generate SVG banners
    print("\nGenerating SVG banners...")
    os.makedirs(BANNERS_SVG_DIR, exist_ok=True)

    svg_banners = [
        ("black_background_white_logo.svg", BLACK, GOLD, WHITE),
        ("white_background_black_logo.svg", WHITE, GOLD, BLACK),
        ("green_background_black_logo.svg", GREEN, GOLD, BLACK),
        ("gradient_green_background_white_logo.svg", GREEN, GOLD, WHITE),
        ("transparent_background_black_logo.svg", TRANSPARENT, GOLD, BLACK),
        ("transparent_background_white_logo.svg", TRANSPARENT, GOLD, WHITE),
        ("transparent_background_green_logo.svg", TRANSPARENT, GOLD, GREEN),
    ]

    for filename, bg, logo_c, text_c in svg_banners:
        svg_content = create_svg_banner(logo, bg, logo_c, text_c)
        with open(os.path.join(BANNERS_SVG_DIR, filename), 'w') as f:
            f.write(svg_content)
        print(f"  Created {filename}")

    # Generate SVG circle icons
    print("\nGenerating SVG circle icons...")
    circle_svg_dir = os.path.join(ICONS_SVG_DIR, "circle")
    os.makedirs(circle_svg_dir, exist_ok=True)

    for filename, bg, logo_c in circle_icons:
        svg_filename = filename.replace('.png', '.svg')
        svg_content = create_svg_icon_circle(logo, bg, logo_c)
        with open(os.path.join(circle_svg_dir, svg_filename), 'w') as f:
            f.write(svg_content)
        print(f"  Created {svg_filename}")

    # Generate SVG square icons
    print("\nGenerating SVG square icons...")
    square_svg_dir = os.path.join(ICONS_SVG_DIR, "square")
    os.makedirs(square_svg_dir, exist_ok=True)

    for filename, bg, logo_c in circle_icons:
        svg_filename = filename.replace('.png', '.svg')
        svg_content = create_svg_icon_square(logo, bg, logo_c)
        with open(os.path.join(square_svg_dir, svg_filename), 'w') as f:
            f.write(svg_content)
        print(f"  Created {svg_filename}")

    # Generate SVG transparent icons
    print("\nGenerating SVG transparent icons...")
    transparent_svg_dir = os.path.join(ICONS_SVG_DIR, "transparent")
    os.makedirs(transparent_svg_dir, exist_ok=True)

    svg_transparent_icons = [
        ("black.svg", BLACK),
        ("white.svg", WHITE),
        ("green.svg", GREEN),
    ]

    for filename, logo_c in svg_transparent_icons:
        svg_content = create_svg_icon_transparent(logo, logo_c)
        with open(os.path.join(transparent_svg_dir, filename), 'w') as f:
            f.write(svg_content)
        print(f"  Created {filename}")

    print("\nAll done! PNG and SVG files generated successfully.")

if __name__ == "__main__":
    main()
