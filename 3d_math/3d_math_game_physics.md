# 3D数学在游戏物理系统中的应用

## 目录
1. 刚体动力学系统
2. 高级碰撞检测
3. 约束求解系统
4. 连续碰撞检测
5. 物理引擎优化

## 1. 刚体动力学系统
### 1.1 基础刚体系统
```csharp
public class RigidBody3D
{
    public Vector3 Position { get; private set; }
    public Quaternion Rotation { get; private set; }
    public Vector3 LinearVelocity { get; private set; }
    public Vector3 AngularVelocity { get; private set; }
    public float Mass { get; private set; }
    public Matrix3x3 InertiaTensor { get; private set; }
    
    public void ApplyForce(Vector3 force, Vector3 point)
    {
        // 计算线性加速度
        Vector3 linearAcceleration = force / Mass;
        LinearVelocity += linearAcceleration * Time.deltaTime;
        
        // 计算力矩和角加速度
        Vector3 torque = Vector3.Cross(point - Position, force);
        Vector3 angularAcceleration = InertiaTensor.Inverse * torque;
        AngularVelocity += angularAcceleration * Time.deltaTime;
    }
    
    public void Integrate(float deltaTime)
    {
        // 更新位置
        Position += LinearVelocity * deltaTime;
        
        // 更新旋转
        Quaternion angularRotation = new Quaternion(
            AngularVelocity.x * deltaTime,
            AngularVelocity.y * deltaTime,
            AngularVelocity.z * deltaTime,
            0
        );
        Rotation = (Rotation + (angularRotation * Rotation) * 0.5f).normalized;
    }
}
```

### 1.2 高级刚体特性
```csharp
public class AdvancedRigidBody : RigidBody3D
{
    private float restitution;
    private float friction;
    private Vector3 gravity = new Vector3(0, -9.81f, 0);
    
    public void ApplyGravity()
    {
        ApplyForce(Mass * gravity, Position);
    }
    
    public void HandleCollision(AdvancedRigidBody other, Vector3 normal, Vector3 point)
    {
        // 计算相对速度
        Vector3 relativeVel = LinearVelocity - other.LinearVelocity;
        
        // 计算冲量
        float normalVel = Vector3.Dot(relativeVel, normal);
        if (normalVel > 0) return; // 物体已经分离
        
        float j = -(1 + restitution) * normalVel;
        j /= 1/Mass + 1/other.Mass;
        
        // 应用冲量
        Vector3 impulse = j * normal;
        LinearVelocity += impulse / Mass;
        other.LinearVelocity -= impulse / other.Mass;
        
        // 处理摩擦力
        Vector3 tangent = relativeVel - (Vector3.Dot(relativeVel, normal) * normal);
        if(tangent.magnitude > 0.0001f)
        {
            tangent.Normalize();
            float jt = -Vector3.Dot(relativeVel, tangent);
            jt /= 1/Mass + 1/other.Mass;
            
            Vector3 frictionImpulse = friction * jt * tangent;
            LinearVelocity += frictionImpulse / Mass;
            other.LinearVelocity -= frictionImpulse / other.Mass;
        }
    }
}
```

## 2. 高级碰撞检测
### 2.1 分离轴定理（SAT）实现
```csharp
public class SATCollisionDetector
{
    public struct Projection
    {
        public float min, max;
    }
    
    public static bool TestCollision(ConvexHull hullA, ConvexHull hullB)
    {
        // 获取所有可能的分离轴
        List<Vector3> axes = GetSeparatingAxes(hullA, hullB);
        
        foreach(Vector3 axis in axes)
        {
            // 在轴上投影两个凸包
            Projection projA = Project(hullA, axis);
            Projection projB = Project(hullB, axis);
            
            // 检查投影是否重叠
            if(!OverlapOnAxis(projA, projB))
            {
                return false; // 找到分离轴，不相交
            }
        }
        
        return true; // 所有轴都重叠，存在碰撞
    }
    
    private static Projection Project(ConvexHull hull, Vector3 axis)
    {
        float min = float.MaxValue;
        float max = float.MinValue;
        
        foreach(Vector3 vertex in hull.vertices)
        {
            float proj = Vector3.Dot(vertex, axis);
            min = Mathf.Min(min, proj);
            max = Mathf.Max(max, proj);
        }
        
        return new Projection { min = min, max = max };
    }
    
    private static bool OverlapOnAxis(Projection projA, Projection projB)
    {
        return projA.max >= projB.min && projB.max >= projA.min;
    }
}
```

## 3. 约束求解系统
### 3.1 基础约束系统
```csharp
public abstract class Constraint
{
    protected RigidBody3D bodyA;
    protected RigidBody3D bodyB;
    
    public abstract void Solve();
    public abstract void Initialize();
}

public class DistanceConstraint : Constraint
{
    private float targetDistance;
    private float stiffness;
    
    public override void Solve()
    {
        Vector3 direction = bodyB.Position - bodyA.Position;
        float currentDistance = direction.magnitude;
        direction.Normalize();
        
        float error = currentDistance - targetDistance;
        Vector3 correction = direction * error * stiffness;
        
        bodyA.Position += correction * 0.5f;
        bodyB.Position -= correction * 0.5f;
    }
}
```

## 4. 连续碰撞检测
### 4.1 扫掠测试
```csharp
public class SweepTest
{
    public struct SweepResult
    {
        public float time;      // 碰撞时间 [0,1]
        public Vector3 point;   // 碰撞点
        public Vector3 normal;  // 碰撞法线
    }
    
    public static SweepResult SweepSpheres(
        Vector3 posA, float radiusA, Vector3 velocityA,
        Vector3 posB, float radiusB, Vector3 velocityB)
    {
        Vector3 relativeVel = velocityA - velocityB;
        Vector3 relativePos = posA - posB;
        float combinedRadius = radiusA + radiusB;
        
        // 求解二次方程
        float a = Vector3.Dot(relativeVel, relativeVel);
        float b = 2.0f * Vector3.Dot(relativeVel, relativePos);
        float c = Vector3.Dot(relativePos, relativePos) - 
                 combinedRadius * combinedRadius;
        
        float discriminant = b * b - 4.0f * a * c;
        
        if(discriminant < 0)
            return new SweepResult { time = float.MaxValue };
            
        float time = (-b - Mathf.Sqrt(discriminant)) / (2.0f * a);
        
        if(time < 0 || time > 1)
            return new SweepResult { time = float.MaxValue };
            
        Vector3 point = posA + velocityA * time;
        Vector3 normal = (point - (posB + velocityB * time)).normalized;
        
        return new SweepResult 
        {
            time = time,
            point = point,
            normal = normal
        };
    }
}
```

## 5. 物理引擎优化
### 5.1 空间分区系统
```csharp
public class OctreeNode
{
    public Bounds bounds;
    public List<RigidBody3D> objects;
    public OctreeNode[] children;
    private const int MAX_OBJECTS = 8;
    private const int MAX_DEPTH = 8;
    
    public void Insert(RigidBody3D obj)
    {
        if (!bounds.Contains(obj.Position))
            return;
            
        if (objects.Count < MAX_OBJECTS || depth >= MAX_DEPTH)
        {
            objects.Add(obj);
            return;
        }
        
        if (children == null)
            Split();
            
        foreach (var child in children)
            child.Insert(obj);
    }
    
    private void Split()
    {
        Vector3 center = bounds.center;
        Vector3 extents = bounds.extents * 0.5f;
        children = new OctreeNode[8];
        
        for (int i = 0; i < 8; i++)
        {
            Vector3 newCenter = center;
            newCenter.x += ((i & 1) == 0 ? -extents.x : extents.x);
            newCenter.y += ((i & 2) == 0 ? -extents.y : extents.y);
            newCenter.z += ((i & 4) == 0 ? -extents.z : extents.z);
            
            children[i] = new OctreeNode
            {
                bounds = new Bounds(newCenter, extents * 2),
                objects = new List<RigidBody3D>()
            };
        }
        
        // 重新分配现有对象
        foreach (var obj in objects)
            foreach (var child in children)
                child.Insert(obj);
                
        objects.Clear();
    }
}
```