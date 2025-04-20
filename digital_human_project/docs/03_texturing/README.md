# 数字人材质系统规范

## 材质目标
- 实现高质量的数字人皮肤渲染
- 建立高效的PBR材质工作流
- 确保实时渲染性能
- 保证跨平台材质一致性

## 技术规范

### 1. PBR材质基础
#### 基础工作流
- 采用Metallic/Roughness工作流
- 统一色彩空间(sRGB/Linear)
- 标准化材质参数范围

#### 基础贴图
| 贴图类型 | 分辨率 | 格式 | 说明 |
|----------|--------|------|------|
| BaseColor | 4K | BC7/DXT5 | sRGB色彩空间 |
| Metallic | 2K | BC4/DXT5 | Linear色彩空间 |
| Roughness | 2K | BC4/DXT5 | Linear色彩空间 |
| Normal | 4K | BC5/DXT5 | Linear色彩空间 |
| AO | 2K | BC4/DXT5 | Linear色彩空间 |
| SSS | 2K | BC4/DXT5 | 次表面散射图 |

### 2. 皮肤材质规范
#### 必需贴图
- 皮肤基础色
- 次表面散射贴图
- 法线贴图(细节+中等+大范围)
- 皮肤光泽度
- 毛孔细节图
- 皱纹贴图

#### 参数设置
```c#
// 皮肤材质基础参数范围
Subsurface Scatter: 0.3 - 0.7
Roughness Base: 0.3 - 0.6
Normal Strength: 0.8 - 1.2
Pore Detail Strength: 0.3 - 0.6
```

### 3. 眼睛材质规范
#### 必需贴图
- 虹膜颜色图
- 巩膜贴图
- 法线贴图
- 光泽度贴图

#### 参数设置
```c#
// 眼睛材质参数范围
Cornea Roughness: 0.05 - 0.15
Iris Roughness: 0.3 - 0.5
Sclera SSS: 0.5 - 0.8
```

### 4. 头发材质规范
#### 必需贴图
- 头发基础色
- Alpha遮罩
- 法线贴图
- 光泽度贴图
- 流向贴图

#### 参数设置
```c#
// 头发材质参数范围
Hair Roughness: 0.2 - 0.6
Anisotropic Strength: 0.6 - 0.9
Specular Shift: -0.5 - 0.5
```

## 制作流程

### 1. 前期准备
- 收集参考资料
- 确定材质风格
- 准备基础贴图模板

### 2. 贴图制作
#### 皮肤贴图
1. 基础色调制作
   - 拍摄参考或收集照片
   - 调整基础肤色
   - 添加色彩变化

2. 细节制作
   - 毛孔细节
   - 皱纹细节
   - 瑕疵细节

3. 法线贴图
   - 大范围形态
   - 中等细节
   - 微观细节

#### 眼睛贴图
1. 虹膜制作
   - 基础图案
   - 深度变化
   - 细节添加

2. 巩膜制作
   - 血管纹理
   - 自然变化
   - 湿润效果

### 3. 材质设置
- 创建主要材质
- 设置材质参数
- 连接贴图节点
- 调试材质效果

## 优化指南

### 1. 贴图优化
- 合理的贴图尺寸
- 适当的压缩格式
- Mipmap设置
- 贴图合并策略

### 2. 着色器优化
- 减少计算复杂度
- 优化采样次数
- LOD策略
- 移动平台适配

### 3. 性能建议
- Draw Call控制
- 材质实例化
- 着色器变体管理
- 内存占用优化

## 常见问题

### 1. 视觉问题
- 皮肤过于塑料感
  - 调整SSS参数
  - 增加细节变化
  - 优化光泽度

- 眼睛不够真实
  - 改进反射模型
  - 调整折射参数
  - 优化视差效果

### 2. 性能问题
- 贴图内存过大
  - 优化贴图尺寸
  - 使用压缩格式
  - 合并贴图通道

- 渲染开销大
  - 简化着色器
  - 优化采样
  - 使用LOD

## 工具推荐
- Substance Painter：主要贴图制作
- Substance Designer：程序化贴图
- Photoshop：贴图调整
- 3D-Coat：烘焙贴图
- Marmoset Toolbag：材质预览

## 参考资源
1. [PBR Guide by Allegorithmic](https://substance3d.adobe.com/tutorials/courses/the-pbr-guide-part-1)
2. [Digital Human Skin Shader](https://www.artstation.com/artwork/digital-human-skin-shader)
3. [Real-Time Character Rendering](https://www.unrealengine.com/en-US/blog/real-time-character-rendering-in-unreal-engine)

## 更新记录
| 日期 | 版本 | 更新内容 | 更新人 |
|------|------|----------|--------|
| 2025-04-19 | v0.1 | 初始版本 | TA | 