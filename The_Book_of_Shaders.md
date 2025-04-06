# The Book of Shaders 学习笔记

## 一、着色器基础

### 1.1 什么是着色器
着色器是在GPU上运行的小程序。它们接收不同类型的输入(uniforms, textures, buffers等)，并为每个像素生成颜色输出。着色器的主要特点是所有像素可以并行处理,这使得它们非常高效。

代码示例:
```glsl
// 基础片段着色器示例
void main() {
    // 设置像素颜色为红色
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
```

应用场景:
- 实时图形渲染
- 后期处理效果
- 程序化纹理生成

相关资源:
- [Shader基础教程](https://shader-tutorial.dev/basics/fragment-shader/)
- [GLSL教程](https://www.lighthouse3d.com/tutorials/glsl-tutorial/)

### 1.2 着色器类型
主要有两种类型:
- 顶点着色器(Vertex Shader): 处理顶点位置和属性
  ```glsl
  // 顶点着色器示例
  attribute vec3 position;
  uniform mat4 modelViewMatrix;
  uniform mat4 projectionMatrix;
  
  void main() {
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
  ```
- 片段着色器(Fragment Shader): 处理像素颜色计算
  ```glsl
  // 片段着色器示例
  uniform vec2 u_resolution;
  uniform float u_time;
  
  void main() {
      vec2 st = gl_FragCoord.xy/u_resolution.xy;
      vec3 color = vec3(st.x, st.y, abs(sin(u_time)));
      gl_FragColor = vec4(color, 1.0);
  }
  ```

### 1.3 GLSL语言基础
GLSL是OpenGL的着色语言,主要特点:
- 类C语法
- 内置数据类型: 
  - vec2: 2D向量
  - vec3: 3D向量
  - vec4: 4D向量
  - mat2/3/4: 2x2/3x3/4x4矩阵
- 内置函数:
  ```glsl
  float a = sin(3.14); // 三角函数
  float b = pow(2.0, 3.0); // 幂函数
  vec3 c = mix(vec3(1.0), vec3(0.0), 0.5); // 线性插值
  ```

性能优化建议:
1. 减少分支语句(if/else)
2. 使用内置函数而不是自己实现
3. 尽量复用计算结果
4. 注意精度限定符的使用(lowp, mediump, highp)

## 二、基础图形绘制

### 2.1 颜色表示
在GLSL中使用vec4表示颜色:
```glsl
vec4 color = vec4(1.0, 0.0, 0.0, 1.0); // 红色
// r,g,b,a 分量范围均为 0.0 - 1.0
```

### 2.2 形状绘制
使用数学函数和距离场(SDF)绘制基本形状:
```glsl
float circle(vec2 st, vec2 center, float radius) {
    vec2 dist = st - center;
    return smoothstep(radius-(radius*0.01), radius+(radius*0.01), dot(dist,dist)*4.0);
}

void main() {
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    vec3 color = vec3(circle(st, vec2(0.5), 0.3));
    gl_FragColor = vec4(color, 1.0);
}
```

### 2.3 图案和纹理
通过数学函数和噪声创建各种图案:
```glsl
// 基础噪声函数
float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

// Perlin噪声实现
float noise(vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);
    
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x) + (c - a)* u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}
```

## 三、高级技术

### 3.1 光照计算
实现基本光照模型:
```glsl
vec3 calculateLighting(vec3 normal, vec3 lightDir) {
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    return ambient + diffuse;
}
```

### 3.2 后期处理
图像滤镜和特效实现:
```glsl
// 高斯模糊示例
vec4 blur(sampler2D image, vec2 uv, vec2 resolution) {
    vec4 color = vec4(0.0);
    vec2 off1 = vec2(1.3846153846) / resolution;
    vec2 off2 = vec2(3.2307692308) / resolution;
    
    color += texture2D(image, uv) * 0.2270270270;
    color += texture2D(image, uv + off1) * 0.3162162162;
    color += texture2D(image, uv - off1) * 0.3162162162;
    color += texture2D(image, uv + off2) * 0.0702702703;
    color += texture2D(image, uv - off2) * 0.0702702703;
    
    return color;
}
```

### 3.3 程序化纹理
使用数学函数生成纹理:
```glsl
// 棋盘格纹理
float checkerboard(vec2 st, float size) {
    vec2 pos = floor(st * size);
    return mod(pos.x + pos.y, 2.0);
}

// 木纹纹理
float wood(vec2 st) {
    float noise = noise(st * 10.0);
    return fract(noise * 10.0);
}
```

## 四、高级渲染技术

### 4.1 光线步进(Ray Marching)
光线步进是一种高级渲染技术,通过数学函数定义场景几何体:

```glsl
// 基础球体SDF(有符号距离函数)
float sphereSDF(vec3 p, vec3 center, float radius) {
    return length(p - center) - radius;
}

// 光线步进主循环
vec3 rayMarch(vec3 ro, vec3 rd) {
    float totalDistance = 0.0;
    const int STEPS = 32;
    const float MIN_DIST = 0.001;
    const float MAX_DIST = 100.0;
    
    for(int i = 0; i < STEPS; i++) {
        vec3 pos = ro + rd * totalDistance;
        float dist = sphereSDF(pos, vec3(0.0), 1.0);
        
        if(dist < MIN_DIST) {
            // 计算法线和光照
            vec3 normal = calcNormal(pos);
            return shade(normal);
        }
        
        totalDistance += dist;
        if(totalDistance > MAX_DIST) break;
    }
    return vec3(0.0); // 背景色
}
```

### 4.2 PBR材质系统
基于物理的渲染实现:

```glsl
struct Material {
    vec3 albedo;
    float metallic;
    float roughness;
    float ao;
};

vec3 calculatePBR(vec3 worldPos, vec3 normal, Material material) {
    vec3 N = normalize(normal);
    vec3 V = normalize(cameraPos - worldPos);
    
    vec3 F0 = mix(vec3(0.04), material.albedo, material.metallic);
    vec3 Lo = vec3(0.0);
    
    // 计算直接光照
    for(int i = 0; i < 4; i++) {
        vec3 L = normalize(lightPositions[i] - worldPos);
        vec3 H = normalize(V + L);
        
        float NDF = DistributionGGX(N, H, material.roughness);
        float G = GeometrySmith(N, V, L, material.roughness);
        vec3 F = fresnelSchlick(max(dot(H, V), 0.0), F0);
        
        vec3 numerator = NDF * G * F;
        float denominator = 4.0 * max(dot(N, V), 0.0) * max(dot(N, L), 0.0);
        vec3 specular = numerator / max(denominator, 0.001);
        
        vec3 kS = F;
        vec3 kD = vec3(1.0) - kS;
        kD *= 1.0 - material.metallic;
        
        float NdotL = max(dot(N, L), 0.0);
        Lo += (kD * material.albedo / PI + specular) * lightColors[i] * NdotL;
    }
    
    vec3 ambient = vec3(0.03) * material.albedo * material.ao;
    return ambient + Lo;
}
```

### 4.3 高级后期处理
实现复杂的后期处理效果:

```glsl
// 景深效果
vec3 depthOfField(sampler2D tex, vec2 uv, float focusPoint, float aperture) {
    vec3 color = vec3(0.0);
    float blurAmount = abs(texture2D(depthTex, uv).r - focusPoint) * aperture;
    
    for(int i = 0; i < SAMPLES; i++) {
        vec2 offset = poissonDisk[i] * blurAmount;
        color += texture2D(tex, uv + offset).rgb;
    }
    return color / float(SAMPLES);
}

// 全局光照
vec3 calculateGI(vec3 pos, vec3 normal) {
    vec3 indirectLight = vec3(0.0);
    for(int i = 0; i < SAMPLES; i++) {
        vec3 sampleDir = sampleHemisphere(normal, i);
        indirectLight += rayMarch(pos, sampleDir);
    }
    return indirectLight / float(SAMPLES);
}
```

## 五、性能优化

### 5.1 着色器优化技巧
1. 避免动态分支
```glsl
// 不推荐
if(condition) {
    color = vec3(1.0);
} else {
    color = vec3(0.0);
}

// 推荐
color = mix(vec3(0.0), vec3(1.0), float(condition));
```

2. 数学优化
```glsl
// 不推荐
float len = sqrt(dot(v,v));

// 推荐(避免不必要的归一化)
float lenSq = dot(v,v);
if(lenSq > radius * radius) {
    // ...
}
```

### 5.2 内存优化
1. 合理使用精度限定符
```glsl
precision mediump float; // 默认精度
precision highp float;   // 需要高精度时使用
```

2. 复用计算结果
```glsl
vec3 normal = normalize(v);
float NdotL = dot(normal, lightDir);
float NdotV = dot(normal, viewDir);
```

## 学习资源
- [The Book of Shaders官网](https://thebookofshaders.com/)
- [Shadertoy](https://www.shadertoy.com/)
- [GLSL Sandbox](http://glslsandbox.com/)
- [Inigo Quilez的博客](https://iquilezles.org/)
- [Ray Marching教程](https://michaelwalczyk.com/blog-ray-marching.html)

## 实践项目
1. 基础形状绘制
   - 实现圆形、矩形等基本图形
   - 添加动画效果
   
2. 程序化图案生成
   - 实现棋盘格纹理
   - 创建渐变效果
   - 添加噪声图案
   
3. 高级渲染效果
   - 实现PBR材质系统
   - 添加光线步进效果
   - 后期处理管线搭建

## 注意事项
1. 理解GPU并行处理特性
   - 避免分支语句
   - 注意数据依赖
   
2. 注意性能优化
   - 减少纹理采样
   - 优化数学计算
   - 使用适当的精度
   
3. 多练习和实验
   - 从简单效果开始
   - 逐步增加复杂度
   - 参考他人代码学习