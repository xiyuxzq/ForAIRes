# 3D数学基础：几何学（第9-10章）

## 第9章 几何图元

### 知识点概述
- 基本几何图元
- 参数方程表示
- 隐式表示
- 几何运算

### 详细知识点

#### 9.1 点和向量
- 点的表示方法
  ```csharp
  public struct Point3D {
      public float x, y, z;
      
      // 计算两点之间的距离
      public float DistanceTo(Point3D other) {
          float dx = other.x - x;
          float dy = other.y - y;
          float dz = other.z - z;
          return Mathf.Sqrt(dx * dx + dy * dy + dz * dz);
      }
      
      // 判断点是否在包围盒内
      public bool IsInBoundingBox(Point3D min, Point3D max) {
          return x >= min.x && x <= max.x &&
                 y >= min.y && y <= max.y &&
                 z >= min.z && z <= max.z;
      }
  }
  ```

#### 9.2 直线和射线
- 直线的参数方程
- 射线的表示方法
- 线段表示
- 距离计算
  ```csharp
  public struct Line3D {
      public Vector3 origin;
      public Vector3 direction;
      
      // 获取直线上的点
      public Vector3 GetPoint(float t) {
          return origin + direction * t;
      }
      
      // 计算点到直线的距离
      public float DistanceToPoint(Vector3 point) {
          Vector3 toPoint = point - origin;
          Vector3 projection = Vector3.Project(toPoint, direction);
          return Vector3.Distance(toPoint, projection);
      }
  }
  
  public struct Ray3D {
      public Vector3 origin;
      public Vector3 direction;
      
      // 射线与平面相交检测
      public bool IntersectPlane(Vector3 planeNormal, Vector3 planePoint, out float t) {
          float denom = Vector3.Dot(planeNormal, direction);
          t = 0;
          
          if (Mathf.Abs(denom) > 1e-6) {
              Vector3 toPlane = planePoint - origin;
              t = Vector3.Dot(toPlane, planeNormal) / denom;
              return t >= 0;
          }
          return false;
      }
  }
  ```

#### 9.3 平面
- 平面方程
- 法向量表示
- 点法式方程
- 一般式方程
  ```csharp
  public struct Plane3D {
      public Vector3 normal;
      public float distance;    // 到原点的距离
      
      public Plane3D(Vector3 normal, Vector3 point) {
          this.normal = normal.normalized;
          this.distance = -Vector3.Dot(normal, point);
      }
      
      // 计算点到平面的距离
      public float DistanceToPoint(Vector3 point) {
          return Vector3.Dot(normal, point) + distance;
      }
      
      // 判断点在平面的哪一侧
      public int ClassifyPoint(Vector3 point, float epsilon = 1e-6f) {
          float dist = DistanceToPoint(point);
          if (dist > epsilon) return 1;      // 正面
          if (dist < -epsilon) return -1;    // 背面
          return 0;                          // 在平面上
      }
  }
  ```

#### 9.4 多边形
- 三角形
- 凸多边形
- 网格表示
- 法向量计算
  ```csharp
  public class Triangle3D {
      public Vector3 v1, v2, v3;
      
      // 计算三角形法线
      public Vector3 CalculateNormal() {
          Vector3 edge1 = v2 - v1;
          Vector3 edge2 = v3 - v1;
          return Vector3.Cross(edge1, edge2).normalized;
      }
      
      // 计算三角形面积
      public float CalculateArea() {
          Vector3 edge1 = v2 - v1;
          Vector3 edge2 = v3 - v1;
          return Vector3.Cross(edge1, edge2).magnitude * 0.5f;
      }
      
      // 判断点是否在三角形内（使用重心坐标）
      public bool ContainsPoint(Vector3 point) {
          Vector3 v0 = v2 - v1;
          Vector3 v1 = v3 - v1;
          Vector3 v2 = point - this.v1;
          
          float d00 = Vector3.Dot(v0, v0);
          float d01 = Vector3.Dot(v0, v1);
          float d11 = Vector3.Dot(v1, v1);
          float d20 = Vector3.Dot(v2, v0);
          float d21 = Vector3.Dot(v2, v1);
          
          float denom = d00 * d11 - d01 * d01;
          float v = (d11 * d20 - d01 * d21) / denom;
          float w = (d00 * d21 - d01 * d20) / denom;
          float u = 1.0f - v - w;
          
          return v >= 0 && w >= 0 && (v + w) <= 1;
      }
  }
  ```

#### 9.5 曲面
- 二次曲面
- 参数曲面
- 隐式曲面
- 曲面细分

### 实际应用示例
1. 游戏碰撞检测
   - 射线检测
   - 包围盒
   - 多边形相交
   - 空间分割

2. 3D建模
   - 网格生成
   - 曲面建模
   - 细分曲面
   - UV展开

3. 计算机辅助设计
   - 几何造型
   - 曲面设计
   - 实体建模
   - 工程图纸

### 补充资料
1. 在线资源
   - [几何图元教程](https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/geometry-of-a-triangle)
   - [计算几何算法](https://www.geometrictools.com/)

2. 开发工具
   - Unity Mesh API
   - OpenGL图元
   - DirectX几何系统

## 第10章 3D图形中的数学主题

### 知识点概述
- 视图和投影
- 光照计算
- 纹理映射
- 几何处理

### 详细知识点

#### 10.1 视图变换
- 相机空间
- 视图矩阵
- 投影矩阵
- 视口变换
  ```csharp
  public class Camera3D {
      public Vector3 position;
      public Vector3 target;
      public Vector3 up;
      
      // 计算视图矩阵
      public Matrix4x4 GetViewMatrix() {
          Vector3 zAxis = (position - target).normalized;
          Vector3 xAxis = Vector3.Cross(up, zAxis).normalized;
          Vector3 yAxis = Vector3.Cross(zAxis, xAxis);
          
          Matrix4x4 viewMatrix = Matrix4x4.identity;
          viewMatrix.SetRow(0, new Vector4(xAxis.x, xAxis.y, xAxis.z, -Vector3.Dot(xAxis, position)));
          viewMatrix.SetRow(1, new Vector4(yAxis.x, yAxis.y, yAxis.z, -Vector3.Dot(yAxis, position)));
          viewMatrix.SetRow(2, new Vector4(zAxis.x, zAxis.y, zAxis.z, -Vector3.Dot(zAxis, position)));
          
          return viewMatrix;
      }
      
      // 计算透视投影矩阵
      public Matrix4x4 GetProjectionMatrix(float fov, float aspect, float near, float far) {
          float tanHalfFov = Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad);
          
          Matrix4x4 projMatrix = Matrix4x4.zero;
          projMatrix[0,0] = 1f / (aspect * tanHalfFov);
          projMatrix[1,1] = 1f / tanHalfFov;
          projMatrix[2,2] = -(far + near) / (far - near);
          projMatrix[2,3] = -(2f * far * near) / (far - near);
          projMatrix[3,2] = -1f;
          
          return projMatrix;
      }
  }
  ```

#### 10.2 光照模型
- 环境光
- 漫反射
- 镜面反射
- 光照方程
  ```csharp
  public class AdvancedLighting {
      // PBR光照计算
      public Vector3 CalculatePBR(Vector3 normal, Vector3 viewDir, Vector3 lightDir,
                                Vector3 albedo, float metallic, float roughness) {
          Vector3 halfVector = Vector3.Normalize(viewDir + lightDir);
          
          // 菲涅尔-施利克近似
          Vector3 F0 = Vector3.Lerp(new Vector3(0.04f), albedo, metallic);
          float NdotV = Mathf.Max(Vector3.Dot(normal, viewDir), 0.0f);
          Vector3 F = F0 + (Vector3.one - F0) * Mathf.Pow(1.0f - NdotV, 5.0f);
          
          // 法线分布函数
          float NdotH = Mathf.Max(Vector3.Dot(normal, halfVector), 0.0f);
          float D = DistributionGGX(NdotH, roughness);
          
          // 几何遮蔽
          float G = GeometrySmith(normal, viewDir, lightDir, roughness);
          
          Vector3 numerator = D * G * F;
          float denominator = 4.0f * NdotV * Mathf.Max(Vector3.Dot(normal, lightDir), 0.0f);
          Vector3 specular = numerator / Mathf.Max(denominator, 0.001f);
          
          return specular;
      }
      
      private float DistributionGGX(float NdotH, float roughness) {
          float a = roughness * roughness;
          float a2 = a * a;
          float NdotH2 = NdotH * NdotH;
          float denom = NdotH2 * (a2 - 1.0f) + 1.0f;
          return a2 / (Mathf.PI * denom * denom);
      }
      
      private float GeometrySmith(Vector3 N, Vector3 V, Vector3 L, float roughness) {
          float NdotV = Mathf.Max(Vector3.Dot(N, V), 0.0f);
          float NdotL = Mathf.Max(Vector3.Dot(N, L), 0.0f);
          float ggx1 = GeometrySchlickGGX(NdotV, roughness);
          float ggx2 = GeometrySchlickGGX(NdotL, roughness);
          return ggx1 * ggx2;
      }
      
      private float GeometrySchlickGGX(float NdotV, float roughness) {
          float r = roughness + 1.0f;
          float k = (r * r) / 8.0f;
          return NdotV / (NdotV * (1.0f - k) + k);
      }
  }
  ```

#### 10.3 纹理映射
- UV坐标
- 纹理投影
- MIP映射
- 过滤方法
  ```csharp
  public class TextureMapping {
      // 三线性过滤实现
      public Color TrilinearSample(Texture2D[] mipmaps, Vector2 uv, float mipLevel) {
          int lowMip = Mathf.FloorToInt(mipLevel);
          int highMip = Mathf.CeilToInt(mipLevel);
          float blend = mipLevel - lowMip;
          
          Color lowColor = BilinearSample(mipmaps[lowMip], uv);
          Color highColor = BilinearSample(mipmaps[highMip], uv);
          
          return Color.Lerp(lowColor, highColor, blend);
      }
      
      // 双线性过滤实现
      public Color BilinearSample(Texture2D texture, Vector2 uv) {
          Vector2 texSize = new Vector2(texture.width, texture.height);
          Vector2 texelPos = uv * texSize - new Vector2(0.5f);
          
          int x0 = Mathf.FloorToInt(texelPos.x);
          int y0 = Mathf.FloorToInt(texelPos.y);
          int x1 = x0 + 1;
          int y1 = y0 + 1;
          
          float fx = texelPos.x - x0;
          float fy = texelPos.y - y0;
          
          Color c00 = texture.GetPixel(x0, y0);
          Color c10 = texture.GetPixel(x1, y0);
          Color c01 = texture.GetPixel(x0, y1);
          Color c11 = texture.GetPixel(x1, y1);
          
          return Color.Lerp(
              Color.Lerp(c00, c10, fx),
              Color.Lerp(c01, c11, fx),
              fy
          );
      }
  }
  ```

#### 10.4 几何处理
- 背面剔除
- 视锥体裁剪
- 深度测试
- LOD技术
  ```csharp
  public class GeometryProcessor {
      // 视锥体裁剪
      public bool FrustumCull(Bounds bounds, Plane[] frustumPlanes) {
          foreach (Plane plane in frustumPlanes) {
              Vector3 normal = plane.normal;
              float distance = plane.distance;
              
              Vector3 positive = bounds.center;
              Vector3 negative = bounds.center;
              
              positive.x += normal.x >= 0 ? bounds.extents.x : -bounds.extents.x;
              positive.y += normal.y >= 0 ? bounds.extents.y : -bounds.extents.y;
              positive.z += normal.z >= 0 ? bounds.extents.z : -bounds.extents.z;
              
              if (plane.GetDistanceToPoint(positive) < 0) {
                  return false;
              }
          }
          return true;
      }
      
      // LOD级别计算
      public int CalculateLODLevel(Vector3 objectPosition, Vector3 cameraPosition, float[] lodDistances) {
          float distance = Vector3.Distance(objectPosition, cameraPosition);
          
          for (int i = 0; i < lodDistances.Length; i++) {
              if (distance < lodDistances[i]) {
                  return i;
              }
          }
          
          return lodDistances.Length;
      }
  }
  ```

### 实际应用示例
1. 渲染管线实现
```cpp
class RenderPipeline {
    void ViewTransform(Vector3[] vertices) {
        Matrix4x4 viewMatrix = camera.GetViewMatrix();
        for(int i = 0; i < vertices.Length; i++) {
            vertices[i] = viewMatrix.MultiplyPoint(vertices[i]);
        }
    }
    
    void ProjectionTransform(Vector3[] vertices) {
        Matrix4x4 projMatrix = camera.GetProjectionMatrix();
        for(int i = 0; i < vertices.Length; i++) {
            vertices[i] = projMatrix.MultiplyPoint(vertices[i]);
        }
    }
    
    void ClipSpace(Vector3[] vertices) {
        // 视锥体裁剪
        for(int i = 0; i < vertices.Length; i++) {
            if(!IsInClipSpace(vertices[i])) {
                // 执行裁剪
            }
        }
    }
}
```

2. 光照计算
```cpp
Vector3 CalculatePhongLighting(Vector3 normal, Vector3 lightDir, Vector3 viewDir) {
    // 环境光
    Vector3 ambient = ambientColor * ambientStrength;
    
    // 漫反射
    float diff = max(dot(normal, lightDir), 0.0);
    Vector3 diffuse = lightColor * diff;
    
    // 镜面反射
    Vector3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    Vector3 specular = lightColor * spec * specularStrength;
    
    return ambient + diffuse + specular;
}
```

3. 纹理映射
```cpp
struct VertexData {
    Vector3 position;
    Vector2 uv;
    Vector3 normal;
};

Vector4 SampleTexture(Texture2D texture, Vector2 uv) {
    // 双线性过滤
    Vector2 texSize = texture.GetSize();
    Vector2 texelPos = uv * texSize;
    
    int x0 = floor(texelPos.x);
    int y0 = floor(texelPos.y);
    int x1 = min(x0 + 1, texSize.x - 1);
    int y1 = min(y0 + 1, texSize.y - 1);
    
    float alpha = texelPos.x - x0;
    float beta = texelPos.y - y0;
    
    Vector4 c00 = texture.GetPixel(x0, y0);
    Vector4 c10 = texture.GetPixel(x1, y0);
    Vector4 c01 = texture.GetPixel(x0, y1);
    Vector4 c11 = texture.GetPixel(x1, y1);
    
    return lerp(
        lerp(c00, c10, alpha),
        lerp(c01, c11, alpha),
        beta
    );
}
```

### 补充资料
1. 图形编程资源
   - [LearnOpenGL](https://learnopengl.com/)
   - [DirectX教程](https://docs.microsoft.com/en-us/windows/win32/direct3d11/dx-graphics-overviews)
   - [Vulkan教程](https://vulkan-tutorial.com/)

2. 着色器编程
   - GLSL基础
   - HLSL编程
   - 着色器优化

### 练习题
1. 基础练习
   - 实现简单的光照模型
   - 编写基本的顶点着色器
   - 实现纹理采样

2. 进阶项目
   - 开发自定义渲染管线
   - 实现高级光照效果
   - 构建几何处理系统

3. 性能优化
   - 视锥体剔除
   - LOD系统实现
   - 渲染状态优化

### 重要算法
1. 视锥体裁剪
```cpp
bool IsInClipSpace(Vector4 clipPos) {
    return clipPos.x >= -clipPos.w && clipPos.x <= clipPos.w &&
           clipPos.y >= -clipPos.w && clipPos.y <= clipPos.w &&
           clipPos.z >= 0 && clipPos.z <= clipPos.w;
}
```

2. 法线贴图变换
```