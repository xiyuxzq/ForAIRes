# 虚幻引擎眼球着色器实现文档

## 1. 概述与原理

眼球着色器旨在模拟真实眼球的视觉效果，主要包括以下特性：
- 角膜反射
- 虹膜细节
- 眼球深度
- 真实感光照

### 1.1 眼球结构
眼球由多个层次组成：
- 角膜层（最外层）：透明、有光泽
- 虹膜层：决定眼睛颜色
- 瞳孔：控制光线进入
- 眼球内部：提供深度感

## 2. 材质层级结构

### 2.1 基础层
```hlsl
// 基础颜色设置
float3 baseColor = lerp(IrisColor, PupilColor, pupilMask);
```

### 2.2 角膜层
```hlsl
float3 CalculateCornealLayer(float3 Normal, float3 ViewDir)
{
    float fresnel = pow(1 - saturate(dot(Normal, ViewDir)), 5.0);
    return float3(fresnel, fresnel, fresnel);
}
```

### 2.3 视差效果
```hlsl
float2 CalculateParallax(float2 UV, float3 ViewDir, float Depth)
{
    float height = Depth * (1 - TextureSample(HeightMap, UV).r);
    float2 parallaxOffset = ViewDir.xy * height;
    return UV - parallaxOffset;
}
```

## 3. 参数设置

### 3.1 材质参数
- IrisColor (Vector3): 虹膜基础颜色
- PupilSize (Float): 瞳孔大小 [0.1 - 0.9]
- CorneaSpecular (Float): 角膜高光强度 [0.5 - 1.0]
- EyeDepth (Float): 眼球深度效果 [0.0 - 1.0]

### 3.2 纹理资源
- IrisTexture: 虹膜纹理贴图
- NormalMap: 法线贴图
- HeightMap: 高度图（用于视差）

## 4. 实现步骤

1. 创建材质
   - 新建材质实例
   - 设置混合模式为 Translucent
   - 启用 TwoSided 选项

2. 设置基础节点
   ```hlsl
   // 主材质节点
   float3 finalColor = baseColor;
   float3 normal = GetNormal();
   float3 specular = CalculateSpecular(normal, viewDir);
   ```

3. 添加角膜效果
   ```hlsl
   float3 cornea = CalculateCornealLayer(normal, viewDir);
   finalColor = lerp(finalColor, cornea, corneaIntensity);
   ```

4. 实现视差映射
   ```hlsl
   float2 parallaxUV = CalculateParallax(UV, ViewDir, EyeDepth);
   float3 irisColor = TextureSample(IrisTexture, parallaxUV).rgb;
   ```

## 5. 优化建议

1. 性能优化
   - 使用适当的纹理分辨率
   - 简化不必要的计算
   - 考虑 LOD 系统

2. 视觉优化
   - 添加色散效果
   - 考虑环境光照影响
   - 添加次表面散射

## 6. 常见问题解决

1. 高光过强
   - 调整 CorneaSpecular 参数
   - 修改 Fresnel 计算公式

2. 视差效果不明显
   - 增加 EyeDepth 值
   - 检查 HeightMap 设置

3. 性能问题
   - 减少纹理采样次数
   - 简化数学计算

## 7. 示例使用

1. 材质设置
   ```
   - 将材质应用到眼球模型
   - 调整基础参数
   - 设置适当的纹理
   ```

2. 运行时调整
   ```cpp
   // 动态调整瞳孔大小
   MaterialInstance->SetScalarParameterValue("PupilSize", newSize);
   ```

## 8. 参考资源

- 虚幻引擎材质文档
- 人眼解剖学资料
- PBR 渲染理论

## 9. 更新日志

### 版本 1.0
- 基础眼球shader实现
- 角膜反射效果
- 视差映射
- 基础文档编写