# 角色湿润效果材质制作教程

## 概述
本教程将指导您在虚幻引擎中创建角色淋雨后的湿润效果材质。这种效果可以让角色表面呈现出真实的潮湿感，包括水滴、水流和整体的湿润表现。

## 所需资源

### 必要贴图
1. 水滴法线贴图 (Water Droplets Normal Map)
   - 下载链接：[Textures.com - Water Drops Normal](https://www.textures.com/download/waterdrops0012/12547)
   - 存放路径：`/Game/shirun/Textures/WaterDrops_N`

2. 水流图案贴图 (Water Flow Pattern)
   - 下载链接：[Textures.com - Water Flow](https://www.textures.com/download/waterflow0004/12789)
   - 存放路径：`/Game/shirun/Textures/WaterFlow_M`

3. 噪声贴图 (Noise Texture)
   - 下载链接：[cc0textures.com - Noise](https://cc0textures.com/view?id=Noise001)
   - 存放路径：`/Game/shirun/Textures/Noise_M`

### 材质参数设置

#### 基础参数
- Base Color: 原始颜色略微调暗（乘以0.9）
- Roughness: 动态调整，干燥区域0.8，湿润区域0.2
- Normal: 原始法线与水滴法线混合
- Metallic: 略微提升（+0.1）

## 材质制作步骤

### 1. 创建基础材质
1. 在内容浏览器中导航到 `/Game/shirun/Materials`
2. 右键点击 > 材质 > 创建新材质，命名为 "M_CharacterWet"
3. 双击打开材质编辑器

### 2. 设置材质基本属性
```
材质属性设置：
- Shading Model: Default Lit
- Two Sided: False
- Use Material Attributes: False
```

### 3. 创建湿润效果节点网络

#### A. 水滴效果
```
1. 添加Water Drops法线贴图
- 添加TextureSample节点
- 设置Texture为WaterDrops_N
- 连接到Normal输入端

2. 创建水滴动画
- 添加Panner节点
- Speed X = 0.01
- Speed Y = 0.02
- 连接到TextureSample的UVs输入端
```

#### B. 湿润度控制
```
1. 添加MaterialParameterScalar节点
- 命名为"Wetness"
- 默认值设为0
- 范围0-1

2. 使用Lerp节点混合干湿状态
- Lerp(干燥参数, 湿润参数, Wetness)
```

#### C. 水流效果
```
1. 添加Water Flow贴图
- 使用TextureSample节点
- 连接到法线混合节点

2. 创建流动效果
- 添加Panner节点
- Speed Y = -0.1
- 连接到Water Flow贴图的UVs
```

### 4. 完整节点网络
![材质节点网络](material_nodes_reference.jpg)

## 使用方法

### 材质实例设置
1. 在材质资源上右键 > 创建材质实例
2. 设置以下参数：
   - Wetness: 0-1之间调节（0为干燥，1为最湿润）
   - DropletIntensity: 控制水滴效果强度
   - FlowSpeed: 控制水流速度

### 在角色上应用
1. 选择角色网格体
2. 在材质槽中应用创建的材质实例
3. 通过蓝图或关卡蓝图控制Wetness参数

## 性能优化建议
1. 使用适当的贴图分辨率（建议1024x1024）
2. 考虑在低配置下禁用水滴动画
3. 使用材质LOD降低远处细节

## 常见问题解决
1. 如果水滴效果不明显，检查法线贴图强度
2. 如果性能下降，考虑减少动态参数数量
3. 如果效果不自然，调整Roughness过渡范围

## 进阶优化
1. 添加温度参数控制水滴蒸发
2. 实现由上至下的渐变湿润效果
3. 添加与环境的交互效果

## 参考资源
1. 虚幻引擎官方文档：[材质系统文档](https://docs.unrealengine.com/5.0/zh-CN/unreal-engine-materials/)
2. 视频教程：[Creating Wet Surface Effects](https://www.youtube.com/watch?v=fYGOZYST-oQ)
3. 社区资源：[Unreal Engine Forums - Wet Material Discussion](https://forums.unrealengine.com/)