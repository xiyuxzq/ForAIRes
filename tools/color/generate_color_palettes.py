from PIL import Image, ImageDraw, ImageFont
import os

# 配色方案数据
color_palettes = {
    "nature_embrace": ["#2C4A3E", "#E6D5C3", "#C35A38", "#462521"],
    "digital_glamour": ["#D9D9D9", "#FFFFFF", "#FF69B4"],
    "serene_escape": ["#89CFF0", "#DEA5A4", "#E6E6FA"],
    "mocha_mousse": ["#9E7967", "#EDE3D9", "#1C2915", "#CCD5C4"],
    "vintage_modern": ["#1B365D", "#7B3F00", "#F5F5DC", "#2F4F4F"],
    "minimalist": ["#FFFFFF", "#F0F0F0", "#333333", "#000000"],
    "ocean_dreams": ["#003366", "#B2D8D8", "#FF7F50", "#FFF5EE"],
    "urban_jungle": ["#808080", "#228B22", "#D35400", "#F8F8FF"],
    "tech_future": ["#1A1A1A", "#8A2BE2", "#00FFFF", "#F8F8FF"],
    "warm_sunset": ["#FFA07A", "#483D8B", "#FFB6C1", "#87CEEB"]
}

def create_color_palette_image(name, colors, width=800, height=200):
    """创建一个色板图片"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # 计算每个颜色块的宽度
    color_width = width // len(colors)
    
    # 绘制颜色块
    for i, color in enumerate(colors):
        draw.rectangle(
            [i * color_width, 0, (i + 1) * color_width, height],
            fill=color
        )
        
        # 在颜色块下方添加颜色代码
        draw.text(
            (i * color_width + 10, height - 30),
            color,
            fill='black' if sum(int(color.strip('#')[i:i+2], 16) for i in (0, 2, 4)) / 3 > 128 else 'white'
        )
    
    return img

def main():
    # 创建输出目录
    output_dir = "D:/exer/Res/color_palettes"
    os.makedirs(output_dir, exist_ok=True)
    
    # 为每个配色方案生成图片
    for name, colors in color_palettes.items():
        img = create_color_palette_image(name, colors)
        img.save(f"{output_dir}/{name}.png")
        print(f"Generated {name}.png")

if __name__ == "__main__":
    main()