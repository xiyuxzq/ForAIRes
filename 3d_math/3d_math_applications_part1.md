# 3D数学实际应用案例集合（第一部分）

## 目录
1. 基础坐标系统应用
2. 向量运算实战
3. 矩阵变换应用
4. 游戏物理系统应用
5. 计算机图形学应用
6. 工程应用

## 1. 基础坐标系统应用

### 1.1 游戏引擎中的坐标系统
#### Unity3D（左手坐标系）
```csharp
// Unity中的坐标系统示例
public class CoordinateSystemExample : MonoBehaviour 
{
    void Example() 
    {
        // 世界坐标系中的位置
        Vector3 worldPosition = transform.position;
        
        // 本地坐标系中的位置
        Vector3 localPosition = transform.localPosition;
        
        // 方向向量
        Vector3 forward = transform.forward;    // (0, 0, 1)
        Vector3 right = transform.right;        // (1, 0, 0)
        Vector3 up = transform.up;              // (0, 1, 0)
    }
}
```

#### Unreal Engine（左手坐标系）
```cpp
// UE中的坐标系统示例
void ACustomActor::CoordinateExample()
{
    // 世界坐标系中的位置
    FVector WorldLocation = GetActorLocation();
    
    // 本地坐标系中的位置
    FVector LocalLocation = GetRootComponent()->GetRelativeLocation();
    
    // 方向向量
    FVector ForwardVector = GetActorForwardVector();
    FVector RightVector = GetActorRightVector();
    FVector UpVector = GetActorUpVector();
}
```

## 2. 向量运算实战

### 2.1 点积应用
#### 视野检测
```csharp
public class VisionSystem : MonoBehaviour 
{
    public float fieldOfView = 90f;
    
    public bool IsInFieldOfView(Vector3 targetPosition) 
    {
        Vector3 directionToTarget = (targetPosition - transform.position).normalized;
        float angle = Vector3.Angle(transform.forward, directionToTarget);
        return angle <= fieldOfView * 0.5f;
    }
    
    public float GetVisibilityFactor(Vector3 targetPosition) 
    {
        Vector3 directionToTarget = (targetPosition - transform.position).normalized;
        float dot = Vector3.Dot(transform.forward, directionToTarget);
        return Mathf.Max(0, dot); // 0表示背向，1表示正向
    }
}
```

### 2.2 叉积应用
#### 判断转向方向
```csharp
public class SteeringSystem : MonoBehaviour 
{
    public enum TurnDirection { Left, Right, None }
    
    public TurnDirection GetTurnDirection(Vector3 forward, Vector3 targetDirection) 
    {
        Vector3 cross = Vector3.Cross(forward, targetDirection);
        if (cross.y > 0.01f) return TurnDirection.Left;
        if (cross.y < -0.01f) return TurnDirection.Right;
        return TurnDirection.None;
    }
}
```

## 3. 矩阵变换应用

### 3.1 基础变换矩阵
```csharp
public class TransformationMatrix 
{
    // 创建平移矩阵
    public static Matrix4x4 CreateTranslation(Vector3 translation) 
    {
        Matrix4x4 matrix = Matrix4x4.identity;
        matrix[0, 3] = translation.x;
        matrix[1, 3] = translation.y;
        matrix[2, 3] = translation.z;
        return matrix;
    }
    
    // 创建缩放矩阵
    public static Matrix4x4 CreateScale(Vector3 scale) 
    {
        Matrix4x4 matrix = Matrix4x4.identity;
        matrix[0, 0] = scale.x;
        matrix[1, 1] = scale.y;
        matrix[2, 2] = scale.z;
        return matrix;
    }
    
    // 创建绕X轴旋转矩阵
    public static Matrix4x4 CreateRotationX(float angleInDegrees) 
    {
        Matrix4x4 matrix = Matrix4x4.identity;
        float rad = angleInDegrees * Mathf.Deg2Rad;
        float cos = Mathf.Cos(rad);
        float sin = Mathf.Sin(rad);
        
        matrix[1, 1] = cos;
        matrix[1, 2] = -sin;
        matrix[2, 1] = sin;
        matrix[2, 2] = cos;
        
        return matrix;
    }
}
```

### 3.2 复合变换应用
```csharp
public class TransformationExample : MonoBehaviour 
{
    void ApplyComplexTransform(Vector3 position, Vector3 rotation, Vector3 scale) 
    {
        // 创建各个变换矩阵
        Matrix4x4 translationMatrix = TransformationMatrix.CreateTranslation(position);
        Matrix4x4 rotationX = TransformationMatrix.CreateRotationX(rotation.x);
        Matrix4x4 rotationY = TransformationMatrix.CreateRotationX(rotation.y);
        Matrix4x4 rotationZ = TransformationMatrix.CreateRotationX(rotation.z);
        Matrix4x4 scaleMatrix = TransformationMatrix.CreateScale(scale);
        
        // 组合变换（注意顺序：缩放->旋转->平移）
        Matrix4x4 finalTransform = translationMatrix * 
                                 rotationZ * 
                                 rotationY * 
                                 rotationX * 
                                 scaleMatrix;
                                 
        // 应用变换到物体
        transform.position = finalTransform.MultiplyPoint3x4(Vector3.zero);
        transform.rotation = Quaternion.Euler(rotation);
        transform.localScale = scale;
    }
}
```

## 4. 游戏物理系统应用

### 4.1 基础物理模拟
```csharp
public class PhysicsSimulation : MonoBehaviour 
{
    public Vector3 velocity;
    public Vector3 acceleration;
    public float mass = 1f;
    
    void Update() 
    {
        // 基础物理更新
        velocity += acceleration * Time.deltaTime;
        transform.position += velocity * Time.deltaTime;
        
        // 重力
        ApplyGravity();
        
        // 空气阻力
        ApplyDrag();
    }
    
    void ApplyGravity() 
    {
        Vector3 gravity = new Vector3(0, -9.81f, 0);
        velocity += gravity * Time.deltaTime;
    }
    
    void ApplyDrag() 
    {
        float dragCoefficient = 0.1f;
        Vector3 drag = -velocity.normalized * velocity.sqrMagnitude * dragCoefficient;
        velocity += drag * Time.deltaTime / mass;
    }
}
```

### 4.2 碰撞检测
```csharp
public class CollisionDetection 
{
    // 球体碰撞检测
    public static bool SphereCollision(Vector3 center1, float radius1, 
                                     Vector3 center2, float radius2) 
    {
        float distanceSquared = (center2 - center1).sqrMagnitude;
        float radiusSum = radius1 + radius2;
        return distanceSquared <= radiusSum * radiusSum;
    }
    
    // AABB碰撞检测
    public static bool AABBCollision(Vector3 min1, Vector3 max1, 
                                   Vector3 min2, Vector3 max2) 
    {
        return (min1.x <= max2.x && max1.x >= min2.x) &&
               (min1.y <= max2.y && max1.y >= min2.y) &&
               (min1.z <= max2.z && max1.z >= min2.z);
    }
}
```

## 5. 计算机图形学应用

### 5.1 光照计算
```csharp
public class LightingCalculator 
{
    public static float CalculateDiffuseLighting(Vector3 normal, Vector3 lightDir) 
    {
        float NdotL = Mathf.Max(0, Vector3.Dot(normal, lightDir));
        return NdotL;
    }
    
    public static Vector3 CalculateSpecularLighting(Vector3 normal, Vector3 lightDir, 
                                                  Vector3 viewDir, float shininess) 
    {
        Vector3 reflectDir = Vector3.Reflect(-lightDir, normal);
        float spec = Mathf.Pow(Mathf.Max(0, Vector3.Dot(viewDir, reflectDir)), shininess);
        return new Vector3(spec, spec, spec);
    }
}
```

### 5.2 相机投影
```csharp
public class CameraProjection 
{
    public static Matrix4x4 CreatePerspectiveProjection(
        float fov, float aspectRatio, float near, float far) 
    {
        Matrix4x4 matrix = Matrix4x4.zero;
        float tanHalfFov = Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad);
        
        matrix[0,0] = 1f / (aspectRatio * tanHalfFov);
        matrix[1,1] = 1f / tanHalfFov;
        matrix[2,2] = -(far + near) / (far - near);
        matrix[2,3] = -(2f * far * near) / (far - near);
        matrix[3,2] = -1f;
        
        return matrix;
    }
}
```

## 6. 工程应用

### 6.1 CAD系统基础操作
```csharp
public class CADSystem 
{
    // 2D绘图功能
    public static Vector2[] CreateRectangle(Vector2 center, float width, float height) 
    {
        Vector2[] points = new Vector2[4];
        points[0] = center + new Vector2(-width/2, -height/2);
        points[1] = center + new Vector2(width/2, -height/2);
        points[2] = center + new Vector2(width/2, height/2);
        points[3] = center + new Vector2(-width/2, height/2);
        return points;
    }
    
    // 3D建模功能
    public static Mesh CreateCube(Vector3 center, Vector3 dimensions) 
    {
        Mesh mesh = new Mesh();
        // 实现省略...
        return mesh;
    }
}
```

### 6.2 机器人运动控制
```csharp
public class RobotController 
{
    public struct Joint 
    {
        public Vector3 position;
        public Vector3 rotation;
        public Vector3 axis;
    }
    
    public static Vector3 CalculateEndEffectorPosition(Joint[] joints) 
    {
        Vector3 position = Vector3.zero;
        Quaternion rotation = Quaternion.identity;
        
        foreach (Joint joint in joints) 
        {
            rotation *= Quaternion.AngleAxis(
                Vector3.Angle(Vector3.forward, joint.axis),
                joint.rotation
            );
            position += rotation * joint.position;
        }
        
        return position;
    }
}
``` 