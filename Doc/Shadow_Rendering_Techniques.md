# 阴影渲染技术详解

## 目录
1. [基础阴影映射技术](#基础阴影映射技术)
2. [软阴影技术](#软阴影技术) 
3. [级联阴影技术](#级联阴影技术)
4. [屏幕空间阴影技术](#屏幕空间阴影技术)
5. [性能优化](#性能优化)

## 基础阴影映射技术

### 传统阴影映射(Shadow Mapping)
Shadow Mapping是实时渲染中最基础和广泛使用的阴影技术。其基本原理是从光源视角渲染场景深度图,然后在最终渲染时比较当前片段到光源的距离与深度图中存储的最近距离,以此判断片段是否在阴影中。

#### 实现步骤
1. 从光源视角渲染深度图
2. 在片段着色器中进行深度比较
3. 应用阴影偏移避免自遮挡

```glsl
// 深度图生成的顶点着色器
void VSMain(float4 position : POSITION) {
    float4 positionLS = mul(lightViewProj, position);
    gl_Position = positionLS;
}

// 深度图采样的片段着色器 
float ShadowCalculation(float4 fragPosLightSpace) {
    // 执行透视除法
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    // 变换到[0,1]范围
    projCoords = projCoords * 0.5 + 0.5;
    // 获取深度图中最近的深度
    float closestDepth = texture(shadowMap, projCoords.xy).r;
    // 获取当前片段深度
    float currentDepth = projCoords.z;
    // 应用偏移量
    float bias = 0.005;
    // 判断是否在阴影中
    float shadow = currentDepth - bias > closestDepth ? 1.0 : 0.0;
    return shadow;
}
```

### 阴影偏移(Shadow Bias)
阴影偏移是解决阴影失真(Shadow Acne)的关键技术。

#### 主要偏移方法
1. 固定偏移量
2. 基于表面法线的动态偏移
3. 基于接收者斜率的自动偏移

```glsl
// 动态偏移计算
float calculateBias(vec3 normal, vec3 lightDir) {
    float minBias = 0.005;
    float maxBias = 0.05;
    float bias = max(maxBias * (1.0 - dot(normal, lightDir)), minBias);
    return bias;
}
```

### 基本PCF实现
PCF(Percentage Closer Filtering)是一种基础的软阴影技术,通过对深度图进行多次采样并平均结果来实现。

```glsl
float PCF(sampler2D shadowMap, vec3 projCoords, float bias) {
    float shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
    
    for(int x = -1; x <= 1; ++x) {
        for(int y = -1; y <= 1; ++y) {
            float pcfDepth = texture(shadowMap, projCoords.xy + vec2(x, y) * texelSize).r;
            shadow += projCoords.z - bias > pcfDepth ? 1.0 : 0.0;
        }
    }
    
    shadow /= 9.0;
    return shadow;
}
```

## 软阴影技术

### 优化的PCF实现
优化的PCF采样通过使用硬件过滤功能和优化的采样模式来提高性能和质量。

#### 主要优化方法
1. 使用硬件双线性PCF
2. 泊松圆盘采样
3. 可变大小的采样核

```glsl
// 使用硬件双线性PCF的优化实现
float OptimizedPCF(sampler2DShadow shadowMap, vec3 projCoords) {
    vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
    float result = 0.0;
    
    // 使用2x2硬件过滤
    for(int x = -2; x <= 2; ++x) {
        for(int y = -2; y <= 2; ++y) {
            vec2 offset = vec2(x,y) * texelSize;
            result += texture(shadowMap, vec3(projCoords.xy + offset, projCoords.z));
        }
    }
    
    return result / 25.0;
}
```

### PCSS(Percentage Closer Soft Shadows)
PCSS通过估计遮挡物到接收者的距离来实现可变大小的软阴影。

#### 实现步骤
1. 遮挡物搜索
2. 半影大小计算
3. PCF过滤

```glsl
float PCSS(sampler2D shadowMap, vec3 projCoords) {
    // 1. 遮挡物搜索
    float blockerDepth = FindBlockerDepth(shadowMap, projCoords);
    
    // 2. 半影大小计算
    float penumbraSize = (projCoords.z - blockerDepth) * lightSize / blockerDepth;
    
    // 3. PCF过滤
    return PCFFilter(shadowMap, projCoords, penumbraSize);
}
```

### VSM和EVSM
VSM(Variance Shadow Maps)和EVSM(Exponential VSM)通过存储深度的统计信息来实现高质量的软阴影。

#### 特点
1. 支持硬件过滤
2. 可以预过滤阴影图
3. 需要更多的存储空间
4. 可能出现光泄漏

```glsl
// VSM实现
vec2 VSM(sampler2D shadowMap, vec3 projCoords) {
    vec2 moments = texture(shadowMap, projCoords.xy).xy;
    float mean = moments.x;
    float variance = max(moments.y - moments.x * moments.x, 0.0);
    
    float d = projCoords.z - mean;
    float pMax = variance / (variance + d * d);
    
    return vec2(mean, pMax);
}
```

## 级联阴影技术

### 级联分区策略
CSM(Cascaded Shadow Maps)通过将视锥体分割成多个区域,对每个区域使用不同分辨率的阴影图来优化阴影质量。

#### 分区方法
1. 对数分区
2. 线性分区
3. 混合分区
4. PSSM(Parallel-Split Shadow Maps)

```cpp
// 计算级联分割点
void CalculateCascadeSplits(float nearClip, float farClip, float lambda, int numCascades, float* splits) {
    float ratio = farClip / nearClip;
    
    for(int i = 0; i < numCascades; i++) {
        float p = (i + 1) / float(numCascades);
        float log = nearClip * pow(ratio, p);
        float uniform = nearClip + (farClip - nearClip) * p;
        float d = lambda * (log - uniform) + uniform;
        splits[i] = d;
    }
}
```

### 投影矩阵优化
优化级联阴影的投影矩阵可以提高阴影质量和稳定性。

#### 优化方法
1. 视锥体裁剪
2. 投影对齐
3. 稳定化处理

### 级联过渡处理
处理级联之间的过渡可以避免可见的阴影跳变。

#### 过渡技术
1. 级联混合
2. 深度基础混合
3. UV空间混合

```glsl
// 级联混合实现
float BlendCascades(float shadow1, float shadow2, float blendFactor) {
    return mix(shadow1, shadow2, blendFactor);
}
```

## 屏幕空间阴影技术

### SSAO(Screen Space Ambient Occlusion)
SSAO通过分析屏幕空间的深度信息来模拟环境光遮蔽。

#### 实现步骤
1. 采样深度和法线缓冲
2. 在半球内生成随机采样点
3. 计算遮蔽因子
4. 模糊处理

```glsl
// SSAO片段着色器
float CalculateSSAO(vec2 texCoord, vec2 screenSize) {
    // 获取当前片段的位置和法线
    vec3 fragPos = GetWorldPosFromDepth(texCoord);
    vec3 normal = texture(normalTex, texCoord).xyz;
    
    // 生成采样核心
    const int KERNEL_SIZE = 64;
    vec3 kernel[KERNEL_SIZE];
    GenerateHemisphereSamples(kernel, KERNEL_SIZE);
    
    // 计算遮蔽
    float occlusion = 0.0;
    for(int i = 0; i < KERNEL_SIZE; i++) {
        // 获取采样点位置
        vec3 samplePos = fragPos + kernel[i] * radius;
        
        // 投影到屏幕空间
        vec4 offset = vec4(samplePos, 1.0);
        offset = projMatrix * offset;
        offset.xyz /= offset.w;
        offset.xyz = offset.xyz * 0.5 + 0.5;
        
        // 采样深度
        float sampleDepth = texture(depthTex, offset.xy).r;
        
        // 比较深度
        float rangeCheck = smoothstep(0.0, 1.0, radius / abs(fragPos.z - sampleDepth));
        occlusion += (sampleDepth <= samplePos.z ? 1.0 : 0.0) * rangeCheck;
    }
    
    return 1.0 - (occlusion / KERNEL_SIZE);
}

// 生成半球采样点
void GenerateHemisphereSamples(out vec3[64] kernel) {
    for(int i = 0; i < 64; ++i) {
        kernel[i] = vec3(
            random(-1.0, 1.0), 
            random(-1.0, 1.0),
            random(0.0, 1.0)
        );
        kernel[i] = normalize(kernel[i]);
        
        // 使采样更偏向法线方向
        float scale = float(i) / 64.0;
        scale = lerp(0.1, 1.0, scale * scale);
        kernel[i] *= scale;
    }
}
```

#### 优化技巧
1. 使用旋转噪声纹理
```glsl
vec3 GetRandomVec(vec2 texCoord) {
    vec2 noiseScale = screenSize / 4.0; // 4x4噪声纹理
    return normalize(texture(noiseTex, texCoord * noiseScale).xyz);
}
```

2. 双边模糊
```glsl
vec4 BilateralBlur(sampler2D ssaoInput, vec2 texCoord, vec2 dir) {
    vec4 color = vec4(0.0);
    vec2 off1 = vec2(1.3333333333333333) * dir;
    
    color += texture2D(ssaoInput, texCoord) * 0.29411764705882354;
    color += texture2D(ssaoInput, texCoord + off1) * 0.35294117647058826;
    color += texture2D(ssaoInput, texCoord - off1) * 0.35294117647058826;
    
    return color;
}
```

### 屏幕空间软阴影
通过分析深度缓冲来生成软阴影效果。

#### 实现步骤
1. 光线步进搜索
2. 遮挡物分析
3. 软阴影计算

```glsl
float ScreenSpaceSoftShadow(vec3 worldPos, vec3 lightDir) {
    // 将世界空间位置转换到屏幕空间
    vec4 screenPos = projMatrix * vec4(worldPos, 1.0);
    screenPos.xyz /= screenPos.w;
    vec2 uv = screenPos.xy * 0.5 + 0.5;
    
    // 光线步进参数
    const int STEPS = 16;
    vec2 stepSize = lightDir.xy * (1.0 / STEPS);
    float stepDepth = lightDir.z * (1.0 / STEPS);
    
    // 光线步进搜索
    float shadow = 1.0;
    float currentDepth = screenPos.z;
    vec2 currentUV = uv;
    
    for(int i = 0; i < STEPS; i++) {
        currentUV += stepSize;
        currentDepth += stepDepth;
        
        // 采样深度图
        float sampledDepth = texture(depthTex, currentUV).r;
        
        // 如果采样点在遮挡物内部
        if(currentDepth > sampledDepth) {
            float delta = currentDepth - sampledDepth;
            shadow = min(shadow, delta * 10.0);
        }
    }
    
    return smoothstep(0.0, 1.0, shadow);
}
```

### 接触阴影(Contact Shadows)
接触阴影通过屏幕空间射线步进来补充传统阴影映射的细节。

#### 实现步骤
1. 射线步进搜索
2. 深度比较
3. 阴影衰减

```glsl
float ContactShadow(vec2 uv, float depth, vec3 lightDir) {
    // 将光照方向转换到屏幕空间
    vec3 screenLightDir = normalize((viewMatrix * vec4(lightDir, 0.0)).xyz);
    vec2 stepUV = screenLightDir.xy * (1.0 / float(CONTACT_SHADOW_STEPS));
    
    // 射线步进参数
    const float stepSize = 0.001; // 步进大小
    const float maxDistance = 0.1; // 最大搜索距离
    
    vec2 currentUV = uv;
    float currentDepth = depth;
    float shadow = 1.0;
    
    // 射线步进搜索
    for(int i = 0; i < CONTACT_SHADOW_STEPS; i++) {
        currentUV += stepUV;
        
        // 检查UV是否有效
        if(currentUV.x < 0.0 || currentUV.x > 1.0 || 
           currentUV.y < 0.0 || currentUV.y > 1.0)
            break;
            
        float sampledDepth = texture(depthTex, currentUV).r;
        
        // 深度比较
        if(sampledDepth < currentDepth) {
            // 计算遮挡强度
            float delta = currentDepth - sampledDepth;
            float occlusion = 1.0 - smoothstep(0.0, 0.1, delta);
            
            // 距离衰减
            float distance = length(currentUV - uv);
            float attenuation = 1.0 - smoothstep(0.0, maxDistance, distance);
            
            shadow = min(shadow, occlusion * attenuation);
        }
        
        currentDepth += stepSize;
    }
    
    return shadow;
}
```

#### 性能优化
1. 自适应步进
```glsl
float AdaptiveContactShadow(vec2 uv, float depth, vec3 lightDir) {
    // 基于深度值调整步进大小
    float adaptiveStepSize = stepSize * (1.0 + depth * 2.0);
    
    // 基于屏幕空间位置调整采样数量
    float screenEdgeFade = 
        (1.0 - pow(abs(uv.x - 0.5) * 2.0, 2.0)) * 
        (1.0 - pow(abs(uv.y - 0.5) * 2.0, 2.0));
    
    int steps = int(float(CONTACT_SHADOW_STEPS) * screenEdgeFade);
    
    // ... 射线步进实现 ...
}
```

2. 降采样处理
```glsl
vec2 CalculateContactShadowUV(vec2 uv) {
    // 使用较低分辨率的深度图
    return uv * CONTACT_SHADOW_SCALE;
}
```


### 性能优化方案

#### 动态分辨率
```csharp
public class DynamicResolutionShadow : MonoBehaviour
{
    public float targetFrameRate = 60f;
    public float resolutionScaleMin = 0.5f;
    public float resolutionScaleMax = 1.0f;
    
    private void UpdateResolution()
    {
        float currentFPS = 1.0f / Time.deltaTime;
        float scale = Mathf.Lerp(resolutionScaleMin, resolutionScaleMax,
            currentFPS / targetFrameRate);
            
        // 更新阴影图分辨率
        Shader.SetGlobalFloat("_ShadowResolutionScale", scale);
    }
}
```

#### 阴影距离剔除
```csharp
public class ShadowDistanceCull : MonoBehaviour
{
    public float maxShadowDistance = 100f;
    public float fadeRange = 10f;
    
    private void UpdateShadowDistance(Camera camera)
    {
        Vector3 cameraPos = camera.transform.position;
        
        // 更新每个光源的阴影距离
        foreach(var light in activeLights)
        {
            float distance = Vector3.Distance(cameraPos, light.transform.position);
            float shadowStrength = 1.0f - Mathf.Clamp01(
                (distance - maxShadowDistance) / fadeRange);
                
            light.shadowStrength = shadowStrength;
        }
    }
}
```

## 性能优化

### GPU优化技术

#### 计算着色器优化
1. 深度图降采样
```glsl
#version 430
layout(local_size_x = 8, local_size_y = 8) in;

layout(binding = 0) uniform sampler2D inputDepth;
layout(binding = 1) writeonly uniform image2D outputDepth;

shared float localDepth[8][8];

void main() {
    ivec2 texCoord = ivec2(gl_GlobalInvocationID.xy);
    ivec2 localCoord = ivec2(gl_LocalInvocationID.xy);
    
    // 加载深度值到共享内存
    localDepth[localCoord.x][localCoord.y] = texelFetch(inputDepth, texCoord, 0).r;
    barrier();
    
    // 2x2降采样
    if(localCoord.x % 2 == 0 && localCoord.y % 2 == 0) {
        float maxDepth = max(max(
            localDepth[localCoord.x][localCoord.y],
            localDepth[localCoord.x + 1][localCoord.y]),
            max(
            localDepth[localCoord.x][localCoord.y + 1],
            localDepth[localCoord.x + 1][localCoord.y + 1]));
            
        imageStore(outputDepth, texCoord / 2, vec4(maxDepth));
    }
}
```

2. 视锥体剔除
```glsl
#version 430
layout(local_size_x = 256) in;

struct DrawCommand {
    uint indexCount;
    uint instanceCount;
    uint firstIndex;
    uint baseVertex;
    uint baseInstance;
};

layout(std430, binding = 0) buffer DrawCommands {
    DrawCommand commands[];
};

layout(std430, binding = 1) buffer VisibilityBuffer {
    uint visibility[];
};

void main() {
    uint idx = gl_GlobalInvocationID.x;
    if(visibility[idx] == 0) {
        commands[idx].instanceCount = 0;
    }
}
```

#### 异步计算优化
```cpp
class ShadowRenderer {
public:
    void RenderShadows() {
        // 开始异步计算深度图生成
        AsyncCompute([this]() {
            for(int cascade = 0; cascade < NUM_CASCADES; cascade++) {
                GenerateShadowMap(cascade);
            }
        });
        
        // 主线程继续其他工作
        RenderScene();
        
        // 等待阴影计算完成
        WaitForAsyncCompute();
        
        // 应用阴影
        ApplyShadows();
    }
private:
    void AsyncCompute(std::function<void()> task) {
        // 实现平台特定的异步计算
    }
};
```

#### 缓存优化
1. 纹理缓存优化
```cpp
void OptimizeTextureCache() {
    // 设置纹理采样器状态
    D3D12_SAMPLER_DESC samplerDesc = {};
    samplerDesc.Filter = D3D12_FILTER_MIN_MAG_MIP_LINEAR;
    samplerDesc.AddressU = D3D12_TEXTURE_ADDRESS_MODE_BORDER;
    samplerDesc.AddressV = D3D12_TEXTURE_ADDRESS_MODE_BORDER;
    samplerDesc.ComparisonFunc = D3D12_COMPARISON_FUNC_LESS_EQUAL;
    
    // 优化纹理布局
    D3D12_RESOURCE_DESC texDesc = {};
    texDesc.Format = DXGI_FORMAT_R32_FLOAT;
    texDesc.Width = SHADOW_MAP_SIZE;
    texDesc.Height = SHADOW_MAP_SIZE;
    texDesc.MipLevels = 1;
    texDesc.SampleDesc.Count = 1;
    texDesc.Layout = D3D12_TEXTURE_LAYOUT_ROW_MAJOR; // 优化内存访问
}
```

2. 常量缓存优化
```cpp
struct alignas(256) ShadowConstants {
    Matrix lightViewProj[MAX_CASCADES];
    Vector4 cascadeSplits;
    Vector4 shadowMapSize;
    Vector4 filterSize;
};

void UpdateShadowConstants() {
    // 使用常量缓存更新阴影数据
    D3D12_CONSTANT_BUFFER_VIEW_DESC cbvDesc = {};
    cbvDesc.BufferLocation = constantBuffer->GetGPUVirtualAddress();
    cbvDesc.SizeInBytes = sizeof(ShadowConstants);
}
```

### 移动平台优化

#### 内存带宽优化
1. 压缩技术
```cpp
void ConfigureShadowMapCompression() {
    // 使用硬件支持的压缩格式
    DXGI_FORMAT compressedFormat = DXGI_FORMAT_R16_UNORM; // 16位深度格式
    
    // 或使用更高压缩率的格式
    if(deviceSupportsBC7) {
        compressedFormat = DXGI_FORMAT_BC7_UNORM;
    }
}
```

2. 分块渲染
```cpp
void TiledShadowRendering() {
    const int TILE_SIZE = 128;
    
    for(int y = 0; y < height; y += TILE_SIZE) {
        for(int x = 0; x < width; x += TILE_SIZE) {
            // 设置视口为当前块
            D3D12_VIEWPORT viewport = {
                (float)x, (float)y,
                (float)TILE_SIZE, (float)TILE_SIZE,
                0.0f, 1.0f
            };
            commandList->RSSetViewports(1, &viewport);
            
            // 渲染当前块的阴影
            RenderShadowTile(x, y, TILE_SIZE);
        }
    }
}
```

#### 动态质量调整
```cpp
class AdaptiveShadowQuality {
public:
    void UpdateQuality(float fps, float targetFps) {
        if(fps < targetFps * 0.9f) {
            // 降低质量
            DecreaseQuality();
        } else if(fps > targetFps * 1.1f) {
            // 提高质量
            IncreaseQuality();
        }
    }
    
private:
    void DecreaseQuality() {
        // 降低阴影图分辨率
        shadowMapResolution *= 0.5f;
        // 减少级联数量
        numCascades = max(numCascades - 1, MIN_CASCADES);
        // 简化过滤
        filterQuality = SIMPLE_PCF;
    }
};
```

### 调试和性能分析

#### 性能分析工具
```cpp
class ShadowProfiler {
public:
    void BeginFrame() {
        QueryPerformanceCounter(&frameStart);
    }
    
    void EndFrame() {
        QueryPerformanceCounter(&frameEnd);
        
        // 计算各阶段耗时
        shadowMapGenTime = GetStageTime(STAGE_SHADOW_GEN);
        shadowFilterTime = GetStageTime(STAGE_SHADOW_FILTER);
        
        // 更新统计信息
        UpdateStats();
    }
    
    void DisplayStats() {
        ImGui::Begin("Shadow Profiler");
        ImGui::Text("Shadow Map Generation: %.2f ms", shadowMapGenTime);
        ImGui::Text("Shadow Filtering: %.2f ms", shadowFilterTime);
        ImGui::Text("Total Shadow Time: %.2f ms", GetTotalTime());
        ImGui::End();
    }
    
private:
    LARGE_INTEGER frameStart, frameEnd;
    float shadowMapGenTime;
    float shadowFilterTime;
    
    struct StageTimings {
        float min, max, avg;
        vector<float> history;
    };
    map<string, StageTimings> stats;
};
```

#### 常见问题排查
1. 性能问题检查表
```cpp
void DiagnoseShadowPerformance() {
    // 检查阴影图分辨率
    if(shadowMapSize > platformMaxSize) {
        LogWarning("Shadow map size exceeds platform maximum");
    }
    
    // 检查采样数量
    if(pcfSamples > 16) {
        LogWarning("High PCF sample count may impact performance");
    }
    
    // 检查级联配置
    if(cascadeCount > 4 && IsMobilePlatform()) {
        LogWarning("Too many cascades for mobile platform");
    }
    
    // 检查内存使用
    size_t shadowMemory = CalculateShadowMemoryUsage();
    if(shadowMemory > memoryBudget) {
        LogError("Shadow memory usage exceeds budget");
    }
}
```

2. 调试可视化
```glsl
vec4 DebugShadowCascades(vec3 worldPos) {
    int cascadeIndex = SelectCascadeIndex(worldPos);
    
    // 为每个级联使用不同颜色
    vec4 cascadeColors[4] = {
        vec4(1,0,0,1), // 红色 - 第一级联
        vec4(0,1,0,1), // 绿色 - 第二级联
        vec4(0,0,1,1), // 蓝色 - 第三级联
        vec4(1,1,0,1)  // 黄色 - 第四级联
    };
    
    return cascadeColors[cascadeIndex];
}
```

#### 性能预算管理
```cpp
class ShadowBudgetManager {
public:
    void SetBudget(float maxGPUTime, size_t maxMemory) {
        gpuBudget = maxGPUTime;
        memoryBudget = maxMemory;
    }
    
    bool IsWithinBudget() {
        float currentGPUTime = MeasureGPUTime();
        size_t currentMemory = CalculateMemoryUsage();
        
        return currentGPUTime <= gpuBudget && 
               currentMemory <= memoryBudget;
    }
    
    void OptimizeForBudget() {
        while(!IsWithinBudget()) {
            // 逐步降低质量直到满足预算
            if(!ReduceQuality()) {
                LogError("Cannot meet performance budget");
                break;
            }
        }
    }
    
private:
    float gpuBudget;
    size_t memoryBudget;
    
    bool ReduceQuality() {
        // 按优先级降低质量
        if(canReduceResolution) {
            ReduceShadowMapResolution();
            return true;
        }
        if(canReduceCascades) {
            ReduceCascadeCount();
            return true;
        }
        if(canSimplifyFiltering) {
            SimplifyFiltering();
            return true;
        }
        return false;
    }
};
```

## 实践建议

### 技术选择指南

#### 场景类型
1. 室外大场景
- 推荐使用CSM
- 考虑使用EVSM处理软阴影
- 重点优化远处阴影质量

2. 室内场景
- 可使用单张阴影图
- 重点优化接触阴影
- 考虑使用PCSS提升质量

3. 角色特写
- 使用高分辨率阴影图
- 添加额外的角色专用光源
- 考虑使用光线追踪阴影

#### 平台特化
1. 高端PC
```cpp
void ConfigureHighEndSettings() {
    ShadowConfig config;
    config.shadowMapSize = 4096;
    config.cascadeCount = 4;
    config.softShadowTechnique = TECHNIQUE_PCSS;
    config.enableRayTracedShadows = true;
    config.contactShadowsEnabled = true;
}
```

2. 移动设备
```cpp
void ConfigureMobileSettings() {
    ShadowConfig config;
    config.shadowMapSize = 1024;
    config.cascadeCount = 2;
    config.softShadowTechnique = TECHNIQUE_PCF;
    config.useShadowMaskOptimization = true;
    config.enableTiledRendering = true;
}
```

### 性能与质量平衡

#### 质量等级设置
```cpp
enum class ShadowQuality {
    Low,
    Medium,
    High,
    Ultra
};

struct ShadowQualityPreset {
    int shadowMapSize;
    int cascadeCount;
    int pcfSamples;
    bool useVSM;
    bool useContactShadows;
};

ShadowQualityPreset GetQualityPreset(ShadowQuality quality) {
    switch(quality) {
        case ShadowQuality::Low:
            return {512, 2, 4, false, false};
        case ShadowQuality::Medium:
            return {1024, 3, 8, false, true};
        case ShadowQuality::High:
            return {2048, 4, 16, true, true};
        case ShadowQuality::Ultra:
            return {4096, 4, 32, true, true};
    }
}
```

#### 动态调整策略
```cpp
class QualityManager {
public:
    void UpdateQuality(float fps, float gpuTime) {
        // 性能监控
        if(IsPerformanceCritical()) {
            // 临时降低质量
            ReduceShadowQuality();
        }
        
        // 定期评估和调整
        qualityAssessmentTimer += deltaTime;
        if(qualityAssessmentTimer >= ASSESSMENT_INTERVAL) {
            EvaluateAndAdjustQuality();
            qualityAssessmentTimer = 0;
        }
    }
    
private:
    void EvaluateAndAdjustQuality() {
        float averageFPS = GetAverageFPS();
        float shadowGPUTime = GetShadowRenderTime();
        
        if(CanIncreaseQuality(averageFPS, shadowGPUTime)) {
            IncreaseQualityStep();
        } else if(NeedsQualityReduction(averageFPS, shadowGPUTime)) {
            DecreaseQualityStep();
        }
    }
};
```

### 调试技巧

#### 可视化工具
```cpp
class ShadowDebugger {
public:
    void RenderDebugView() {
        switch(currentDebugView) {
            case DebugView::CascadeSplits:
                RenderCascadeVisualization();
                break;
            case DebugView::ShadowMap:
                RenderShadowMapView();
                break;
            case DebugView::PCFKernel:
                RenderPCFKernelView();
                break;
        }
    }
    
    void RenderImGuiControls() {
        ImGui::Begin("Shadow Debug");
        
        if(ImGui::CollapsingHeader("Visualization")) {
            ImGui::RadioButton("Cascade Splits", &currentDebugView, 
                             DebugView::CascadeSplits);
            ImGui::RadioButton("Shadow Map", &currentDebugView, 
                             DebugView::ShadowMap);
            ImGui::RadioButton("PCF Kernel", &currentDebugView, 
                             DebugView::PCFKernel);
        }
        
        if(ImGui::CollapsingHeader("Settings")) {
            ImGui::SliderFloat("Bias", &shadowBias, 0.0f, 0.01f);
            ImGui::SliderInt("PCF Samples", &pcfSamples, 4, 32);
        }
        
        ImGui::End();
    }
};
```

## 未来发展趋势

### 实时光线追踪阴影

#### 混合渲染管线
```cpp
class HybridShadowRenderer {
public:
    void RenderShadows() {
        // 根据场景复杂度和距离选择技术
        for(auto& object : scene.objects) {
            if(ShouldUseRayTracedShadows(object)) {
                RenderRayTracedShadows(object);
            } else {
                RenderTraditionalShadows(object);
            }
        }
    }
    
private:
    bool ShouldUseRayTracedShadows(const Object& obj) {
        float distanceToCamera = CalculateDistance(obj, camera);
        bool isComplexGeometry = obj.geometryComplexity > complexityThreshold;
        bool isInFocus = distanceToCamera < rayTracingRange;
        
        return isComplexGeometry && isInFocus && 
               rayTracingHardwareAvailable;
    }
};
```

#### 性能优化
```cpp
class RayTracedShadowOptimizer {
public:
    void OptimizeRayTracing() {
        // 光线预算管理
        int raysPerPixel = CalculateOptimalRayCount();
        
        // 降噪设置
        denoiser.ConfigureForShadows(
            raysPerPixel,
            temporalAccumulation,
            spatialFiltering
        );
        
        // 混合设置
        hybridRenderer.SetRayTracingRatio(
            CalculateRayTracingWorkload()
        );
    }
    
private:
    int CalculateOptimalRayCount() {
        float performanceHeadroom = GetGPUHeadroom();
        float sceneComplexity = EvaluateSceneComplexity();
        
        return static_cast<int>(
            baseRayCount * performanceHeadroom * sceneComplexity
        );
    }
};
```

### 机器学习优化

#### 智能采样
```cpp
class MLShadowOptimizer {
public:
    void OptimizeSampling() {
        // 使用ML模型预测最佳采样位置
        vector<vec2> samplePositions = 
            mlModel.PredictOptimalSamples(
                currentFrame,
                previousFrame,
                motionVectors
            );
            
        // 应用预测的采样模式
        shadowRenderer.SetSamplePositions(samplePositions);
    }
    
    void TrainModel() {
        // 收集训练数据
        TrainingData data;
        data.AddSample(
            currentFrame,
            groundTruth,
            currentSamples,
            qualityMetrics
        );
        
        // 定期更新模型
        if(data.GetSize() >= BATCH_SIZE) {
            mlModel.Update(data);
            data.Clear();
        }
    }
};
```

#### 实时优化
```cpp
class RealTimeOptimizer {
public:
    void UpdateParameters() {
        // 实时参数优化
        ShadowParameters params = mlModel.PredictOptimalParameters(
            sceneComplexity,
            viewportChanges,
            performanceMetrics
        );
        
        // 平滑参数变化
        currentParams = SmoothTransition(currentParams, params);
        
        // 应用新参数
        shadowRenderer.UpdateParameters(currentParams);
    }
    
private:
    ShadowParameters SmoothTransition(
        const ShadowParameters& current,
        const ShadowParameters& target) {
        // 使用指数移动平均平滑参数变化
        float alpha = 0.3f;
        return Lerp(current, target, alpha);
    }
};
```

### 新硬件特性支持

#### 网格着色器应用
```cpp
class MeshShaderShadowRenderer {
public:
    void SetupMeshShaderPipeline() {
        // 配置网格着色器管线
        D3D12_MESH_SHADER_PIPELINE_STATE_DESC pipelineDesc = {};
        pipelineDesc.MS = meshShaderBytecode;
        pipelineDesc.AS = amplificationShaderBytecode;
        
        // 设置阴影渲染状态
        pipelineDesc.RasterizerState.DepthBias = 100;
        pipelineDesc.RasterizerState.SlopeScaledDepthBias = 1.0f;
        
        device->CreateMeshShaderPipeline(&pipelineDesc, &pipeline);
    }
    
    void DispatchMeshShadows() {
        // 使用网格着色器渲染阴影
        commandList->SetPipelineState(pipeline);
        commandList->DispatchMesh(
            meshletCount,
            instanceCount,
            1
        );
    }
};
```

#### 可变速率着色
```cpp
class VariableRateShadowRenderer {
public:
    void ConfigureVRS() {
        // 设置阴影渲染的可变采样率
        D3D12_SHADING_RATE_COMBINER combiners[2] = {
            D3D12_SHADING_RATE_COMBINER_MIN,
            D3D12_SHADING_RATE_COMBINER_SUM
        };
        
        commandList->RSSetShadingRate(
            D3D12_SHADING_RATE_2X2,
            combiners
        );
    }
    
    void UpdateShadingRates() {
        // 根据场景内容更新着色率
        for(int y = 0; y < tileCountY; y++) {
            for(int x = 0; x < tileCountX; x++) {
                float importance = CalculateTileImportance(x, y);
                D3D12_SHADING_RATE rate = 
                    SelectShadingRate(importance);
                    
                shadingRateImage[y * tileCountX + x] = rate;
            }
        }
    }
};
```

## 参考资源

### 技术文章
1. [Real-Time Rendering - Shadow Algorithms](http://www.realtimerendering.com/Real-Time_Rendering_4th-Shadow_Algorithms.pdf)
2. [Cascaded Shadow Maps (GPU Gems 3)](https://developer.nvidia.com/gpugems/gpugems3/part-ii-light-and-shadows/chapter-10-parallel-split-shadow-maps-programmable-gpus)
3. [Hybrid Ray Traced Shadows](https://developer.nvidia.com/blog/hybrid-ray-traced-shadows/)
4. [The Theory of Stochastic Soft Shadow Mapping](https://casual-effects.com/research/Yuksel2019Stochastic/index.html)

### 工具和库
1. [NVIDIA Shadow Playground](https://developer.nvidia.com/shadowplay)
2. [Intel Shadow Library](https://www.intel.com/content/www/us/en/developer/articles/tool/intel-shadow-library.html)
3. [AMD FidelityFX SSSR](https://gpuopen.com/fidelityfx-sssr/)

### 学习资源
1. [Shadow Mapping Tutorial Series](https://learnopengl.com/Advanced-Lighting/Shadows/Shadow-Mapping)
2. [Unreal Engine Shadow Documentation](https://docs.unrealengine.com/en-US/RenderingAndGraphics/Lighting/Shadows/)
3. [Unity Shadow Guide](https://docs.unity3d.com/Manual/Shadows.html)

### 研究论文
1. Percentage-Closer Soft Shadows (SIGGRAPH 2005)
2. Variance Shadow Maps (SIGGRAPH 2006)
3. Moment Shadow Mapping (SIGGRAPH 2015)
4. Real-Time Ray Traced Shadows (SIGGRAPH 2019)