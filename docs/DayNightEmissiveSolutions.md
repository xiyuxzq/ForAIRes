# UE5昼夜循环中自发光材质优化方案

## 问题描述
在UE5项目中，当场景在白天和黑夜之间切换时，自发光材质在夜晚显得过于明显，影响视觉效果和沉浸感。

## 解决方案

### 方案1：Material Parameter Collection全局控制
**实现原理：**
- 创建全局Material Parameter Collection
- 根据时间设置发光强度系数
- 在材质中使用参数集合来调整发光强度

**优点：**
- 实现简单
- 性能开销小
- 易于统一管理
- 支持平滑过渡

**缺点：**
- 缺乏个体化控制
- 不够灵活

**示例代码：**
```cpp
// 在材质中：
float EmissiveIntensity = MaterialParameterCollection.EmissiveScale * BaseEmissive;
```

### 方案2：动态材质实例（Material Instance Dynamic）
**实现原理：**
- 为需要控制的物体创建动态材质实例
- 根据时间和环境分别控制每个实例的发光强度
- 可以实现更细致的控制

**优点：**
- 精确控制每个物体
- 可以实现复杂的发光效果
- 支持动态调整

**缺点：**
- 性能开销较大
- 管理复杂
- 不适合大量物体

**示例代码：**
```cpp
// 在Blueprint中：
void UpdateEmissiveIntensity(float DayTime)
{
    float IntensityScale = FMath::Lerp(NightIntensity, DayIntensity, DayTime);
    DynamicMaterial->SetScalarParameterValue("EmissiveIntensity", IntensityScale);
}
```

### 方案3：基于环境光照的自适应调整
**实现原理：**
- 获取场景环境光照强度
- 根据环境光照动态调整发光强度
- 可以结合距离因素进行调整

**优点：**
- 自动适应环境变化
- 更真实的视觉效果
- 无需手动控制

**缺点：**
- 实现较复杂
- 需要careful tuning
- 可能需要额外的性能开销

**示例代码：**
```cpp
// 在材质中：
float AmbientLight = SceneColor.rgb * (1 - DayNightBlend);
float AdaptiveEmissive = BaseEmissive * (1 + AmbientLight);
```

### 方案4：后处理体积调整
**实现原理：**
- 使用后处理体积来调整发光效果
- 可以通过Bloom和Eye Adaptation来增强效果
- 结合时间系统动态调整参数

**优点：**
- 整体效果好
- 易于调整
- 可以实现电影级效果

**缺点：**
- 影响全局效果
- 可能影响性能
- 需要谨慎调整以避免过度效果

## 业界案例分析

### 1. 赛博朋克2077
- 使用动态自发光强度
- 结合环境光照进行调整
- 实现了令人印象深刻的霓虹效果

### 2. GTA5
- 使用全局光照系统
- 动态调整发光强度
- 结合天气系统

## 建议实施方案

根据项目规模和需求，建议采用以下组合方案：

1. **中小型场景：**
   - 使用Material Parameter Collection
   - 配合简单的后处理调整
   - 重点关注性能优化

2. **大型开放场景：**
   - 结合环境光照的自适应调整
   - 对重要物体使用动态材质实例
   - 使用LOD系统优化性能

3. **性能优化建议：**
   - 使用材质LOD
   - 实现发光材质的距离衰减
   - 控制同时可见的发光物体数量

## 实现步骤

1. 创建基础系统：
   ```cpp
   // 1. 创建Material Parameter Collection
   // 2. 设置基础参数
   // 3. 创建时间管理器
   ```

2. 材质设置：
   ```cpp
   // 1. 创建基础发光材质
   // 2. 添加强度控制参数
   // 3. 实现距离衰减
   ```

3. 时间系统集成：
   ```cpp
   // 1. 实现时间更新
   // 2. 更新发光参数
   // 3. 平滑过渡处理
   ```

## 注意事项

1. 性能优化：
   - 使用材质LOD
   - 实现视距剔除
   - 控制同时可见的发光物体数量

2. 视觉效果：
   - 避免过度发光
   - 确保平滑过渡
   - 保持视觉一致性

3. 维护性：
   - 良好的参数命名
   - 清晰的结构组织
   - 完整的文档说明