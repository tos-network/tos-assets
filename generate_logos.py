#!/usr/bin/env python3
"""
Generate different sizes of logo files from TOS.png
"""

from PIL import Image
import subprocess
import os

# Source files
SOURCE_LOGO = "logo/TOS.png"
SOURCE_LOGO_TRANSPARENT = "logo/TOS_transparent.png"

# Output directory
OUTPUT_DIR = "logo"

# Sizes to generate for logo files
LOGO_SIZES = [16, 32, 48, 64, 128, 256, 512, 1024]

# Sizes to generate for logo-transparent files
TRANSPARENT_SIZES = [16, 32, 48, 64, 128, 150, 200, 256, 400, 512, 800]

def remove_background_with_rembg(image_path):
    """
    Use rembg to professionally remove background using AI
    """
    try:
        from rembg import remove
        from PIL import Image as PILImage

        print("Using rembg AI model to remove background (this may take a moment)...")
        print("First run will download the AI model (~175MB)...")

        # Open and process image
        with open(image_path, 'rb') as input_file:
            input_data = input_file.read()

        # Remove background
        output_data = remove(input_data)

        # Convert to PIL Image
        from io import BytesIO
        img = PILImage.open(BytesIO(output_data)).convert('RGBA')

        print("Background removed successfully!")
        return img

    except ImportError:
        print("Error: rembg module not found. Please run:")
        print("  source venv/bin/activate")
        print("  python3 generate_logos.py")
        return None
    except Exception as e:
        print(f"Error removing background: {e}")
        return None

def resize_image(image, size, resample=Image.Resampling.LANCZOS):
    """
    Resize image to target size while maintaining aspect ratio and quality
    """
    # Create a copy to avoid modifying original
    img = image.copy()

    # For high quality resizing, use LANCZOS
    img.thumbnail((size, size), resample)

    return img

def main():
    # Load source image
    print(f"Loading source image: {SOURCE_LOGO}")
    source_img = Image.open(SOURCE_LOGO).convert('RGBA')
    print(f"Source size: {source_img.size}")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate logo files (with background)
    print("\nGenerating logo files...")
    for size in LOGO_SIZES:
        resized = resize_image(source_img, size)
        output_path = os.path.join(OUTPUT_DIR, f"logo-{size}x{size}.png")
        resized.save(output_path, "PNG", optimize=True, quality=95)
        print(f"  Created: logo-{size}x{size}.png ({resized.size[0]}x{resized.size[1]})")

    # Save full size logo.png
    logo_full = source_img.copy()
    logo_full.save(os.path.join(OUTPUT_DIR, "logo.png"), "PNG", optimize=True, quality=95)
    print(f"  Created: logo.png ({logo_full.size[0]}x{logo_full.size[1]})")

    # Generate logo-transparent files
    print("\nGenerating transparent logo files...")

    # Check if transparent source exists
    if not os.path.exists(SOURCE_LOGO_TRANSPARENT):
        print(f"Error: {SOURCE_LOGO_TRANSPARENT} not found")
        return

    # Load transparent source
    transparent_source = Image.open(SOURCE_LOGO_TRANSPARENT).convert('RGBA')
    print(f"Loaded transparent source: {transparent_source.size}")

    for size in TRANSPARENT_SIZES:
        resized = resize_image(transparent_source, size)
        output_path = os.path.join(OUTPUT_DIR, f"logo-transparent-{size}x{size}.png")
        resized.save(output_path, "PNG", optimize=True, quality=95)
        print(f"  Created: logo-transparent-{size}x{size}.png ({resized.size[0]}x{resized.size[1]})")

    # Save full size logo-transparent.png
    transparent_source.save(os.path.join(OUTPUT_DIR, "logo-transparent.png"), "PNG", optimize=True, quality=95)
    print(f"  Created: logo-transparent.png ({transparent_source.size[0]}x{transparent_source.size[1]})")

    print("\n✓ All logo files generated successfully!")

if __name__ == "__main__":
    main()
