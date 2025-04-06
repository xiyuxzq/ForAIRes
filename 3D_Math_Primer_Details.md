# 3D数学重点知识详解与应用示例

## 第1章：笛卡尔坐标系详解

### 1. 左手和右手坐标系统
**详细解释：**
- 左手坐标系：伸开左手，大拇指指向X轴正方向，食指指向Y轴正方向，中指指向Z轴正方向
- 右手坐标系：伸开右手，同样操作
- DirectX使用左手坐标系，OpenGL使用右手坐标系

**应用示例：**
```cpp
// DirectX（左手坐标系）中的前向量
Vector3 forward = Vector3(0, 0, 1);

// OpenGL（右手坐标系）中的前向量
Vector3 forward = Vector3(0, 0, -1);
```

### 2. 角度与弧度转换
**详细解释：**
- 一圈 = 360度 = 2π弧度
- 弧度 = 角度 × (π/180)
- 角度 = 弧度 × (180/π)

**应用示例：**
```cpp
// 游戏中的视角旋转
class Camera {
    float fieldOfView; // 通常以角度定义（如90度）
    
    void SetFOV(float degrees) {
        // OpenGL需要弧度
        float radians = degrees * (M_PI / 180.0f);
        glMatrixMode(GL_PROJECTION);
        gluPerspective(radians, aspect, near, far);
    }
};
```

## 第2章：矢量详解

### 1. 点积（Dot Product）
**详细解释：**
- 数学定义：a·b = |a||b|cos(θ)
- 几何意义：一个向量在另一个向量方向上的投影
- 结果是标量

**应用示例：**
```cpp
class GameCharacter {
    // 判断敌人是否在视野内
    bool IsInFieldOfView(Vector3 targetDirection) {
        Vector3 forward = GetForwardVector();
        float dot = forward.Dot(targetDirection);
        // dot > 0.866 表示夹角小于30度
        return dot > 0.866f;
    }
    
    // 计算光照强度
    float CalculateLightIntensity(Vector3 normal, Vector3 lightDir) {
        return max(0.0f, normal.Dot(lightDir));
    }
};
```

### 2. 叉积（Cross Product）
**详细解释：**
- 数学定义：|a×b| = |a||b|sin(θ)
- 几何意义：得到一个垂直于两个输入向量的新向量
- 方向由右手法则决定

**应用示例：**
```cpp
class Physics {
    // 判断点在三角形哪一侧
    bool IsPointLeftOfLine(Vector2 lineStart, Vector2 lineEnd, Vector2 point) {
        Vector2 lineDir = lineEnd - lineStart;
        Vector2 pointDir = point - lineStart;
        // 二维叉积，正值表示在左侧
        float cross = lineDir.x * pointDir.y - lineDir.y * pointDir.x;
        return cross > 0;
    }
    
    // 计算面法线
    Vector3 CalculateTriangleNormal(Vector3 v1, Vector3 v2, Vector3 v3) {
        Vector3 edge1 = v2 - v1;
        Vector3 edge2 = v3 - v1;
        return edge1.Cross(edge2).Normalize();
    }
    
    // 判断物体是否在转弯
    bool IsTurning(Vector3 velocity, Vector3 acceleration) {
        return velocity.Cross(acceleration).Length() > 0.01f;
    }
};
```

## 第3章：多个坐标空间详解

### 1. 坐标空间转换
**详细解释：**
- 模型空间：物体自身的局部坐标系
- 世界空间：游戏世界的全局坐标系
- 观察空间：以摄像机为原点的坐标系
- 裁剪空间：用于视锥体裁剪的标准化空间

**应用示例：**
```cpp
class RenderSystem {
    // 完整的渲染变换管线
    Vector3 TransformVertex(Vector3 modelSpaceVertex) {
        // 模型空间 -> 世界空间
        Vector3 worldPos = modelMatrix.MultiplyPoint(modelSpaceVertex);
        
        // 世界空间 -> 观察空间
        Vector3 viewPos = viewMatrix.MultiplyPoint(worldPos);
        
        // 观察空间 -> 裁剪空间
        Vector4 clipPos = projectionMatrix.MultiplyPoint(viewPos);
        
        // 透视除法
        Vector3 ndcPos = clipPos.xyz / clipPos.w;
        
        return ndcPos;
    }
};
```

## 第4-6章：矩阵详解

### 1. 特殊矩阵及其性质
**详细解释：**
- 单位矩阵：对角线为1，其他为0
- 正交矩阵：转置等于逆矩阵
- 对称矩阵：转置等于自身

**应用示例：**
```cpp
class Transform {
    // 构建观察矩阵（正交矩阵示例）
    Matrix4x4 CreateViewMatrix(Vector3 position, Vector3 target, Vector3 up) {
        Vector3 zaxis = (target - position).Normalize();
        Vector3 xaxis = up.Cross(zaxis).Normalize();
        Vector3 yaxis = zaxis.Cross(xaxis);
        
        // 正交矩阵的逆等于其转置
        Matrix4x4 rotation = Matrix4x4(
            xaxis.x, yaxis.x, zaxis.x, 0,
            xaxis.y, yaxis.y, zaxis.y, 0,
            xaxis.z, yaxis.z, zaxis.z, 0,
            0, 0, 0, 1
        );
        
        Matrix4x4 translation = Matrix4x4::Translation(-position);
        return rotation * translation;
    }
};
```

## 第7章：极坐标系详解

### 1. 极坐标系应用
**详细解释：**
- 适用于圆形运动
- 处理周期性运动
- 螺旋形路径生成

**应用示例：**
```cpp
class GameEffects {
    // 生成螺旋形子弹模式
    vector<Vector2> GenerateSpiralPattern(float startRadius, float endRadius, 
                                        float angleStep, int count) {
        vector<Vector2> positions;
        float radiusStep = (endRadius - startRadius) / count;
        
        for(int i = 0; i < count; i++) {
            float radius = startRadius + radiusStep * i;
            float angle = angleStep * i;
            float x = radius * cos(angle);
            float y = radius * sin(angle);
            positions.push_back(Vector2(x, y));
        }
        return positions;
    }
    
    // 环绕目标运动
    Vector3 OrbitAround(Vector3 target, float radius, float height, float time) {
        float angle = time * 2.0f; // 每秒转两圈
        return Vector3(
            target.x + radius * cos(angle),
            target.y + height,
            target.z + radius * sin(angle)
        );
    }
};
```

## 第8章：三维旋转详解

### 1. 四元数的优势
**详细解释：**
- 避免万向节死锁
- 插值平滑（SLERP）
- 计算效率高
- 存储空间小

**应用示例：**
```cpp
class Animation {
    // 平滑相机旋转
    Quaternion SmoothRotation(Quaternion current, Quaternion target, float t) {
        // 球面线性插值
        return Quaternion::Slerp(current, target, t);
    }
    
    // 防止万向节死锁的相机系统
    class Camera {
        Quaternion rotation;
        
        void LookAround(float yaw, float pitch) {
            // 使用四元数避免万向节死锁
            Quaternion yawRotation = Quaternion::AngleAxis(yaw, Vector3::up);
            Quaternion pitchRotation = Quaternion::AngleAxis(pitch, Vector3::right);
            rotation = yawRotation * pitchRotation;
        }
    };
};
```

## 第9章：几何图元详解

### 1. 包围体优化
**详细解释：**
- AABB（轴对齐包围盒）：最简单，更新快
- OBB（有向包围盒）：更紧凑，计算复杂
- 包围球：方向无关，适合快速测试

**应用示例：**
```cpp
class CollisionSystem {
    // 分层包围盒检测
    bool CheckCollision(GameObject* obj1, GameObject* obj2) {
        // 第一层：包围球快速测试
        if (!obj1->boundingSphere.Intersects(obj2->boundingSphere))
            return false;
            
        // 第二层：AABB测试
        if (!obj1->aabb.Intersects(obj2->aabb))
            return false;
            
        // 第三层：详细碰撞检测
        return DetailedCollisionCheck(obj1, obj2);
    }
    
    // 动态更新AABB
    void UpdateAABB(Model* model, const Matrix4x4& transform) {
        Vector3 min = Vector3(INFINITY);
        Vector3 max = Vector3(-INFINITY);
        
        for(const Vector3& vertex : model->vertices) {
            Vector3 transformed = transform.MultiplyPoint(vertex);
            min = Vector3::Min(min, transformed);
            max = Vector3::Max(max, transformed);
        }
        
        model->aabb.SetMinMax(min, max);
    }
};
```

## 第10章：三维图形数学详解

### 1. 光照模型
**详细解释：**
- 环境光：模拟间接光照
- 漫反射：满足Lambert定律
- 镜面反射：基于视角方向
- 菲涅尔效应：边缘反射增强

**应用示例：**
```glsl
// 现代PBR光照模型
vec3 CalculatePBR(vec3 normal, vec3 viewDir, vec3 lightDir, 
                  float roughness, float metallic) {
    // 计算基本光照参数
    vec3 halfDir = normalize(viewDir + lightDir);
    float NdotL = max(dot(normal, lightDir), 0.0);
    float NdotH = max(dot(normal, halfDir), 0.0);
    float NdotV = max(dot(normal, viewDir), 0.0);
    
    // 计算菲涅尔效应
    vec3 F0 = mix(vec3(0.04), albedo, metallic);
    vec3 F = FresnelSchlick(NdotV, F0);
    
    // 计算法线分布
    float D = DistributionGGX(NdotH, roughness);
    
    // 计算几何遮蔽
    float G = GeometrySmith(NdotV, NdotL, roughness);
    
    // 组合PBR光照
    vec3 specular = (D * F * G) / (4.0 * NdotV * NdotL + 0.001);
    vec3 diffuse = albedo * (1.0 - metallic);
    
    return (diffuse + specular) * lightColor * NdotL;
}
```

## 第11-12章：力学详解

### 1. 物理模拟
**详细解释：**
- 显式欧拉积分：简单但可能不稳定
- 半隐式欧拉：更稳定
- Verlet积分：能量守恒更好

**应用示例：**
```cpp
class PhysicsSimulation {
    // Verlet积分实现
    class VerletObject {
        Vector3 currentPos;
        Vector3 oldPos;
        Vector3 acceleration;
        
        void Update(float dt) {
            Vector3 temp = currentPos;
            Vector3 velocity = currentPos - oldPos;
            
            // Verlet积分
            currentPos = currentPos + velocity + acceleration * dt * dt;
            oldPos = temp;
            
            // 重置加速度
            acceleration = Vector3::zero;
        }
        
        void ApplyForce(Vector3 force, float mass) {
            acceleration += force / mass;
        }
    };
    
    // 弹簧约束
    void SolveSpringConstraint(VerletObject& p1, VerletObject& p2, float restLength) {
        Vector3 delta = p2.currentPos - p1.currentPos;
        float currentLength = delta.Length();
        float difference = (currentLength - restLength) / currentLength;
        
        p1.currentPos += delta * 0.5f * difference;
        p2.currentPos -= delta * 0.5f * difference;
    }
};
```

## 第13章：三维曲线详解

### 1. 贝塞尔曲线应用
**详细解释：**
- 平滑路径生成
- UI动画
- 相机运动
- 粒子系统轨迹

**应用示例：**
```cpp
class SplineSystem {
    // 生成平滑相机路径
    class CameraSpline {
        vector<Vector3> controlPoints;
        
        Vector3 GetCameraPosition(float t) {
            // 三次贝塞尔曲线
            int segment = (int)(t * (controlPoints.size() - 3));
            float localT = t * (controlPoints.size() - 3) - segment;
            
            Vector3 p0 = controlPoints[segment];
            Vector3 p1 = controlPoints[segment + 1];
            Vector3 p2 = controlPoints[segment + 2];
            Vector3 p3 = controlPoints[segment + 3];
            
            float u = 1 - localT;
            float tt = localT * localT;
            float uu = u * u;
            float uuu = uu * u;
            float ttt = tt * localT;
            
            return uuu * p0 +
                   3 * uu * localT * p1 +
                   3 * u * tt * p2 +
                   ttt * p3;
        }
    };
    
    // 粒子系统轨迹
    class ParticleTrail {
        void UpdateParticle(Particle& particle, float t) {
            Vector3 start = particle.startPos;
            Vector3 control1 = start + particle.initialVelocity;
            Vector3 control2 = particle.endPos - particle.endVelocity;
            Vector3 end = particle.endPos;
            
            // 贝塞尔曲线轨迹
            float u = 1 - t;
            particle.position = u*u*u * start +
                              3*u*u*t * control1 +
                              3*u*t*t * control2 +
                              t*t*t * end;
        }
    };
};
```

## 实际应用总结

1. **游戏开发中的应用**
   - 角色控制和相机系统
   - 物理模拟和碰撞检测
   - 特效系统和粒子效果
   - 动画系统和路径规划

2. **图形渲染中的应用**
   - 光照计算和阴影
   - 几何变换和空间转换
   - 曲线和曲面生成
   - 视锥体裁剪和投影

3. **AI和游戏逻辑中的应用**
   - 寻路算法
   - 视野检测
   - 行为控制
   - 目标跟踪

4. **UI系统中的应用**
   - 动画过渡
   - 布局计算
   - 手势识别
   - 交互响应