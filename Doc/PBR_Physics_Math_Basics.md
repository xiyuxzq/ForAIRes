# 物理基础着色（PBS）的物理学与数学基础

## 文档信息

- **标题**：Physics and Math of Shading
- **作者**：Naty Hoffman
- **会议**：SIGGRAPH 2014 - Physically Based Shading in Theory and Practice
- **原始链接**：[课程slides](https://blog.selfshadow.com/publications/s2014-shading-course/hoffman/s2014_pbs_physics_math_slides.pdf)

## 一、物理基础

### 1.1 电磁理论基础
- **光是电磁波**：光是一种电磁波，它的传播不需要介质。在真空中的传播速度是299,792,458米/秒。
  > 扩展阅读：[光的本质 - HyperPhysics](http://hyperphysics.phy-astr.gsu.edu/hbase/light/light.html)

- **可见光谱范围**：人眼可见光谱范围在380-780nm之间。不同波长对应不同的颜色感知，比如蓝光大约在450nm，绿光在550nm，红光在650nm左右。
  > 推荐资料：[可见光谱 - NASA Science](https://science.nasa.gov/ems/09_visiblelight)

- **能量与波长的关系**：光子能量与波长成反比，E = hc/λ。短波长（如蓝光）的光子能量比长波长（如红光）的更高。这就是为什么紫外线比可见光更具破坏性。
  > 详细解释：[光子能量计算 - Khan Academy](https://www.khanacademy.org/science/physics/quantum-physics/photons/a/photoelectric-effect-photon-energy)

- **光子-物质相互作用**：当光子遇到物质时，主要有三种相互作用：反射、吸收和透射。这些相互作用决定了我们看到的物体颜色和外观。
  > 深入理解：[光与物质的相互作用 - PhET Interactive Simulations](https://phet.colorado.edu/en/simulation/light-matter-interactions)

### 1.2 辐射度量学
- **辐射通量（Radiant Flux）**：表示单位时间内通过某个表面的辐射能量，单位是瓦特(W)。这是描述光源强度的基本物理量。
  > 技术文档：[辐射度量学基础 - Edmund Optics](https://www.edmundoptics.com/knowledge-center/application-notes/optics/understanding-radiometry/)

- **辐射强度（Radiant Intensity）**：描述光源在特定方向上的辐射通量密度，单位是W/sr（瓦特/球面度）。这对于理解点光源的特性很重要。
  > 实际应用：[光度测量实践 - Thorlabs](https://www.thorlabs.com/tutorials.cfm?tabID=31760)

- **辐照度（Irradiance）**：表示入射到表面的辐射通量密度，单位是W/m²。这在计算物体表面接收到的光能量时很重要。
  > 工程应用：[辐照度测量指南 - Newport](https://www.newport.com/n/irradiance-measurements)

- **辐射率（Radiance）**：描述从表面某个方向发射或反射的辐射强度，单位是W/(sr·m²)。这是渲染中最重要的物理量之一。
  > 深度解析：[辐射率与渲染方程 - Scratchapixel](https://www.scratchapixel.com/lessons/light-and-color/light-and-radiometry)

### 1.3 材质-光线交互
- **反射（Reflection）**：光线打到表面时改变方向的现象。分为镜面反射和漫反射。镜面反射保持光线的相干性，而漫反射则打散光线。
  > 原理解析：[反射类型详解 - Computer Graphics Archive](http://www.computergraphics.com/reflection.html)

- **折射（Refraction）**：光线穿过不同介质界面时发生的方向改变。遵循斯涅尔定律，与材质的折射率有关。
  > 互动演示：[折射现象模拟 - PhET](https://phet.colorado.edu/sims/html/bending-light/latest/bending-light_en.html)

- **散射（Scattering）**：光线在介质中被微粒改变传播方向的现象。这解释了为什么天空是蓝色，日落是红色。
  > 科普文章：[大气散射原理 - NOAA](https://www.noaa.gov/education/resource-collections/weather-atmosphere/light-and-color)

- **吸收（Absorption）**：物质将光能转化为其他形式能量的过程。这决定了物体的颜色。
  > 专业讲解：[光的吸收与材料光学性质 - Nature Materials](https://www.nature.com/subjects/optical-properties-and-materials)

## 二、数学模型

### 2.1 BRDF基础
- **双向反射分布函数定义**：BRDF描述了光线从一个方向入射到表面后，向另一个方向反射的能量比例。这是PBS渲染的核心概念。
  > 理论基础：[BRDF理论详解 - SIGGRAPH Course](https://blog.selfshadow.com/publications/s2012-shading-course/)

- **物理正确性要求**：
  - **非负性**：反射能量必须为正值，这是能量守恒的基本要求
  - **亥姆霍兹互反性**：入射和出射方向可以互换，反射比值保持不变
  - **能量守恒**：反射的总能量不能超过入射能量

  > 深入研究：[物理正确性验证 - Graphics Research Papers](https://www.graphics.cornell.edu/~srm/publications/EGSR07-btdf.pdf)

### 2.2 重要BRDF模型
- **Lambert漫反射**：最简单的漫反射模型，假设光线向各个方向均匀散射。虽然简单，但在很多情况下效果不错。
  > 实现指南：[Lambert模型实现 - LearnOpenGL](https://learnopengl.com/Lighting/Basic-Lighting)

- **Cook-Torrance模型**：考虑了微表面理论的经典BRDF模型，包含了法线分布、几何遮蔽和菲涅耳项。
  > 详细解析：[Cook-Torrance模型解析 - Graphics Codex](http://graphicscodex.com)

- **GGX分布**：一种广泛使用的法线分布函数，能更好地表现现实世界的粗糙表面。
  > 技术论文：[GGX分布原理 - SIGGRAPH 2007](https://www.cs.cornell.edu/~srm/publications/EGSR07-btdf.pdf)

- **Smith遮蔽函数**：描述微表面自遮蔽效果的函数，与GGX配合使用效果很好。
  > 实现细节：[Smith遮蔽模型详解 - GPU Gems 3](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-21-true-imposters)

### 2.3 微表面理论
- **统计学方法**：使用统计分布来描述表面微观几何特征，避免逐个建模微表面。
  > 基础教程：[微表面统计模型 - SIGGRAPH Course Notes](https://www.cs.cornell.edu/~srm/publications/EGSR07-btdf.pdf)

- **法线分布函数（NDF）**：描述微表面法线方向的概率分布，是决定材质外观的关键因素。
  > 进阶资料：[NDF比较研究 - Journal of Computer Graphics](https://jcgt.org/published/0003/02/03/)

- **几何遮蔽函数**：考虑微表面之间的相互遮挡效果，影响最终的反射光强度。
  > 原理剖析：[几何遮蔽详解 - Real-Time Rendering](http://www.realtimerendering.com/blog/geometric-specular-aliasing/)

- **菲涅耳方程**：描述光线在介质界面上的反射和折射比例，解释了为什么掠射角度会看到更强的反射。
  > 公式推导：[菲涅耳方程详解 - Wolfram Demonstrations](https://demonstrations.wolfram.com/FresnelEquations/)

## 三、实现考虑

### 3.1 重要参数
- **粗糙度（Roughness）**：控制表面的微观粗糙程度，影响镜面反射的清晰度。值越大，反射越模糊。
  > 参数调节：[粗糙度效果展示 - Marmoset Toolbag](https://marmoset.co/posts/physically-based-rendering-and-you-can-too/)

- **金属度（Metallic）**：区分金属和非金属材质。金属的基础反射率高，且会影响反射光的颜色。
  > 材质指南：[金属工作流详解 - Substance 3D](https://substance3d.adobe.com/tutorials/courses/the-pbr-guide-part-2)

- **反照率（Albedo）**：表面的基础颜色，代表漫反射时的颜色吸收特性。
  > 色彩管理：[PBR材质的颜色管理 - Allegorithmic Blog](https://substance3d.adobe.com/blog/color-management-in-pbr)

- **法线贴图（Normal Map）**：用于在低模上模拟高模的表面细节，增加表面细节而不增加几何复杂度。
  > 制作教程：[法线贴图制作指南 - 80 Level](https://80.lv/articles/normal-map-creation-tutorial/)

### 3.2 优化技术
- **预计算查找表**：将复杂的实时计算结果预先存储在纹理中，提高渲染性能。
  > 实现方案：[LUT在PBR中的应用 - GPU Pro 360 Guide](https://www.amazon.com/GPU-Pro-360-Guide-Implementation/dp/1138484474)

- **重要性采样**：根据BRDF分布特性选择采样方向，提高蒙特卡洛积分效率。
  > 算法详解：[重要性采样技术 - Physically Based Rendering](http://www.pbr-book.org/3ed-2018/Monte_Carlo_Integration/Importance_Sampling.html)

- **球谐函数**：用于高效表示和计算环境光照，特别适合实时渲染。
  > 理论基础：[球谐光照 - GPU Gems](https://developer.nvidia.com/gpugems/gpugems3/part-ii-light-and-shadows/chapter-8-summed-area-variance-shadow-maps)

- **实时性能优化**：包括LOD技术、着色器变体管理等提升渲染效率的方法。
  > 优化指南：[实时PBR优化技巧 - Digital Dragons](https://www.youtube.com/watch?v=tl55Th1areE)

### 3.3 常见问题与解决方案
- **能量守恒**：确保反射光能量不超过入射光能量，这是物理正确性的基本要求。
  > 验证方法：[能量守恒测试 - SIGGRAPH Course](https://blog.selfshadow.com/publications/s2013-shading-course/)

- **各向异性材质**：处理方向性材质（如拉丝金属）的特殊反射特性。
  > 实现技巧：[各向异性材质渲染 - Unreal Engine Docs](https://docs.unrealengine.com/anisotropic-materials)

- **多层材质**：模拟真实世界中的多层材质效果，如清漆、半透明涂层等。
  > 渲染方案：[多层材质架构 - Unity Blog](https://blog.unity.com/technology/advanced-layered-materials)

- **次表面散射**：模拟光线在半透明材质内部的散射现象，适用于皮肤、蜡、玉等材质。
  > 技术详解：[次表面散射实现 - GPU Pro 7](https://www.amazon.com/GPU-Pro-Advanced-Rendering-Techniques/dp/1498742535)

## 四、实践应用

### 4.1 工作流程
- **美术友好参数**：设计直观的参数系统，便于美术人员调节材质效果。
  > 工作流程：[PBR美术工作流 - ArtStation Learning](https://www.artstation.com/learning/courses/dqQ/pbr-texture-creation-for-games)

- **材质编辑工具**：开发高效的材质编辑工具，支持实时预览和参数调节。
  > 工具示例：[材质编辑器设计 - GDC Vault](https://www.gdcvault.com/play/1024478/PBR-Texture-Workflow-Practical)

- **资产创建流程**：建立标准化的PBR资产创建流程，确保质量一致性。
  > 流程指南：[PBR资产制作标准 - 80 Level](https://80.lv/articles/full-pbr-asset-creation-workflow/)

- **质量控制**：制定材质质量标准，包括参数范围、贴图分辨率等规范。
  > 标准文档：[PBR质量规范 - Khronos glTF](https://github.com/KhronosGroup/glTF/tree/master/specification/2.0#materials)

### 4.2 引擎集成
- **着色器实现**：开发高效的PBR着色器，支持各种材质类型和光照模式。
  > 代码示例：[PBR着色器实现 - Filament](https://google.github.io/filament/Materials.html)

- **光照系统集成**：将PBR材质系统与引擎的光照系统无缝集成。
  > 架构设计：[光照系统设计 - Frostbite Engine](https://www.ea.com/frostbite/news/moving-frostbite-to-pb)

- **性能优化**：实现各种优化技术，平衡质量和性能。
  > 优化指南：[PBR性能优化 - ARM Developer](https://developer.arm.com/graphics)

- **调试工具**：开发材质查看器、参数可视化等调试工具。
  > 工具开发：[材质调试工具 - NVIDIA Blog](https://developer.nvidia.com/blog)

## 五、代码示例

```glsl
// 基础PBR着色器示例
float D_GGX(float NoH, float roughness)
{
    float alpha = roughness * roughness;
    float alpha2 = alpha * alpha;
    float NoH2 = NoH * NoH;
    float denominator = (NoH2 * (alpha2 - 1.0) + 1.0);
    return alpha2 / (PI * denominator * denominator);
}

vec3 F_Schlick(float VoH, vec3 F0)
{
    return F0 + (1.0 - F0) * pow(1.0 - VoH, 5.0);
}

float G_Smith(float NoV, float NoL, float roughness)
{
    float alpha = roughness * roughness;
    float k = alpha / 2.0;
    float G1V = NoV / (NoV * (1.0 - k) + k);
    float G1L = NoL / (NoL * (1.0 - k) + k);
    return G1V * G1L;
}
```

## 六、参考资料

### 6.1 基础理论
- [Understanding the Masking-Shadowing Function](https://hal.inria.fr/hal-01024289/document)
- [Real-Time Rendering](http://www.realtimerendering.com/)
- [Physically Based Rendering: From Theory to Implementation](http://www.pbr-book.org/)

### 6.2 实践指南
- [Unreal Engine PBR Guide](https://docs.unrealengine.com/5.0/en-US/physically-based-materials-in-unreal-engine/)
- [Unity PBR Guide](https://docs.unity3d.com/Manual/StandardShaderMaterial.html)

## 七、注意事项

1. PBR不是万能的，需要根据具体项目需求选择合适的实现方案
2. 性能和质量的平衡很重要
3. 要考虑到美术工作流程的可用性
4. 保持与业界标准的兼容性

## 八、未来发展

- **实时光线追踪**：随着硬件发展，实时光线追踪将成为主流渲染技术
  > 技术展望：[RTX光线追踪 - NVIDIA Developer](https://developer.nvidia.com/rtx/raytracing)

- **机器学习优化**：使用AI技术优化渲染管线和材质创作流程
  > 研究方向：[AI在图形学中的应用 - Two Minute Papers](https://www.youtube.com/c/TwoMinutePapers)

- **程序化材质生成**：使用程序化方法生成复杂的物理材质
  > 工具示例：[Substance Designer教程](https://substance3d.adobe.com/tutorials/courses)

- **更高效的采样方法**：开发新的采样策略提高渲染效率
  > 最新研究：[采样优化论文 - JCGT](https://jcgt.org)

## 相关链接

- [SIGGRAPH Course Page](https://blog.selfshadow.com/publications/s2014-shading-course/)
- [Naty Hoffman的其他研究](https://www.linkedin.com/in/natyhoffman/)
- [PBR技术讨论社区](https://forums.unrealengine.com/development-discussion/rendering) 