# 眼神光Shader材质图示说明

## 材质图基础结构

```
[Base Material Node]
    |
    |----[Translucent Blend Mode]
    |    |----Surface Based Translucency
    |    |----Refraction Settings (1.3)
    |
    |----[Normal Map]
    |    |----Base Eye Normal
    |    |----Surface Details
    |
    |----[Eye Shine Layer]
         |----[UV Coordinates]
         |    |----Custom UV Offset
         |    |----Position Control
         |
         |----[Shape Generator]
         |    |----Circle Pattern
         |    |----Star Pattern
         |    |----Cross Pattern
         |
         |----[Effects]
              |----Blur
              |----Glow
              |----Color Tint

```

## 参数连接图

```
[Material Parameters]
    |
    |----[Shape Selection]
    |    |----Shape Type Enum
    |    |----Shape Size
    |    |----Shape Blur
    |
    |----[Position Control]
    |    |----X Offset
    |    |----Y Offset
    |
    |----[Visual Effects]
         |----Brightness
         |----Glow Intensity
         |----Color Tint
```

## UV坐标计算

```
Final UV = Base UV + Offset * (Size * Direction)

Where:
- Base UV: 原始UV坐标
- Offset: 位置偏移参数(-1 to 1)
- Size: 大小参数(0 to 2)
- Direction: 方向向量
```

## 形状生成数学公式

### 圆形
```
Circle(UV, Size, Blur) = smoothstep(Size + Blur, Size - Blur, length(UV - center))
```

### 星形
```
Star(UV, Size, Points, Blur) = 
    let angle = atan2(UV.y - 0.5, UV.x - 0.5)
    let radius = length(UV - center)
    let star = cos(angle * Points) * 0.5 + 0.5
    return smoothstep(Size + Blur, Size - Blur, radius - star * Size)
```

### 十字形
```
Cross(UV, Size, Blur) =
    let horizontal = smoothstep(Size + Blur, Size - Blur, abs(UV.y - 0.5))
    let vertical = smoothstep(Size + Blur, Size - Blur, abs(UV.x - 0.5))
    return max(horizontal, vertical)
```

## 发光效果计算

```
Glow(BaseColor, Shape, Intensity) = 
    BaseColor + Shape * Intensity * GlowColor
```

## 性能优化节点

```
[Optimization Nodes]
    |
    |----[Texture Sampling]
    |    |----Mip Level Control
    |    |----Compression Settings
    |
    |----[Computation]
         |----Pre-computed LUT
         |----Simplified Math
```

## 调试视图设置

```
[Debug Views]
    |
    |----Base UV
    |----Shape Mask
    |----Normal Map
    |----Final Composite
```

## 材质实例参数范围

```
Parameter Ranges:
- Shape Size: 0.0 - 2.0
- Blur: 0.0 - 1.0
- Brightness: 0.0 - 5.0
- Glow Intensity: 0.0 - 10.0
- Position Offset: (-1,-1) - (1,1)
```