# 动漫眼神光Shader实现文档

## 1. 概述

本文档描述了在虚幻引擎中实现动漫风格眼神光效果的shader实现方案。眼神光是动漫角色中常见的艺术表现手法，用于增强角色的表情和情感表达。

## 2. 艺术效果参考

### 2.1 眼神光的艺术特点
- 通常出现在眼睛上方或侧面
- 用于增强角色表情和情感表达
- 可以有多种形状：圆形、星形、十字形等
- 带有发光和模糊效果
- 可能随角色情感变化而改变形状和亮度

### 2.2 常见表现形式
1. 基础圆形高光
2. 星形装饰高光
3. 十字形高光
4. 多点组合高光
5. 渐变模糊高光

## 3. 技术实现方案

### 3.1 材质层级结构

#### Base Layer (眼球基础材质)
- 材质类型：Translucent
- 关键设置：
  * Surface Based Translucency Lighting
  * 基础法线贴图
  * 折射率设置(约1.3)
  
#### Highlight Layer (眼神光层)
- 材质特性：
  * 自定义UV坐标系统
  * 形状遮罩控制
  * 发光和模糊效果
  * 参数化控制系统

### 3.2 Shader参数设计

#### 基础参数
- Shape (形状选择)
  * 类型：Enum
  * 选项：Circle, Star, Cross, Custom
  * 默认值：Circle
  
- Brightness (亮度)
  * 类型：Float
  * 范围：0.0 - 5.0
  * 默认值：1.0
  
- Size (大小)
  * 类型：Float
  * 范围：0.0 - 2.0
  * 默认值：0.5
  
- Blur (模糊度)
  * 类型：Float
  * 范围：0.0 - 1.0
  * 默认值：0.2
  
- Position Offset (位置偏移)
  * 类型：Vector2
  * 范围：-1.0 to 1.0
  * 默认值：(0.0, 0.0)

#### 高级参数
- Color Tint (颜色色调)
  * 类型：Color
  * 默认值：White (1,1,1,1)
  
- Glow Intensity (发光强度)
  * 类型：Float
  * 范围：0.0 - 10.0
  * 默认值：2.0

### 3.3 实现步骤

1. 创建基础材质
```hlsl
// 基础材质设置
Material {
    ShadingModel = Translucent;
    BlendMode = Translucent;
    TranslucencyLightingMode = Surface;
}
```

2. 实现眼神光形状生成
```hlsl
// 圆形高光
float CircleHighlight(float2 UV, float Size, float Blur) {
    float2 center = float2(0.5, 0.5);
    float dist = length(UV - center);
    return smoothstep(Size + Blur, Size - Blur, dist);
}

// 星形高光
float StarHighlight(float2 UV, float Size, float Points, float Blur) {
    float2 center = float2(0.5, 0.5);
    float2 pos = UV - center;
    float angle = atan2(pos.y, pos.x);
    float radius = length(pos);
    float star = cos(angle * Points) * 0.5 + 0.5;
    return smoothstep(Size + Blur, Size - Blur, radius - star * Size);
}
```

3. 添加发光效果
```hlsl
float3 AddGlow(float3 Color, float Intensity, float Shape) {
    return Color + Shape * Intensity;
}
```

4. 实现参数控制系统
```hlsl
struct ShaderParams {
    float4 Color;
    float Brightness;
    float Size;
    float Blur;
    float2 Offset;
    float GlowIntensity;
};
```

### 3.4 性能优化建议

1. 纹理优化
- 使用合适的纹理大小(建议512x512或1024x1024)
- 合理设置纹理压缩格式

2. Shader复杂度控制
- 避免过多的数学运算
- 使用查找表(LUT)优化复杂计算
- 合理设置材质更新频率

3. 内存管理
- 合理使用材质实例
- 及时释放未使用的资源

## 4. 使用指南

### 4.1 基础设置
1. 创建新材质
2. 设置材质类型为Translucent
3. 启用Surface Based Translucency
4. 设置基础参数

### 4.2 常见问题解决
1. 高光不显示
- 检查材质是否正确设置为Translucent
- 确认Surface Based Translucency已启用
- 检查参数值是否在有效范围内

2. 高光位置偏移
- 检查UV坐标设置
- 调整Position Offset参数

3. 发光效果异常
- 检查Glow Intensity参数
- 确认后处理效果是否正确启用

## 5. 参考资料

1. 虚幻引擎材质文档
2. 动漫眼神光艺术参考
3. Shader编程指南

## 6. 更新历史

### Version 1.0 (2024-03-21)
- 初始版本
- 基础功能实现
- 文档编写