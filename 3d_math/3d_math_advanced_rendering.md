# 3D数学在高级渲染技术中的应用

## 目录
1. 光线追踪系统
2. 全局光照
3. 实时阴影
4. PBR渲染
5. 后处理效果

## 1. 光线追踪系统
### 1.1 基础光线追踪器
```csharp
public class RayTracer
{
    public struct Ray
    {
        public Vector3 origin;
        public Vector3 direction;
        
        public Vector3 GetPoint(float t)
        {
            return origin + direction * t;
        }
    }
    
    public struct RayHit
    {
        public float distance;
        public Vector3 point;
        public Vector3 normal;
        public Material material;
    }
    
    public Color TraceRay(Ray ray, int depth)
    {
        if (depth <= 0) return Color.black;
        
        RayHit hit;
        if (!Scene.Intersect(ray, out hit))
            return GetEnvironmentColor(ray);
            
        // 计算直接光照
        Color directLight = CalculateDirectLighting(hit);
        
        // 计算反射
        Ray reflectedRay = new Ray
        {
            origin = hit.point + hit.normal * 0.001f,
            direction = Vector3.Reflect(ray.direction, hit.normal)
        };
        
        Color reflectedColor = TraceRay(reflectedRay, depth - 1);
        
        return directLight + reflectedColor * hit.material.reflectivity;
    }
    
    private Color CalculateDirectLighting(RayHit hit)
    {
        Color totalLight = Color.black;
        
        foreach (Light light in Scene.lights)
        {
            Vector3 lightDir = (light.position - hit.point).normalized;
            float diffuse = Mathf.Max(0, Vector3.Dot(hit.normal, lightDir));
            
            // 检查阴影
            Ray shadowRay = new Ray
            {
                origin = hit.point + hit.normal * 0.001f,
                direction = lightDir
            };
            
            if (!Scene.Intersect(shadowRay, out _))
                totalLight += light.color * diffuse;
        }
        
        return totalLight;
    }
}
```

### 1.2 路径追踪
```csharp
public class PathTracer : RayTracer
{
    public Color TracePath(Ray ray, int depth)
    {
        if (depth <= 0) return Color.black;
        
        RayHit hit;
        if (!Scene.Intersect(ray, out hit))
            return GetEnvironmentColor(ray);
            
        // 俄罗斯轮盘赌
        float survivalProbability = 0.8f;
        if (Random.value > survivalProbability)
            return Color.black;
            
        // 生成随机方向
        Vector3 randomDir = GenerateRandomDirection(hit.normal);
        Ray bounceRay = new Ray
        {
            origin = hit.point + hit.normal * 0.001f,
            direction = randomDir
        };
        
        Color incomingLight = TracePath(bounceRay, depth - 1);
        float cosTheta = Vector3.Dot(randomDir, hit.normal);
        
        return (hit.material.albedo * incomingLight * cosTheta) / 
               (survivalProbability * Mathf.PI);
    }
    
    private Vector3 GenerateRandomDirection(Vector3 normal)
    {
        // 在法线半球上生成随机方向
        float u1 = Random.value;
        float u2 = Random.value;
        
        float r = Mathf.Sqrt(u1);
        float theta = 2 * Mathf.PI * u2;
        
        float x = r * Mathf.Cos(theta);
        float y = r * Mathf.Sin(theta);
        float z = Mathf.Sqrt(1 - u1);
        
        // 将方向对齐到法线空间
        Vector3 tangent = Vector3.Cross(normal, 
            Mathf.Abs(normal.x) > 0.9f ? Vector3.up : Vector3.right);
        Vector3 bitangent = Vector3.Cross(normal, tangent);
        
        return (tangent * x + bitangent * y + normal * z).normalized;
    }
}
```

## 2. 全局光照
### 2.1 光照探针系统
```csharp
public class LightProbeSystem
{
    public struct ProbeData
    {
        public Vector3 position;
        public SphericalHarmonics3 sh;
    }
    
    private List<ProbeData> probes = new List<ProbeData>();
    
    public void BakeProbes()
    {
        foreach (var probe in probes)
        {
            SphericalHarmonics3 sh = new SphericalHarmonics3();
            
            // 在球面上采样
            for (int i = 0; i < 64; i++)
            {
                Vector3 dir = GetSphericalDirection(i);
                Color radiance = SampleEnvironment(probe.position, dir);
                
                // 投影到球谐函数
                sh.AddDirectionalLight(dir, radiance, 1.0f);
            }
            
            probe.sh = sh;
        }
    }
    
    public Color SampleProbes(Vector3 position, Vector3 normal)
    {
        // 找到最近的探针
        List<ProbeData> nearestProbes = FindNearestProbes(position);
        
        // 三线性插值
        Color result = Color.black;
        float totalWeight = 0;
        
        foreach (var probe in nearestProbes)
        {
            float weight = 1.0f / (position - probe.position).magnitude;
            totalWeight += weight;
            
            Color probeLight = probe.sh.EvaluateLight(normal);
            result += probeLight * weight;
        }
        
        return result / totalWeight;
    }
}
```

## 3. 实时阴影
### 3.1 级联阴影贴图
```csharp
public class CascadedShadowMapping
{
    private struct Cascade
    {
        public Matrix4x4 viewProjection;
        public float splitDistance;
        public RenderTexture shadowMap;
    }
    
    private Cascade[] cascades;
    
    public void UpdateCascades(Camera camera)
    {
        float nearClip = camera.nearClipPlane;
        float farClip = camera.farClipPlane;
        int cascadeCount = cascades.Length;
        
        for (int i = 0; i < cascadeCount; i++)
        {
            // 计算分割距离
            float splitStart = i == 0 ? nearClip : 
                cascades[i-1].splitDistance;
            float splitEnd = i == cascadeCount-1 ? farClip :
                CalculateSplitDistance(nearClip, farClip, i, cascadeCount);
                
            cascades[i].splitDistance = splitEnd;
            
            // 计算包围盒
            Bounds bounds = CalculateCascadeBounds(camera, splitStart, splitEnd);
            
            // 设置阴影相机
            Matrix4x4 view = CalculateLightViewMatrix();
            Matrix4x4 proj = CalculateOrthographicProjection(bounds);
            cascades[i].viewProjection = proj * view;
        }
    }
    
    private float CalculateSplitDistance(
        float near, float far, int cascadeIndex, int cascadeCount)
    {
        float lambda = 0.75f;
        float ratio = cascadeIndex / (float)cascadeCount;
        
        float uniformSplit = near + (far - near) * ratio;
        float logarithmicSplit = near * Mathf.Pow(far/near, ratio);
        
        return logarithmicSplit * lambda + uniformSplit * (1 - lambda);
    }
    
    public void RenderShadowMaps(Light light)
    {
        foreach (var cascade in cascades)
        {
            // 设置阴影相机
            Graphics.SetRenderTarget(cascade.shadowMap);
            GL.Clear(true, true, Color.white);
            
            // 渲染场景到阴影贴图
            RenderShadowCasters(cascade.viewProjection);
        }
    }
}
```

## 4. PBR渲染
### 4.1 基于物理的材质系统
```csharp
public class PBRMaterial
{
    public Color albedo;
    public float metallic;
    public float roughness;
    public Vector3 normal;
    
    public Color CalculateBRDF(
        Vector3 lightDir, 
        Vector3 viewDir, 
        Color lightColor)
    {
        Vector3 halfVector = (lightDir + viewDir).normalized;
        
        float NdotL = Mathf.Max(0, Vector3.Dot(normal, lightDir));
        float NdotV = Mathf.Max(0, Vector3.Dot(normal, viewDir));
        float NdotH = Mathf.Max(0, Vector3.Dot(normal, halfVector));
        float HdotV = Mathf.Max(0, Vector3.Dot(halfVector, viewDir));
        
        // 菲涅尔项
        Color F0 = Color.Lerp(
            new Color(0.04f, 0.04f, 0.04f), 
            albedo, 
            metallic
        );
        Color F = FresnelSchlick(HdotV, F0);
        
        // 几何项
        float G = GeometrySmith(NdotV, NdotL);
        
        // 法线分布
        float D = DistributionGGX(NdotH);
        
        // 镜面反射项
        Color specular = (F * G * D) / 
            (4.0f * NdotV * NdotL + 0.001f);
            
        // 漫反射项
        Color kD = (Color.white - F) * (1 - metallic);
        Color diffuse = kD * albedo / Mathf.PI;
        
        return (diffuse + specular) * lightColor * NdotL;
    }
    
    private float DistributionGGX(float NdotH)
    {
        float a = roughness * roughness;
        float a2 = a * a;
        float NdotH2 = NdotH * NdotH;
        
        float nom = a2;
        float denom = NdotH2 * (a2 - 1.0f) + 1.0f;
        denom = Mathf.PI * denom * denom;
        
        return nom / denom;
    }
    
    private float GeometrySmith(float NdotV, float NdotL)
    {
        float r = roughness + 1.0f;
        float k = (r * r) / 8.0f;
        
        float ggx1 = NdotV / (NdotV * (1 - k) + k);
        float ggx2 = NdotL / (NdotL * (1 - k) + k);
        
        return ggx1 * ggx2;
    }
    
    private Color FresnelSchlick(float cosTheta, Color F0)
    {
        return F0 + (Color.white - F0) * 
            Mathf.Pow(1.0f - cosTheta, 5.0f);
    }
}
```

## 5. 后处理效果
### 5.1 屏幕空间环境光遮蔽
```csharp
public class SSAO
{
    private const int SAMPLE_COUNT = 64;
    private Vector3[] sampleKernel;
    private Texture2D noiseTexture;
    
    public void Initialize()
    {
        // 生成采样核心
        sampleKernel = new Vector3[SAMPLE_COUNT];
        for (int i = 0; i < SAMPLE_COUNT; i++)
        {
            Vector3 sample = new Vector3(
                Random.Range(-1f, 1f),
                Random.Range(-1f, 1f),
                Random.Range(0f, 1f)
            ).normalized;
            
            float scale = (float)i / SAMPLE_COUNT;
            scale = Mathf.Lerp(0.1f, 1.0f, scale * scale);
            sampleKernel[i] = sample * scale;
        }
        
        // 生成噪声纹理
        GenerateNoiseTexture();
    }
    
    public void Render(
        RenderTexture source, 
        RenderTexture destination,
        Camera camera)
    {
        Material ssaoMaterial = new Material(Shader.Find("Hidden/SSAO"));
        
        ssaoMaterial.SetVectorArray("_Samples", 
            Array.ConvertAll(sampleKernel, v => (Vector4)v));
        ssaoMaterial.SetTexture("_NoiseTex", noiseTexture);
        ssaoMaterial.SetMatrix("_ProjectionMatrix", 
            camera.projectionMatrix);
        
        Graphics.Blit(source, destination, ssaoMaterial);
    }
    
    private void GenerateNoiseTexture()
    {
        const int noiseSize = 4;
        noiseTexture = new Texture2D(noiseSize, noiseSize, 
            TextureFormat.RGB24, false);
        
        Color[] noiseData = new Color[noiseSize * noiseSize];
        for (int i = 0; i < noiseSize * noiseSize; i++)
        {
            Vector3 noise = new Vector3(
                Random.Range(-1f, 1f),
                Random.Range(-1f, 1f),
                0
            ).normalized;
            
            noiseData[i] = new Color(noise.x, noise.y, noise.z);
        }
        
        noiseTexture.SetPixels(noiseData);
        noiseTexture.Apply();
    }
}
```