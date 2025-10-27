#!/usr/bin/env python3
"""
Generate SVG format banners - Embed logo using PNG to base64
"""

import os
import base64
import xml.etree.ElementTree as ET

# Configuration
BANNER_WIDTH = 950
BANNER_HEIGHT = 370
LOGO_SIZE = (250, 250)
PADDING = 60
TEXT = "TOS Network"
FONT_SIZE = 90

# SVG configuration
CONFIGS = {
    'black_background_white_logo': {
        'bg_color': '#000000',
        'text_color': '#FFFFFF',
        'logo_brightness': 2.0,  # Brighten logo
        'logo_invert': True
    },
    'white_background_black_logo': {
        'bg_color': '#FFFFFF',
        'text_color': '#000000',
        'logo_brightness': 1.0,
        'logo_invert': False
    },
    'green_background_black_logo': {
        'bg_color': '#008000',
        'text_color': '#000000',
        'logo_brightness': 1.0,
        'logo_invert': False
    },
    'transparent_background_black_logo': {
        'bg_color': 'none',
        'text_color': '#000000',
        'logo_brightness': 1.0,
        'logo_invert': False
    },
    'transparent_background_white_logo': {
        'bg_color': 'none',
        'text_color': '#FFFFFF',
        'logo_brightness': 2.0,
        'logo_invert': True
    },
    'transparent_background_green_logo': {
        'bg_color': 'none',
        'text_color': '#00FF00',
        'logo_brightness': 1.0,
        'logo_invert': False
    },
}

def load_logo_as_base64(logo_path):
    """Load logo and convert to base64"""
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    return base64.b64encode(logo_data).decode('utf-8')

def create_svg_banner(name, config, logo_base64):
    """Create SVG banner"""
    svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'xmlns:xlink': 'http://www.w3.org/1999/xlink',
        'width': str(BANNER_WIDTH),
        'height': str(BANNER_HEIGHT),
        'viewBox': f'0 0 {BANNER_WIDTH} {BANNER_HEIGHT}'
    })

    # Add definitions section (for filters)
    defs = ET.SubElement(svg, 'defs')

    # If gradient background
    if name == 'gradient_green_background_white_logo':
        gradient = ET.SubElement(defs, 'linearGradient', {
            'id': 'greenGradient',
            'x1': '0%',
            'y1': '0%',
            'x2': '100%',
            'y2': '0%'
        })
        ET.SubElement(gradient, 'stop', {
            'offset': '0%',
            'style': 'stop-color:#003200;stop-opacity:1'
        })
        ET.SubElement(gradient, 'stop', {
            'offset': '100%',
            'style': 'stop-color:#00C864;stop-opacity:1'
        })
        # Add background rectangle
        ET.SubElement(svg, 'rect', {
            'width': str(BANNER_WIDTH),
            'height': str(BANNER_HEIGHT),
            'fill': 'url(#greenGradient)'
        })
        text_color = '#FFFFFF'
        logo_brightness = 2.0
        logo_invert = True
    else:
        # Add background (if not transparent)
        if config['bg_color'] != 'none':
            ET.SubElement(svg, 'rect', {
                'width': str(BANNER_WIDTH),
                'height': str(BANNER_HEIGHT),
                'fill': config['bg_color']
            })
        text_color = config['text_color']
        logo_brightness = config['logo_brightness']
        logo_invert = config['logo_invert']

    # Add filter definition (for logo color adjustment)
    if logo_invert or logo_brightness != 1.0:
        filter_id = f'logoFilter_{name}'
        filter_elem = ET.SubElement(defs, 'filter', {'id': filter_id})

        if logo_brightness != 1.0:
            ET.SubElement(filter_elem, 'feComponentTransfer').append(
                ET.Element('feFuncR', {'type': 'linear', 'slope': str(logo_brightness)})
            )
            filter_elem[-1].append(
                ET.Element('feFuncG', {'type': 'linear', 'slope': str(logo_brightness)})
            )
            filter_elem[-1].append(
                ET.Element('feFuncB', {'type': 'linear', 'slope': str(logo_brightness)})
            )

        if logo_invert:
            ET.SubElement(filter_elem, 'feColorMatrix', {
                'type': 'matrix',
                'values': '-1 0 0 0 1  0 -1 0 0 1  0 0 -1 0 1  0 0 0 1 0'
            })

    # Add logo (as embedded base64 image)
    logo_x = PADDING
    logo_y = (BANNER_HEIGHT - LOGO_SIZE[1]) // 2

    image_attrs = {
        'x': str(logo_x),
        'y': str(logo_y),
        'width': str(LOGO_SIZE[0]),
        'height': str(LOGO_SIZE[1]),
        'xlink:href': f'data:image/png;base64,{logo_base64}'
    }

    if logo_invert or logo_brightness != 1.0:
        image_attrs['filter'] = f'url(#{filter_id})'

    ET.SubElement(svg, 'image', image_attrs)

    # Add text
    spacing = 40
    text_x = logo_x + LOGO_SIZE[0] + spacing
    text_y = BANNER_HEIGHT // 2 + FONT_SIZE // 3  # Adjust for visual centering

    text_elem = ET.SubElement(svg, 'text', {
        'x': str(text_x),
        'y': str(text_y),
        'font-family': 'Helvetica, Arial, sans-serif',
        'font-size': str(FONT_SIZE),
        'font-weight': 'bold',
        'fill': text_color
    })
    text_elem.text = TEXT

    return svg

def save_svg(svg, filepath):
    """Save SVG file"""
    # Create XML declaration
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str += ET.tostring(svg, encoding='unicode', method='xml')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(xml_str)

def main():
    """Main function"""
    print("Starting SVG banner generation...")

    # Ensure output directory exists
    os.makedirs('svg', exist_ok=True)

    # Load logo and convert to base64
    logo_path = '/Users/tomisetsu/tos-network/tos-assets/tos/logo512x512.png'
    if not os.path.exists(logo_path):
        print(f"Error: Logo file not found: {logo_path}")
        return

    print(f"Loading logo: {logo_path}")
    logo_base64 = load_logo_as_base64(logo_path)
    print("Logo converted to base64")

    # Process each banner
    for name, config in CONFIGS.items():
        print(f"Generating: {name}")
        svg = create_svg_banner(name, config, logo_base64)
        output_path = f'svg/{name}.svg'
        save_svg(svg, output_path)
        print(f"  Saved: {output_path}")

    # Generate gradient background banner
    print("Generating: gradient_green_background_white_logo")
    svg = create_svg_banner('gradient_green_background_white_logo', {}, logo_base64)
    output_path = 'svg/gradient_green_background_white_logo.svg'
    save_svg(svg, output_path)
    print(f"  Saved: {output_path}")

    print("\nAll SVG banners generated successfully!")
    print("Logo is embedded directly in SVG files, can be used independently.")

if __name__ == '__main__':
    main()
