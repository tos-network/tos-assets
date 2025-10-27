# TOS Network Banners

This directory contains TOS Network banners in various formats and color schemes.

## Banner Specifications

- **Dimensions**: 950 x 370 pixels
- **Logo Size**: 250 x 250 pixels
- **Font**: Helvetica, 90pt
- **Text**: "TOS Network"
- **Layout**: Logo on left with 60px padding, text follows with 40px spacing

## Available Variants

### 1. Black Background + White Logo
- **PNG**: `png/black_background_white_logo.png`
- **SVG**: `svg/black_background_white_logo.svg`

### 2. White Background + Black Logo
- **PNG**: `png/white_background_black_logo.png`
- **SVG**: `svg/white_background_black_logo.svg`

### 3. Green Background + Black Logo
- **PNG**: `png/green_background_black_logo.png`
- **SVG**: `svg/green_background_black_logo.svg`

### 4. Gradient Green Background + White Logo
- **PNG**: `png/gradient_green_background_white_logo.png`
- **SVG**: `svg/gradient_green_background_white_logo.svg`

### 5. Transparent Background + Black Logo
- **PNG**: `png/transparent_background_black_logo.png`
- **SVG**: `svg/transparent_background_black_logo.svg`

### 6. Transparent Background + White Logo
- **PNG**: `png/transparent_background_white_logo.png`
- **SVG**: `svg/transparent_background_white_logo.svg`

### 7. Transparent Background + Green Logo
- **PNG**: `png/transparent_background_green_logo.png`
- **SVG**: `svg/transparent_background_green_logo.svg`

## Generation Scripts

### PNG Banner Generator
**Script**: `update_banners.py`

Generates PNG format banners with the TOS logo and "TOS Network" text.

**Requirements**:
- Python 3.7+
- Pillow (PIL)

**Usage**:
```bash
python3 update_banners.py
```

**Features**:
- Automatic size calculation based on content
- Multiple color schemes
- Gradient background support
- High-quality image rendering

### SVG Banner Generator
**Script**: `generate_svg_banners_v2.py`

Generates SVG format banners with embedded logo (base64 encoded).

**Requirements**:
- Python 3.7+
- Standard library only (no external dependencies)

**Usage**:
```bash
python3 generate_svg_banners_v2.py
```

**Features**:
- Embedded base64 logo (no external dependencies)
- Color filters for logo adjustment
- Gradient background support
- Scalable vector graphics

## Preview

Open `test_svg.html` in a web browser to preview all banner variants:

```bash
open test_svg.html
```

## Customization

### Changing Banner Text
Edit the `TEXT` variable in either script:

```python
TEXT = "Your Custom Text"
```

### Adjusting Dimensions
Modify the configuration variables:

```python
LOGO_SIZE = (250, 250)  # Logo dimensions
PADDING = 60            # Padding around content
FONT_SIZE = 90          # Text font size
```

### Adding New Color Schemes

In `update_banners.py`, add to `BACKGROUND_COLORS`:

```python
BACKGROUND_COLORS = {
    'your_custom_name': ((R, G, B, A), 'text_color'),
    # ...
}
```

In `generate_svg_banners_v2.py`, add to `CONFIGS`:

```python
CONFIGS = {
    'your_custom_name': {
        'bg_color': '#HEXCOLOR',
        'text_color': '#HEXCOLOR',
        'logo_brightness': 1.0,
        'logo_invert': False
    },
    # ...
}
```

## Notes

- SVG files have embedded logo data, making them ~153KB each but fully self-contained
- PNG files are optimized and range from 48-58KB
- All banners use the logo from: `/Users/tomisetsu/tos-network/tos-assets/tos/logo512x512.png`
- Transparent background variants are best viewed on a checkered/patterned background

## License

© TOS Network. All rights reserved.
