#!/usr/bin/env python3
"""
生成SVG格式的banner
"""

import os
import xml.etree.ElementTree as ET

# 配置
BANNER_WIDTH = 950
BANNER_HEIGHT = 370
LOGO_SIZE = (250, 250)
PADDING = 60
TEXT = "TOS Network"
FONT_SIZE = 90

# SVG配置
CONFIGS = {
    'black_background_white_logo': {
        'bg_color': '#000000',
        'text_color': '#FFFFFF',
        'logo_filter': 'brightness(0) invert(1)'  # 将logo变为白色
    },
    'white_background_black_logo': {
        'bg_color': '#FFFFFF',
        'text_color': '#000000',
        'logo_filter': 'none'
    },
    'green_background_black_logo': {
        'bg_color': '#008000',
        'text_color': '#000000',
        'logo_filter': 'none'
    },
    'transparent_background_black_logo': {
        'bg_color': 'none',
        'text_color': '#000000',
        'logo_filter': 'none'
    },
    'transparent_background_white_logo': {
        'bg_color': 'none',
        'text_color': '#FFFFFF',
        'logo_filter': 'brightness(0) invert(1)'
    },
    'transparent_background_green_logo': {
        'bg_color': 'none',
        'text_color': '#00FF00',
        'logo_filter': 'hue-rotate(120deg)'
    },
}

def create_svg_banner(name, config):
    """创建SVG banner"""
    svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'xmlns:xlink': 'http://www.w3.org/1999/xlink',
        'width': str(BANNER_WIDTH),
        'height': str(BANNER_HEIGHT),
        'viewBox': f'0 0 {BANNER_WIDTH} {BANNER_HEIGHT}'
    })

    # 添加定义部分（用于渐变）
    defs = ET.SubElement(svg, 'defs')

    # 如果是渐变背景
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
        # 添加背景矩形
        ET.SubElement(svg, 'rect', {
            'width': str(BANNER_WIDTH),
            'height': str(BANNER_HEIGHT),
            'fill': 'url(#greenGradient)'
        })
        text_color = '#FFFFFF'
        logo_filter = 'brightness(0) invert(1)'
    else:
        # 添加背景（如果不是透明的）
        if config['bg_color'] != 'none':
            ET.SubElement(svg, 'rect', {
                'width': str(BANNER_WIDTH),
                'height': str(BANNER_HEIGHT),
                'fill': config['bg_color']
            })
        text_color = config['text_color']
        logo_filter = config['logo_filter']

    # 添加logo（作为嵌入的图片引用）
    logo_x = PADDING
    logo_y = (BANNER_HEIGHT - LOGO_SIZE[1]) // 2

    # 使用相对路径引用logo SVG
    logo_ref = '../tos/logo512x512.svg'

    image_attrs = {
        'x': str(logo_x),
        'y': str(logo_y),
        'width': str(LOGO_SIZE[0]),
        'height': str(LOGO_SIZE[1]),
        'xlink:href': logo_ref
    }

    if logo_filter != 'none':
        image_attrs['style'] = f'filter: {logo_filter}'

    ET.SubElement(svg, 'image', image_attrs)

    # 添加文字
    spacing = 40
    text_x = logo_x + LOGO_SIZE[0] + spacing
    text_y = BANNER_HEIGHT // 2 + FONT_SIZE // 3  # 调整以实现视觉居中

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
    """保存SVG文件"""
    # 创建XML声明
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_str += ET.tostring(svg, encoding='unicode', method='xml')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(xml_str)

def main():
    """主函数"""
    print("开始生成SVG banners...")

    # 确保输出目录存在
    os.makedirs('svg', exist_ok=True)

    # 处理每个banner
    for name, config in CONFIGS.items():
        print(f"正在生成: {name}")
        svg = create_svg_banner(name, config)
        output_path = f'svg/{name}.svg'
        save_svg(svg, output_path)
        print(f"  已保存: {output_path}")

    # 生成渐变背景banner
    print("正在生成: gradient_green_background_white_logo")
    svg = create_svg_banner('gradient_green_background_white_logo', {})
    output_path = 'svg/gradient_green_background_white_logo.svg'
    save_svg(svg, output_path)
    print(f"  已保存: {output_path}")

    print("\n所有SVG banners已生成完成！")

if __name__ == '__main__':
    main()
